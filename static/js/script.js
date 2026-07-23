const createDutyButton = document.getElementById("create-duty");
const createCoinButton = document.getElementById("create-coin");
const dutyForm = document.getElementById("duty-form");
const coinForm = document.getElementById("coin-form");
const loginView = document.getElementById('login-view');
const guestView = document.getElementById('dashboard-view');
const coinsList = document.getElementById('coins-list');

const showDashboard = () => {
    loginView.classList.add('hidden')
    guestView.classList.remove('hidden')
}


const fetchAndRenderCoins = async (role) => {
    const response = await fetch('/coins')
    const dutyResponse = await fetch('/duties');
    const duties = await dutyResponse.json();
    const data = await response.json()
    let coinsListHtml = "";
    let optionsHtml = `<option value="">-- Select Duty --</option>`;

    duties.forEach(duty => {
        optionsHtml += `<option value="${duty.id}">${duty.name}</option>`
    })


    data.forEach((coin) => {
        const coinName = coin.name;
        const coinId = coin.id;

        const dutyDropdown = (role === "admin") ?
            `<select id="${coinId}-duty-dropdown" data-id="${coinId}">
                ${optionsHtml}
            </select>
            <button class="assign-duty-btn" data-coin-id="${coinId}">
                Assign
            </button>
            ` : ""

        coinsListHtml += `
        <li class="listed-coin" id="${coinId}-duty-list">
            <h2>${coinName}</h2>
            <span class="assign-duty-dropdown">
                ${dutyDropdown}
            </span>
            <ul class="duty-list" id="linked-duty-${coinId}">
            </ul>
        </li>
        `
    })
    coinsList.innerHTML = coinsListHtml;
}

const handleDutyAssignment = (role) => {
    coinsList.addEventListener('click', async (event) => {
        if (!event.target.classList.contains("assign-duty-btn")) return;

        const coinId = event.target.dataset.coinId;

        const dutyDropdown = document.getElementById(`${coinId}-duty-dropdown`);
        const dutyId = dutyDropdown.value;

        if (!dutyId) {
            alert("Please select a duty first!");
            return;
        }

        const payload = {
            coin_id: coinId,
            duty_id: dutyId,
        }

        try {
            const response = await fetch('/coin-duties', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            })
            if (response.ok) {
               await fetchAndRenderDuties(role)
            } else {
                const errorData = await response.json()
                alert(`Error: ${errorData.error}`)
            }
        } catch (error) {
            console.error("Network communication error", error)
        }
    })
}

const displayCreateCoinForm = () => {
    createCoinButton.addEventListener('click', () => {
        coinForm.classList.remove("hidden")
    });
}

const createCoin = (role) => {
    coinForm.addEventListener('submit', async (event)  => {
        event.preventDefault()

        const coinName = document.getElementById('coin-name').value;

        const payload = {
            name: coinName,
        }

        try {
            const response = await fetch('/coins', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            })
            if (!response.ok) {
                const errorData = await response.json()
                alert(errorData.error)
            } else {
                coinForm.reset()
                coinForm.classList.add('hidden')
                await fetchAndRenderCoins(role)
            }
        } catch (error) {
            console.error("Network error", error)
        }
    })
}

const handleCoinCompletionToggle = () => {
    const dutyCheckbox = document.querySelectorAll('.duty-checkbox')

    for (let checkbox = 0; checkbox < dutyCheckbox.length; checkbox++) {
        dutyCheckbox[checkbox].addEventListener('change', async (e) => {
            let isChecked = e.target.checked;
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
                        e.target.checked = !isChecked;
                        alert(errorData.error)
                    }
            } catch (error) {
                e.target.checked = !isChecked;
                console.error("Network error", error)
            }
        })
    }
}

const fetchAndRenderDuties = async (role) => {
    const response = await fetch("/coin-duties")
    const data = await response.json()

    document.querySelectorAll('.duty-list').forEach(list => list.innerHTML = "")

    data.forEach(linkedDuty => {
        const linkedDutyList = document.getElementById(`linked-duty-${linkedDuty.coin_id}`)

        if (!linkedDutyList) return;

        const isDisabled = (role === "user" || role === "admin") ? "" : "disabled"
        const isChecked = linkedDuty.is_complete ? "checked" : ""

        const deleteButtonHtml = (role === "admin") ? `<button class="remove-duty" data-id="${linkedDuty.id}">X</button>` : ""

        const dutyHtml = `
        <li class="listed-duty">
            <span>${linkedDuty.duty_name}</span>
            <input type="checkbox" class="duty-checkbox" data-link-id="${linkedDuty.id}" ${isDisabled} ${isChecked}>
            ${deleteButtonHtml}
        </li>
        `

        linkedDutyList.innerHTML += dutyHtml
    })
    handleCoinCompletionToggle()
}

const displayCreateDutyForm = () => {
    createDutyButton.addEventListener("click", () => {
        dutyForm.classList.remove("hidden")
    })
}

const createDuty = (role) => {
    dutyForm.addEventListener("submit", async (event) => {
        event.preventDefault()

        const nameValue = document.getElementById("duty-name").value
        const descriptionValue = document.getElementById("duty-description").value

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
                await fetchAndRenderDuties(role)
            } else {
                const errorData = await response.json()
                alert(`Error: ${JSON.stringify(errorData)}`)
            }
        } catch (error) {
            console.error("Network communication error", error)
        }
    })
}

const handleDutyRemoval = (role) => {
    const coinsList = document.getElementById('coins-list');
    if (!coinsList) return;

    coinsList.addEventListener("click", async (event) => {
        if (!event.target.classList.contains("remove-duty")) return;

        const button = event.target;
        const dutyId = button.dataset.id
        try {
            const response = await fetch(`/duties/${dutyId}`, {
                method: "DELETE"
            })
            if (response.ok) {
                await fetchAndRenderDuties(role)
            } else {
                const errorData = await response.json()
                alert(`Failed to delete: ${errorData.error || JSON.stringify(errorData)}`)
            }
        } catch (error) {
            console.error("Network communication error", error)
        }
    })
}

const initialiseDashboard = async (role) => {
    showDashboard()
    await fetchAndRenderCoins(role)
    await fetchAndRenderDuties(role)

    if (role === "admin") {
        displayCreateDutyForm()
        displayCreateCoinForm()
        createDuty(role)
        createCoin(role)
        handleDutyAssignment(role)
        handleDutyRemoval(role)
    }
}

