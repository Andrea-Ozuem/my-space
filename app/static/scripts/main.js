$(document).ready(function () {
    $('input[type=checkbox]').change(function() {
        let isChecked = $(this).is(':checked');
        let status = isChecked ? 1 : 0;
        
        // send request to update task using api
        $.ajax({
            url: 'http://0.0.0.0:5001/api/v1/tasks/task_id',
            type: 'PUT',
            data: JSON.stringify('completed': status),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
        }).done(function( json ) {
            console.log(json);
        })
    });
});