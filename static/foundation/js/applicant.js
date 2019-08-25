/**
 * Application form helper
 */
export default class Applicant {

    /**
     * Constructor.
     */
    constructor() {
        this.form = document.getElementById('applicationForm');
        this.isProcessing = false;
    }

    /**
     * Determine if we can continue with initialization.
     *
     * @returns {boolean}
     */
    isValid() {
        return this.form != null;
    }

    init() {
        if (this.isValid()) {
            this.form.addEventListener('submit', (event) => this.handleSubmit(event));
        }
    }

    handleSubmit(event) {
        event.preventDefault();
        if (!this.isProcessing) {
            this.isProcessing = true;
            this.form.submit();
        }
    }
}
