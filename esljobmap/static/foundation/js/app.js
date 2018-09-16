$(document).foundation();

import JobToggle from './job.js'
import JobApplication from './apply.js';
import GoogleMap from './googleMap.js';

$(document).ready(function() {
    let jtoggle = new JobToggle(),
        japply = new JobApplication();

    jtoggle.init();
    japply.init();
});

function initMap() {
    let gmap = new GoogleMap();
    gmap.init();
}
window.initMap = initMap;