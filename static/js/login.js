const loginView = document.getElementById('login-view')
const loginForm = document.getElementById('login-form');
const loginButton = document.getElementById('login-button');
const guestLogin = document.getElementById('guest-login');
const guestView = document.getElementById('guest-view');

document.addEventListener('DOMContentLoaded', () => {
    const showDashboard = () => {
        loginView.classList.add('hidden')
        guestView.classList.remove('hidden')
    }

    guestLogin.addEventListener('click', () => {
        showDashboard()
    })

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault()
        
    })
})