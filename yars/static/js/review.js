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

    onAddReviewClick = function () {
        layer.open({
            type: 1,
            title: 'Add review',
            content: $('#add_review'),
            btn: ['Add', 'Cancel'],
            area: ['600px', 'auto'],
            shadeClose: true,
            yes: function (index, layero) {
                let description = $("#description").val();
                $.ajax({
                    type: "POST",
                    url: "/tutti/reviews/",
                    data: {
                        rating: rating,
                        description: description
                    },
                    success: function (response) {
                        if(response.status){
                            layer.msg(response.msg, {icon: 6});
                            setTimeout(function () {
                                window.location.reload();
                            }, 1500);
                        }
                    },
                    error: function (xhr, status, error) {
                        layer.msg(xhr.responseText, {icon: 5});
                    }
                });
                layer.close(index);
            },
            btn2: function (index, layero) {
                layer.close(index);
            }
        });
    }
});