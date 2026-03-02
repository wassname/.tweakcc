<!--
name: 'Tool Description: ReadFile'
description: Tool description for reading files
ccVersion: 2.1.30
variables:
  - DEFAULT_READ_LINES
  - MAX_LINE_LENGTH
  - CONDITIONAL_READ_LINES
  - CAN_READ_PDF_FILES
  - BASH_TOOL_NAME
-->
Read files from the local filesystem. Absolute paths only.

- Reads up to ${DEFAULT_READ_LINES} lines by default. Lines truncated at ${MAX_LINE_LENGTH} chars.
- Optional offset/limit for long files. Results in cat -n format (line numbers from 1).
- Reads images (PNG, JPG etc) visually, Jupyter notebooks (.ipynb) with outputs.${CAN_READ_PDF_FILES()?`
- PDFs: large (>10 pages) MUST use pages parameter (e.g. "1-5"). Max 20 pages/request.`:""}
- Cannot read directories -- use \`ls\` via ${BASH_TOOL_NAME}.
- Speculatively read multiple files in parallel when useful.
- Always use this tool for screenshots the user provides.
