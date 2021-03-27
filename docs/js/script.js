$( document ).ready(function() {

    $('.owl-carousel').owlCarousel({
        loop:true,
        margin:10,
        nav:true,
        navigation : false,
        responsive:{
            0:{
                items:1
            },
            600:{
                items:2
            },
            1000:{
                items:3
            }
        }
    })

    lightbox.option({
        'resizeDuration': 200,
        'wrapAround': true
    });

    $("#contact form").on("submit", function(event){
        event.preventDefault();

        const $spinner = $('#spinner .spinner-container');

        $spinner.show()

        const url = 'https://api.navonigiardini.com/send/mail';

        const formValues= $(this).serializeArray();

        const data = {};
        formValues.forEach(function (item) {
            data[item.name] = item.value;
        });

        $.ajax({
            type: 'post',
            url: url,
            crossDomain: true,
            dataType: "json",
            data: JSON.stringify(data),
            headers: {
                "accept": "application/json"
            },
            success: function (data) {
                $("#form-message").html("<div class=\"alert alert-success\">Thank you for your message</div>");
                $spinner.hide();
            },
            error: function (data) {
                $("#form-message").html("<div class=\"alert alert-danger\">Error</div>");
                $spinner.hide();
            },
        });
    });


});