$(function () {

    var BarChart = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    BarChart.prototype = {
        setup: function() {
            this.target = this.wrapper.find('.bar-chart');
            this.value = this.wrapper.data('value');
            this.label = this.wrapper.data('label');
            this.title = this.wrapper.data('title');
            this.desc = this.wrapper.data('desc');
            this.renderChart();
        },

        renderChart: function() {
            Highcharts.chart(this.target[0], {
                chart: {
                    type: 'bar',
                    height: '40px',
                    spacing: [0,70,0,1],
                    styledMode: true,
                    shadow: true
                },
                title: {
                    text: this.value + '%',
                    verticalAlign: 'middle',
                    align: 'right',
                    x: 70,
                    y: 20,
                    style: {
                        color: '#6E6E6E',
                        fontSize: '19px',
                        fontFamily: 'Nunito Sans',
                        fontWeight: 'bold',
                        marginLeft: '15px'
                    },
                },
                xAxis: {
                    categories: [''],
                    lineWidth: 1,
                },
                yAxis: {
                    min: 0,
                    max: 100,
                    gridLineWidth: 0,
                    lineWidth: 0,
                    labels: {
                        enabled: false,
                    },
                    title: '',
                },
                legend: {
                    enabled: false
                },
                plotOptions: {
                    series: {
                        stacking: 'percentage',
                        borderWidth: 2,
                        borderColor: '#308282',
                        color: {
                            linearGradient: {
                              x1: 0,
                              x2: 0,
                              y1: 0,
                              y2: 1
                            },
                            stops: [
                              [0, '#f79685'],
                              [1, '#f45c42']
                            ]
                          },
                        y: this.value,
                        pointWidth: '40',
                    }
                },
                series: [{
                    data: [{
                        color: {
                            linearGradient: {
                              x1: 0,
                              x2: 0,
                              y1: 0,
                              y2: 1
                            },
                            stops: [
                              [0, '#f79685'],
                              [1, '#f45c42']
                            ]
                          },
                        y: this.value,
                        pointWidth: '40'
                    }]
                }], 
                   
                tooltip: {
                    enabled: false,
                }
            });

            var chart = this.target.find('svg');
            chart.attr('role', 'img');

            var titleNode = document.createElement('title');
            var titleId = this.label + '-title';
            titleNode.setAttribute('id', titleId);
            var title = document.createTextNode(this.title);
            titleNode.appendChild(title);

            var descNode = document.createElement('desc');
            var descId = this.label + '-desc';
            descNode.setAttribute('id', descId);
            var desc = document.createTextNode(this.value + '%' + this.desc);
            descNode.appendChild(desc);

            chart.prepend(descNode);
            chart.prepend(titleNode);
            chart.attr('aria-labelledby', titleId + ' ' + descId);
        }
    }


    function init() {
        var barCharts = $('.discover-uni-chart.bar');
        for (var i = 0; i < barCharts.length; i++) {
            new BarChart(barCharts[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
});

