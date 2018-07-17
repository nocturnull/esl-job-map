$(document).foundation();

import JobToggle from './job.js'

$(document).ready(function() {
    let jtoggle = new JobToggle();
    if (jtoggle.isValid()) {
        jtoggle.init();
    }
});
