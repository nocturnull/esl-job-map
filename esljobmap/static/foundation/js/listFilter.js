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
        this.bindRepostHoverEvent();
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

    bindRepostHoverEvent() {
        let takenDown = this.$dom.find('.taken-down');
        if (takenDown.length > 0) {
            takenDown.on('mouseover', () => {
                takenDown.html('Repost');
            })
            takenDown.on('mouseleave', () => {
                takenDown.html('Taken down');
            })
        }
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
        this.$secondarySearchFilters = $('#secondarySearchFilters');
        this.$resetFiltersButton = $('#resetFiltersButton');
        this.$cards = $('.flow-card');
        this.$filterCardsParent = $('#filterCardsParent');
        this.flowCardList = [];
        this.listFilterResults = null;
        this.buttonList = [];
        this.secondaryButtonList = [];
        this.buttonStateMap = {};
        this.secondaryButtonStateMap = {};
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
            // Update results tracker.
            this.listFilterResults = $('#listFilterResults');

            // Track filter buttons.
            this.buttonList = this.$searchFilters.find('button');

            // Track secondary filter options if they exist.
            if (this.$secondarySearchFilters.length > 0) {
                this.secondaryButtonList = this.$secondarySearchFilters.find('button');
            }

            // Attach listeners to filter buttons.
            this.attachPrimaryFilterListeners();
            this.attachSecondaryFilterListeners();

            // Organize to be filtered items.
            this.prepareFlowCards();

            // Reset all filters button.
            this.$resetFiltersButton.on('click', () => {
                this.resetAllFilters();
            });
        }
    }

    /**
     * Go through the primary filters and attach their action callbacks.
     */
    attachPrimaryFilterListeners() {
        this.attachFilterListeners(this.buttonList, this.buttonStateMap);
    }

    /**
     * Go through the secondary filters and attach their action callbacks.
     */
    attachSecondaryFilterListeners() {
        if (this.secondaryButtonList.length > 0) {
            this.attachFilterListeners(this.secondaryButtonList, this.secondaryButtonStateMap);
        }
    }

    /**
     * Attach button listeners to apply filters.
     *
     * @param filterButtonList
     * @param filterStateMap
     */
    attachFilterListeners(filterButtonList, filterStateMap) {
        for (let i = 0; i < filterButtonList.length; i++) {
            let $button = $(filterButtonList[i]),
                tag = $button.data('filtertag');

            // Track states and set default values.
            filterStateMap[tag] = true;

            // Attach listener
            $button.on('click', () => {
                let ctag = $button.data('filtertag');

                // Update active state and button styling.
                if (filterStateMap[ctag]) {
                    $button.attr('class', 'disabled-button');
                    filterStateMap[ctag] = false;
                    this.removeFilter(ctag, filterStateMap);
                } else {
                    $button.attr('class', 'secondary-selected-button-1');
                    filterStateMap[ctag] = true;
                    this.applyFilter(ctag, filterStateMap);
                }
            });
        }
    }

    /**
     * Applies the filter and shows the relevant items.
     *
     * @param tag
     * @param filterStateMap
     */
    applyFilter(tag, filterStateMap) {
        // Go through each flow card and check the filter.
        for (let k = 0; k < this.flowCardList.length; k++) {
            let fc = this.flowCardList[k];

            // Attach if we have the tag, is currently hidden, and is not being filtered across all filter sets.
            if (fc.hasTag(tag) && !this.isCardFilteredOut(fc)) {
                if (fc.isDetached) {
                    fc.attach();
                }
            } else if (!fc.hasTag(tag) && !fc.hasAnActiveTag(filterStateMap)) {
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
     *
     * @param tag
     * @param filterStateMap
     */
    removeFilter(tag, filterStateMap) {
        // Go through each flow card and check the filter.
        for (let k = 0; k < this.flowCardList.length; k++) {
            let fc = this.flowCardList[k];

            // Attach if we have the tag, is currently hidden, and has an active filter.
            if (!fc.hasTag(tag) && fc.isDetached && fc.hasAnActiveTag(filterStateMap)) {
                fc.attach();
            } else if (fc.hasTag(tag)) {
                if (!fc.isDetached && !fc.hasAnActiveTag(filterStateMap)) {
                    fc.detach();
                }
            }
        }

        // Inform the user how many items are showing.
        this.updateDisplayCount();
    }

    /**
     * Check all the filter maps to see if the supplied flow card is being filtered out.
     *
     * @param flowCard
     * @returns {boolean}
     */
    isCardFilteredOut(flowCard) {
        if (this.secondaryButtonStateMap.length > 0) {
            return !flowCard.hasAnActiveTag(this.buttonStateMap) &&
                !flowCard.hasAnActiveTag(this.secondaryButtonStateMap);
        }

        return !flowCard.hasAnActiveTag(this.buttonStateMap);
    }

    /**
     * Adjust all buttons and cards to default values.
     */
    resetAllFilters() {
        // Reset primary filters.
        this.resetFilters(this.buttonList, this.buttonStateMap);

        // Reset secondary filters if need be.
        this.resetFilters(this.secondaryButtonList, this.secondaryButtonStateMap);

        // Reset cards.
        for (let k = 0; k < this.flowCardList.length; k++) {
            let fc = this.flowCardList[k];
            if (fc.isDetached) {
                fc.attach();
            }
        }

        this.updateDisplayCount();
    }

    /**
     * Reset filters from the supplied list of buttons.
     *
     * @param filterButtonList
     * @param filterStateMap
     */
    resetFilters(filterButtonList, filterStateMap) {
        if (filterButtonList.length > 0) {
            for (let i = 0; i < filterButtonList.length; i++) {
                let $button = $(filterButtonList[i]),
                    tag = $button.data('filtertag');

                filterStateMap[tag] = true;
                $button.attr('class', 'secondary-selected-button-1');
            }
        }
    }

    /**
     * Prepare flow card items to make filtering easier.
     */
    prepareFlowCards() {
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
