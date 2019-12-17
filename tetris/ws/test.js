let socket = new WebSocket("ws://localhost:9000");

let chan = document.getElementById('chan');
let connect = document.getElementById('connect');
let disconnect = document.getElementById('disconnect');
let send = document.getElementById('send');
let msg = document.getElementById('msg');

connect.addEventListener('click', function (){
  let obj = {
    type: 'connect',
    room_id : chan.value
  };
  socket.send(JSON.stringify(obj));
});

disconnect.addEventListener('click', function (){
  let obj = {
    type: 'disconnect',
  };
  socket.send(JSON.stringify(obj));
});

send.addEventListener('click', function(){
  let obj = {
    type: 'msg',
    room_id : chan.value,
    msg: msg.value
  };
  socket.send(JSON.stringify(obj));
});

function opened(event){
  console.log(event.type);
  console.log(event.data);
}

function closed(event){
  socket.send('close connection');
}

socket.onopen = opened;
socket.onmessage = opened;
socket.onclose = closed;
