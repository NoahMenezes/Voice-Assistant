$(document).ready(function () {
    $('.tlt').textillate({
        loop: true,
        in: {
            effect: 'bounceIn',
            delayScale: 1.5,   // delay between letters
            delay: 50,
            sync: false,
        },
        out: {
            effect: 'bounceOut',
            delayScale: 1.5,
            delay: 50,
            sync: false,
        }
    });
});
