function loadRoom(){
  // conn.onopen = function(){
  //   let number = document.getElementById('room-number').dataset.roomNumber;
  //   conn.send(JSON.stringify({type: 'load-room',
  //                             room_id: number
  //                           })
  //             )
  //   };


}

function sendConnectToRoomSignal(){
  let number = document.getElementById('room-number').dataset.roomNumber;
  let pos = this.dataset.pos;
  conn.send(JSON.stringify({type: 'connect',
                            room_id: number,
                            pos: pos,
                            player: player
                          }));
}


let conn = new WebSocket('ws://localhost/ws/connect/');

conn.onopen = function(event){
  let number = document.getElementById('room-number').dataset.roomNumber;
  conn.send(JSON.stringify({
    'type': 'init',
    'room_id': number
  }));
}


conn.onmessage = function(event){
  let data = JSON.parse(event.data);
  console.log(data);
  let type = data.type;
  if(type === 'player'){
     player = data.player;
     console.log(`player ${player}`);
  } else if (type === 'info'){
    console.log(data.msg);
    let info = document.getElementById('info')
    info.innerHTML = data.msg;
    info.classList.add('new-info');

  } else if (type === 'connected'){
    let pos = data.pos;
    let div = document.getElementById('position'+pos);
    div.classList.add('connected');
  } else if (type === 'update-players'){
    console.log('update');
    let new_player = data.player;
    let pos = data.pos;
    let selector = `#position${pos} .player-name`;
    let span = document.querySelector(selector);
    span.innerHTML = new_player;
  }

};

conn.onerror = function(error){
  console.log('websocket error');
  console.log(error);
};

conn.onclose = function(event){
  console.log('websocket closed');
  console.log(event);
};
let player;

//sendInitRoomSignal();
// loadRoom();
fields = document.querySelectorAll('.tetris-field');
[...fields].forEach(a=> a.addEventListener('click', sendConnectToRoomSignal));
