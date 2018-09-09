
class JobApplication {
    constructor() {
        this.useExistingResume = $('#id_use_existing_resume');
        this.resumeFileUploadField = $('#resumeFileUploadField');
    }

    isValid() {
        return this.useExistingResume.length > 0;
    }

    init() {
        if (this.isValid()) {
            this.useExistingResume.change(e => {
                this.resumeFileUploadField.toggleClass('invisible');
            });
        }
    }
}

export default JobApplication;
