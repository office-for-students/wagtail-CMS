$(function () {

    var BarChart = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    BarChart.prototype = {
        setup: function() {
            this.target = this.wrapper.find('.bar-chart');
            this.value = this.wrapper.data('value');
            this.renderChart();
        },

        renderChart: function() {
            Highcharts.chart(this.target[0], {
                chart: {
                    type: 'bar',
                    height: '40px',
                    spacing: [0,70,0,1],
                    styledMode: true
                },
                defs: {
                    gradientBar: {
                        tagName: 'linearGradient',
                        id: 'gradient-bar',
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1,
                        children: [{
                            tagName: 'stop',
                            offset: 0
                        }, {
                            tagName: 'stop',
                            offset: 1
                        }]
                    }
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
                        borderColor: '#308282'
                    }
                },
                series: [{
                    data: [{
                        color: '#FFFFFF',
                        y: (100 - this.value),
                        pointWidth: '40',
                    }]
                }, {
                    data: [{
                        color: {
                            linearGradient: { x1: 0, x2: 0, y1: 0, y2: 1 },
                            stops: [
                                [0, '#308282'],
                                [1, '#4EA27D']
                            ]
                        },
                        y: this.value,
                        pointWidth: '40',
                    }]
                }],
                tooltip: {
                    enabled: false,
                },
            });
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

