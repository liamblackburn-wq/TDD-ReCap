const addDutiesButton = document.getElementById("add-duty")
const form = document.getElementById("form")

const displayDutySelectDropdown = () => {
    addDutiesButton.addEventListener("click", (event) => {
        form.classList.remove("hidden")
    })
}

displayDutySelectDropdown()