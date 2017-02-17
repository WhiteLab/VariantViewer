/**
 * Created by dfitzgerald on 8/23/16.
 */
$(document).ready(function() {
    var common_options = {
        chart: {
            type: 'pie',
            backgroundColor: '#FBFCFD'
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            series: {
                animation: {duration: 300},
                dataLabels: {
                    enabled: true,
                    formatter: function () {
                        return this.point.name + ': ' + this.y + ' (' + Math.round(this.percentage * 100) / 100 + '%)'
                    }
                }
            }
        }
    };

    var vals = {};
    for (var impact in impact_json['conf']) {
        if (impact_json['conf'].hasOwnProperty(impact)) {
            vals.push({name: impact, y: impact_json['conf'][impact]});
        }
    }

    $('#conf_chart').highcharts($.extend(common_options, {
        title: {
            text: 'High Confidence Impact'
        },
        series: [{
            name: 'High Confidence Impact',
            data: vals
        }]
    }));
});

