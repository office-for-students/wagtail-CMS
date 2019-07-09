(function ($) {

    var  DiscoverUniWidget = function(targetDiv) {
        this.targetDiv = targetDiv;
        this.setup();
    }

    DiscoverUniWidget.prototype = {
        setup: function() {
            this.institution = this.targetDiv.dataset.datainstitution;
            this.course = this.targetDiv.dataset.datacourse;
            this.kismode = this.targetDiv.dataset.datakismode;
            this.orientation = this.targetDiv.dataset.dataorientation;
            this.language = this.targetDiv.dataset.datalanguage;

            this.renderWidget();
        },

        renderWidget: function() {
            var headingNode = document.createElement("H1");
            headingNode.classList.add('title');
            var heading = document.createTextNode('DiscoverUni');
            headingNode.appendChild(heading);
            this.targetDiv.appendChild(headingNode);
        }
    }

    function init() {
        var widgetTarget = $('.kis-widget');
        for (var i = 0; i < widgetTarget.length; i++) {
            new DiscoverUniWidget(widgetTarget[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
