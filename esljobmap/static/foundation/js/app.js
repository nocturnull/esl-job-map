$(document).foundation();

import JobToggle from './job.js'


$(document).ready(function() {
    let jtoggle = new JobToggle($('#partTimeFields'), $('#fullTimeFields'));

    $('#id_is_full_time').change(function() {
        jtoggle.update(this.checked);
    });
});
