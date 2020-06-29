$(function () {
    var DICT = {
        title: {
            'en': 'Graph showing percentage of students who thought ',
            'cy': 'Graff yn dangos canran y myfyrwyr a oedd yn meddwl '
        },
        desc: {
            'en': ' of students said ',
            'cy': ' Canran y myfyfrwyr a ddywedodd '
        }
    }

    var DoughnutChart = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    DoughnutChart.prototype = {
        setup: function() {
            this.target = this.wrapper.find('.doughnut-chart');
            this.value = this.wrapper.data('value');
            this.field = this.wrapper.data('field');
            this.question = this.wrapper.data('question');
            this.language = this.wrapper.data('language');
            this.renderChart();
        },

        renderChart: function() {
            Highcharts.chart(this.target[0], {

                chart: {
                    type: 'solidgauge',
                    height: '100%',
                    margin: [0, 0, 0, 0],
                    styledMode: true
                },

                title: {
                    text: this.value + '%',
                    verticalAlign: 'middle',
                    style: {
                        fontFamily: 'Nunito Sans',
                        color: '#8D8D8D',
                        fontSize: '36px',
                    },
                },

                yAxis: {
                    min: 0,
                    max: 100,
                    lineWidth: 0,
                    tickPositions: []
                },

                pane: {
                    startAngle: 0,
                    endAngle: 360,
                    background: [{
                        borderWidth: '15px',
                        backgroundColor: 'transparent',
                        borderWidth: 0
                    }]
                },

                plotOptions: {
                    solidgauge: {
                        borderWidth: '15px',
                        dataLabels: {
                            enabled: false
                        },
                        linecap: 'square',
                        stickyTracking: false
                    }
                },

                series: [
                    {
                        name: '',
                        borderColor: '#EDEDED',
                        data: [{
                            color: '#EDEDED',
                            radius: '100%',
                            innerRadius: '100%',
                            y: 100
                        }]
                    },
                    {
                        name: '',
                        borderColor: '#4EA27D',
                        data: [{
                            color: '#4EA27D',
                            radius: '100%',
                            innerRadius: '100%',
                            y: this.value
                        }]
                    }
                ],
                tooltip: {
                    enabled: false,
                },
            });

            var chart = this.target.find('svg');
            chart.attr('role', 'img');

            var titleNode = document.createElement('title');
            var titleId = this.question + '-title';
            titleNode.setAttribute('id', titleId);
            var title = document.createTextNode(DICT.title[this.language] + this.field);
            titleNode.appendChild(title);

            var descNode = document.createElement('desc');
            var descId = this.question + '-desc';
            descNode.setAttribute('id', descId);
            var desc = document.createTextNode(this.value + '%' + DICT.desc[this.language] + this.field);
            descNode.appendChild(desc);

            chart.prepend(descNode);
            chart.prepend(titleNode);
            chart.attr('aria-labelledby', titleId + ' ' + descId);
        }
    }


    function init() {
        var doughnutCharts = $('.discover-uni-chart.doughnut');
        for (var i = 0; i < doughnutCharts.length; i++) {
            new DoughnutChart(doughnutCharts[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
});
