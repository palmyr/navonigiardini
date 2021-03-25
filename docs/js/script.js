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

        const url = 'https://b8mgab3rvd.execute-api.eu-west-1.amazonaws.com/navonApiStAOYIAOOM5W0Y/email';

        const formValues= $(this).serializeArray();

        const data = {};
        formValues.forEach(function (item) {
            data[item.name] = item.value;
        });

        // $.post(url, formValues, function(data){
        //     // Display the returned data in browser
        //     console.log(data);
        // });

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
            },
            error: function (data) {
                $("#form-message").html("<div class=\"alert alert-danger\">Error</div>");
            },
        });
    });


});