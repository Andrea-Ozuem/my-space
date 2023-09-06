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
            let total = parseInt($('span.total').text());
            done = json.completed ? done + 1 : done - 1;
            $('span.done').text(done);
            let percent = Math.floor(done / total * 100);
            console.log(percent)
            $('span.percent').text(percent);
        })
    });
    $('form.new-task').submit(function(event) {
        event.preventDefault();

        // Get input value
        let todo = $('input[name="description"]');
        let u_id = todo.attr('data-id');
        data = {};
        data.completed = 0;
        data.description = todo.val()

        $.ajax({
        type: "POST",
        url: `http://0.0.0.0:5001/api/v1/users/${u_id}/tasks`,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function(response) {
          console.log(response)
          $('ul').prepend(`<li>
                        <input type="checkbox" id="${response.id}" data-id="${response.id}">
                        <label for="${response.id}">
                            <span class="custom-check"><i class="fa-solid fa-check"></i>
                            </span>
                            ${response.description}
                        </label>
                    </li>`)
          },
        error: function(error) {
          console.error("Error adding todo:", error);
          }
       });
       $('input[name="description"]').val("")
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
