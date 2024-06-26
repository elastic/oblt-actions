const fs = require('fs')

module.exports = async ({github, context, core}) => {
    const clusterInfo = JSON.parse(fs.readFileSync(`${process.env.GITHUB_WORKSPACE}/cluster-info.json`, 'utf8'))
    const statusUrl = `https://github.com/elastic/observability-test-environments/pulls?q=is%3Apr+${clusterInfo.ClusterName}`
    await core.summary
        .addHeading('Test Results')
        .addTable([
            [{data: 'Cluster Name', header: true}, {data: 'Stack Version', header: true}, {data: 'Status', header: true}],
            [clusterInfo.ClusterName, clusterInfo.StackVersion, clusterInfo.RemoteClusterName],
        ])
        .addLink('View staging deployment!', statusUrl)
        .write()
}
