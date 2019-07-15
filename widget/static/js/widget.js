var  DiscoverUniWidget = function(targetDiv) {
    this.targetDiv = targetDiv;
    this.setup();
}

DiscoverUniWidget.prototype = {
    setup: function() {
        this.institution = this.targetDiv.dataset.institution;
        this.course = this.targetDiv.dataset.course;
        this.kismode = this.targetDiv.dataset.kismode;
        this.orientation = this.targetDiv.dataset.orientation;
        this.language = this.targetDiv.dataset.language;

        this.targetDiv.classList.add(this.orientation);

        this.addCss();
        this.loadCourseData();
    },

    addCss: function() {
        var fontNode = document.createElement('link');
        fontNode.href = "http://fonts.googleapis.com/css?family=Montserrat";
        fontNode.rel = "stylesheet";
        fontNode.type = "text/css";
        styling = "{% styles %}";
        var stylingNode = document.createElement('style');
        var stylingTextNode = document.createTextNode(styling);
        stylingNode.appendChild(stylingTextNode);
        var widgetScript = document.getElementById('unistats-widget-script');
        widgetScript.parentNode.insertBefore(stylingNode, widgetScript);
        widgetScript.parentNode.insertBefore(fontNode, widgetScript);
    },

    loadCourseData: function() {
        var that = this;
        var xhttp = new XMLHttpRequest();
        xhttp.addEventListener("load", function() {
            console.log(this.status)
            if (this.status === 200) {
                that.renderDataWidget();
            } else {
                that.renderWidget();
            }
        });
        xhttp.open("GET", "/dummy-link", true);
        xhttp.send();
    },

    renderDataWidget: function() {
        this.renderDataLead();
        this.renderCTABlock();
    },

    renderDataLead: function() {
        var leadNode = document.createElement('div');
        leadNode.classList.add('widget-lead');
        var titleNode = document.createElement('h1');
        titleNode.classList.add('title');
        // TODO replace with actual data from the api
        var title = document.createTextNode('XX%');
        titleNode.appendChild(title);

        var introNode = document.createElement("p");
        introNode.classList.add('intro');
        var intro = document.createTextNode('of students were satisfied with their course.');
        introNode.appendChild(intro);

        var courseNode = document.createElement("p");
        courseNode.classList.add('course');
        var course = document.createTextNode('BA (Hons) History, 3-year course, Full time, optional foundation year.');
        courseNode.appendChild(course);

        leadNode.appendChild(titleNode);
        leadNode.appendChild(introNode);
        leadNode.appendChild(courseNode);

        this.targetDiv.appendChild(leadNode);
    },

    renderCTABlock: function() {
        var ctaBlockNode = document.createElement('div');
        ctaBlockNode.classList.add('widget-cta-block');

        var leadNode1 = document.createElement("span");
        leadNode1.classList.add('cta-lead');
        var lead1 = document.createTextNode('For ');
        var leadNode2 = document.createElement("strong");
        leadNode2.classList.add('cta-lead');
        var lead2 = document.createTextNode('more');
        var leadNode3 = document.createElement("span");
        leadNode3.classList.add('cta-lead');
        var lead3 = document.createTextNode(' official course information visit.');
        leadNode1.appendChild(lead1);
        leadNode2.appendChild(lead2);
        leadNode3.appendChild(lead3);
        ctaBlockNode.appendChild(leadNode1);
        ctaBlockNode.appendChild(leadNode2);
        ctaBlockNode.appendChild(leadNode3);

        var logoNode = document.createElement('p');
        logoNode.classList.add('logo');
        var logo = document.createTextNode('Discover Uni');
        logoNode.appendChild(logo);
        ctaBlockNode.appendChild(logoNode);

        var ctaWrapperNode = document.createElement('div');
        ctaWrapperNode.classList.add('cta');
        var ctaNode = document.createElement('a');
        var cta = document.createTextNode('See course data');
        ctaWrapperNode.appendChild(ctaNode);
        ctaNode.appendChild(cta);
        ctaBlockNode.appendChild(ctaWrapperNode);

        this.targetDiv.appendChild(ctaBlockNode);
    },

    renderWidget: function() {
        this.renderNoDataLead();
        this.renderNoDataCTABlock();
    },

    renderNoDataLead: function() {
        this.targetDiv.classList.add('no-data');
        var leadNode = document.createElement('div');
        leadNode.classList.add('widget-lead');
        var introNode = document.createElement("p");
        introNode.classList.add('intro');
        var intro = document.createTextNode('To see official information about this course and others visit Discover Uni.');
        introNode.appendChild(intro);
        leadNode.appendChild(introNode);
        this.targetDiv.appendChild(leadNode);
    },

    renderNoDataCTABlock: function() {
        var ctaBlockNode = document.createElement('div');
        ctaBlockNode.classList.add('widget-cta-block');

        var leadNode1 = document.createElement("span");
        leadNode1.classList.add('cta-lead');
        var lead1 = document.createTextNode('Make an ');
        var leadNode2 = document.createElement("strong");
        leadNode2.classList.add('cta-lead');
        var lead2 = document.createTextNode('informed');
        var leadNode3 = document.createElement("span");
        leadNode3.classList.add('cta-lead');
        var lead3 = document.createTextNode(' choice.');
        leadNode1.appendChild(lead1);
        leadNode2.appendChild(lead2);
        leadNode3.appendChild(lead3);
        ctaBlockNode.appendChild(leadNode1);
        ctaBlockNode.appendChild(leadNode2);
        ctaBlockNode.appendChild(leadNode3);

        var logoNode = document.createElement('p');
        logoNode.classList.add('logo');
        var logo = document.createTextNode('Discover Uni');
        logoNode.appendChild(logo);
        ctaBlockNode.appendChild(logoNode);

        var ctaWrapperNode = document.createElement('div');
        ctaWrapperNode.classList.add('cta');
        var ctaNode = document.createElement('a');
        var cta = document.createTextNode('See Discover Uni');
        ctaWrapperNode.appendChild(ctaNode);
        ctaNode.appendChild(cta);
        ctaBlockNode.appendChild(ctaWrapperNode);

        this.targetDiv.appendChild(ctaBlockNode);
    }
}

function init() {
    var widgetTarget = document.getElementsByClassName('kis-widget');
    for (var i = 0; i < widgetTarget.length; i++) {
        new DiscoverUniWidget(widgetTarget[i]);
    }
}

init();
