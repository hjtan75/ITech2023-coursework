$(document).ready(function() {

    $('.edit_booking').click(function() {
        alert('You clicked the button using JQuery!');

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



