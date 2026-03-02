<!--
name: 'Tool Description: LSP'
description: Description for the LSP tool.
ccVersion: 2.0.73
-->
LSP code intelligence. Operations: goToDefinition, findReferences, hover, documentSymbol, workspaceSymbol, goToImplementation, prepareCallHierarchy, incomingCalls, outgoingCalls.

All require: filePath, line (1-based), character (1-based). LSP server must be configured for the file type.
