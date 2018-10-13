/**
 * Google Maps API wrapper class.
 *
 * Relevant documentation
 * @link https://developers.google.com/maps/documentation/javascript/events
 * @link https://developers.google.com/maps/documentation/javascript/infowindows
 * @link https://developers.google.com/maps/documentation/javascript/geocoding#ReverseGeocoding
 */
class JobApplyMap {

    /**
     * Constructor
     */
    constructor() {
        this.map = null;
    }

    /**
     * Initialize API
     */
    init() {
        let mapContainer = document.getElementById('jobPostingsMap');
        if (mapContainer !== null ) {
            this.map = new google.maps.Map(mapContainer, {
                zoom: 13,
                center: {lat: 37.5, lng: 127}
            });

            this.addMarkers();
        }
    }

    addMarkers() {
        for (let i = 0; i < window.mapMarkers.length; i++) {
            let marker = window.mapMarkers[i],
                latlng = new google.maps.LatLng(marker.lat, marker.lng);

            let newMarker = new google.maps.Marker({
                position: latlng,
                title: marker.title
            });

            newMarker.setMap(this.map);
        }
    }

}

export default JobApplyMap;
