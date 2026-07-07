import { useState, useEffect } from 'react'

function App() {
  const [health, setHealth] = useState<string>("Connecting to API...")

    useEffect(() => {
        fetch('http://localhost:5000/')
            .then(res => res.json())
            .then((data) => {
                setHealth(`${data.api} is ${data.status.toUpperCase()}!`)
            })
            .catch((err) => {
                setHealth("Failed to connect to backend server.")
                console.error("Connection error:", err)
            })

    }, []);

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Coins & Duties Dashboard</h1>
      <hr />
      <h3>API Status: <span style={{ color: 'blue' }}>{health}</span></h3>
    </div>
  )
}

export default App