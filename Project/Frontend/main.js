$(document).ready(function () {

    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",   // fixed typo (correct case)
        },
        out: {
            effect: "bounceOut",
        },

    });


    // Siri configuration
    var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 640,
    height: 200,
    style: "ios9",
    amplitude: "1",
    speed: "0.3",
    autostart:true,
  });
    // Siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",   // fixed typo (correct case)
            sync:true,
        },
        out: {
            effect: "fadeOutUp",
            sync:true,
        },

    });
    // mic button click event
    $('#MicBtn').click(function () { 
        eel.playAssistantSound()
        $('#Oval').attr("hidden", true);
        $('#SiriWave').attr("hidden", false);
        eel.allcommands()()
    });
});
