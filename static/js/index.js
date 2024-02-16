let webcam_on = false;
let webcamStream;

function test_webcam(camera_identifier) {
    if (!webcam_on) { //Start webcam
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                let webcam = document.getElementById(`camera_feed_${camera_identifier}`);
                webcam.srcObject = stream;
                webcamStream = stream;
            })
            .catch(function (err) {
                console.error('Unable to transmit camera feed: ', err);
            });
        webcam_on = true;
    } else { //Turn off webcam
        let webcam = document.getElementById(`camera_feed_1`);
        let webcam_2 = document.getElementById(`camera_feed_2`);
        webcam.srcObject = null;
        webcam_2.srcObject = null;
        if (webcamStream) {
            let tracks = webcamStream.getTracks();
            tracks.forEach(function (track) {
                track.stop();
            });
        }
        webcam_on = false;
    }
}