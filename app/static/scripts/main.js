$(document).ready(function () {
    $('input[type=checkbox]').change(function() {
        let isChecked = $(this).is(':checked');
        let status = isChecked ? 1 : 0;
        let task_id = $(this).attr('data-id');
        
        // send request to update task using api
        $.ajax({
            url: `http://0.0.0.0:5001/api/v1/tasks/${task_id}`,
            type: 'PUT',
            data: JSON.stringify({'completed': status}),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
        }).done(function( json ) {
            let done = parseInt($('span.done').text())
            let total = $('span.percent');
            done = json.completed ? done + 1 : done - 1;
            $('span.done').text(done);
            $('span.percent').text(done/total);
        })
    });

    $('.wid-icon').click(function() {
        console.log('here')
        if($('.widgets').hasClass('pane')) {
            $('.widgets').removeClass('pane');
        } else {
            // slide out
            $('.widgets').addClass('pane');
        }
    })
});
