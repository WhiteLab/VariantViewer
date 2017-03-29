/**
 * Created by Miguel on 3/29/17.
 */
var $metadataTbody = $('#metadata-tbody');
$(document).ready(function(){


    for (var j = 3, start = 1; start <= total_rows;j++) {
        var nextN = Math.floor(Math.log(j) * 10);
        var stop = start + nextN - 1;
        $.get('/viewer/metadata/ajax_rows/' + start + '/' + stop + '/', function(data){
            var $data = $(data);
            $metadataTbody.append($data);
            $data.find('span.igsbviewer-view-report').click(function() {
                var pk = $(this).data('pk');
                var $csrf = $($(this).data('csrf'));
                $("<form>").attr({
                    action: '/viewer/metadata/manage_metadata/' + pk + '/',
                    method: 'POST'
                }).append($csrf).appendTo($("body")).submit();

            });
        });
        start = stop + 1;
    }
});