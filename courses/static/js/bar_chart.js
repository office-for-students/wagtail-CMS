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
                        tooltip: {enabled: false},           // keep a tooltip if you want it
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
                        padding: {
                            right: 60
                        }
                    },
                },
                plugins: [{
                    id: 'barLabels',
                    afterDatasetsDraw: function(chart, args, options) {
                        const ctx = chart.ctx;
                        ctx.save();
                        ctx.font = 'bold 16px "Nunito Sans", sans-serif';
                        ctx.fillStyle = '#1F283A';
                        ctx.textAlign = 'left';
                        ctx.textBaseline = 'middle';

                        chart.data.datasets.forEach((dataset, i) => {
                            const meta = chart.getDatasetMeta(i);
                            meta.data.forEach((bar, index) => {
                                const data = dataset.data[index];
                                ctx.fillText(data + '%', bar.x + 5, bar.y);
                            });
                        });
                        ctx.restore();
                    }
                }]
            });
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
