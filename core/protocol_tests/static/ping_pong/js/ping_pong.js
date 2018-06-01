var messageParagraph = document.getElementById('message');
var sendPingButton = document.getElementById('send-ping');
var sendPongButton = document.getElementById('send-pong');

var url = 'ws://' + window.location.host + '/ws/protocol_tests/ping_pong/';
var socket = new WebSocket(url);

function onOpen() {
    console.log('WebSocket opened');
    sendPingButton.disabled = false;
    sendPongButton.disabled = false;

    messageParagraph.innerText = 'Send a \'Ping\' or a \'Pong\' to the server';
}

function onClose() {
    console.log('WebSocket closed');
    sendPingButton.disabled = true;
    sendPongButton.disabled = true;

    messageParagraph.innerText = 'Connection to the server has been closed';
}

function onError() {
    console.log('WebSocket faced an error');
    sendPingButton.disabled = true;
    sendPongButton.disabled = true;

    messageParagraph.innerText = 'Connection to the server faced an error';
}

function onMessage(event) {
    var data = JSON.parse(event.data);
    var message = data['message'];
    console.log('WebSocket received a message \'' + message + '\'');

    messageParagraph.innerText = 'Server says \'' + message + '\'';
}

socket.onopen = onOpen;
socket.onclose = onClose;
socket.onmessage = onMessage;
socket.onerror = onError;

function sendMessage(message) {
    console.log('WebSocket is sending a message \'' + message + '\'');
    socket.send(JSON.stringify(
        {
            'message': message
        }
    ));
}

sendPingButton.onclick = function () {
    sendMessage('Ping');
};
sendPongButton.onclick = function () {
    sendMessage('Pong');
};