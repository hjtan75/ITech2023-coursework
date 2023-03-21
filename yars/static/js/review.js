// the onAddReviewClick function is executed, when the Add Comment button is clicked, 
function onAddReviewClick() {
}

layui.use(['jquery', 'rate'], function () {
    var $ = layui.jquery;
    var rate = layui.rate;

    var rating = 0;

    rate.render({
        elem: '#star',
        choose: function (value) {
            rating = value;
        }
    });
    // define the onAddReviewClick function to open the Add Comment pop-up window
    onAddReviewClick = function () {
        layer.open({
            type: 1,
            title: 'Add review',
            content: $('#add_review'),
            btn: ['Add', 'Cancel'],
            area: ['600px', 'auto'],
            shadeClose: true,
            yes: function (index, layero) { // click the Confirm button
                let description = $("#description").val();
                // invoking Ajax for asynchronous submission
                $.ajax({
                    type: "POST",
                    url: "/tutti/reviews/", // Url address
                    // data that needs to be transferred to the background
                    data: {  
                        rating: rating,
                        description: description
                    },
                    
                    success: function (response) {
                        // asynchronous operation executed successfully
                        if(response.status){ // if the response status is true
                            layer.msg(response.msg, {icon: 6}); // display success prompt box
                            setTimeout(function () { // refresh the page after 1.5s
                                window.location.reload();
                            }, 1500);
                        }
                    },
                    error: function (xhr, status, error) {
                        // Asynchronous operation execution error
                        layer.msg(xhr.responseText, {icon: 5}); // display error prompt box
                    }
                });
                layer.close(index); // close Popup
            },
            btn2: function (index, layero) { // click the cancel button
                layer.close(index);
            }
        });
    }
});