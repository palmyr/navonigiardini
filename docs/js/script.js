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
    })
});