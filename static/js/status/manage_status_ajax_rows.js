/**
* Created by Miguel on 3/9/17.
*/
var $statusTbody = $('#status-tbody');
$(document).ready(function(){

    for (var j = 3, start = 1; start <= total_rows;j++) {
        var nextN = Math.floor(Math.log(j) * 10);
        var stop = start + nextN - 1;
        $.get('/viewer/status/ajax_rows/' + start + '/' + stop + '/', function(data){
            $statusTbody.append($(data));
        });
        start = stop + 1;
    }
});
