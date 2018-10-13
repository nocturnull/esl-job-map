$(document).foundation();

import JobToggle from './job.js'
import JobApplication from './apply.js';
import JobMapSetup from './jobMap.js';


$(document).ready(function() {
    let jtoggle = new JobToggle(),
        japply = new JobApplication();

    jtoggle.init();
    japply.init();
});

function initMap() {
    let jmap = new JobMapSetup();
    jmap.init();
}
window.initMap = initMap;