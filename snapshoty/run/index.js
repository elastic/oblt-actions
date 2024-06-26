const core = require('@actions/core');
const exec = require('@actions/exec');
const os = require("os");

async function run() {
  try {
    const gcsClientEmail = core.getInput('gcs-client-email');
    const gcsPrivateKey = core.getInput('gcs-private-key');
    const gcsPrivateKeyId = core.getInput('gcs-private-key-id');
    const gcsProject = core.getInput('gcs-project');
    const bucketName = core.getInput('bucket-name');
    const config = core.getInput('config');

    const workDir = process.env.GITHUB_WORKSPACE;
    const userInfo = os.userInfo();

    const args = [
      'run', '--rm',
      '-v', `${workDir}:/app`,
      '-u', `${userInfo.uid}:${userInfo.gid}`,
      '-w', '/app',
      '-e', `GCS_CLIENT_EMAIL=${gcsClientEmail}`,
      '-e', `GCS_PRIVATE_KEY=${gcsPrivateKey}`,
      '-e', `GCS_PRIVATE_KEY_ID=${gcsPrivateKeyId}`,
      '-e', `GCS_PROJECT=${gcsProject}`
    ]

    // GCS env vars are secrets
    for (secret of [gcsClientEmail, gcsPrivateKey, gcsPrivateKeyId, gcsProject]) {
        core.setSecret(secret);
    }

    // Forward env vars
    Object.keys(process.env).forEach(function (key) {
      if (key.startsWith("GITHUB_") || key.startsWith("RUNNER_")) {
        let value = process.env[key];
        args.push('-e', `${key}=${value}`);

        if (key === 'GITHUB_TOKEN') {
          core.setSecret(value);
        }
      }

      // Special case so we can inject env variables
      if (key.startsWith("SNAPSHOTY_")) {
        let value = process.env[key];
        let variable = key.replace("SNAPSHOTY_", "")
        args.push('-e', `${variable}=${value}`);
      }
    });
    args.push('docker.elastic.co/observability-ci/snapshoty:v1', 'snapshoty');
    if (core.isDebug()) {
      args.push('--debug');
    }
    args.push('--config', config, 'upload', '--bucket-name', bucketName);

    return await exec.exec('docker', args);
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
