var mapContainer = document.getElementById('map');
var agent = window.navigator.userAgent;
// agent = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'; // IE 10
// agent = 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'; // IE 11

if (mapContainer !== null) {
    if (agent.indexOf('MSIE ') > 0 || agent.indexOf('Trident/') > 0) {
        alert('Internet explorer detected, in order to use the map please use a modern web browser.')
    }
}
