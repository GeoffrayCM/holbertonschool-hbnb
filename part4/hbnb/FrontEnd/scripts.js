document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            loginUser(email, password);
        });
    }
});
async function loginUser(email, password) {
    try {
        const response = await fetch('http://127.0.0.1:5500/api/v1/places', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();

            // stocker le token
            document.cookie = `token=${data.access_token}; path=/`;

            // redirection
            window.location.href = 'index.html';

        } else {
            alert('Login failed');
        }

    } catch (error) {
        console.error(error);
        alert('Erreur serveur');
    }
}