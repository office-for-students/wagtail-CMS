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

        this.addCss();
        this.renderWidget();
    },

    addCss: function() {
        styling = ".kis-widget {background-color: black;padding: 10px;} .kis-widget .title {color: white;}";
        var stylingNode = document.createElement('style');
        var stylingTextNode = document.createTextNode(styling);
        stylingNode.appendChild(stylingTextNode);
        var widgetScript = document.getElementById('unistats-widget-script');
        widgetScript.parentNode.insertBefore(stylingNode, widgetScript);
    },

    renderWidget: function() {
        var headingNode = document.createElement("h1");
        headingNode.classList.add('title');
        var heading = document.createTextNode('DiscoverUni');
        headingNode.appendChild(heading);
        this.targetDiv.appendChild(headingNode);
    }
}

function init() {
    var widgetTarget = document.getElementsByClassName('kis-widget');
    for (var i = 0; i < widgetTarget.length; i++) {
        new DiscoverUniWidget(widgetTarget[i]);
    }
}

init();
