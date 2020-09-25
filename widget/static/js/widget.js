var CONTENT = {
    'satisfactionIntro': {
        'en-gb': 'of students were satisfied overall with their course.',
        'cy-gb':"cyfran y myfyrwyr a oedd yn fodlon â'u cwrs ar y cyfan."
    },
    'explanationIntro': {
        'en-gb': 'of students agreed staff were good at explaining things.',
        'cy-gb': 'cyfran y myfyrwyr sydd yn cytuno bod staff yn dda am esbonio pethau.'
    },
    'workIntro': {
        'en-gb': 'in work or doing further study 15 months after the course.',
        'cy-gb': "yn symud ymlaen i weithio ac/neu astudio o fewn 15 mis ar ôl y cwrs"
    },
    'ctaLead1': {
        'en-gb': 'For ',
        'cy-gb': 'Am '
    },
    'ctaLead2': {
        'en-gb': 'more',
        'cy-gb': 'fwy'
    },
    'ctaLead3': {
        'en-gb': ' official course information visit.',
        'cy-gb': ' o wybodaeth swyddogol am y cwrs, ewch i'
    },
    'logo': {
        'en-gb': '{{domain_name}}/static/images/logos/widget_logo_english.svg',
        'cy-gb': '{{domain_name}}/static/images/logos/widget_logo_welsh.svg'
    },
    'logoAlt': {
        'en-gb': 'DiscoverUni',
        'cy-gb': 'Darganfod Prifysgol'
    },
    'cta': {
        'en-gb': 'See course data',
        'cy-gb': "Gweld data'r cwrs"
    },
    'noDataIntro': {
        'en-gb': 'To see official information about this course and others visit Discover Uni.',
        'cy-gb': 'I weld gwybodaeth swyddogol am y cwrs hwn a chyrsiau eraill, ewch i Darganfod y Brifysgol.'
    },
    'noDataCtaLead1': {
        'en-gb': 'Make an ',
        'cy-gb': 'Dewis '
    },
    'noDataCtaLead2': {
        'en-gb': 'informed',
        'cy-gb': 'yn'
    },
    'noDataCtaLead3': {
        'en-gb': ' choice.',
        'cy-gb': ' ddeallus.'
    },
    'noDataCta': {
        'en-gb': 'See course info',
        'cy-gb': 'Gweld gwybodaeth y cwrs'
    },
    'placement': {
        'en-gb': 'Placement year',
        'cy-gb': 'Blwyddyn ar leoliad'
    },
    'placementOptional': {
        'en-gb': 'Placement year optional',
        'cy-gb': 'Blwyddyn ar leoliad yn ddewisol'
    },
    'foundation': {
        'en-gb': 'Foundation year',
        'cy-gb': 'Blwyddyn sylfaen'
    },
    'foundationOptional': {
        'en-gb': 'Foundation year optional',
        'cy-gb': 'Blwyddyn sylfaen yn ddewisol'
    },
    'abroad': {
        'en-gb': 'Year abroad',
        'cy-gb': 'Blwyddyn dramor'
    },
    'abroadOptional': {
        'en-gb': 'Year abroad optional',
        'cy-gb': 'Blwyddyn dramor yn ddewisol'
    },
    'dataFor': {
        'en-gb': 'Data for: ',
        'cy-gb': 'Data ar gyfer: '
    },
    'dataForAggregated': {
        'en-gb': 'Data for courses in ',
        'cy-gb': 'Data ar gyfer cyrsiau '
    },
    'at': {
        'en-gb': ' at ',
        'cy-gb': ' yn '
    }
}


var MODES = {
    'fulltime': 1,
    'parttime': 2,
}

var MODE_KEYS = {
    'fulltime': 'FullTime',
    'parttime': 'PartTime',
}

var LANGUAGE_KEYS = {
    'en-gb': 'english',
    'cy-gb': 'welsh'
}

var MINIMUM_RESPONSIVE_HORIZONTAL_WIDTH = 400;

var  DiscoverUniWidget = function(targetDiv) {
    this.targetDiv = targetDiv;
    this.setup();
}

DiscoverUniWidget.prototype = {
    setup: function() {
        this.institution = this.targetDiv.dataset.institution;
        this.course = this.targetDiv.dataset.course;
        this.kismode = this.targetDiv.dataset.kismode ? MODE_KEYS[this.targetDiv.dataset.kismode.toLowerCase()] : 'FullTime';
        this.orientation = this.targetDiv.dataset.orientation ? this.targetDiv.dataset.orientation.toLowerCase() : 'vertical';
        this.language = this.targetDiv.dataset.language ? this.targetDiv.dataset.language.toLowerCase() : 'en-gb';
        this.languageKey = LANGUAGE_KEYS[this.language];
        this.size = this.targetDiv.dataset.size;

        this.targetDiv.classList.add(this.orientation);
        if (this.orientation === 'responsive') {
            this.handleResponsive();
        }

        this.addCss();
        this.loadCourseData();
    },

    handleResponsive: function() {
        if (this.inIframe()) {
            if (window.innerWidth > window.innerHeight) {
                this.targetDiv.classList.add('horizontal');
            } else {
                this.targetDiv.classList.add('vertical');
            }
        } else {
            if (this.targetDiv.clientWidth > MINIMUM_RESPONSIVE_HORIZONTAL_WIDTH) {
                this.targetDiv.classList.add('horizontal');
            } else {
                this.targetDiv.classList.add('vertical');
            }
        }
    },

    inIframe: function() {
        try {
            return window.location !== window.parent.location;
        } catch (e) {
            return true;
        }
    },

    addCss: function() {
        var logoFontNode = document.createElement('link');
        logoFontNode.href = "https://fonts.googleapis.com/css?family=Montserrat:regular,bold&display=swap";
        logoFontNode.rel = "stylesheet";
        logoFontNode.type = "text/css";
        var generalFontNode = document.createElement('link');
        generalFontNode.href = "https://fonts.googleapis.com/css?family=Nunito+Sans:regular,bold&display=swap";
        generalFontNode.rel = "stylesheet";
        generalFontNode.type = "text/css";
        styling = "{% styles %}";
        var stylingNode = document.createElement('style');
        var stylingTextNode = document.createTextNode(styling);
        stylingNode.appendChild(stylingTextNode);
        var widgetScript = document.getElementById('unistats-widget-script');
        widgetScript.parentNode.insertBefore(stylingNode, widgetScript);
        widgetScript.parentNode.insertBefore(logoFontNode, widgetScript);
        widgetScript.parentNode.insertBefore(generalFontNode, widgetScript);
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
            var courseData = JSON.parse(response);

            if (this.hasRequiredStats(courseData) && !this.isMultiSubject(courseData)) {
                new DataWidget(this.targetDiv, courseData, this.language, this.languageKey, this.kismode,
                                this.hasOverallSatisfactionStats, this.hasTeachingSatisfactionStats, this.hasWorkStats,
                                this.generateLink.bind(this));
            }
            else {
                new NoDataWidget(this.targetDiv, courseData.course_name, courseData.institution_name, this.language,
                this.languageKey, this.kismode, this.generateLink.bind(this));
            }
        } else {
            new NoDataWidget(this.targetDiv, "", "", this.language, this.languageKey, this.kismode,
                                this.generateLink.bind(this));
        }
    },

    isMultiSubject: function(courseData) {
        return Boolean(courseData.statistics.nss.length > 1 || courseData.statistics.employment.length > 1);
    },

    setOverallSatisfactionStats: function(nssStats) {
        this.hasOverallSatisfactionStats = Boolean(nssStats && nssStats[0] && nssStats[0].question_1);
    },

    setTeachingSatisfactionStats: function(nssStats) {
        this.hasTeachingSatisfactionStats = Boolean(nssStats && nssStats[0] && nssStats[0].question_27);
    },

    setWorkStats: function(workStats) {
        this.hasWorkStats = Boolean(workStats && workStats[0] && workStats[0].in_work_or_study);
    },

    hasRequiredStats: function(courseData) {
        this.setOverallSatisfactionStats(courseData.statistics.nss)
        this.setTeachingSatisfactionStats(courseData.statistics.nss)
        this.setWorkStats(courseData.statistics.employment)
        return Boolean(courseData && courseData.statistics &&
            Boolean(this.hasOverallSatisfactionStats || this.hasTeachingSatisfactionStats || this.hasWorkStats));
    },

    generateLink: function() {
        var base_domain = '{{domain_name}}';
        if (this.languageKey === 'welsh') {
            base_domain +=  '/cy';
        }
        coursePageBase = '{{base_domain}}/course-details/{{uni_id}}/{{course_id}}/{{mode}}/';
        coursePage = coursePageBase.replace('{{base_domain}}', base_domain);
        coursePage = coursePage.replace('{{uni_id}}', this.institution);
        coursePage = coursePage.replace('{{course_id}}', this.course);
        coursePage = coursePage.replace('{{mode}}', this.kismode);
        return coursePage;
    }
}

var DataWidget = function(targetDiv, courseData, language, languageKey, kismode, hasOverall, hasTeaching, hasWork,
                            generateLink) {
    this.targetDiv = targetDiv;
    this.courseData = courseData
    this.language = language;
    this.languageKey= languageKey;
    this.kismode =  kismode;
    this.hasOverall = hasOverall;
    this.hasTeaching = hasTeaching;
    this.hasWork = hasWork;
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
        if (this.hasOverall) {
            leadNode.appendChild(this.renderSatisfactionSlide());
        }
        if (this.hasTeaching) {
            leadNode.appendChild(this.renderExplanationSlide());
        }
        if (this.hasWork) {
            leadNode.appendChild(this.renderWorkSlide());
        }

        this.targetDiv.appendChild(leadNode);
        this.carousel();
    },

    createSlideNode: function(idName, statNode, isNotAggregated) {
        var slideNode = document.createElement('div');
        slideNode.classList.add('lead-slide', 'fade');
        slideNode.id = idName;

        slideNode.appendChild(statNode);
        slideNode.appendChild(this.renderCourseDetails(isNotAggregated));

        return slideNode;
    },

    createStatNode: function(titleNode, introNode) {
        var statNode = document.createElement('div');
        statNode.classList.add('stat');

        statNode.appendChild(titleNode);
        statNode.appendChild(introNode);

        return statNode;
    },

    createTitleNode: function(titleText) {
        var titleNode = document.createElement('h1');
        titleNode.classList.add('title');
        var title = document.createTextNode(titleText);
        titleNode.appendChild(title);
        return titleNode;
    },

    createIntroNode: function(introText) {
        var introNode = document.createElement("p");
        introNode.classList.add('intro');
        var intro = document.createTextNode(introText);
        introNode.appendChild(intro);
        return introNode;
    },

    renderSatisfactionSlide: function() {
        var isNotAggregated = this.courseData.statistics.nss[0].aggregation_level === 14 ||
                                this.courseData.statistics.nss[0].aggregation_level === 24

        var percentage = this.courseData.statistics.nss[0].question_27.agree_or_strongly_agree + '%';
        var introText = CONTENT.satisfactionIntro[this.language];

        var statNode = this.createStatNode(this.createTitleNode(percentage), this.createIntroNode(introText));

        var slideNode = this.createSlideNode('satisfaction', statNode, isNotAggregated);

        return slideNode;
    },

    renderExplanationSlide: function() {
        var isNotAggregated = this.courseData.statistics.nss[0].aggregation_level === 14 ||
                                this.courseData.statistics.nss[0].aggregation_level === 24

        var percentage = this.courseData.statistics.nss[0].question_1.agree_or_strongly_agree + '%';
        var introText = CONTENT.explanationIntro[this.language];

        var statNode = this.createStatNode(this.createTitleNode(percentage), this.createIntroNode(introText));

        var slideNode = this.createSlideNode('explanation', statNode, isNotAggregated);

        return slideNode;
    },

    renderWorkSlide: function() {
        var isNotAggregated = this.courseData.statistics.employment[0].aggregation_level === 14 ||
                                this.courseData.statistics.employment[0].aggregation_level === 24

        var percentage = this.courseData.statistics.employment[0].in_work_or_study + '%';
        var introText = CONTENT.workIntro[this.language];

        var statNode = this.createStatNode(this.createTitleNode(percentage), this.createIntroNode(introText));

        var slideNode = this.createSlideNode('work', statNode, isNotAggregated);

        return slideNode;
    },

    renderCourseDetails: function(isNotAggregated)  {
        var courseDetailsNode = document.createElement('div');
        courseDetailsNode.classList.add('course-details');

        var courseNode = document.createElement("p");
        courseNode.classList.add('course');

        var courseName = this.courseData.course_name[this.languageKey];
        if (typeof courseName === 'undefined') {
            courseName = this.courseData.course_name['english'];
        }
        if (isNotAggregated) {
            courseName += this.courseData.honours_award_provision === 1 ? ' (Hons) ' : ' ';
            courseName += this.courseData.title[this.languageKey]
            var dataFor = CONTENT.dataFor[this.language];
            var course = document.createTextNode(dataFor + courseName);
        } else {
            var dataFor = CONTENT.dataForAggregated[this.language];
            var at = CONTENT.at[this.language];
            var institution = this.courseData.institution_name[this.languageKey];
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

        var headingNode = document.createElement('h1');
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
        headingNode.appendChild(leadNode1);
        headingNode.appendChild(leadNode2);
        headingNode.appendChild(leadNode3);

        ctaBlockNode.appendChild(headingNode);

        var logoNode = document.createElement('img');
        logoNode.classList.add('logo');
        logoNode.setAttribute('src', CONTENT.logo[this.language]);
        logoNode.setAttribute('alt', CONTENT.logoAlt[this.language]);
        ctaBlockNode.appendChild(logoNode);

        var ctaWrapperNode = document.createElement('div');
        ctaWrapperNode.classList.add('cta');

        var ctaNode = document.createElement('a');
        ctaNode.href = this.generateLink();
        ctaNode.setAttribute('target', '_blank');
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
        setTimeout(this.carousel.bind(this), 5000); // Change image every 5 seconds
    }
}

var NoDataWidget = function(targetDiv, courseName, institutionName ,language, languageKey, kismode, generateLink) {
    this.targetDiv = targetDiv;
    this.courseName = courseName;
    this.institutionName = institutionName;
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

    renderNoDataLead: function(parentNode) {
        var leadNode = document.createElement('div');
        leadNode.classList.add('widget-lead');

        if (typeof this.courseName[this.languageKey] !== 'undefined' && typeof this.institutionName[this.languageKey] !== 'undefined') {
            var courseNode = document.createElement("p");
            courseNode.classList.add('intro');

            var courseName = this.courseName[this.languageKey];
            var at = CONTENT.at[this.language];
            var institution = this.institutionName[this.languageKey];
            var course = document.createTextNode(courseName + at + institution);

            courseNode.appendChild(course);
            leadNode.appendChild(courseNode);
        } else {
            var courseNode = document.createElement("p");
            courseNode.classList.add('intro');
            courseName = this.courseName['english'];
            var at = CONTENT.at['en-gb']
            var institution = this.institutionName['english'];
            var course = document.createTextNode(courseName + at + institution);

            courseNode.appendChild(course);
            leadNode.appendChild(courseNode);
        }

        var courseDetailsNode = document.createElement('div');
        courseDetailsNode.classList.add('course-details');

        var introNode = document.createElement("p");
        introNode.classList.add('course');
        var intro = document.createTextNode(CONTENT.noDataIntro[this.language]);
        introNode.appendChild(intro);
        courseDetailsNode.appendChild(introNode);
        leadNode.appendChild(courseDetailsNode);
        this.targetDiv.appendChild(leadNode);
    },

    renderNoDataCTABlock: function() {
        var ctaBlockNode = document.createElement('div');
        ctaBlockNode.classList.add('widget-cta-block');

        var headingNode = document.createElement('h1');
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
        headingNode.appendChild(leadNode1);
        headingNode.appendChild(leadNode2);
        headingNode.appendChild(leadNode3);

        ctaBlockNode.appendChild(headingNode);

        var logoNode = document.createElement('img');
        logoNode.classList.add('logo');
        logoNode.setAttribute('src', CONTENT.logo[this.language]);
        logoNode.setAttribute('alt', CONTENT.logoAlt[this.language]);
        ctaBlockNode.appendChild(logoNode);

        var ctaWrapperNode = document.createElement('div');
        ctaWrapperNode.classList.add('cta');
        var ctaNode = document.createElement('a');
        ctaNode.setAttribute('target', '_blank');
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
