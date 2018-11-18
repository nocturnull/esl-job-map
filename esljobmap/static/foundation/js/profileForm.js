/**
 * Profile Form
 */
class ProfileForm {

    /**
     * Constructor.
     */
    constructor() {
        this.visaType = $('#id_visa_type');
        this.visaConditions = $('#visaConditions');
    }

    /**
     * Determine if we are on the right page.
     *
     * @returns {boolean}
     */
    isValid() {
        return this.visaType.length > 0;
    }

    /**
     * Initialize
     */
    init() {
        if (this.isValid()) {
            this.visaType.change(e => {
                if (this.visaType.val() === 2 || this.visaType.val() === '2') {
                    this.visaConditions.removeClass('invisible');
                } else {
                    this.visaConditions.addClass('invisible');
                }
            });
        }
    }
}

export default ProfileForm;
