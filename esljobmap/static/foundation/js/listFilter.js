/**
 * Flow Card Wrapper.
 */
class FlowCard {

    /**
     * Constructor.
     *
     * @param tags
     * @param dom
     * @param parent
     */
    constructor(tags, dom, parent) {
        this.tagList = tags.split(',');
        this.$dom = $(dom);
        this.$parent = parent;
        this.isDetached = false;
        this.detachedCase = null;
    }

    /**
     * Determine if we have a specific tag.
     *
     * @param tag
     * @returns {boolean}
     */
    hasTag(tag) {
        for (let i = 0; i < this.tagList.length; i++) {
            if (this.tagList[i].trim() === tag.trim()) {
                return true;
            }
        }

        return false;
    }

    /**
     * Determine if the current card possesses a tag that is active.
     *
     * @param tagList
     * @returns {boolean}
     */
    hasAnActiveTag(tagList) {
        for (let tag in tagList) {
            if (tagList.hasOwnProperty(tag)) {
                // Check the active tags only.
                if (tagList[tag]) {
                    if (this.hasTag(tag)) {
                        return true;
                    }
                }
            }
        }

        return false;
    }

    /**
     * Hide the underlying DOM.
     */
    detach() {
        this.detachedCase = this.$dom.parent().detach();
        this.isDetached = true;
    }

    /**
     * Show the underlying DOM.
     */
    attach() {
        this.$parent.append(this.detachedCase);
        this.isDetached = false;
    }
}

/**
 * Dynamic filterer for job posts and applications.
 */
class ListFiler {

    /**
     * Constructor.
     */
    constructor() {
        this.$searchFilters = $('#searchFilters');
        this.$cards = $('.flow-card');
        this.$filterCardsParent = $('#filterCardsParent');
        this.flowCardList = [];
        this.listFilterResults = null;
        this.buttonList = [];
        this.buttonStateMap = {};
    }

    /**
     * Determine if it's neceassry to manipulate any data.
     *
     * @returns {boolean}
     */
    isValid() {
        return this.$searchFilters.length > 0;
    }

    /**
     * Fire up.
     */
    init() {
        if (this.isValid()) {
            this.listFilterResults = $('#listFilterResults');
            this.buttonList = this.$searchFilters.find('button');
            this.attachFilterListeners();
            this.organizeData();
        }
    }

    /**
     * Attach button listeners to apply filters.
     */
    attachFilterListeners() {
        for (let i = 0; i < this.buttonList.length; i++) {
            let $button = $(this.buttonList[i]),
                tag = $button.data('filtertag');

            // Track states and set default values.
            this.buttonStateMap[tag] = true;

            // Attach listener
            $button.on('click', () => {
                let ctag = $button.data('filtertag');

                // Update active state and button styling.
                if (this.buttonStateMap[ctag]) {
                    $button.attr('class', 'primary-button-1');
                    this.buttonStateMap[ctag] = false;
                    this.removeFilter(ctag);
                } else {
                    $button.attr('class', 'accent-selected-button-1');
                    this.buttonStateMap[ctag] = true;
                    this.applyFilter(ctag);
                }
            });
        }
    }

    /**
     * Applies the filter and shows the relevant items.
     */
    applyFilter(tag) {
        // Go through each flow card and check the filter.
        for (let k = 0; k < this.flowCardList.length; k++) {
            let fc = this.flowCardList[k];

            if (fc.hasTag(tag)) {
                // Attach if we have the tag and is currently hidden.
                if (fc.isDetached) {
                    fc.attach();
                }
            } else if (!fc.hasTag(tag) && !fc.hasAnActiveTag(this.buttonStateMap)) {
                console.log(this.buttonStateMap);
                // Detach if we dont have the tag, is currently showing, and the card has no active filter.
                if (!fc.isDetached) {
                    fc.detach();
                }
            }
        }

        // Inform the user how many items are showing.
        this.updateDisplayCount();
    }

    /**
     * Removes the filter and hides the relevant items.
     */
    removeFilter(tag) {
        // Go through each flow card and check the filter.
        for (let k = 0; k < this.flowCardList.length; k++) {
            let fc = this.flowCardList[k];

            // Attach if we have the tag and is currently hidden.
            if (!fc.hasTag(tag) && fc.isDetached) {
                fc.attach();
            } else if (fc.hasTag(tag)) {
                if (!fc.isDetached && !fc.hasAnActiveTag(this.buttonStateMap)) {
                    fc.detach();
                }
            }
        }

        // Inform the user how many items are showing.
        this.updateDisplayCount();
    }

    /**
     * Prepare items to make filtering easier.
     */
    organizeData() {
        for (let j = 0; j < this.$cards.length; j++) {
            let d = this.$cards[j];
            this.flowCardList.push(new FlowCard($(d).data('filtertaglist'), d, this.$filterCardsParent));
        }
    }

    /**
     * Each time a filter is added a removed we need to show the new shown amount.
     */
    updateDisplayCount() {
        let totalCount = this.flowCardList.length;

        if (this.$filterCardsParent.children().length === this.flowCardList.length) {
            this.listFilterResults.html(`Currently displaying ${totalCount}/${totalCount}`);
        } else {
            let filterCount = this.$filterCardsParent.children().length;

            this.listFilterResults.html(`Currently displaying ${filterCount}/${totalCount}`);
        }
    }
}

export default ListFiler;
