#!/usr/bin/env node
// verify_html_js.js - Basic JS syntax check for an HTML file
// Usage: node verify_html_js.js <html-file>
const fs = require('fs');
const path = require('path');

const file = process.argv[2];
if (!file) { console.error('Usage: node verify_html_js.js <html-file>'); process.exit(1); }

const html = fs.readFileSync(file, 'utf8');
const scriptBlocks = [...html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/gi)].map(m => m[1]);

let errors = 0;
scriptBlocks.forEach((src, i) => {
  try { new Function(src); }
  catch(e) { console.error(`Script block ${i+1} syntax error: ${e.message}`); errors++; }
});

if (errors === 0) { console.log(`OK: ${path.basename(file)} — ${scriptBlocks.length} script block(s) passed.`); }
else { process.exit(1); }
