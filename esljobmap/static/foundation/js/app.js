$(document).foundation();

import JobApplication from './apply.js';
import JobMapSetup from './jobMap.js';
import ListFilter from './listFilter.js';


$(document).ready(function() {
    let japply = new JobApplication(),
        lfilter = new ListFilter();

    japply.init();
    lfilter.init();
});

function initMap() {
    let jmap = new JobMapSetup();
    jmap.init();
}
window.initMap = initMap;