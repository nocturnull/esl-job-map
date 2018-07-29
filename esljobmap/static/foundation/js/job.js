
class JobToggle {
    constructor() {
        this.partTime = $('#partTimeFields');
        this.fullTime = $('#fullTimeFields');
        this.fullTimeOption = $('input[type=radio][name=is_full_time]');
    }

    isValid() {
        return this.partTime.length > 0 && this.fullTime.length > 0 && this.fullTimeOption.length > 0
    }

    init() {
        if (this.isValid()) {
            this.fullTimeOption.change(e => {
                this.update(e.currentTarget.value);
            });
            this.update(this.fullTimeOption.val());
        }
    }

    update(val) {
        console.log(val);
        if (val === 'True') {
            this.partTime.hide();
            this.fullTime.show('slow');
            this.fullTimeOption.val([val]);
        } else if (val === 'False') {
            this.fullTime.hide();
            this.partTime.show('slow');
            this.fullTimeOption.val([val]);
        }
    }
}

export default JobToggle;
