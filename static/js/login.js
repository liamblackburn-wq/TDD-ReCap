const loginView = document.getElementById('login-view')
const loginForm = document.getElementById('login-form');
const loginButton = document.getElementById('login-button');
const guestLogin = document.getElementById('guest-login');
const guestView = document.getElementById('dashboard-view');

document.addEventListener('DOMContentLoaded', () => {
    const showDashboard = () => {
        loginView.classList.add('hidden')
        guestView.classList.remove('hidden')
    }

    guestLogin.addEventListener('click', () => {
        showDashboard()
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
                showDashboard()
            }
        }
        else {
           const errorData = await response.json();
           alert(errorData.error)
        }

    })
})