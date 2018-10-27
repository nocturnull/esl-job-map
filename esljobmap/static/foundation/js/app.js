$(document).foundation();

import JobApplication from './apply.js';
import JobMapSetup from './jobMap.js';


$(document).ready(function() {
    let japply = new JobApplication();

    japply.init();
});

function initMap() {
    let jmap = new JobMapSetup();
    jmap.init();
}
window.initMap = initMap;