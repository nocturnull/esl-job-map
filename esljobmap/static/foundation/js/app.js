$(document).foundation();

import JobApplication from './apply.js';
import ProfileForm from './profileForm.js';
import JobMapSetup from './jobMap.js';
import ListFilter from './listFilter.js';


$(document).ready(function() {
    let japply = new JobApplication(),
        pform = new ProfileForm(),
        lfilter = new ListFilter();

    japply.init();
    pform.init();
    lfilter.init();
});

function initMap() {
    let jmap = new JobMapSetup();
    jmap.init();
}
window.initMap = initMap;