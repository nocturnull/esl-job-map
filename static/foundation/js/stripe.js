/**
 * Stripe.js API wrapper
 *
 * Relevant documentation
 * @link https://stripe.com/docs/stripe-js
 */
class StripeClient {

    /**
     * Constructor.
     */
    constructor() {
        this.cardElementId = '#card-element';
        this.displayError = document.getElementById('card-errors');
        this.form = document.getElementById('payment-form');
        this.singleCredit = document.getElementById('id_single_credit');
        this.tenCredits = document.getElementById('id_ten_credits');
        this.oneHundredCredits = document.getElementById('id_one_hundred_credits');
        this.priceDisplay = document.getElementById('priceDisplay');
        this.finalPriceDisplay = document.getElementById('finalPriceDisplay');
        this.confirmPurchaseButton = document.getElementById('confirmPurchaseButton');
        this.$purchaseConfirmModal = $('#purchaseConfirmModal');
        this.stripeToken = null;
        this.singleCreditPrice = 20;
        this.tenCreditsPrice = 160;
        this.oneHundredCreditsPrice = 1200;
    }

    /**
     * Determine if it's necessary to manipulate any data.
     *
     * @returns {boolean}
     */
    isValid() {
        return this.form.length > 0;
    }

    /**
     * Initialize the API.
     */
    init() {
        if (this.isValid()) {
            this.stripe = Stripe(window.stripePublishableKey);
            this.elements = this.stripe.elements();
            this.card = this.elements.create('card', {style: StripeClient.getCardStyles()});
            this.card.mount(this.cardElementId);
            // Payment info events.
            this.card.addEventListener('change', (event) => this.handleError(event));
            this.form.addEventListener('submit', (event) => this.handleSubmit(event));
            // Pricing events.
            this.singleCredit.addEventListener('change', () => this.handleQuantityChange());
            this.tenCredits.addEventListener('change', () => this.handleQuantityChange());
            this.oneHundredCredits.addEventListener('change', () => this.handleQuantityChange());
            // Update display on page load.
            this.handleQuantityChange();
            // Confirm events.
            this.confirmPurchaseButton.addEventListener('click', () => this.stripeTokenHandler());
        }
    }

    /**
     * Handle real-time validation errors from the card Element.
     *
     * @param event
     */
    handleError(event) {
        if (event.error) {
            this.displayError.textContent = event.error.message;
        } else {
            this.displayError.textContent = '';
        }
    }

    /**
     * Handle form submission.
     *
     * @param event
     */
    handleSubmit(event) {
        event.preventDefault();

        this.stripe.createToken(this.card).then((result) => {
            if (result.error) {
                // Inform the user if there was an error.
                this.displayError.textContent = result.error.message;
            } else {
                this.stripeToken = result.token;
                this.showConfirmationPopup();
            }
          });
    }

    /**
     * Update price display as the user toggles the quantities.
     */
    handleQuantityChange() {
        let singleCredits = parseInt(this.singleCredit.value),
            tenCredits = parseInt(this.tenCredits.value),
            oneHundrenCredits = parseInt(this.oneHundredCredits.value);
        if (Number.isNaN(singleCredits)) {
            singleCredits = 0;
        }
        if (Number.isNaN(tenCredits)) {
            tenCredits = 0;
        }
        if (Number.isNaN(oneHundrenCredits)) {
            oneHundrenCredits = 0;
        }

        let totalCredits = singleCredits + 10 * tenCredits + 100 * oneHundrenCredits;
        let totalPrice = singleCredits * this.singleCreditPrice +
            tenCredits * this.tenCreditsPrice +
            oneHundrenCredits * this.oneHundredCreditsPrice;

        let priceText = totalCredits + ' credits for $' + totalPrice;
        this.priceDisplay.textContent = priceText;
        this.finalPriceDisplay.textContent = 'Purchase ' + priceText + '?'
    }

    /**
     * Show the final price in a modal.
     */
    showConfirmationPopup() {
        this.$purchaseConfirmModal.foundation('open');
    }

    /**
     * Submit the form with the token ID.
     */
    stripeTokenHandler() {
        // Insert the token ID into the form so it gets submitted to the server
        let hiddenInput = document.createElement('input');
        hiddenInput.setAttribute('type', 'hidden');
        hiddenInput.setAttribute('name', 'stripeToken');
        hiddenInput.setAttribute('value', this.stripeToken.id);
        this.form.appendChild(hiddenInput);

        // Submit the form
        this.form.submit();
    }

    /**
     * Custom styling of stripe card element.
     *
     * @returns {{invalid: {color: string, iconColor: string}, base: {fontFamily: string, color: string, "::placeholder": {color: string}, fontSize: string, fontSmoothing: string}}}
     */
    static getCardStyles() {
        return {
            base: {
                color: '#32325d',
                fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                fontSmoothing: 'antialiased',
                fontSize: '16px',
                '::placeholder': {
                    color: '#aab7c4'
                }
            },
            invalid: {
                color: '#fa755a',
                iconColor: '#fa755a'
            }
        };
    }
}

export default StripeClient;
