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
            this.attachFilterListeners();
            this.organizeData();
        }
    }

    /**
     * Attach button listeners to apply filters.
     */
    attachFilterListeners() {
        let buttonList = this.$searchFilters.find('button');

        for (let i = 0; i < buttonList.length; i++) {
            let $cur = $(buttonList[i]);

            $cur.on('click', () => {
                let tag = $cur.data('filtertag');

                if ($cur.data('isactive') === 0) {
                    this.applyFilter(tag);
                    $cur.data('isactive', 1)
                        .attr('class', 'disabled-button');
                } else {
                    this.removeFilter(tag);
                    $cur.data('isactive', 0)
                        .attr('class', 'secondary-button');
                }
            })
        }
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
     * Applies the filter and hides the relevant items.
     *
     * @param tag
     */
    applyFilter(tag) {
        for (let k = 0; k < this.flowCardList.length; k++) {
            let fc = this.flowCardList[k];

            if (!fc.hasTag(tag)) {
                if (!fc.isDetached) {
                    fc.detach();
                }
            }
        }

        // Inform the user how many items are showing.
        this.updateDisplayCount();
    }

    /**
     * Removes a filter and shows previously hidden items.
     *
     * @param tag
     */
    removeFilter(tag) {
        for (let k = 0; k < this.flowCardList.length; k++) {
            let fc = this.flowCardList[k];

            if (!fc.hasTag(tag) && fc.isDetached) {
                fc.attach();
            }
        }

        // Inform the user how many items are showing.
        this.updateDisplayCount();
    }

    /**
     * Each time a filter is added a removed we need to show the new shown amount.
     */
    updateDisplayCount() {
        if (this.$filterCardsParent.children().length === this.flowCardList.length) {
            this.listFilterResults.html('');
        } else {
            let filterCount = this.$filterCardsParent.children().length,
            totalCount = this.flowCardList.length;

            this.listFilterResults.html(`Currently displaying ${filterCount}/${totalCount}`);
        }
    }
}

export default ListFiler;
