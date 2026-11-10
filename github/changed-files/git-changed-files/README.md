# Vendored `git-changed-files`

This directory contains an internal, vendored fork of
[`git-changed-files`](https://github.com/kandhavivekraj/git-changed-files) used
by the [`github/changed-files` action](../README.md). It is not the public
package entry point and should not be installed from npm or yarn.

The helper is an ES module and exports a default function:

```js
import gitChangedFiles from './index.js';

const result = await gitChangedFiles({
  baseBranch: 'main',
  showStatus: true,
});
```

Its `baseBranch` default is `main`. When `showStatus` is enabled, each status
object uses the `filename` key, for example:

```js
{ filename: 'src/example.js', status: 'Modified' }
```

For action inputs, outputs, and usage, see the
[`github/changed-files` README](../README.md). Changes to this vendored helper
should be made and tracked in
[`elastic/oblt-actions`](https://github.com/elastic/oblt-actions).
