// helper function to convert 12-hour time format to 24-hour format
function convertTo24HourFormat(timeString) {
  var colon_index = timeString.indexOf(":");
  var hours = timeString.substring(0,colon_index);
  hours = parseInt(hours);
  var minutes = timeString.substring(colon_index+1, colon_index+3);
  var ampm = timeString.substr(timeString.length-2);
  if (ampm == "pm" && hours < 12) hours = hours + 12;
  if (ampm == "am" && hours == 12) hours = hours - 12;
  var sHours = hours.toString();
  var sMinutes = minutes.toString();

  return sHours + ":" + sMinutes;
}
$(document).ready(function() {

    // datepicker and timepicker from jquery to choose date and time for the booking
    $("#bookingDate").datepicker({
            dateFormat: "yy/mm/dd"
         });
    $("#bookingTime").timepicker();

    // event linked with click on edit_booking icon, to trigger the edit on booking
    $('.edit_booking').click(function() {
        var bookingID;
        bookingID = $(this).attr('data-bookingid');
        // event listener on modal form submit
        $(document).on('click', '#submit-form', function() {
        // get the form data
            var date = $('#bookingDate').val();
            var time = $("#bookingTime").val();
            var numberOFPeople = $("#numberOFPeople").val();
            var notes = $("#Description-text").val();
            var bookingDate = new Date($('#bookingDate').val());
            var date = bookingDate.getFullYear() + '-' + ('0' + (bookingDate.getMonth()+1)).slice(-2) + '-' + ('0' + bookingDate.getDate()).slice(-2);
            // alert(date);
            // alert(time);
            var time24 = convertTo24HourFormat(time);
            //alert(time24);
            //alert(numberOFPeople);
            //alert(notes)
            // use ajax to update the bookings
            $.get('/tutti/edit_booking/',
                {'booking_id': bookingID,'date': date,
                    'time': time24, 'numberOFPeople': numberOFPeople,
                    'notes': notes},
                function(data) {

                    if (data.status == 'success') {
                    // status == success means the update is successful
                    // and we can change the html of the corresponding booking row
                    alert("success edited!");
                    $("#booking-" + bookingID + " .date").html(date);
                    $("#booking-" + bookingID + " .time").html(time24);
                    $("#booking-" + bookingID + " .numOFPeople").html(numberOFPeople);
                    $("#booking-" + bookingID + " .notes").html(notes);

                }
                    else {
                        // if not, tell the user the edit is not successful
                        alert("Sorry, not enough seats");
                    }

                })

    });

    });

    // event on delete icon to delete the booking
    $('.delete_booking').click(function() {
        // get the bookingID and the row holds this booking
        var bookingID;
        var row = $(this).closest('tr');
        bookingID = $(this).attr('data-bookingid');
        //alert(bookingID);
        // have a warning to alert user that he is deleting this booking
        if (confirm('Are you sure you want to delete this booking?')) {
            $.get('/tutti/delete_booking/',
                {'booking_id': bookingID},
                function (data) {

                    if (data.status == 'success') {
                        // if success, delete the row from the table
                        row.remove();
                    }

                })
        }

});


});



