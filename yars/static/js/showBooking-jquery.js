$(document).ready(function() {

    $("#bookingDate").datepicker({
            dateFormat: "yy-mm-dd"
         });
    $("#bookingTime").timepicker();

    $('.edit_booking').click(function() {
        //alert('You clicked the button using JQuery!');
        var bookingID;
        var row = $(this).closest('tr');
        bookingID = $(this).attr('data-bookingid');

        //alert(bookingID);
        $(document).on('click', '#submit-form', function() {
        // get the form data
            var date = $('#bookingDate').val();
            var time = $("#bookingTime").val();
            var numberOFPeople = $("#numberOFPeople").val();
            var notes = $("#Description-text").val();
        //alert(date);
        //alert(time);
        //alert(numberOFPeople);
        //alert(notes)
            $.get('/tutti/edit_booking/',
                {'booking_id': bookingID,'date': date,
                    'time': time, 'numberOFPeople': numberOFPeople,
                'notes': notes},
                function(data) {

                    if (data.status == 'success') {
                    // remove the row from the table
                    //alert('success');
                    $("#booking-" + bookingID + " .date").html(date);
                    $("#booking-" + bookingID + " .time").html(time);
                    $("#booking-" + bookingID + " .numOFPeople").html(numberOFPeople);
                    $("#booking-" + bookingID + " .notes").html(notes);

                }

                })

    });

    });



    $('p').hover(
function() {
        $(this).css('color', 'red');
},
function() {
        $(this).css('color', 'black');
});
    $('.delete_booking').click(function() {

        var bookingID;
        var row = $(this).closest('tr');
        bookingID = $(this).attr('data-bookingid');
        alert(bookingID);
        $.get('/tutti/delete_booking/',
            {'booking_id': bookingID},
            function(data) {

                if (data.status == 'success') {
                // remove the row from the table
                row.remove();
            }

            })

});


});



