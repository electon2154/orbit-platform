// Initialize location picker
function initLocationPicker(mapElementId, latInputId, lngInputId, defaultLat = 24.7136, defaultLng = 46.6753) {
    if (!document.getElementById(mapElementId)) return;

    const map = new google.maps.Map(document.getElementById(mapElementId), {
        center: { lat: defaultLat, lng: defaultLng },
        zoom: 8
    });

    const marker = new google.maps.Marker({
        position: { lat: defaultLat, lng: defaultLng },
        map: map,
        draggable: true
    });

    // Update marker position on map click
    map.addListener('click', (e) => {
        marker.setPosition(e.latLng);
        updateLocationInputs(e.latLng);
    });

    // Update marker position on marker drag
    marker.addListener('dragend', (e) => {
        updateLocationInputs(e.latLng);
    });

    function updateLocationInputs(latLng) {
        document.getElementById(latInputId).value = latLng.lat();
        document.getElementById(lngInputId).value = latLng.lng();
    }
}

// Interactive search with suggestions
function initSearchSuggestions(inputId, suggestionsUrl) {
    const searchInput = document.getElementById(inputId);
    if (!searchInput) return;

    let timeoutId;
    const suggestionsList = document.createElement('div');
    suggestionsList.className = 'suggestions-list';
    searchInput.parentNode.appendChild(suggestionsList);

    searchInput.addEventListener('input', () => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            const query = searchInput.value.trim();
            if (query.length < 2) {
                suggestionsList.innerHTML = '';
                return;
            }

            fetch(`${suggestionsUrl}?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsList.innerHTML = '';
                    data.forEach(item => {
                        const div = document.createElement('div');
                        div.className = 'suggestion-item';
                        div.textContent = item.name;
                        div.addEventListener('click', () => {
                            searchInput.value = item.name;
                            suggestionsList.innerHTML = '';
                            if (item.url) {
                                window.location.href = item.url;
                            }
                        });
                        suggestionsList.appendChild(div);
                    });
                });
        }, 300);
    });

    // Close suggestions on click outside
    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target)) {
            suggestionsList.innerHTML = '';
        }
    });
}

// Order preparation code generator
function generatePreparationCode() {
    return Math.random().toString(36).substring(2, 8).toUpperCase();
}

// Cart management
const cart = {
    items: [],
    
    addItem(productId, quantity = 1) {
        fetch('/cart/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ product_id: productId, quantity: quantity })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.updateCartCount(data.count);
                showNotification('تمت إضافة المنتج إلى السلة', 'success');
            } else {
                showNotification(data.message, 'error');
            }
        });
    },
    
    updateCartCount(count) {
        const cartCountElement = document.getElementById('cart-count');
        if (cartCountElement) {
            cartCountElement.textContent = count;
        }
    }
};

// Notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Utility Functions
function showToast(message, type = 'success') {
    const toastContainer = document.createElement('div');
    toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    document.body.appendChild(toastContainer);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', () => {
        toastContainer.remove();
    });
}

// Cart Functions
function updateCartCount() {
    fetch('/cart/count/')
        .then(response => response.json())
        .then(data => {
            const cartCount = document.getElementById('cartCount');
            if (cartCount) {
                cartCount.textContent = data.count;
            }
        })
        .catch(error => console.error('Error:', error));
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize cart count
    // updateCartCount();
});

// Handle form submissions with CSRF token
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form[method="post"]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const csrfToken = getCookie('csrftoken');
            if (csrfToken) {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'csrfmiddlewaretoken';
                input.value = csrfToken;
                form.appendChild(input);
            }
        });
    });
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}); 