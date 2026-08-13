const loggerTableBody = document.getElementById('logs-table-body');

const fetchLogs = async () => {
    try {
        const response = await fetch('/api/logs', { method: 'GET' })

        if (!response.ok) {
            console.error(`Failed to fetch logs: ${response.status}`);
            return;
        }

        const logs = await response.json()

        let tableRows = ''

        logs.forEach(log => {
            tableRows += `<tr>
                    <td>${new Date(log.timestamp).toLocaleString()}</td>
                    <td>${log.path}</td>
                    <td>${log.request_method}</td>
                    <td>${log.status_code}</td>
                </tr>
                `
        })
        loggerTableBody.innerHTML = tableRows;
    } catch (error) { console.error("Network error", error)}
}

document.addEventListener('DOMContentLoaded', async () => {
    await fetchLogs();
})
