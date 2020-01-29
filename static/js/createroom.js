function sendInit(event){
  let starter = {
    'command' : 'init_room',
    'players' : document.getElementById('players').value,
    'game_type' : document.getElementById('game_type').value,
  }
  conn.send(JSON.stringify(starter));
}
let conn = new WebSocket('ws://localhost/ws/create/');

conn.onmessage = function(event){
  let data = JSON.parse(event.data);
  console.log(data);
  let type = data.type;

};

conn.onopen = function(event){
  console.log('websocket open');
};

conn.onerror = function(error){
  console.log('websocket error');
  console.log(error);
};

conn.onclose = function(event){
  console.log('websocket closed');
  console.log(event);
};

let btn = document.getElementById('create');
btn.addEventListener('click', sendInit);
