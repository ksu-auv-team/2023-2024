// Function to send an HTTP request
function sendRequest(url) {
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
}

// Add event listeners to buttons
document.getElementById('runAll').addEventListener('click', () => sendRequest('/run-all'));
document.getElementById('stopAll').addEventListener('click', () => sendRequest('/stop-all'));
document.getElementById('testHardware').addEventListener('click', () => sendRequest('/test-hardware'));
document.getElementById('testMovement').addEventListener('click', () => sendRequest('/test-movement'));
document.getElementById('testNeuralNetwork').addEventListener('click', () => sendRequest('/test-neural-network'));
document.getElementById('shutdown').addEventListener('click', () => sendRequest('/shutdown'));
