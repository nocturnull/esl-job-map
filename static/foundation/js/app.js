$(document).foundation();

import JobMapSetup from './jobMap.js';
import ListFilter from './listFilter.js';
import StripeClient from './stripe.js';
import Applicant from './applicant.js';



$(document).ready(function() {
    let lfilter = new ListFilter(),
        stripe = new StripeClient(),
        applicant = new Applicant();

    lfilter.init();
    stripe.init();
    applicant.init();
});

function initMap() {
    let jmap = new JobMapSetup();
    jmap.init();

    window.jobMapHandle = jmap;
}

function updateMapMarker(event, anchor, id, isDisinterested) {
    if (event !== null) {
        event.preventDefault();
    }
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
