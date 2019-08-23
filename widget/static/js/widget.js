var CONTENT = {
    'satisfactionIntro': {
        'en-GB': 'of students were satisfied overall with their course.',
        'cy-GB': ''
    },
    'explanationIntro': {
        'en-GB': 'of students agreed staff were good at explaining things.',
        'cy-GB': ''
    },
    'workIntro': {
        'en-GB': 'in work or doing further study six months after finishing.',
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
        'en-GB': 'See course info',
        'cy-GB': ''
    },
    'placement': {
        'en-GB': 'Placement year',
        'cy-GB': ''
    },
    'placementOptional': {
        'en-GB': 'Placement year optional',
        'cy-GB': ''
    },
    'foundation': {
        'en-GB': 'Foundation year',
        'cy-GB': ''
    },
    'foundationOptional': {
        'en-GB': 'Foundation year optional',
        'cy-GB': ''
    },
    'abroad': {
        'en-GB': 'Year abroad',
        'cy-GB': ''
    },
    'placementOptional': {
        'en-GB': 'Year abroad optional',
        'cy-GB': ''
    },
    'dataFor': {
        'en-GB': 'Data for: ',
        'cy-GB': ''
    },
    'dataForAggregated': {
        'en-GB': 'Data for courses in ',
        'cy-GB': ''
    },
    'at': {
        'en-GB': ' at ',
        'cy-GB': ''
    }
}

var MODES = {
    'fulltime': 1,
    'parttime': 2,
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
        fontNode.href = "https://fonts.googleapis.com/css?family=Montserrat:regular,bold&display=swap";
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
            that.renderWidget(this.status, this.response);
        });
        base_url = "{{api_domain}}/institutions/{{uni_id}}/courses/{{course_id}}/modes/{{mode}}";
        url = base_url.replace('{{uni_id}}', this.institution);
        url = url.replace('{{course_id}}', this.course);
        url = url.replace('{{mode}}', MODES[this.kismode.toLowerCase()]);

        xhttp.open("GET", url, true);
        xhttp.setRequestHeader('Ocp-Apim-Subscription-Key', '{{api_key}}');
        xhttp.send();
    },


    renderWidget: function(status, response) {
        if (status === 200) {
            var courseData = JSON.parse(response).course;

            if (this.hasRequiredStats(courseData) && !this.isMultiSubject(courseData)) {
                new DataWidget(this.targetDiv, courseData, this.language, this.languageKey, this.kismode,
                                this.generateLink.bind(this));
            } else {
                new NoDataWidget(this.targetDiv, this.language, this.languageKey, this.kismode,
                                    this.generateLink.bind(this));
            }
        } else {
            new NoDataWidget(this.targetDiv, this.language, this.languageKey, this.kismode,
                                this.generateLink.bind(this));
        }
    },

    isMultiSubject: function(courseData) {
        return Boolean(courseData.statistics.nss.length > 1 || courseData.statistics.employment.length > 1);
    },

    hasNSSStats: function(nssStats) {
        return Boolean(nssStats && nssStats[0] && nssStats[0].question_1 && nssStats[0].question_27);
    },

    hasWorkStats: function(workStats) {
        return Boolean(workStats && workStats[0] && workStats[0].in_work_or_study);
    },

    hasRequiredStats: function(courseData) {
        return Boolean(courseData && courseData.statistics && this.hasNSSStats(courseData.statistics.nss) &&
            this.hasWorkStats(courseData.statistics.employment));
    },

    generateLink: function() {
        coursePageBase = '{{domain_name}}/course-details/{{uni_id}}/{{course_id}}/{{mode}}/';
        coursePage = coursePageBase.replace('{{uni_id}}', this.institution);
        coursePage = coursePage.replace('{{course_id}}', this.course);
        coursePage = coursePage.replace('{{mode}}', this.kismode);
        return coursePage;
    }
}

var DataWidget = function(targetDiv, courseData, language, languageKey, kismode, generateLink) {
    this.targetDiv = targetDiv;
    this.courseData = courseData
    this.language = language;
    this.languageKey= languageKey;
    this.kismode =  kismode;
    this.generateLink = generateLink;
    this.setup();
}

DataWidget.prototype = {
    setup: function() {
        this.slideIndex = 0;
        this.renderDataLead();
        this.renderCTABlock();
    },

    renderDataLead: function() {
        var leadNode = document.createElement('div');
        leadNode.classList.add('widget-lead');

        leadNode.appendChild(this.renderSatisfactionSlide());
        leadNode.appendChild(this.renderExplanationSlide());
        leadNode.appendChild(this.renderWorkSlide());

        this.targetDiv.appendChild(leadNode);
        this.carousel();
    },

    renderSatisfactionSlide: function() {
        var isNotAggregated = this.courseData.statistics.nss[0].aggregation_level === 14 ||
                                this.courseData.statistics.nss[0].aggregation_level === 24

        var slideNode = document.createElement('div');
        slideNode.classList.add('lead-slide', 'fade');
        slideNode.id = 'satisfaction';

        var statNode = document.createElement('div');
        statNode.classList.add('stat');

        var titleNode = document.createElement('h1');
        titleNode.classList.add('title');
        var percentage = this.courseData.statistics.nss[0].question_27.agree_or_strongly_agree + '%';
        var title = document.createTextNode(percentage);
        titleNode.appendChild(title);

        var introNode = document.createElement("p");
        introNode.classList.add('intro');
        var intro = document.createTextNode(CONTENT.satisfactionIntro[this.language]);
        introNode.appendChild(intro);

        statNode.appendChild(titleNode);
        statNode.appendChild(introNode);

        slideNode.appendChild(statNode);
        slideNode.appendChild(this.renderCourseDetails(isNotAggregated));

        return slideNode;
    },

    renderExplanationSlide: function() {
        var isNotAggregated = this.courseData.statistics.nss[0].aggregation_level === 14 ||
                                this.courseData.statistics.nss[0].aggregation_level === 24

        var slideNode = document.createElement('div');
        slideNode.classList.add('lead-slide', 'fade');
        slideNode.id = 'satisfaction';

        var statNode = document.createElement('div');
        statNode.classList.add('stat');

        var titleNode = document.createElement('h1');
        titleNode.classList.add('title');
        var percentage = this.courseData.statistics.nss[0].question_1.agree_or_strongly_agree + '%';
        var title = document.createTextNode(percentage);
        titleNode.appendChild(title);

        var introNode = document.createElement("p");
        introNode.classList.add('intro');
        var intro = document.createTextNode(CONTENT.explanationIntro[this.language]);
        introNode.appendChild(intro);

        statNode.appendChild(titleNode);
        statNode.appendChild(introNode);

        slideNode.appendChild(statNode);
        slideNode.appendChild(this.renderCourseDetails(isNotAggregated));

        return slideNode;
    },

    renderWorkSlide: function() {
        var isNotAggregated = this.courseData.statistics.employment[0].aggregation_level === 14 ||
                                this.courseData.statistics.employment[0].aggregation_level === 24

        var slideNode = document.createElement('div');
        slideNode.classList.add('lead-slide', 'fade');
        slideNode.id = 'satisfaction';

        var statNode = document.createElement('div');
        statNode.classList.add('stat');

        var titleNode = document.createElement('h1');
        titleNode.classList.add('title');
        var percentage = this.courseData.statistics.employment[0].in_work_or_study + '%';
        var title = document.createTextNode(percentage);
        titleNode.appendChild(title);

        var introNode = document.createElement("p");
        introNode.classList.add('intro');
        var intro = document.createTextNode(CONTENT.workIntro[this.language]);
        introNode.appendChild(intro);

        statNode.appendChild(titleNode);
        statNode.appendChild(introNode);

        slideNode.appendChild(statNode);
        slideNode.appendChild(this.renderCourseDetails(isNotAggregated));

        return slideNode;
    },

    renderCourseDetails: function(isNotAggregated)  {
        var courseDetailsNode = document.createElement('div');
        courseDetailsNode.classList.add('course-details');

        var courseNode = document.createElement("p");
        courseNode.classList.add('course');

        if (isNotAggregated) {
            var courseName = this.courseData.qualification.label;
            courseName += this.courseData.honours_award_provision === 1 ? ' (Hons) ' : ' ';
            courseName += this.courseData.title[this.languageKey]
            var dataFor = CONTENT.dataFor[this.language];
            var course = document.createTextNode(dataFor + courseName);
        } else {
            var courseName = this.courseData.statistics.employment.subject[this.languageKey + '_label'];
            var dataFor = CONTENT.dataForAggregated[this.language];
            var at = CONTENT.at[this.language];
            var institution = this.courseData.institution.pub_ukprn_name;
            var course = document.createTextNode(dataFor + courseName + at + institution);
        }
        courseNode.appendChild(course);

        courseDetailsNode.appendChild(courseNode);

        if (isNotAggregated) {
            var featuresNode = document.createElement("p");
            featuresNode.classList.add('course');
            var featureList = [this.kismode];
            var placementYear = this.courseData.sandwich_year.code;
            featureList.push(placementYear === 1 ? CONTENT.placementOptional[this.language] :
                                placementYear === 2 ? CONTENT.placement[this.language] : null)
            var yearAbroad = this.courseData.sandwich_year.code;
            featureList.push(yearAbroad === 1 ? CONTENT.abroadOptional[this.language] :
                                yearAbroad === 2 ? CONTENT.abroad[this.language] : null)
            var foundationYear = this.courseData.sandwich_year.code;
            featureList.push(foundationYear === 1 ? CONTENT.foundationOptional[this.language] :
                                foundationYear === 2 ? CONTENT.foundation[this.language] : null)
            var features = document.createTextNode(featureList.filter(Boolean).join(', '));
            featuresNode.appendChild(features);

            courseDetailsNode.appendChild(featuresNode);
        }

        return courseDetailsNode;
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

        var ctaNode = document.createElement('a');
        ctaNode.href = this.generateLink();
        var cta = document.createTextNode(CONTENT.cta[this.language]);

        ctaWrapperNode.appendChild(ctaNode);
        ctaNode.appendChild(cta);
        ctaBlockNode.appendChild(ctaWrapperNode);

        this.targetDiv.appendChild(ctaBlockNode);
    },

    carousel: function() {
        var i;
        var slides = document.getElementsByClassName("lead-slide");
        for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
        }

        this.slideIndex++;
        if (this.slideIndex > slides.length) {this.slideIndex = 1}

        slides[this.slideIndex-1].style.display = "block";
        setTimeout(this.carousel.bind(this), 5000); // Change image every 2 seconds
    }
}

var NoDataWidget = function(targetDiv, language, languageKey, kismode, generateLink) {
    this.targetDiv = targetDiv;
    this.language = language;
    this.languageKey= languageKey;
    this.kismode =  kismode;
    this.generateLink = generateLink;
    this.setup();
}

NoDataWidget.prototype = {
    setup: function() {
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
        ctaNode.href = this.generateLink();

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
