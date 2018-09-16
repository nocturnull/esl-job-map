/**
 * Google Maps API wrapper class.
 *
 * Relevant documentation
 * @link https://developers.google.com/maps/documentation/javascript/events
 * @link https://developers.google.com/maps/documentation/javascript/infowindows
 * @link https://developers.google.com/maps/documentation/javascript/geocoding#ReverseGeocoding
 */
class GoogleMap {

    /**
     * Constructor
     */
    constructor() {
        this.currentMarker = null;
        this.map = null;
        this.infoWindow = null;
        this.geocoder = null;
        this.latitude = 0;
        this.longitude = 0;
        this.address = '';
        this.form = null;
        this.$formErrors = null;
    }

    /**
     * Initialize API
     */
    init() {
        let mapContainer = document.getElementById('map');
        if (mapContainer !== null ) {
            this.map = new google.maps.Map(mapContainer, {
                zoom: 13,
                center: {lat: 37.5, lng: 127}
            });
            this.infoWindow = new google.maps.InfoWindow;
            this.geocoder = new google.maps.Geocoder;
            this.$formErrors = $('#postJobformErrors');

            // Add click listener to the map.
            this.map.addListener('click', (e) => {
                this.placeMarkerAndPanTo(e.latLng);
            });

            // Bind ajax form listener.
            this.form = $('#jobPostForm');
            this.form.submit((e) => {
                this.$formErrors.addClass('no-show');
                this.appendMapData(this.form.attr('action'));
                e.preventDefault();
                return false;
            })
        }
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
            animation: google.maps.Animation.DROP
        });
        this.map.panTo(latLng);

        // Track the location.
        this.latitude = latLng.lat();
        this.longitude = latLng.lng();

        // Inform the user of the address.
        this.geocodeLatLng(this.latitude, this.longitude, this.currentMarker);
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
                  // Track the address.
                  this.address = results[0].formatted_address;
                  this.infoWindow.setContent(this.address);

                  // Open up the window and display the address.
                  this.infoWindow.open(this.map, marker);
              } else {
                window.alert('No results found');
              }
            } else {
              window.alert('Geocoder failed due to: ' + status);
            }
          });
    }

    /**
     * Appends the map data to the form before submitting it.
     *
     * @param action
     */
    appendMapData(action) {
        let formData = {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'title': $('#id_title').val(),
            'class_type': $('#id_class_type').val(),
            'contact_name': $('#id_contact_name').val(),
            'contact_email': $('#id_contact_email').val(),
            'contact_number': $('#id_contact_number').val(),
            'schedule': $('#id_schedule').val(),
            'other_requirements': $('#id_other_requirements').val(),
            'is_full_time': $('input[name="is_full_time"]').val(),
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
            if (response.includes('jobPostListConfirm')) {
                window.location = '/employment/recruiter/job/my-jobs';
            } else {
                this.$formErrors.removeClass('no-show');
            }
        });
    }
}

export default GoogleMap;
