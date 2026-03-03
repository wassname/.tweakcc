#!/usr/bin/env node
/**
 * Discover all Claude Code installations and patch each via tweakcc.
 *
 * Strategy: for each install, temporarily set ccInstallationPath in config.json,
 * run `npx tweakcc --apply`, then restore the original (npm) path.
 */

import { findAllInstallations, helpers } from 'tweakcc';
const { clearCaches } = helpers;
import { readFile, writeFile, mkdir, copyFile } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { resolve, dirname } from 'node:path';

const CONFIG_PATH = resolve(import.meta.dirname, '..', 'config.json');
const OUT_DIR = resolve(import.meta.dirname, '..', 'out');

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

async function main() {
  const config = await readConfig();
  const originalPath = config.ccInstallationPath;

  console.log('Discovering installations...');
  const installs = await findAllInstallations();
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

    // Backup
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

    // Update config to point at this installation
    const cfg = await readConfig();
    cfg.ccInstallationPath = inst.path;
    await writeConfig(cfg);

    // Apply tweakcc
    try {
      const applyOut = execFileSync('npx', ['tweakcc', '--apply'], {
        encoding: 'utf8',
        timeout: 120_000,
        cwd: resolve(import.meta.dirname, '..'),
        stdio: ['pipe', 'pipe', 'pipe'],
      });
      console.log(`  applied`);

      // Save patched copy
      const patchedPath = resolve(backupDir, 'patched' + (inst.kind === 'npm' ? '.js' : ''));
      await copyFile(inst.path, patchedPath);
    } catch (e) {
      const stderr = e.stderr?.toString() || e.message;
      console.error(`  apply FAILED: ${stderr.slice(0, 200)}`);
      results.push({ ...inst, status: 'FAILED (apply)', error: stderr.slice(0, 200) });
      // Restore backup
      await copyFile(backupPath, inst.path).catch((restoreErr) => {
        console.error(`  RESTORE FAILED: ${restoreErr.message}`);
        console.error(`  Manual restore from: ${backupPath}`);
      });
      continue;
    }

    // Smoke test
    let smokeStatus = 'OK';
    try {
      smoke(inst);
      console.log(`  smoke OK`);
    } catch (e) {
      smokeStatus = 'OK (smoke failed)';
      console.warn(`  smoke FAILED: ${e.message}`);
    }

    clearCaches();
    results.push({ ...inst, status: smokeStatus });
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

  const failed = results.filter(r => r.status !== 'OK');
  if (failed.length > 0) {
    console.error(`\n${failed.length} installation(s) failed.`);
    process.exit(1);
  }
}

main();
