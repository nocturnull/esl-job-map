/**
 * Detect IE
 *
 * returns version of IE or false, if browser is not Internet Explorer
 * @link https://codepen.io/gapcode/pen/vEJNZN
 */
class DetectInternetExplorer {

    /**
     * Constructor
     */
    constructor() {
        this.mapContainer = document.getElementById('map');
        this.agent = window.navigator.userAgent;
        // this.agent = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'; // IE 10
        // this.agent = 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'; // IE 11
    }

    init() {
        if (this.mapContainer !== null) {
            if (this.agent.indexOf('MSIE ') > 0 || this.agent.indexOf('Trident/') > 0) {
                alert('Internet explorer detected, in order to use the map please use a modern web browser.')
            }
        }
    }
}

export default DetectInternetExplorer;
