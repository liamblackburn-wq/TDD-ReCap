const loginForm = document.getElementById('login-form');
const guestLogin = document.getElementById('guest-login');

document.addEventListener('DOMContentLoaded',  () => {
    guestLogin?.addEventListener('click', async() => {
        await fetch("/api/logout", {method: 'POST'})
        window.location.href = "/apprenticeduties";
    })

    loginForm?.addEventListener('submit', async (event) => {
        event.preventDefault();
        const usernameValue = document.getElementById('username').value;
        const passwordValue= document.getElementById('password').value;

        const response = await fetch("/api/login", {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
                },
            body: JSON.stringify({
                "username": usernameValue,
                "password": passwordValue
            })
        });

        if (response.ok) {
            window.location.href = "/apprenticeduties";
        }
        else {
           const errorData = await response.json();
           alert(errorData.error || "Invalid Login");
        }

    })
})