let webcam_on = false;
let webcamStream;

function test_webcam() {
    if (!webcam_on) { //Start webcam
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                let webcam = document.getElementById('camera_feed_1');
                webcam.srcObject = stream;
                webcamStream = stream;
            })
            .catch(function (err) {
                console.error('Unable to transmit camera feed: ', err);
            });
        webcam_on = true;
    } else { //Turn off webcam
        let webcam = document.getElementById('camera_feed_1');
        webcam.srcObject = null;
        if (webcamStream) {
            let tracks = webcamStream.getTracks();
            tracks.forEach(function (track) {
                track.stop();
            });
        }
        webcam_on = false;
    }
}