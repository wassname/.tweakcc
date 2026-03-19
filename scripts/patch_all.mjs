#!/usr/bin/env node
/**
 * Discover all Claude Code installations and patch each via tweakcc.
 *
 * Strategy: for each install, temporarily set ccInstallationPath in config.json,
 * run `npx tweakcc --apply`, then restore the original (npm) path.
 */

import { findAllInstallations, readContent, helpers } from 'tweakcc';
const { clearCaches } = helpers;
import { readFile, writeFile, mkdir, copyFile, stat, rename, unlink, readdir, chmod } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { resolve, dirname, basename } from 'node:path';

const CONFIG_PATH = resolve(import.meta.dirname, '..', 'config.json');
const OUT_DIR = resolve(import.meta.dirname, '..', 'out');
const BACKUP_RO_DIR = resolve(import.meta.dirname, '..', 'DO_NOT_DELETE_patched_binaries');
const PROMPT_CACHE_DIR = resolve(import.meta.dirname, '..', 'prompt-data-cache');

/** Copy src -> dest, handling ETXTBSY by unlinking dest first (rename to .old, then copy). */
async function robustCopy(src, dest) {
  try {
    await copyFile(src, dest);
  } catch (e) {
    if (e.code !== 'ETXTBSY') throw e;
    // Binary is busy -- rename it out of the way, then copy
    const old = dest + '.old';
    await rename(dest, old);
    await copyFile(src, dest);
    await unlink(old).catch(() => {}); // best-effort cleanup
  }
}

async function readConfig() {
  return JSON.parse(await readFile(CONFIG_PATH, 'utf8'));
}

async function writeConfig(cfg) {
  await writeFile(CONFIG_PATH, JSON.stringify(cfg, null, 2) + '\n');
}

function smoke(installation) {
  // npm global: binary is in the nvm bin dir (parent of lib/node_modules)
  // native: the path IS the binary
  const bin = installation.kind === 'npm'
    ? resolve(dirname(installation.path), '..', '..', '..', '..', 'bin', 'claude')
    : installation.path;
  const env = { ...process.env };
  delete env.CLAUDECODE; // allow nested invocation during testing
  const out = execFileSync(bin, ['-p', 'ping', '-v'], {
    encoding: 'utf8',
    timeout: 30_000,
    stdio: ['pipe', 'pipe', 'pipe'],
    env,
  });
  if (!out.includes('Claude Code')) {
    throw new Error(`smoke test failed: no "Claude Code" in output`);
  }
  return out;
}

/** Build an Installation object from an explicit path (for installs findAllInstallations misses). */
async function installationFromPath(filePath) {
  const absPath = resolve(filePath);
  const info = await stat(absPath);
  // Native binaries are large ELF files; npm cli.js is smaller JS
  const kind = absPath.endsWith('.js') ? 'npm' : 'native';
  // Version: try directory name first (native binaries are named by version),
  // then try reading JS content via tweakcc unpack
  const dirName = basename(absPath);
  const parentName = basename(dirname(absPath));
  let version = 'unknown';
  if (/^\d+\.\d+\.\d+$/.test(dirName)) version = dirName;
  else if (/^\d+\.\d+\.\d+$/.test(parentName)) version = parentName;
  else {
    try {
      const inst = { path: absPath, version: '0.0.0', kind };
      const content = await readContent(inst);
      const m = content.match(/"version"\s*:\s*"(\d+\.\d+\.\d+)"/);
      if (m) version = m[1];
    } catch {}
  }
  return { path: absPath, version, kind };
}

/** Create a prompt cache entry for targetVersion by copying the latest available version. */
async function ensurePromptCache(targetVersion) {
  const targetFile = resolve(PROMPT_CACHE_DIR, `prompts-${targetVersion}.json`);
  try {
    await stat(targetFile);
    return false; // already exists
  } catch (e) {
    if (e.code !== 'ENOENT') throw e;
  }

  // Find latest cached prompts file (excluding backups)
  const files = (await readdir(PROMPT_CACHE_DIR))
    .filter(f => /^prompts-\d+\.\d+\.\d+\.json$/.test(f))
    .sort((a, b) => {
      const va = a.match(/(\d+\.\d+\.\d+)/)[1].split('.').map(Number);
      const vb = b.match(/(\d+\.\d+\.\d+)/)[1].split('.').map(Number);
      return va[0] - vb[0] || va[1] - vb[1] || va[2] - vb[2];
    });
  if (files.length === 0) return false;

  const latestFile = resolve(PROMPT_CACHE_DIR, files.at(-1));
  const data = JSON.parse(await readFile(latestFile, 'utf8'));
  const sourceVersion = data.version;
  data.version = targetVersion;
  await writeFile(targetFile, JSON.stringify(data, null, 2), 'utf8');
  console.log(`  prompt fallback: copied ${sourceVersion} templates as ${targetVersion}`);
  return true;
}

/** Fix known tweakcc 4.0.11 bugs in patched output. */
async function postPatchFix(filePath) {
  // Native ELF binaries can't be safely round-tripped through UTF-8 strings.
  // The embedded JS is inside a binary container; skip and accept minor template bugs there.
  if (!filePath.endsWith('.js')) return;

  let content = await readFile(filePath, 'utf8');
  let fixes = 0;

  // Bug 1: tweakcc injects ${...ASK_USER_QUESTION_TOOL...} as a raw JS expression,
  // but CC runtime uses positional identifier substitution, not JS scope variables.
  // Neither ASK_USER_QUESTION_TOOL nor _NAME exist in scope -> ReferenceError.
  // Fix: replace the whole conditional with static text (AskUserQuestion is always available).
  const badExpr = /\$\{[A-Z_]*\.has\(ASK_USER_QUESTION_TOOL[A-Z_]*\)\?[^}]*\}/g;
  if (badExpr.test(content)) {
    content = content.replace(badExpr, ' If unclear why, use AskUserQuestion to ask.');
    fixes++;
  }

  // Bug 2: version string duplicated 4x
  const quadVersion = /\\n4\.\d+\.\d+ \(tweakcc\)(\\n4\.\d+\.\d+ \(tweakcc\)){1,}/g;
  if (quadVersion.test(content)) {
    content = content.replace(quadVersion, (m) => m.split('\\n').filter(Boolean)[0] ? '\\n' + m.split('\\n').filter(Boolean)[0] : m);
    fixes++;
  }

  if (fixes > 0) {
    await writeFile(filePath, content);
    // Restore execute permission for native binaries
    if (!filePath.endsWith('.js')) await chmod(filePath, 0o755);
    console.log(`  post-patch: fixed ${fixes} tweakcc bug(s)`);
  }
}

function runApply() {
  const out = execFileSync('npx', ['tweakcc', '--apply'], {
    encoding: 'utf8',
    timeout: 120_000,
    cwd: resolve(import.meta.dirname, '..'),
    stdio: ['pipe', 'pipe', 'pipe'],
  });
  // Surface warnings/errors from tweakcc (otherwise silently swallowed)
  for (const line of out.split('\n')) {
    if (/^\s*(✖|⚠|Error|Warning)/i.test(line)) {
      console.log(`  ${line.trim()}`);
    }
  }
  return out;
}

async function main() {
  const config = await readConfig();
  const originalPath = config.ccInstallationPath;

  // If explicit paths given as CLI args, use those instead of discovery
  const extraPaths = process.argv.slice(2);

  let installs;
  if (extraPaths.length > 0) {
    console.log('Building installations from explicit paths...');
    installs = await Promise.all(extraPaths.map(installationFromPath));
  } else {
    console.log('Discovering installations...');
    installs = await findAllInstallations();
  }
  if (installs.length === 0) {
    console.error('No Claude Code installations found!');
    process.exit(1);
  }

  console.log(`Found ${installs.length} installation(s):\n`);
  for (const inst of installs) {
    console.log(`  ${inst.kind.padEnd(6)} v${inst.version}  ${inst.path}`);
  }
  console.log();

  const results = [];

  for (const inst of installs) {
    const label = `${inst.kind} v${inst.version}`;
    console.log(`--- Patching ${label} ---`);

    // Backup: out/ (overwritten each run) + backup_ro/ (write-once, never overwritten)
    const backupDir = resolve(OUT_DIR, inst.version, inst.kind);
    await mkdir(backupDir, { recursive: true });
    const backupPath = resolve(backupDir, 'backup' + (inst.kind === 'npm' ? '.js' : ''));
    try {
      await copyFile(inst.path, backupPath);
      console.log(`  backup -> ${backupPath}`);
    } catch (e) {
      console.error(`  backup failed: ${e.message}`);
      results.push({ ...inst, status: 'FAILED (backup)', error: e.message });
      continue;
    }

    // Read-only backup: only written once per version+kind, never overwritten
    const roDir = resolve(BACKUP_RO_DIR, inst.version, inst.kind);
    await mkdir(roDir, { recursive: true });
    const roPath = resolve(roDir, 'original' + (inst.kind === 'npm' ? '.js' : ''));
    try {
      await stat(roPath);
      // already exists, don't overwrite
    } catch {
      await copyFile(inst.path, roPath);
      console.log(`  backup_ro -> ${roPath} (first-time, read-only)`);
    }

    // Update config to point at this installation
    const cfg = await readConfig();
    cfg.ccInstallationPath = inst.path;
    await writeConfig(cfg);

    // Apply tweakcc
    try {
      let applyOut = runApply();

      // tweakcc exits 0 but skips prompts when templates are unavailable
      if (applyOut.includes('skipping system prompt customizations')) {
        console.warn(`  prompts unavailable for v${inst.version}, trying fallback...`);
        const created = await ensurePromptCache(inst.version);
        if (created) {
          clearCaches();
          // Restore binary to clean state before retry
          await robustCopy(backupPath, inst.path);
          applyOut = runApply();
        }
        if (applyOut.includes('skipping system prompt customizations')) {
          console.error(`  FAILED: system prompts skipped even after fallback`);
          results.push({ ...inst, status: 'FAILED (no prompts)' });
          await robustCopy(backupPath, inst.path).catch(() => {});
          continue;
        }
      }

      console.log(`  applied`);

      // Fix known tweakcc bugs in the patched output
      await postPatchFix(inst.path);

      // Save extracted JS files to versioned out dir (tweakcc writes these during --apply)
      if (inst.kind === 'native') {
        const tweakccDir = resolve(import.meta.dirname, '..');
        const origJs = resolve(tweakccDir, 'native-claudejs-orig.js');
        const patchedJs = resolve(tweakccDir, 'native-claudejs-patched.js');
        await copyFile(origJs, resolve(backupDir, 'backup.js')).catch(() => {});
        await copyFile(patchedJs, resolve(backupDir, 'patched.js')).catch(() => {});
      }

      // Save patched copy
      const patchedPath = resolve(backupDir, 'patched' + (inst.kind === 'npm' ? '.js' : ''));
      await copyFile(inst.path, patchedPath);
    } catch (e) {
      const stderr = e.stderr?.toString() || e.message;
      console.error(`  apply FAILED: ${stderr.slice(0, 200)}`);
      results.push({ ...inst, status: 'FAILED (apply)', error: stderr.slice(0, 200) });
      // Restore backup
      await robustCopy(backupPath, inst.path).catch((restoreErr) => {
        console.error(`  RESTORE FAILED: ${restoreErr.message}`);
        console.error(`  Manual restore from: ${backupPath}`);
      });
      continue;
    }

    // Smoke test -- if it fails, the binary is broken, restore backup
    try {
      smoke(inst);
      console.log(`  smoke OK`);
      clearCaches();
      results.push({ ...inst, status: 'OK' });
    } catch (e) {
      console.error(`  smoke FAILED: ${e.message}`);
      console.error(`  Restoring backup (patched binary is broken)...`);
      await robustCopy(backupPath, inst.path).catch((restoreErr) => {
        console.error(`  RESTORE FAILED: ${restoreErr.message}`);
        console.error(`  Manual restore from: ${backupPath}`);
      });
      clearCaches();
      results.push({ ...inst, status: 'FAILED (smoke)', error: e.message });
    }
  }

  // Restore original config path (npm = primary terminal claude)
  const cfg = await readConfig();
  cfg.ccInstallationPath = originalPath;
  await writeConfig(cfg);
  console.log(`\nRestored ccInstallationPath -> ${originalPath}`);

  // Summary
  console.log('\n=== Summary ===');
  console.log('Kind    Version  Status          Path');
  console.log('-'.repeat(80));
  for (const r of results) {
    console.log(
      `${r.kind.padEnd(7)} v${r.version.padEnd(8)} ${r.status.padEnd(15)} ${r.path}`
    );
  }

  const hardFailed = results.filter(r => r.status.startsWith('FAILED'));
  if (hardFailed.length > 0) {
    console.error(`\n${hardFailed.length} installation(s) failed.`);
    process.exit(1);
  }
}

main();
