/**
 * Google Maps API wrapper class.
 *
 * Relevant documentation
 * @link https://developers.google.com/maps/documentation/javascript/events
 * @link https://developers.google.com/maps/documentation/javascript/markers
 * @link https://developers.google.com/maps/documentation/javascript/infowindows
 * @link https://developers.google.com/maps/documentation/javascript/geocoding#ReverseGeocoding
 */
export default class JobMapSetup {

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
        this.googleMarkerMapHoverListeners = {};
        this.googleMarkerMapClickListeners = {};
        this.disinterestedIconImage = this.cdnImg('koco-man/gray-60x60.png') + '?v=1549075351';
        this.appliedIconImage = this.cdnImg('koco-man/black-60x60.png');
        this.interestedUri = '/korea/employment/teacher/job/interested/';
        this.isProcessing = false;
    }

    /**
     * Initialize API
     */
    init() {
        let mapContainer = document.getElementById('map');
        if (mapContainer !== null) {
            let gestureControls = 'greedy';
            if (window.jobMap.isRecruiter) {
                gestureControls = 'cooperative';
            }
            if (window.jobMap.isMobile) {
                this.jobInterestClickEventType = 'dblclick';
            } else {
                this.jobInterestClickEventType = 'click';
            }
            this.map = new google.maps.Map(mapContainer, {
                zoom: window.jobMap.zoom,
                center: {lat: window.jobMap.lat, lng: window.jobMap.lng},
                mapTypeControlOptions: {
                    mapTypeIds: ['roadmap'],
                },
                mapTypeControl: false,
                streetViewControl: false,
                gestureHandling: gestureControls
            });
            this.addExistingJobMarkers();
            this.infoWindow = new google.maps.InfoWindow;
            this.geocoder = new google.maps.Geocoder;
            this.$addressError = $('#addressSearchError');
            this.$locationError = $('#postJobLocationError');
            this.$addressInput = $('#mapAddressInput');
            this.$warningModal = $('#warningModal');

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

            // Bind window close event.
            this.map.addListener('click', () => {
                this.closeMapInfoWindow();
            });

            // Show warning modal if neccesary.
            if (this.$warningModal.length > 0) {
                this.$warningModal.foundation('open');
            }
        }
    }

    /**
     * Create the CDN url for the supplied file path.
     *
     * @param path
     * @returns {string}
     */
    cdnImg(path)
    {
        return '/assets/images/' + path
    }

    /**
     * Load all uploaded job posts into the map.
     */
    addExistingJobMarkers() {
        for (let i = 0; i < window.jobMap.markers.length; i++) {
            let markerData = window.jobMap.markers[i],
                latlng = new google.maps.LatLng(markerData.lat, markerData.lng),
                iconImageUrl = this.resolveIconImage(markerData),
                marker = new google.maps.Marker({
                    position: latlng,
                    optimized: false,
                    icon: this.makeComplexIcon(iconImageUrl)
                });

            marker.setMap(this.map);
            let clickListener = null;

            // Display job info on hover if they are interested.
            if (markerData.isDisinterested === 0) {
                let lamb = () => {
                    // Open up the window and display the job info.
                    this.infoWindow.setContent(markerData.content);
                    this.infoWindow.open(this.map, marker);
                };

                // Add marker listeners to the map.
                let hoverListener = marker.addListener('mouseover', lamb);
                clickListener = marker.addListener('click', lamb);
                this.googleMarkerMapHoverListeners[markerData.id] = hoverListener;
            } else {
                // No hover events but when the user clicks, they can mark the job as interested again.
                clickListener = marker.addListener(this.jobInterestClickEventType, () => {
                    // Mark the job as interested.
                    let a = document.createElement('a');
                    a.setAttribute('href', this.interestedUri + markerData.id);
                    updateMapMarker(null, a, markerData.id, 0);
                });
            }

            // Track marker for easy access later on.
            this.googleMarkerMap[markerData.id] = marker;

            // Track the listeners so that we can replace them when needed.
            this.googleMarkerMapClickListeners[markerData.id] = clickListener;
        }
    }

    /**
     * Determine which image to use for the marker icon.
     *
     * @param markerData
     * @returns {string}
     */
    resolveIconImage(markerData) {
        let iconImageUrl = window.jobMap.iconImage;

        if (window.jobMap.isRecruiter) {
            // When the job post does not belong to the recruiter, gray it out.
            if (markerData.isJobPoster === 0) {
                iconImageUrl = this.disinterestedIconImage;
            }
        } else {
            if (markerData.hasApplied === 1) {
                iconImageUrl = this.appliedIconImage;
            } else if (markerData.isDisinterested === 1) {
                iconImageUrl = this.disinterestedIconImage;
            }
        }

        return iconImageUrl;
    }

    /**
     * Go through the markers and update the one that matches the supplied id.
     *
     * @param id
     * @param content
     * @param isDisinterested
     */
    updateExistingJobMarker(id, content, isDisinterested) {
        let marker = this.googleMarkerMap[id],
            iconImage = isDisinterested === 1 ? this.disinterestedIconImage : window.jobMap.iconImage;

        marker.setIcon(this.makeComplexIcon(iconImage));

        // Remove the old listeners.
        let hoverListener = this.googleMarkerMapHoverListeners[id],
            clickListener = this.googleMarkerMapClickListeners[id];

        google.maps.event.removeListener(hoverListener);
        google.maps.event.removeListener(clickListener);
        delete this.googleMarkerMapHoverListeners[id];
        delete this.googleMarkerMapClickListeners[id];

        // Add new listeners with the updated data.
        if (isDisinterested === 1) {
            clickListener = marker.addListener(this.jobInterestClickEventType, () => {
                // Mark the job as interested.
                let a = document.createElement('a');
                a.setAttribute('href', this.interestedUri + id);
                updateMapMarker(null, a, id, 0);
            });
        } else {
            hoverListener = marker.addListener('mouseover', () => {
                // Open up the window and display the job info.
                this.infoWindow.setContent(content);
                this.infoWindow.open(this.map, marker);
            });

            clickListener = marker.addListener('click', () => {
                // Open up the window and display the job info.
                this.infoWindow.setContent(content);
                this.infoWindow.open(this.map, marker);
            });
        }

        // Keep track of listeners so that we can remove them later.
        this.googleMarkerMapHoverListeners[id] = hoverListener;
        this.googleMarkerMapClickListeners[id] = clickListener;
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
            icon: this.makeComplexIcon(window.jobMap.markerImage),
            animation: google.maps.Animation.DROP,
            draggable: true
        });

        // Add drag listener.
        google.maps.event.addListener(this.currentMarker, 'dragend', (e) => {
            this.retrackCurrentLocation(e.latLng)
        });

        // Track new location.
        this.retrackCurrentLocation(latLng);
    }

    /**
     * When the marker is placed or moved, we need to track the new value and inform the user.
     *
     * @param latLng
     */
    retrackCurrentLocation(latLng) {
        // Track the location.
        this.latitude = latLng.lat();
        this.longitude = latLng.lng();

        // Show the user the current address.
        this.geocodeLatLng(this.latitude, this.longitude, this.currentMarker);
    }

    /**
     * Make a complex google maps icon from an image URL.
     *
     * @param imageUrl
     * @returns {{url: *, size: google.maps.Size, scaledSize: google.maps.Size}}
     */
    makeComplexIcon(imageUrl) {
        return {
            url: imageUrl,
            size: new google.maps.Size(30, 30),
            scaledSize: new google.maps.Size(30, 30)
        };
    }

    /**
     * Lookup the real address, get the latitude and longitude values, and place a marker.
     *
     * @param address
     */
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
                    icon: this.makeComplexIcon(window.jobMap.markerImage),
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

                // Shift the position to the top of the screen.
                $(window).scrollTop(0);
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
        if (!this.isProcessing) {
            this.isProcessing = true;

            $.ajax({
                type: 'POST',
                url: action,
                data: formData
            }).done((response) => {
                let responseHtml = $.parseHTML(response);
                let extGeneralJobFields = $(responseHtml).find('#generalJobFields');

                if (response.includes('jobPostListConfirm')) {
                    window.location = window.jobMap.successLocation;
                } else {
                    this.$generalJobFields.html(extGeneralJobFields.html());
                    this.isProcessing = false;
                }
            });
        }
    }

    /**
     * Wrapper function to close the window from an external invoker.
     */
    closeMapInfoWindow() {
        this.infoWindow.close();
    }
}
