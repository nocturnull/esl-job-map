/**
 * Job Application Form
 */
class JobApplication {

    /**
     * Constructor.
     */
    constructor() {
        this.useExistingResume = $('#id_use_existing_resume');
        this.resumeFileUploadField = $('#resumeFileUploadField');
    }

    /**
     * Determine if we are on the right page.
     *
     * @returns {boolean}
     */
    isValid() {
        return this.useExistingResume.length > 0;
    }

    /**
     * Initialize
     */
    init() {
        if (this.isValid()) {
            this.useExistingResume.change(e => {
                this.resumeFileUploadField.toggleClass('invisible');
            });
        }
    }
}

export default JobApplication;
