/**
 * Created by dfitzgerald on 8/23/16.
 */
$(document).ready(function(){
    var $reportTable = $('#report-table');
    var tableHeaders = [];
    var $currentlySelected;
    $reportTable.find('thead tr').first().find('th').each(function(){
        tableHeaders.push($(this).text());
    });

    $reportTable.find('tbody tr').click(function(){
        // Don't fetch new plots if clicked mutiple times
        if ($currentlySelected === JSON.stringify($(this))) return;
        $currentlySelected = JSON.stringify($(this));

        var record = {};
        var i = 0;
        $(this).find('td').each(function(){
            record[tableHeaders[i]] = $(this).html();
            i++;
        });

        $('#igsbviewer-right-panel').text('Loading...');
        // Get sidebar content
        $.post('/viewer/report/get_right_sidebar/', {
            json_str: JSON.stringify(record)
        }, function(data){
            $('#igsbviewer-right-panel').html($(data));
        });
    });
});
