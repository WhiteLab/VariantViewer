/**
 * Created by dfitzgerald on 8/23/16.
 */
$(document).ready(function(){
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
                    formatter: function(){
                        return this.point.name + ': ' + this.y + ' (' + Math.round(this.percentage*100)/100 + '%)'
                    }
                }
            }
        }
    };

    if (absolute_normal_alt && absolute_normal_ref){
        $('#normal_chart').highcharts($.extend(common_options, {
            title: {
                text: 'Normal'
            },
            series: [{
                name: 'Normal',
                data: [{
                    name: 'Alt ' + alt_base,
                    y: absolute_normal_alt
                }, {
                    name: 'Ref ' + ref_base,
                    y: absolute_normal_ref
                }]
            }]
        }));
    } else {
        $('#normal_chart').html('Normal Plot Not Available');
    }

    if (absolute_tumor_alt && absolute_tumor_ref) {
        $('#tumor_chart').highcharts($.extend(common_options, {
            title: {
                text: 'Tumor'
            },
            series: [{
                name: 'Tumor',
                data: [{
                    name: 'Alt ' + alt_base,
                    y: absolute_tumor_alt
                }, {
                    name: 'Ref ' + ref_base,
                    y: absolute_tumor_ref
                }]
            }]
        }));
    } else {
        $('#tumor_chart').html('Tumor Plot Not Available');
    }
});