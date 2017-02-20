/**
 * Created by dfitzgerald on 8/23/16.
 */
$(document).ready(function(){
    var $reportTable = $('#report-table');
    var tableHeaders = [];
    $reportTable.find('thead tr').first().find('th').each(function(){
        tableHeaders.push($(this).text());
    });


    // Get sidebar content
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

    var hi_impact_vals = [];
    for (var impact in effect_json['conf']) {
        if (impact_json['conf'].hasOwnProperty(impact)) {
            hi_impact_vals.push({name: impact, y: effect_json['conf'][impact]});
        }
    }

    $('#conf_chart').highcharts($.extend(common_options, {
        title: {
            text: 'High Confidence Impact'
        },
        series: [{
            name: 'High Confidence Impact',
            data: hi_impact_vals
        }]
    }));

    var hi_effect_vals = [];
    for (var effect in effect_json['conf']) {
        if (effect_json['conf'].hasOwnProperty(effect)) {
            hi_effect_vals.push({name: effect, y: effect_json['conf'][effect]});
        }
    }

    $('#conf_eff_chart').highcharts($.extend(common_options, {
        title: {
            text: 'High Confidence Effects'
        },
        series: [{
            name: 'High Confidence Effects',
            data: hi_effect_vals
        }]
    }));


});
