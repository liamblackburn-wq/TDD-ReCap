const loginForm = document.getElementById('login-form');
const guestLogin = document.getElementById('guest-login');

document.addEventListener('DOMContentLoaded',  () => {
    guestLogin.addEventListener('click', async() => {
         await initialiseDashboard('guest')
    })

    loginForm.addEventListener('submit', async (event) => {
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
            const data = await response.json();
            console.log(data.role)
            if (data.role === "user" || data.role === "admin") {
                await initialiseDashboard(data.role)
            }
        }
        else {
           const errorData = await response.json();
           alert(errorData.error)
        }

    })
})