$(document).foundation();

import JobApplication from './apply.js';
import ProfileForm from './profileForm.js';
import JobMapSetup from './jobMap.js';
import ListFilter from './listFilter.js';
import DetectInternetExplorer from './detectIE.js';


$(document).ready(function() {
    let japply = new JobApplication(),
        pform = new ProfileForm(),
        lfilter = new ListFilter(),
        detie = new DetectInternetExplorer();

    detie.init();
    japply.init();
    pform.init();
    lfilter.init();
});

function initMap() {
    let jmap = new JobMapSetup();
    jmap.init();

    window.jobMapHandle = jmap;
}

function updateMapMarker(event, anchor, id, isDisinterested) {
    event.preventDefault();
    $.ajax({
        type: 'GET',
        url: $(anchor).attr('href')
    }).done((response) => {
        window.jobMapHandle.updateExistingJobMarker(id, response, isDisinterested);
    });

    return false;
}


window.initMap = initMap;
window.updateMapMarker = updateMapMarker;
