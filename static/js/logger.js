const fetchLogs = async () => {
    try {
        const response = await fetch('/api/logs', { method: 'GET' })

        if (!response.ok) {
            console.error(`Failed to fetch logs: ${response.status}`);
            return;
        }

        const logs = await response.json()

        logs.forEach(log => {
            console.log(log)
        })
    } catch (error) { console.error("Network error", error)}
}

document.addEventListener('change', async () => {
    await fetchLogs();
})
