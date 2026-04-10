/* ============================================================
   HBnB — scripts.js
   API Base : http://127.0.0.1:5000/api/v1
   ============================================================ */

const API = 'http://127.0.0.1:5000/api/v1';

function getToken() { return localStorage.getItem('hbnb_token'); }
function setToken(t) { localStorage.setItem('hbnb_token', t); }
function removeToken() { localStorage.removeItem('hbnb_token'); }
function isLoggedIn() { return !!getToken(); }

function updateHeader() {
  var btn = document.querySelector('.login-button');
  if (!btn) return;
  if (isLoggedIn()) {
    btn.textContent = 'Logout';
    btn.href = '#';
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      removeToken();
      window.location.reload();
    });
  } else {
    btn.textContent = 'Login';
    btn.href = 'login.html';
  }
}

/* ── LOGIN ── */
function initLoginPage() {
  var loginBtn = document.getElementById('login-btn');
  if (!loginBtn) return;
  loginBtn.addEventListener('click', async function(e) {
    e.preventDefault();
    var email    = document.getElementById('email').value.trim();
    var password = document.getElementById('password').value.trim();
    var errorEl  = document.getElementById('login-error');
    try {
      var res = await fetch(API + '/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, password: password })
      });
      if (res.ok) {
        var data = await res.json();
        setToken(data.access_token);
        window.location.href = 'index.html';
      } else {
        if (errorEl) errorEl.textContent = 'Email ou mot de passe incorrect.';
      }
    } catch (err) {
      if (errorEl) errorEl.textContent = 'Impossible de joindre le serveur.';
    }
  });
}

/* ── INDEX ── */
var IMAGES = [
  'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&q=80',
  'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600&q=80',
  'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=600&q=80',
  'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=600&q=80',
  'https://images.unsplash.com/photo-1560347876-aeef00ee58a1?w=600&q=80',
  'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=600&q=80'
];

function initIndexPage() {
  var grid = document.querySelector('.places-grid');
  if (!grid) return;
  loadPlaces(grid, 'all');
  var filter = document.getElementById('price-filter');
  if (filter) {
    filter.addEventListener('change', function() { loadPlaces(grid, filter.value); });
  }
}

async function loadPlaces(grid, priceFilter) {
  grid.innerHTML = '<p style="color:var(--text-muted);padding:1rem;">Chargement...</p>';
  try {
    var headers = {};
    if (getToken()) headers['Authorization'] = 'Bearer ' + getToken();
    var res = await fetch(API + '/places/', { headers: headers });
    if (!res.ok) throw new Error('Impossible de charger les places');
    var places = await res.json();
    grid.innerHTML = '';
    if (places.length === 0) {
      grid.innerHTML = '<p style="color:var(--text-muted);padding:1rem;">Aucune place trouvée.</p>';
      return;
    }
    places.forEach(function(place, i) {
      var name = place.title || place.name || 'Sans nom';
      var id   = place.id;
      var img  = IMAGES[i % IMAGES.length];
      var article = document.createElement('article');
      article.className = 'place-card';
      article.innerHTML =
        '<img class="place-card-img" src="' + img + '" alt="' + name + '" />' +
        '<div class="place-card-body">' +
          '<h3>' + name + '</h3>' +
          '<p class="price" id="price-' + id + '">...</p>' +
          '<a href="place.html?id=' + id + '&img=' + (i % IMAGES.length) + '" class="details-button">View Details</a>' +
        '</div>';
      grid.appendChild(article);
      fetch(API + '/places/' + id)
        .then(function(r) { return r.json(); })
        .then(function(d) {
          var priceEl = document.getElementById('price-' + id);
          var price = d.price !== undefined ? d.price : '—';
          var numPrice = parseFloat(price);
          var show = true;
          if (priceFilter === '0-50')    show = numPrice < 50;
          if (priceFilter === '50-150')  show = numPrice >= 50  && numPrice < 150;
          if (priceFilter === '150-300') show = numPrice >= 150 && numPrice < 300;
          if (priceFilter === '300+')    show = numPrice >= 300;
          if (!show) {
            article.style.display = 'none';
          } else if (priceEl) {
            priceEl.innerHTML = '$' + price + ' <span>/ night</span>';
          }
        })
        .catch(function() {
          var priceEl = document.getElementById('price-' + id);
          if (priceEl) priceEl.textContent = '—';
        });
    });
  } catch (err) {
    grid.innerHTML = '<p style="color:var(--accent);padding:1rem;">Erreur : ' + err.message + '</p>';
  }
}

/* ── PLACE DETAILS ── */
function initPlacePage() {
  var params  = new URLSearchParams(window.location.search);
  var placeId = params.get('id');
  if (!placeId) return;
  var imgIndex = parseInt(params.get('img') || '0');
  loadPlaceDetails(placeId, imgIndex);
  loadReviews(placeId);
  var reviewBtn = document.querySelector('.add-review-btn');
  if (reviewBtn) {
    if (isLoggedIn()) {
      reviewBtn.href = 'add_review.html?id=' + placeId;
      reviewBtn.style.display = 'inline-block';
    } else {
      reviewBtn.style.display = 'none';
    }
  }
}

async function loadPlaceDetails(placeId, imgIndex) {
  var heroImg = document.querySelector('.place-details-hero');
  if (heroImg && IMAGES[imgIndex]) heroImg.src = IMAGES[imgIndex];
  var infoEl = document.querySelector('.place-info');
  if (!infoEl) return;
  try {
    var res = await fetch(API + '/places/' + placeId);
    if (!res.ok) throw new Error('Place introuvable');
    var p = await res.json();
    document.title = 'HBnB — ' + (p.title || p.name || 'Place');
    var h1 = infoEl.querySelector('h1');
    if (h1) h1.textContent = p.title || p.name || 'Sans nom';
    var metas = infoEl.querySelectorAll('.place-meta-item .value');
    if (metas[0]) metas[0].textContent = (p.owner && p.owner.first_name) ? p.owner.first_name : 'Inconnu';
    if (metas[1]) metas[1].textContent = '$' + (p.price || '—') + ' / night';
    if (metas[2]) metas[2].textContent = p.latitude && p.longitude ? p.latitude + ', ' + p.longitude : '—';
    if (metas[3]) metas[3].textContent = '—';
    var desc = infoEl.querySelector('.place-description');
    if (desc) desc.textContent = p.description || 'Aucune description disponible.';
    var amenList = infoEl.querySelector('.amenities-list');
    if (amenList && p.amenities && p.amenities.length > 0) {
      var iconMap = {
        'wifi': 'icon_wifi.png',
        'wi-fi': 'icon_wifi.png',
        'bath': 'icon_bath.png',
        'bathroom': 'icon_bath.png',
        'bed': 'icon_bed.png',
        'bedroom': 'icon_bed.png'
      };
      amenList.innerHTML = p.amenities.map(function(a) {
        var name = a.name || a;
        var key = name.toLowerCase();
        var icon = null;
        for (var k in iconMap) {
          if (key.includes(k)) { icon = iconMap[k]; break; }
        }
        var img = icon ? '<img src="' + icon + '" alt="' + name + '" style="width:18px;height:18px;margin-right:5px;vertical-align:middle;" />' : '';
        return '<li class="amenity-tag">' + img + name + '</li>';
      }).join('');
    }
  } catch (err) {
    if (infoEl) infoEl.innerHTML = '<p style="color:var(--accent);">Erreur : ' + err.message + '</p>';
  }
}

async function loadReviews(placeId) {
  var section = document.querySelector('.reviews-section');
  if (!section) return;
  try {
    var res = await fetch(API + '/places/' + placeId + '/reviews');
    if (!res.ok) throw new Error('Impossible de charger les avis');
    var reviews = await res.json();
    var h2 = section.querySelector('h2');
    section.innerHTML = '';
    if (h2) section.appendChild(h2);
    if (reviews.length === 0) {
      section.innerHTML += '<p style="color:var(--text-muted);">Aucun avis. Soyez le premier !</p>';
      return;
    }
    reviews.forEach(function(r) {
      var stars = '★'.repeat(r.rating || 0) + '☆'.repeat(5 - (r.rating || 0));
      var card = document.createElement('article');
      card.className = 'review-card';
      card.innerHTML =
        '<div class="review-card-inner">' +
          '<div class="review-header">' +
            '<span class="reviewer-name">' + (r.user_name || 'Anonyme') + '</span>' +
            '<span class="review-rating">' + stars + ' ' + r.rating + '/5</span>' +
          '</div>' +
          '<p class="review-comment">' + (r.text || '') + '</p>' +
        '</div>';
      section.appendChild(card);
    });
  } catch (err) {
    console.error(err);
  }
}

/* ── ADD REVIEW ── */
function initAddReviewPage() {
  if (!isLoggedIn()) {
    window.location.href = 'login.html';
    return;
  }
  var params  = new URLSearchParams(window.location.search);
  var placeId = params.get('id');
  var form = document.querySelector('.add-review');
  if (!form) return;
  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    var ratingInput = form.querySelector('input[name="rating"]:checked');
    var rating  = ratingInput ? ratingInput.value : null;
    var comment = document.getElementById('comment').value.trim();
    var errorEl = document.getElementById('review-error');
    if (!rating) {
      if (errorEl) errorEl.textContent = 'Veuillez sélectionner une note.';
      return;
    }
    try {
      var res = await fetch(API + '/reviews/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + getToken()
        },
        body: JSON.stringify({ text: comment, rating: parseInt(rating), place_id: placeId })
      });
      if (res.ok) {
        window.location.href = 'place.html?id=' + placeId;
      } else {
        var data = await res.json();
        if (errorEl) errorEl.textContent = data.error || data.message || 'Échec de la soumission.';
      }
    } catch (err) {
      if (errorEl) errorEl.textContent = 'Impossible de joindre le serveur.';
    }
  });
}

/* ── INIT ── */
document.addEventListener('DOMContentLoaded', function() {
  updateHeader();
  var path = window.location.pathname;
  if (path.includes('login.html'))      initLoginPage();
  else if (path.includes('place.html')) initPlacePage();
  else if (path.includes('add_review')) initAddReviewPage();
  else                                  initIndexPage();
});