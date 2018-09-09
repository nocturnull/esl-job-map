$(document).foundation();

import JobToggle from './job.js'
import JobApplication from './apply.js';

$(document).ready(function() {
    let jtoggle = new JobToggle(),
        japply = new JobApplication();

    jtoggle.init();
    japply.init();
});
