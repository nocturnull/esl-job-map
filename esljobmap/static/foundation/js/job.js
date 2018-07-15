
class JobToggle {
    constructor(pfields, ffields) {
        this.part_time = pfields;
        this.full_time = ffields;
    }

    update(isChecked) {
        if (isChecked) {
            this.part_time.hide();
            this.full_time.show('slow');
        } else {
            this.full_time.hide('');
            this.part_time.show('slow');
        }
    }
}

export default JobToggle;
