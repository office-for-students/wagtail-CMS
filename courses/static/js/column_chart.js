$(function () {

    var ColumnChart = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    ColumnChart.prototype = {
        setup: function() {
            this.target = this.wrapper.find('.column-chart');
            this.value = this.wrapper.data('value');
            this.label = this.wrapper.data('label');
            this.title = this.wrapper.data('title');
            this.desc = this.wrapper.data('desc');
            this.renderChart();
        },

        renderChart: function() {
          
            Highcharts.chart(this.target[0], {
                chart: {
                    type: 'column',
                    // height: '400px',
                    spacing: [0,70,0,1],
                    styledMode: true,
                    shadow: true
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
                    title: 'hello',
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
                                [0, '#368382'],
                                [1, '#4fa37e']
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

            var chart = this.target.find('svg');
            chart.attr('role', 'img');

            // var titleNode = document.createElement('title');
            // var titleId = this.label + '-title';
            // titleNode.setAttribute('id', titleId);
            // var title = document.createTextNode(this.title);
            // titleNode.appendChild(title);

            // var descNode = document.createElement('desc');
            // var descId = this.label + '-desc';
            // descNode.setAttribute('id', descId);
            // var desc = document.createTextNode(this.value + '%' + this.desc);
            // descNode.appendChild(desc);

            // chart.prepend(descNode);
            // chart.prepend(titleNode);
            // chart.attr('aria-labelledby', titleId + ' ' + descId);
        }
    }


    function init() {
        var columnCharts = $('.discover-uni-chart.column');
        console.log('no of columnCharts: ' + columnCharts.length);
        for (var i = 0; i < columnCharts.length; i++) {
            new ColumnChart(columnCharts[i]);

            console.log('new column chart');
        }
    }

    $(document).on('page:load', init);
    $(init)
});



