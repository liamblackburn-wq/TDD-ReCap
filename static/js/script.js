const addDutiesButton = document.getElementById("add-duty")
const form = document.getElementById("form")
const loginView = document.getElementById('login-view')
const guestView = document.getElementById('dashboard-view');

const showDashboard = () => {
    loginView.classList.add('hidden')
    guestView.classList.remove('hidden')
}

const handleCoinCompletionToggle = () => {
    const coinCheckbox = document.querySelectorAll('.coin-checkbox')

    for (let checkbox = 0; checkbox < coinCheckbox.length; checkbox++) {
        coinCheckbox[checkbox].addEventListener('change', async (e) => {
            const isChecked = e.target.checked;
            const linkedId = e.target.dataset.linkId

            try {
                const response = await fetch(`/coin-duties/${linkedId}`, {
                    method: 'PUT',
                    headers: {
                        "Content-Type": "application/json"
                        },
                    body: JSON.stringify({is_complete: isChecked}),

                })
                if (!response.ok) {
                        const errorData = await response.json();
                        alert(errorData.error)
                    }
            } catch (error) {
                console.error("Network error", error)
            }
        })
    }
}

const fetchAndRenderDuties = async (role) => {
    const response = await fetch("/coin-duties")
    const data = await response.json()
    const automateList = document.getElementById('automate-list')
    let htmlTemplate = ""

    data.forEach(linkedDuty => {
        const isDisabled = (role === "user" || role === "admin") ? "" : "disabled"
        const isChecked = linkedDuty.is_complete ? "checked" : ""

        htmlTemplate += `
        <li class="listed-duty">
            <span>${linkedDuty.duty_name}</span>
            <input type="checkbox" class="coin-checkbox" data-link-id="${linkedDuty.id}" ${isDisabled} ${isChecked}>
        </li>
        `
    })
    automateList.innerHTML = htmlTemplate

    handleCoinCompletionToggle()
}

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

const initialiseDashboard = async (role) => {
    showDashboard()
    await fetchAndRenderDuties(role)

    if (role === "admin") {
        displayDutySelectDropdown()
        handleFormSubmission()
        handleDutyRemoval()
    }
}

