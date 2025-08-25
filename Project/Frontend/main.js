$(document).ready(function () {
    $('.tlt').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",   // fixed typo (correct case)
        },
        out: {
            effect: "bounceOut",
        },
    });
});
