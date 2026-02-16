import { spawnSync } from 'child_process';
import matcher from 'matcher';

function filterFiles(files, options) {
  let filteredFiles = [];
  for (let format of options) {
    let tempFiles = files.filter(file => {
      return matcher(Array.of(file), Array.of(format)).length >= 1;
    });
    filteredFiles.push(...tempFiles);
  }
  return filteredFiles;
}

export {
  filterFiles
};
