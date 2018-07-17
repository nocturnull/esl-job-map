
class JobToggle {
    constructor() {
        this.partTime = $('#partTimeFields');
        this.fullTime = $('#fullTimeFields');
        this.fullTimeCheckbox = $('#id_is_full_time');
    }

    isValid() {
        return this.partTime.length > 0 && this.fullTime.length > 0 && this.fullTimeCheckbox.length > 0
    }

    init() {
        this.fullTimeCheckbox.change(e => {
            this.update(e.currentTarget.checked);
        });
        if (this.fullTimeCheckbox[0].checked) {
            this.update(true);
        }
    }

    update(isChecked) {
        if (isChecked) {
            this.partTime.hide();
            this.fullTime.show('slow');
        } else {
            this.fullTime.hide();
            this.partTime.show('slow');
        }
    }
}

export default JobToggle;
