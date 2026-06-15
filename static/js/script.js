const addDutiesButton = document.getElementById("add-duty")
const form = document.getElementById("form")

const displayDutySelectDropdown = () => {
    addDutiesButton.addEventListener("click", (event) => {
        form.classList.remove("hidden")
    })
}

const handleFormSubmission = () => {
    form.addEventListener("submit", async (event) => {
        event.preventDefault()

        const nameValue = document.getElementById("duty_name").value
        const descriptionValue = document.getElementById("duty_description").value

        const payload = {
            name: nameValue,
            description: descriptionValue
        }

        try {
            const response = await fetch('/duties', {
                method: 'POST',
                headers: {
                    "content-type": "application/json",
                },
                body: JSON.stringify(payload)
            })

            if (response.ok) {
                window.location.reload()
            } else {
                const errorData = await response.json()
                alert(`Error: ${errorData}`)
            }
        } catch (error) {
            console.error("Network communication error", error)
        }
    })
}

displayDutySelectDropdown()
handleFormSubmission()