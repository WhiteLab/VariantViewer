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
    for (var impact in impact_json['conf']) {
        if (impact_json['conf'].hasOwnProperty(impact)) {
            hi_impact_vals.push({name: impact, y: impact_json['conf'][impact]});
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
    var all_impact_vals = [];
    for (var impact_all in impact_json['all']) {
        if (impact_json['all'].hasOwnProperty(impact_all)) {
            all_impact_vals.push({name: impact_all, y: impact_json['all'][impact_all]});
        }
    }

    $('#all_chart').highcharts($.extend(common_options, {
        title: {
            text: 'All On-target Impacts'
        },
        series: [{
            name: 'All On-target Impacts',
            data: all_impact_vals
        }]
    }));

    var all_effect_vals = [];
    for (var effect_all in effect_json['all']) {
        if (effect_json['all'].hasOwnProperty(effect_all)) {
            all_effect_vals.push({name: effect_all, y: effect_json['all'][effect_all]});
        }
    }

    $('#all_eff_chart').highcharts($.extend(common_options, {
        title: {
            text: 'All On-target Effects'
        },
        series: [{
            name: 'All On-target Effects',
            data: all_effect_vals
        }]
    }));
});
