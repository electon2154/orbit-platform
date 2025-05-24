// Geolocation utilities for Leaflet maps
const GeolocationUtil = {
    // Default fallback coordinates (Iraq - Baghdad)
    defaultCoords: {
        lat: 33.3152,
        lng: 44.3661,
        zoom: 7
    },

    /**
     * Get user's current location and execute callback
     * @param {Function} successCallback - Function to call with coordinates {lat, lng}
     * @param {Function} errorCallback - Function to call if geolocation fails
     * @param {Object} options - Geolocation options
     */
    getCurrentLocation: function(successCallback, errorCallback, options = {}) {
        const defaultOptions = {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 300000 // 5 minutes cache
        };
        
        const geoOptions = { ...defaultOptions, ...options };

        if (!navigator.geolocation) {
            console.warn('Geolocation is not supported by this browser');
            if (errorCallback) errorCallback(new Error('Geolocation not supported'));
            return;
        }

        // Show loading indicator if available
        this.showLocationLoading();

        navigator.geolocation.getCurrentPosition(
            (position) => {
                this.hideLocationLoading();
                const coords = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                    accuracy: position.coords.accuracy
                };
                
                console.log('Current location obtained:', coords);
                if (successCallback) successCallback(coords);
            },
            (error) => {
                this.hideLocationLoading();
                console.warn('Geolocation error:', error.message);
                
                // Use default coordinates as fallback
                console.log('Using default coordinates as fallback');
                if (successCallback) {
                    successCallback(this.defaultCoords);
                }
                
                if (errorCallback) errorCallback(error);
            },
            geoOptions
        );
    },

    /**
     * Initialize a Leaflet map with user's current location
     * @param {String} mapElementId - ID of the map container element
     * @param {Object} options - Map options
     * @returns {Object} Leaflet map instance
     */
    initMapWithCurrentLocation: function(mapElementId, options = {}) {
        const defaultOptions = {
            zoom: 13,
            fallbackZoom: 7,
            showAccuracyCircle: true,
            autoSetView: true
        };
        
        const mapOptions = { ...defaultOptions, ...options };
        
        // Create map with default view first
        const map = L.map(mapElementId).setView([this.defaultCoords.lat, this.defaultCoords.lng], mapOptions.fallbackZoom);
        
        // Add tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Get current location and update map
        this.getCurrentLocation(
            (coords) => {
                if (mapOptions.autoSetView) {
                    map.setView([coords.lat, coords.lng], mapOptions.zoom);
                }
                
                // Add accuracy circle if requested and accuracy is available
                if (mapOptions.showAccuracyCircle && coords.accuracy) {
                    L.circle([coords.lat, coords.lng], {
                        radius: coords.accuracy,
                        fillOpacity: 0.1,
                        color: '#4285f4'
                    }).addTo(map);
                }
            },
            (error) => {
                // Map already initialized with default coordinates
                console.log('Using default map location due to geolocation error');
            }
        );

        return map;
    },

    /**
     * Update existing map to user's current location
     * @param {Object} map - Leaflet map instance
     * @param {Object} options - Update options
     */
    updateMapToCurrentLocation: function(map, options = {}) {
        const defaultOptions = {
            zoom: 13,
            showAccuracyCircle: false,
            addMarker: false
        };
        
        const updateOptions = { ...defaultOptions, ...options };

        this.getCurrentLocation(
            (coords) => {
                map.setView([coords.lat, coords.lng], updateOptions.zoom);
                
                if (updateOptions.addMarker) {
                    const marker = L.marker([coords.lat, coords.lng]).addTo(map);
                    if (updateOptions.markerPopup) {
                        marker.bindPopup(updateOptions.markerPopup).openPopup();
                    }
                }
                
                if (updateOptions.showAccuracyCircle && coords.accuracy) {
                    L.circle([coords.lat, coords.lng], {
                        radius: coords.accuracy,
                        fillOpacity: 0.1,
                        color: '#4285f4'
                    }).addTo(map);
                }
            },
            (error) => {
                console.log('Could not update map to current location:', error.message);
            }
        );
    },

    /**
     * Show loading indicator for location acquisition
     */
    showLocationLoading: function() {
        const existingLoader = document.getElementById('geolocation-loader');
        if (existingLoader) return;

        const loader = document.createElement('div');
        loader.id = 'geolocation-loader';
        loader.innerHTML = `
            <div style="position: fixed; top: 20px; right: 20px; z-index: 10000; 
                        background: rgba(66, 133, 244, 0.9); color: white; 
                        padding: 10px 15px; border-radius: 5px; font-size: 14px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.3);">
                <i class="fas fa-location-arrow fa-spin" style="margin-left: 8px;"></i>
                جاري تحديد موقعك...
            </div>
        `;
        document.body.appendChild(loader);
    },

    /**
     * Hide loading indicator
     */
    hideLocationLoading: function() {
        const loader = document.getElementById('geolocation-loader');
        if (loader) {
            loader.remove();
        }
    },

    /**
     * Set coordinates in form fields
     * @param {Object} coords - Coordinates {lat, lng}
     * @param {String} latFieldId - ID of latitude input field
     * @param {String} lngFieldId - ID of longitude input field
     * @param {String} locationFieldId - ID of combined location field (optional)
     */
    setCoordinatesInForm: function(coords, latFieldId = 'latitude', lngFieldId = 'longitude', locationFieldId = null) {
        const latField = document.getElementById(latFieldId);
        const lngField = document.getElementById(lngFieldId);
        
        if (latField) latField.value = coords.lat.toFixed(6);
        if (lngField) lngField.value = coords.lng.toFixed(6);
        
        if (locationFieldId) {
            const locationField = document.getElementById(locationFieldId);
            if (locationField) {
                locationField.value = `${coords.lat.toFixed(6)}, ${coords.lng.toFixed(6)}`;
            }
        }
    }
};

// Make it globally available
window.GeolocationUtil = GeolocationUtil; 