$(function () {

    var DoughnutChart = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    DoughnutChart.prototype = {
        setup: function() {
            this.target = this.wrapper.find('.doughnut-chart');
            this.value = this.wrapper.data('value');
            this.renderChart();
        },

        renderChart: function() {
            Highcharts.chart(this.target[0], {

                chart: {
                    type: 'solidgauge',
                    height: '100%',
                    margin: [0, 0, 0, 0]
                },

                title: {
                    text: this.value + '%',
                    verticalAlign: 'middle',
                    style: {
                        color: '#8D8D8D',
                        fontSize: '26px',
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
                        borderColor: '#DFDFDF',
                        data: [{
                            color: '#DFDFDF',
                            radius: '100%',
                            innerRadius: '100%',
                            y: 100
                        }]
                    },
                    {
                        name: '',
                        borderColor: '#B1C5D4',
                        data: [{
                            color: '#B1C5D4',
                            radius: '100%',
                            innerRadius: '100%',
                            y: this.value
                        }]
                    }
                ],
                tooltip: {
                    enabled: false,
                },
            })
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
