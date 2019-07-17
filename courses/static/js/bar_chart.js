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
                    height: '50px',
                    spacing: [0,0,0,0]
                },
                title: {
                    text: this.value + '%',
                    verticalAlign: 'middle',
                    align: 'left',
                    x: 15,
                    y: 10,
                    style: {
                        color: '#000000',
                        fontSize: '19px',
                        fontFamily: 'Helvetica Neue',
                        marginLeft: '15px'
                    },
                },
                xAxis: {
                    categories: [''],
                    lineWidth: 0,
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
                        stacking: 'percentage'
                    }
                },
                series: [{
                    data: [{
                        color: '#DFDFDF',
                        y: (100 - this.value),
                        pointWidth: '40',
                    }]
                }, {
                    data: [{
                        color: '#B1C5D4',
                        y: this.value,
                        pointWidth: '40',
                    }]
                }]
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

