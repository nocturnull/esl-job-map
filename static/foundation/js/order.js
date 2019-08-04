/**
 * Job credit order helper.
 */
export default class Order {

    /**
     * Constructor
     */
    constructor() {
        this.orderCodeInput = document.getElementById('id_order_code');
        this.displayInfo = document.getElementById('orderDisplayInfo');
        this.finalPriceDisplay = document.getElementById('finalPriceDisplay');
        if (this.displayInfo !== null) {
            this.lookupUrl = this.displayInfo.dataset.lookupUrl;
        } else {
            this.lookupUrl = '/';
        }
    }

    /**
     * Determine if the state is valid.
     *
     * @returns {boolean}
     */
    isValid() {
        return this.orderCodeInput !== null;
    }

    /**
     * Initialize.
     */
    init() {
        if (this.isValid()) {
            $(this.orderCodeInput).blur(() => this.submitLookup());
        }
    }

    /**
     * Perform network request.
     */
    submitLookup() {
        let orderCode = this.orderCodeInput.value;
        if (orderCode.length > 0) {
            $.ajax({
                type: 'GET',
                url: this.lookupUrl + orderCode
            }).done((response) => {
                $(this.displayInfo).html(response);
                this.finalPriceDisplay.textContent = 'Purchase ' + response + '?'
            });
        }
    }
}
