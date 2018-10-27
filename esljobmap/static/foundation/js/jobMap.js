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
        this.form = null;
        this.$locationError = null;
        this.$generalJobFields = null;
    }

    /**
     * Initialize API
     */
    init() {
        let mapContainer = document.getElementById('map');
        if (mapContainer !== null ) {
            this.map = new google.maps.Map(mapContainer, {
                zoom: 13,
                center: {lat: 37.5, lng: 127},
                mapTypeControlOptions: {
                    mapTypeIds: ['roadmap'],
                },
                mapTypeControl: false,
                streetViewControl: false
            });
            this.addExistingJobMarkers();
            this.infoWindow = new google.maps.InfoWindow;
            this.geocoder = new google.maps.Geocoder;
            this.$locationError = $('#postJobLocationError');

            // Add click listener to the map if a recruiter.
            if (window.isRecruiter) {
                this.map.addListener('click', (e) => {
                    this.placeMarkerAndPanTo(e.latLng);
                });
            }

            // Bind ajax form listener.
            this.form = $('#jobPostForm');
            this.form.submit((e) => {
                this.$locationError.addClass('no-show');
                if (this.latitude > 0 && this.longitude > 0) {
                    this.submitMapData(this.form.attr('action'));
                } else {
                    this.$locationError.removeClass('no-show');
                }
                e.preventDefault();
                return false;
            });

            // Bind job field sets.
            this.$generalJobFields = $('#generalJobFields');
        }
    }

    addExistingJobMarkers() {
        for (let i = 0; i < window.mapMarkers.length; i++) {
            let markerData = window.mapMarkers[i],
                latlng = new google.maps.LatLng(markerData.lat, markerData.lng);

            let marker = new google.maps.Marker({
                position: latlng,
                icon: window.mapIconImage
            });

            marker.setMap(this.map);
            marker.addListener('mouseover', () => {
                // Open up the window and display the job info.
                this.infoWindow.setContent(markerData.content);
                this.infoWindow.open(this.map, marker);
            });
            marker.addListener('mouseout', function () {
                if (this.infoWindow) {
                    this.infoWindow.close();
                }
            });
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
            icon: window.mapIconImage,
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
            console.log(response);
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
