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
                alert(`Error: ${JSON.stringify(errorData)}`)
            }
        } catch (error) {
            console.error("Network communication error", error)
        }
    })
}

const handleDutyRemoval = () => {
    const removeButtons = document.querySelectorAll(".remove-duty")

    removeButtons.forEach(button => {
        button.addEventListener("click", async (event) => {
            event.preventDefault()

            const dutyId = button.dataset.id

            try {
                const response = await fetch(`/duties/${dutyId}`, {
                    method: "DELETE"
                })

                if (response.ok) {
                    window.location.reload()
                } else {
                    const errorData = await response.json()
                    alert(`Failed to delete: ${JSON.stringify(errorData)}`)
                }
            } catch (error) {
                console.error("Network communication error", error)
            }
        })
    })
}

displayDutySelectDropdown()
handleFormSubmission()
handleDutyRemoval()