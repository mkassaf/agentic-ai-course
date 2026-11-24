'use strict';
// Exercise the exact sampling function used by the published browser tool.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync('assets/tools/sampling.html', 'utf8');
const tokenStart = html.indexOf('    const BASE_TOKENS = [');
const tokenEnd = html.indexOf('    const PRESETS =', tokenStart);
const functionStart = html.indexOf('    function computePipeline(', tokenEnd);
const functionEnd = html.indexOf('    function getStatusColors(', functionStart);
assert(tokenStart >= 0 && tokenEnd > tokenStart && functionStart > tokenEnd && functionEnd > functionStart);
const sandbox = {};
vm.runInNewContext(html.slice(tokenStart, tokenEnd) + html.slice(functionStart, functionEnd)
                   + '\nthis.run = computePipeline;', sandbox);
const run = sandbox.run;
const nearly = (a, b) => Math.abs(a - b) < 1e-8;

// After top-k, 0.42 / (0.42 + 0.22) = 0.65625. This already exceeds p=0.60,
// so top-p must remove the second token rather than using the old 0.42 probability.
let result = run(1.0, 2, 0.60);
assert.equal(result.keptCount, 1);
assert.equal(result.items[0].token, 'timeout');
assert(nearly(result.items[0].cumProb, 65.625));
assert(nearly(result.items[0].finalProb, 100));
assert.equal(result.items[1].status, 'cut_by_top_p');
assert.equal(result.items[2].status, 'cut_by_top_k');

result = run(1.0, 3, 0.80);
assert.equal(result.keptCount, 2);
assert.equal(result.items[2].status, 'cut_by_top_p');
assert(nearly(result.items[0].finalProb, 65.625));
assert(nearly(result.items[1].finalProb, 34.375));
assert(result.items[2].cumProb >= 80);
assert.equal(result.items[3].cumProb, null);

result = run(1.0, 8, 1.0);
assert.equal(result.keptCount, 8);
assert(nearly(result.items.reduce((sum, item) => sum + item.finalProb, 0), 100));
assert(nearly(result.items[0].finalProb, 42));
assert(run(0.2, 8, 1.0).items[0].finalProb > run(1.4, 8, 1.0).items[0].finalProb);
console.log('Interactive sampling math passed');
