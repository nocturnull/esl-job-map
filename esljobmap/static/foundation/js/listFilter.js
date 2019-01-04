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
        this.detachedCase = null;
        this.tooltips = [];
        this.bindRepostHoverEvent();
        this.bindTooltipHideEvents();
        this.isShowing = false;
    }

    /**
     * Determine if we have all tags in the specified list.
     *
     * @param tagList
     * @returns {boolean}
     */
    hasTags(tagList) {
        let containsAll = true;

        for (let i = 0; i < tagList.length; i++) {
            let tag = tagList[i].trim(),
                contains = false;

            for (let j = 0; j < this.tagList.length; j++) {
                if (this.tagList[j].trim() === tag) {
                    contains = true;
                }
            }

            if (!contains) {
                containsAll = false;
                break;
            }
        }

        return containsAll;
    }

    /**
     * Hide the underlying DOM.
     */
    detach() {
        this.detachedCase = this.$dom.parent().detach();
    }

    /**
     * Show the underlying DOM.
     */
    attach() {
        this.$parent.append(this.detachedCase);
    }

    /**
     * Switch between hover events for reposting and taking down.
     */
    bindRepostHoverEvent() {
        let takenDown = this.$dom.find('.taken-down');
        if (takenDown.length > 0) {
            takenDown.on('mouseover', () => {
                takenDown.html('Repost');
            });
            takenDown.on('mouseleave', () => {
                takenDown.html('Taken down');
            });
        }
    }

    bindTooltipHideEvents() {
        this.tooltips = $('.flowcard-tooltip');
        window.tooltipIsOpen = false;

        if (this.tooltips.length > 0) {
            // Hide all tooltips on click when needed.
            $('body').click(() => {
                if (window.tooltipIsOpen) {
                    window.tooltipIsOpen = false;
                    for (let i = 0; i  < this.tooltips.length; i++) {
                        let tip = this.tooltips[i];
                        $(tip).foundation('hide');
                    }
                }
            });

            // Track when the tooltips open.
            for (let i = 0; i  < this.tooltips.length; i++) {
                let tip = this.tooltips[i];
                $(tip).on('show.zf.tooltip', function() {
                    setTimeout(() => {
                        window.tooltipIsOpen = true;
                    }, 1000)
                });
            }
        }
    }
}

/**
 * Dynamic filterer for job posts and applications.
 */
class ListFilter {

    /**
     * Constructor.
     */
    constructor() {
        this.$filter1 = $('input[name="job-filter-1"]');
        this.$filter2 = $('input[name="job-filter-2"]');
        this.$cards = $('.flow-card');
        this.$filterCardsParent = $('#filterCardsParent');
        this.flowCardList = [];
        this.activeFilters = [];
        this.listFilterResults = null;
    }

    /**
     * Determine if it's necessary to manipulate any data.
     *
     * @returns {boolean}
     */
    isValid() {
        return this.$cards.length > 0;
    }

    /**
     * Fire up.
     */
    init() {
        if (this.isValid()) {
            // Update results tracker.
            this.listFilterResults = $('#listFilterResults');

            // Attach listeners to filter buttons.
            this.setActiveFilters();
            this.attachPrimaryFilterListener();
            this.attachSecondaryFilterListener();

            // Organize to be filtered items.
            this.prepareFlowCards();
        }
    }

    /**
     * Get the active filters on page load.
     */
    setActiveFilters() {
        let mainFilter = $('input[name="job-filter-1"]:checked').val();

        if (this.$filter2.length > 0) {
            this.activeFilters = [mainFilter, $('input[name="job-filter-2"]:checked').val()];
        } else {
            this.activeFilters = [mainFilter];
        }
    }

    /**
     * Attach primary filter listener.
     */
    attachPrimaryFilterListener() {
        this.$filter1.click((e) => {
            let targetFilter = $(e.currentTarget).val();

            // Update active filter list.
            if (this.$filter2.length > 0) {
                this.activeFilters = [targetFilter, $('input[name="job-filter-2"]:checked').val()];
            } else {
                this.activeFilters = [targetFilter];
            }

            // Apply filters.
            this.applyFilter();
        });
    }

    /**
     * Attach secondary filter listener if needed.
     */
    attachSecondaryFilterListener() {
        if (this.$filter2.length > 0) {
            this.$filter2.click((e) => {
                let targetFilter = $(e.currentTarget).val();

                // Update active filter list.
                this.activeFilters = [targetFilter, $('input[name="job-filter-1"]:checked').val()];

                // Apply filters.
                this.applyFilter();
            });
        }
    }

    /**
     * Applies the filter and shows the relevant items.
     */
    applyFilter() {
        // Go through each flow card and check to see if it has all active filters.
        for (let k = 0; k < this.flowCardList.length; k++) {
            let fc = this.flowCardList[k];

            // Attach if match filters.
            if (fc.hasTags(this.activeFilters)) {
                fc.attach();
            // Otherwise we detach it.
            } else {
                fc.detach();
            }
        }

        // Inform the user how many items are showing.
        this.updateDisplayCount();
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

export default ListFilter;
