const createDutyButton = document.getElementById("create-duty");
const createCoinButton = document.getElementById("create-coin");
const dutyForm = document.getElementById("duty-form");
const coinForm = document.getElementById("coin-form");
const loginView = document.getElementById('login-view');
const adminView = document.getElementById('admin-view');
const guestView = document.getElementById('dashboard-view');
const coinsList = document.getElementById('coins-list');
const logsLink = document.getElementById('logs-link');

let currentRole = 'guest';

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
            `<select class="duty-option" id="${coinId}-duty-dropdown" data-id="${coinId}">
                ${optionsHtml}
            </select>
            <button class="assign-duty-btn" data-coin-id="${coinId}">
                Assign
            </button>
            ` : ""

        const deleteCoinBtn = (role === "admin") ?
            `<button class="delete-coin-btn" data-coin-id="${coinId}">Delete Coin</button>
            ` : ""

        coinsListHtml += `
        <li class="listed-coin" id="${coinId}-duty-list">
            <div class="coin-header">
                <h2>${coinName}</h2>
                ${deleteCoinBtn}
            </div>
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

const fetchAndRenderDuties = async (role) => {
    const response = await fetch("/coin-duties")
    const data = await response.json()

    document.querySelectorAll('.duty-list').forEach(list => list.innerHTML = "")

    data.forEach(linkedDuty => {
        const linkedDutyList = document.getElementById(`linked-duty-${linkedDuty.coin_id}`)

        if (!linkedDutyList) return;

        const isDisabled = (role === "user" || role === "admin") ? "" : "disabled"
        const isChecked = linkedDuty.is_complete ? "checked" : ""

        const unassignButtonHtml = (role === "admin") ? `<button class="remove-duty" data-id="${linkedDuty.id}">Unassign</button>` : ""

        const dutyHtml = `
        <li class="listed-duty">
            <span>${linkedDuty.duty_name}</span>
            <p>${linkedDuty.duty_description}</p>
            <div class="complete-checkbox">
                <label for="duty-check-${linkedDuty.id}">Complete?</label>
                <input type="checkbox" id="duty-check-${linkedDuty.id}" class="duty-checkbox" data-link-id="${linkedDuty.id}" ${isDisabled} ${isChecked}>
            </div>
            ${unassignButtonHtml}
        </li>
        `

        linkedDutyList.innerHTML += dutyHtml
    })
}

createCoinButton?.addEventListener('click', () => coinForm.classList.remove("hidden"));
createDutyButton?.addEventListener("click", () => dutyForm.classList.remove("hidden"));

coinForm?.addEventListener("submit", async (event) => {
    event.preventDefault()

    const coinName = document.getElementById('coin-name').value;

    try {
        const response = await fetch('/coins', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({name: coinName})
        })
        if (response.ok) {
            coinForm.reset()
            coinForm.classList.add('hidden')
            await fetchAndRenderCoins(currentRole)
        } else {
            const errorData = await response.json()
            alert(errorData.error || "An unknown error occurred.");
        }
    } catch (error) {
        console.error("Network error", error)
    }
})

dutyForm?.addEventListener("submit", async (event) => {
    event.preventDefault()
    const dutyName = document.getElementById('duty-name').value;
    const dutyDescription = document.getElementById('duty-description').value;

    const payload = {
        name: dutyName,
        description: dutyDescription,
    }

    try {
        const response = await fetch('/duties', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        })
        if (response.ok) {
            dutyForm.reset()
            dutyForm.classList.add('hidden')
            await fetchAndRenderCoins(currentRole)
            await fetchAndRenderDuties(currentRole)
        } else {
            const errorData = await response.json()
            alert(errorData.error || "An unknown error occurred.");
        }
    } catch (error) {
        console.error("Network error", error)
    }
})

coinsList?.addEventListener("click", async (event) => {
    const button = event.target

    if (button.classList.contains('delete-coin-btn')) {
        const coinId = button.dataset.coinId

        try {
            const response = await fetch(`/coins/${coinId}`, { method: 'DELETE' })
            if (response.ok) {
                await fetchAndRenderCoins(currentRole);
                await fetchAndRenderDuties(currentRole);
            } else {
                const errorData = await response.json()
                alert(errorData.error || "An unknown error occurred.");
            }
        } catch (error) {
            console.error("Network error", error)
        }
    }

    if (button.classList.contains('assign-duty-btn')) {
        const coinId = button.dataset.coinId
        const dutyDropdown = document.getElementById(`${coinId}-duty-dropdown`)
        const dutyId = dutyDropdown?.value;

        if (!dutyId) {
            alert("Please select a duty first!")
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
                await fetchAndRenderDuties(currentRole)
            } else {
                const errorData = await response.json()
                alert(errorData.error || "An unknown error occurred.");
            }
        } catch (error) {
            console.error("Network error", error)
        }
    }

    if (button.classList.contains('remove-duty')) {
        const linkId = button.dataset.id
        try {
            const response = await fetch(`/coin-duties/${linkId}`, { method: 'DELETE' })
            if (response.ok) {
                await fetchAndRenderDuties(currentRole)
            } else {
                const errorData = await response.json()
                alert(errorData.error || "An unknown error occurred.");
            }
        } catch (error) {
            console.error("Network error", error)
        }
    }
});

coinsList?.addEventListener("change", async (event) => {
    if (!event.target.classList.contains('duty-checkbox')) return;

    const checkbox = event.target;
    const isChecked = checkbox.checked;
    const linkedId = checkbox.dataset.linkId;

    try {
        const response = await fetch(`/coin-duties/${linkedId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({is_complete: isChecked})
        })
        if (!response.ok) {
            checkbox.checked = !isChecked;
            const errorData = await response.json()
            alert(errorData.error || "An unknown error occurred.");
        }
    } catch (error) {
        checkbox.checked = !isChecked;
        console.error("Network error", error)
    }
})

const initialiseDashboard = async (role) => {
    console.log("INIT DASHBOARD")
    currentRole = role
    showDashboard()

    if (role === "admin") {
        adminView.classList.remove('hidden');
        logsLink.classList.remove('hidden');

    } else {
        adminView.classList.add('hidden');
    }

    await fetchAndRenderCoins(role)
    await fetchAndRenderDuties(role)
}

