/**
 * Google Maps API wrapper class.
 *
 * Relevant documentation
 * @link https://developers.google.com/maps/documentation/javascript/events
 * @link https://developers.google.com/maps/documentation/javascript/markers
 * @link https://developers.google.com/maps/documentation/javascript/infowindows
 * @link https://developers.google.com/maps/documentation/javascript/geocoding#ReverseGeocoding
 */
class JobMapSetup {

    /**
     * Constructor
     */
    constructor() {
        this.map = null;
        this.currentMarker = null;
        this.infoWindow = null;
        this.geocoder = null;
        this.latitude = 0;
        this.longitude = 0;
        this.address = '';
        this.$form = null;
        this.$addressForm = null;
        this.$addressInput = null;
        this.$addressError = null;
        this.$locationError = null;
        this.$generalJobFields = null;
        this.googleMarkerMap = {};
        this.googleMarkerMapListeners = {};
    }

    /**
     * Initialize API
     */
    init() {
        let mapContainer = document.getElementById('map');
        if (mapContainer !== null) {
            this.map = new google.maps.Map(mapContainer, {
                zoom: window.jobMap.zoom,
                center: {lat: window.jobMap.lat, lng: window.jobMap.lng},
                mapTypeControlOptions: {
                    mapTypeIds: ['roadmap'],
                },
                mapTypeControl: false,
                streetViewControl: false
            });
            this.addExistingJobMarkers();
            this.infoWindow = new google.maps.InfoWindow;
            this.geocoder = new google.maps.Geocoder;
            this.$addressError = $('#addressSearchError');
            this.$locationError = $('#postJobLocationError');
            this.$addressInput = $('#mapAddressInput');

            // Add click listener to the map if a recruiter.
            if (window.jobMap.isRecruiter) {
                this.map.addListener('click', (e) => {
                    this.placeMarkerAndPanTo(e.latLng);
                });
            }

            // Bind ajax form listener.
            this.$form = $('#jobPostForm');
            this.$form.submit((e) => {
                this.$locationError.addClass('no-show');
                if (this.latitude > 0 && this.longitude > 0) {
                    this.submitMapData(this.$form.attr('action'));
                } else {
                    this.$locationError.removeClass('no-show');
                }
                e.preventDefault();
                return false;
            });

            // Bind address lookup form.
            this.$addressForm = $('#addressSearchForm');
            this.$addressForm.submit((e) => {
                this.$addressError.addClass('no-show');
                e.preventDefault();
                this.geocodeAddressAndPlaceMarker($('#mapAddressInput').val());
                return false;
            });

            // Bind job field sets.
            this.$generalJobFields = $('#generalJobFields');
        }
    }

    addExistingJobMarkers() {
        for (let i = 0; i < window.jobMap.markers.length; i++) {
            let markerData = window.jobMap.markers[i],
                latlng = new google.maps.LatLng(markerData.lat, markerData.lng),
                markerIcon = window.jobMap.iconImage;

            if (markerData.hasApplied === 1) {
                markerIcon = window.jobMap.appliedIconImage;
            } else if (markerData.isDisinterested === 1) {
                markerIcon = window.jobMap.disinterestedIconImage;
            }

            let marker = new google.maps.Marker({
                position: latlng,
                icon: markerIcon
            });

            marker.setMap(this.map);
            let listener = marker.addListener('mouseover', () => {
                // Open up the window and display the job info.
                this.infoWindow.setContent(markerData.content);
                this.infoWindow.open(this.map, marker);
            });

            this.googleMarkerMap[markerData.id] = marker;
            this.googleMarkerMapListeners[markerData.id] = listener;
        }
    }

    /**
     * Go through the markers and update the one that matches the supplied id.
     *
     * @param id
     * @param content
     * @param isDisinterested
     */
    updateExistingJobMarker(id, content, isDisinterested) {
        let marker = this.googleMarkerMap[id];
        if (isDisinterested === 1) {
            marker.setIcon(window.jobMap.disinterestedIconImage);
        } else {
            marker.setIcon(window.jobMap.iconImage);
        }

        // Remove the old listener.
        let listener = this.googleMarkerMapListeners[id];
        google.maps.event.removeListener(listener);
        delete this.googleMarkerMapListeners[id];

        // Add a new listener with the updated data.
        marker.addListener('mouseover', () => {
            // Open up the window and display the job info.
            this.infoWindow.setContent(content);
            this.infoWindow.open(this.map, marker);
        });

        this.infoWindow.close();
    }

    /**
     * Callback: Places marker on the map when a user clicks on it.
     *
     * @param latLng
     */
    placeMarkerAndPanTo(latLng) {
        // Delete any old marker they selected.
        if (this.currentMarker !== null) {
            this.currentMarker.setMap(null);
        }

        // Place the marker.
        this.currentMarker = new google.maps.Marker({
            position: latLng,
            map: this.map,
            icon: window.jobMap.iconImage,
            animation: google.maps.Animation.DROP
        });
        this.map.panTo(latLng);

        // Track the location.
        this.latitude = latLng.lat();
        this.longitude = latLng.lng();

        // Inform the user of the address.
        this.geocodeLatLng(this.latitude, this.longitude, this.currentMarker);
    }

    geocodeAddressAndPlaceMarker(address) {
        this.geocoder.geocode({'address': address}, (results, status) => {
            if (status === 'OK') {
                let loc = results[0].geometry.location,
                    formatted_address = results[0].formatted_address;

                this.map.setCenter(loc);
                // Clear old marker location.
                if (this.currentMarker !== null) {
                    this.currentMarker.setMap(null);
                }

                // Add new marker.
                this.currentMarker = new google.maps.Marker({
                    map: this.map,
                    position: loc,
                    icon: window.jobMap.iconImage,
                    animation: google.maps.Animation.DROP
                });

                // Track the location.
                this.latitude = loc.lat();
                this.longitude = loc.lng();

                // Track the human readable address.
                this.address = formatted_address;

                // Show in the info window.
                this.infoWindow.setContent(formatted_address);

                // Open up the window and display the address.
                this.infoWindow.open(this.map, this.currentMarker);
            } else {
                this.$addressError.removeClass('no-show');
            }
        });
    }

    /**
     * Callback: Looks up the user-friendly address and displays it in the marker.
     *
     * @param lat
     * @param lng
     * @param marker
     */
    geocodeLatLng(lat, lng, marker) {
        let latlng = {lat: lat, lng: lng};
        this.geocoder.geocode({'location': latlng}, (results, status) => {
            if (status === 'OK') {
              if (results[0]) {
                  // Track the human readable address.
                  this.address = results[0].formatted_address;

                  // Update the address in the input field.
                  this.$addressInput.val(results[0].formatted_address);

                  // Show in the info window.
                  this.infoWindow.setContent(this.address);

                  // Open up the window and display the address.
                  this.infoWindow.open(this.map, marker);
              } else {
                console.log('No results found');
              }
            } else {
              console.log('Geocoder failed due to: ' + status);
            }
          });
    }

    /**
     * Appends the map data to the form before submitting it.
     *
     * @param action
     */
    submitMapData(action) {
        let formData = {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'title': $('#id_title').val(),
            'class_type': $('#id_class_type').val(),
            'contact_name': $('#id_contact_name').val(),
            'contact_email': $('#id_contact_email').val(),
            'contact_number': $('#id_contact_number').val(),
            'schedule': $('#id_schedule').val(),
            'other_requirements': $('#id_other_requirements').val(),
            'is_full_time': $('input[name="is_full_time"]:checked').val(),
            'salary': $('#id_salary').val(),
            'benefits': $('#id_benefits').val(),
            'pay_rate': $('#id_pay_rate').val(),
            'latitude': this.latitude,
            'longitude': this.longitude,
            'address': this.address
        };

        $.ajax({
            type: 'POST',
            url: action,
            data: formData
        }).done((response) => {
            let responseHtml = $.parseHTML(response);
            let extGeneralJobFields = $(responseHtml).find('#generalJobFields');

            if (response.includes('jobPostListConfirm')) {
                window.location = '/employment/recruiter/job/my-jobs';
            } else {
                this.$generalJobFields.html(extGeneralJobFields.html());
            }
        });
    }
}

export default JobMapSetup;
