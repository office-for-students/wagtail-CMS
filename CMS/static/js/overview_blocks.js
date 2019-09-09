(function ($) {

    var OverViewGroup = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    OverViewGroup.prototype = {
        setup: function() {
            this.blocks = this.wrapper.find('.overview-block');

            this.setView();
        },

        setView: function()  {
            totalHeight = this.getMaxHeight();
            padding = this.getPadding();
            height = totalHeight - (padding * 2);
            for (var i = 0; i < this.blocks.length; i++) {
                this.blocks.css('height', height);
            }
        },

        getMaxHeight: function() {
            maxHeight = 0;
            for (var i = 0; i < this.blocks.length; i++) {
                if (this.blocks[i].clientHeight > maxHeight) {
                    maxHeight = this.blocks[i].clientHeight;
                }
            }
            return maxHeight
        },

        getPadding: function() {
            return this.blocks.css('padding-top').slice(0,-2);
        }
    }

    function init() {
        var overviewGroups = $('.overview-group');
        for (var i = 0; i < overviewGroups.length; i++) {
            new OverViewGroup(overviewGroups[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
