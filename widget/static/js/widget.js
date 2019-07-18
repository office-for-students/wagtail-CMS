var CONTENT = {
    'intro': {
        'en-GB': 'of students were satisfied with their course.',
        'cy-GB': ''
    },
    'ctaLead1': {
        'en-GB': 'For ',
        'cy-GB': ''
    },
    'ctaLead2': {
        'en-GB': 'more',
        'cy-GB': ''
    },
    'ctaLead3': {
        'en-GB': ' official course information visit.',
        'cy-GB': ''
    },
    'logo': {
        'en-GB': 'Discover Uni',
        'cy-GB': ''
    },
    'cta': {
        'en-GB': 'See course data',
        'cy-GB': ''
    },
    'noDataIntro': {
        'en-GB': 'To see official information about this course and others visit Discover Uni.',
        'cy-GB': ''
    },
    'noDataCtaLead1': {
        'en-GB': 'Make an ',
        'cy-GB': ''
    },
    'noDataCtaLead2': {
        'en-GB': 'informed',
        'cy-GB': ''
    },
    'noDataCtaLead3': {
        'en-GB': ' choice.',
        'cy-GB': ''
    },
    'noDataCta': {
        'en-GB': 'See Discover Uni',
        'cy-GB': ''
    }
}

var MODES = {
    'full-time': 1,
    'part-time': 2,
}

var LANGUAGE_KEYS = {
    'en-GB': 'english',
    'cy-GB': 'welsh'
}

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
        this.languageKey = LANGUAGE_KEYS[this.language];
        this.size = this.targetDiv.dataset.size;

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
            if (this.status === 200) {
                that.renderDataWidget(JSON.parse(this.response).course);
            } else {
                that.renderWidget();
            }
        });
        base_url = "{{api_domain}}/dataset/institutions/{{uni_id}}/courses/{{course_id}}/modes/{{mode}}";
        url = base_url.replace('{{uni_id}}', this.institution);
        url = url.replace('{{course_id}}', this.course);
        url = url.replace('{{mode}}', MODES[this.kismode.toLowerCase()]);

        xhttp.open("GET", url, true);
        xhttp.setRequestHeader('Ocp-Apim-Subscription-Key', '{{api_key}}');
        xhttp.send();
    },

    renderDataWidget: function(courseData) {
        this.renderDataLead(courseData);
        this.renderCTABlock(courseData);
    },

    renderDataLead: function(courseData) {
        var leadNode = document.createElement('div');
        leadNode.classList.add('widget-lead');
        var titleNode = document.createElement('h1');
        titleNode.classList.add('title');

        var percentage = courseData.statistics.nss[0].question_27.agree_or_strongly_agree + '%';
        var title = document.createTextNode(percentage);
        titleNode.appendChild(title);

        var introNode = document.createElement("p");
        introNode.classList.add('intro');
        var intro = document.createTextNode(CONTENT.intro[this.language]);
        introNode.appendChild(intro);

        var courseNode = document.createElement("p");
        courseNode.classList.add('course');
        var course = document.createTextNode(courseData.title[this.languageKey]);
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
        var lead1 = document.createTextNode(CONTENT.ctaLead1[this.language]);
        var leadNode2 = document.createElement("strong");
        leadNode2.classList.add('cta-lead');
        var lead2 = document.createTextNode(CONTENT.ctaLead2[this.language]);
        var leadNode3 = document.createElement("span");
        leadNode3.classList.add('cta-lead');
        var lead3 = document.createTextNode(CONTENT.ctaLead3[this.language]);
        leadNode1.appendChild(lead1);
        leadNode2.appendChild(lead2);
        leadNode3.appendChild(lead3);
        ctaBlockNode.appendChild(leadNode1);
        ctaBlockNode.appendChild(leadNode2);
        ctaBlockNode.appendChild(leadNode3);

        var logoNode = document.createElement('p');
        logoNode.classList.add('logo');
        var logo = document.createTextNode(CONTENT.logo[this.language]);
        logoNode.appendChild(logo);
        ctaBlockNode.appendChild(logoNode);

        var ctaWrapperNode = document.createElement('div');
        ctaWrapperNode.classList.add('cta');
        coursePageBase = '{{domain_name}}/course-details/{{uni_id}}/{{course_id}}/{{mode}}/';
        coursePage = coursePageBase.replace('{{domain_name}}', 'http://localhost:8000');
        coursePage = coursePage.replace('{{uni_id}}', this.institution);
        coursePage = coursePage.replace('{{course_id}}', this.course);
        coursePage = coursePage.replace('{{mode}}', this.kismode);

        var ctaNode = document.createElement('a');
        ctaNode.href = coursePage;
        var cta = document.createTextNode(CONTENT.cta[this.language]);

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
        var intro = document.createTextNode(CONTENT.noDataIntro[this.language]);
        introNode.appendChild(intro);
        leadNode.appendChild(introNode);
        this.targetDiv.appendChild(leadNode);
    },

    renderNoDataCTABlock: function() {
        var ctaBlockNode = document.createElement('div');
        ctaBlockNode.classList.add('widget-cta-block');

        var leadNode1 = document.createElement("span");
        leadNode1.classList.add('cta-lead');
        var lead1 = document.createTextNode(CONTENT.noDataCtaLead1[this.language]);
        var leadNode2 = document.createElement("strong");
        leadNode2.classList.add('cta-lead');
        var lead2 = document.createTextNode(CONTENT.noDataCtaLead2[this.language]);
        var leadNode3 = document.createElement("span");
        leadNode3.classList.add('cta-lead');
        var lead3 = document.createTextNode(CONTENT.noDataCtaLead3[this.language]);
        leadNode1.appendChild(lead1);
        leadNode2.appendChild(lead2);
        leadNode3.appendChild(lead3);
        ctaBlockNode.appendChild(leadNode1);
        ctaBlockNode.appendChild(leadNode2);
        ctaBlockNode.appendChild(leadNode3);

        var logoNode = document.createElement('p');
        logoNode.classList.add('logo');
        var logo = document.createTextNode(CONTENT.logo[this.language]);
        logoNode.appendChild(logo);
        ctaBlockNode.appendChild(logoNode);

        var ctaWrapperNode = document.createElement('div');
        ctaWrapperNode.classList.add('cta');
        var ctaNode = document.createElement('a');

        coursePageBase = '{{domain_name}}/course-details/{{uni_id}}/{{course_id}}/{{mode}}/';
        coursePage = coursePageBase.replace('{{domain_name}}', 'http://localhost:8000');
        coursePage = coursePage.replace('{{uni_id}}', this.institution);
        coursePage = coursePage.replace('{{course_id}}', this.course);
        coursePage = coursePage.replace('{{mode}}', this.kismode);
        ctaNode.href = coursePage;

        var cta = document.createTextNode(CONTENT.noDataCta[this.language]);
        ctaNode.appendChild(cta);
        ctaWrapperNode.appendChild(ctaNode);
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
