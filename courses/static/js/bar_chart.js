$(function () {

    var BarChart = function (wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    BarChart.prototype = {
        setup: function () {
            this.target = this.wrapper.find('.bar-chart');
            this.value = this.wrapper.data('value');
            this.label = this.wrapper.data('label');
            this.title = this.wrapper.data('title');
            this.desc = this.wrapper.data('desc');
            this.renderChart();
        },

        renderChart: function () {
            const canvas = this.target.find('canvas')[0];
            new Chart(canvas, {
                type: 'bar',                     // “bar” works for horizontal bars when we set indexAxis
                data: {
                    labels: [""],
                    datasets: [{
                        label: this.value + '%',
                        data: [parseInt(this.value)],
                        backgroundColor: '#1F283A', // any color you like
                        barThickness: 40
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    // Flip the orientation to horizontal
                    indexAxis: 'y',

                    // Remove everything that isn’t the bar itself
                    plugins: {
                        legend: {display: false},          // hide legend
                        tooltip: {enabled: true}           // keep a tooltip if you want it
                    },

                    scales: {
                        x: {
                            display: false,                    // hide the X‑axis line & labels
                            grid: {display: false, drawBorder: false},
                            min: 0,
                            max: 100
                        },
                        y: {
                            display: false,                    // hide the Y‑axis line & labels
                            grid: {display: false, drawBorder: false}
                        }
                    },

                    // Optional: remove the default padding around the chart area
                    layout: {
                        padding: 0
                    },

                    // Ensure the background stays plain (transparent)
                    // backgroundColor: 'transparent'
                }
            });

            // var chart = this.target.find('svg');
            // chart.attr('role', 'img');
            //
            // var titleNode = document.createElement('title');
            // var titleId = this.label + '-title';
            // titleNode.setAttribute('id', titleId);
            // var title = document.createTextNode(this.title);
            // titleNode.appendChild(title);
            //
            // var descNode = document.createElement('desc');
            // var descId = this.label + '-desc';
            // descNode.setAttribute('id', descId);
            // var desc = document.createTextNode(this.value + '%' + this.desc);
            // descNode.appendChild(desc);
            //
            // chart.prepend(descNode);
            // chart.prepend(titleNode);
            // chart.attr('aria-labelledby', titleId + ' ' + descId);
        }
    }

    function init() {
        var barCharts = $('.discover-uni-chart.bar');
        for (var i = 0; i < barCharts.length; i++) {
            console.log("barCharts[i]: ", barCharts[i])
            new BarChart(barCharts[i]);
            console.log(i)
        }
    }

    $(document).on('page:load', init);
    $(init)
});
