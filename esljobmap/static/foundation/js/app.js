$(document).foundation();

import JobToggle from './job.js'
import JobApplication from './apply.js';
import JobPostMap from './jobPostMap.js';
import JobApplyMap from './jobApplyMap.js';


$(document).ready(function() {
    let jtoggle = new JobToggle(),
        japply = new JobApplication();

    jtoggle.init();
    japply.init();
});

function initMap() {
    let jpmap = new JobPostMap(),
        jamap = new JobApplyMap();

    jpmap.init();
    jamap.init();
}
window.initMap = initMap;