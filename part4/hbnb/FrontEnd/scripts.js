document.addEventListener('DOMContentLoaded', () => {
    // ==========================================
    // 1. PARTIE LOGIN (Page login.html)
    // ==========================================
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    const token = data.access_token || data.token;
                    document.cookie = `token=${token}; path=/`;
                    window.location.href = 'index.html';
                } else {
                    const errorData = await response.json();
                    alert('Login failed: ' + (errorData.message || response.statusText));
                }
            } catch (error) {
                alert('Erreur: ' + error.message);
            }
        });
    }

    // ==========================================
    // 2. PARTIE INDEX (Page index.html - Task 2)
    // ==========================================
    const placesList = document.getElementById('places-list');
    if (placesList) {
        checkAuthentication();
        setupPriceFilter();
    }

    // ==========================================
    // 3. PARTIE PLACE DETAILS (Page place.html - Task 3)
    // ==========================================
    const placeDetailsContainer = document.getElementById('place-details');
    if (placeDetailsContainer) {
        const placeId = getPlaceIdFromURL();
        if (placeId) {
            checkPlaceAuthentication(placeId);
        } else {
            placeDetailsContainer.innerHTML = "<p>Erreur : Aucun ID de lieu spécifié dans l'URL.</p>";
        }
    }
});


// ==========================================
// OUTILS COMMUNS
// ==========================================
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}


// ==========================================
// FONCTIONS POUR INDEX.HTML (Task 2)
// ==========================================
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
    } else {
        if (loginLink) loginLink.style.display = 'none';
    }
    fetchPlaces(token);
}

async function fetchPlaces(token) {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
            method: 'GET',
            headers: headers
        });
        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        }
    } catch (error) {
        console.error("Erreur Fetch:", error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = ''; 
    places.forEach(place => {
        const placeElement = document.createElement('div');
        placeElement.classList.add('place-card'); 
        const placePrice = place.price || place.price_by_night || 50;
        placeElement.dataset.price = placePrice; 

        placeElement.innerHTML = `
            <h3>${place.title || place.name || 'Lieu sans nom'}</h3>
            <p><strong>Prix par nuit :</strong> $${placePrice}</p>
            <p><strong>Localisation :</strong> Lat: ${place.latitude}, Lng: ${place.longitude}</p>
            <a href="place.html?id=${place.id}">Voir les détails</a>
        `;
        placesList.appendChild(placeElement);
    });
}

function setupPriceFilter() {
    const filterDropdown = document.getElementById('price-filter');
    if (!filterDropdown) return;

    const options = ['10', '50', '100', 'All'];
    filterDropdown.innerHTML = ''; 
    options.forEach(price => {
        const optionElement = document.createElement('option');
        optionElement.value = price;
        optionElement.textContent = price;
        filterDropdown.appendChild(optionElement);
    });

    filterDropdown.addEventListener('change', (event) => {
        const selectedPrice = event.target.value;
        const placeCards = document.querySelectorAll('.place-card');
        placeCards.forEach(card => {
            const placePrice = parseFloat(card.dataset.price);
            if (selectedPrice === 'All' || placePrice <= parseFloat(selectedPrice)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}


// ==========================================
// FONCTIONS POUR PLACE.HTML (Task 3)
// ==========================================
function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

function checkPlaceAuthentication(placeId) {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');
    const loginLink = document.getElementById('login-link');

    // Gestion de l'affichage si connecté ou non
    if (!token) {
        if (addReviewSection) addReviewSection.style.display = 'none';
        if (loginLink) loginLink.style.display = 'block';
    } else {
        if (addReviewSection) addReviewSection.style.display = 'block';
        if (loginLink) loginLink.style.display = 'none';
    }

    // Récupération des données du lieu
    fetchPlaceDetails(token, placeId);
}

async function fetchPlaceDetails(token, placeId) {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            document.getElementById('place-details').innerHTML = "<p>Lieu introuvable.</p>";
        }
    } catch (error) {
        console.error("Erreur Fetch:", error);
    }
}

function displayPlaceDetails(place) {
    const container = document.getElementById('place-details');
    
    const title = place.title || place.name || 'Lieu sans nom';
    const price = place.price || place.price_by_night || 'Non précisé';
    const description = place.description || 'Pas de description fournie.';

    const amenitiesHTML = (place.amenities && place.amenities.length > 0)
        ? `<ul>${place.amenities.map(a => `<li>${a.name || a}</li>`).join('')}</ul>`
        : '<p>Aucun équipement spécifié.</p>';

    const reviewsHTML = (place.reviews && place.reviews.length > 0)
        ? `<ul>${place.reviews.map(r => `<li><strong>Avis :</strong> ${r.text || r.comment}</li>`).join('')}</ul>`
        : '<p>Aucun avis pour le moment.</p>';

    container.innerHTML = `
        <h2>${title}</h2>
        <p><strong>Prix par nuit :</strong> $${price}</p>
        <p><strong>Description :</strong> ${description}</p>
        
        <div class="amenities-section">
            <h3>Équipements (Amenities)</h3>
            ${amenitiesHTML}
        </div>
        
        <div class="reviews-section">
            <h3>Avis (Reviews)</h3>
            ${reviewsHTML}
        </div>
    `;
}
    