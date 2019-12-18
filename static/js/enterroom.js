function sendInitRoomSignal(){
  conn.onopen = function(){
    let number = document.getElementById('room-number').dataset.roomNumber;
    let type = document.getElementById('room-type').dataset.roomType;
    let players = document.getElementById('room-players').dataset.roomPlayers;
    conn.send(JSON.stringify({type: 'init',
                              room: {
                                  type: type,
                                  id: number,
                                  players: players,
                              }
                            })
              )
    };
  conn.onmessage = function(event){
    let data = JSON.parse(event.data);
    let type = data.type;
    if(type === 'player'){
       player = data.player;
       console.log(`player ${player}`);
    } else if (type === 'info'){
      console.log(data.msg);
    }
  };

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


let conn = new WebSocket('ws://localhost:9000');
conn.onerror = function(error){
  console.log('websocket error');
  console.log(error);
};

conn.onclose = function(){
  console.log('websocket closed');
};
let player;

sendInitRoomSignal();
fields = document.querySelectorAll('.tetris-field');
[...fields].forEach(a=> a.addEventListener('click', sendConnectToRoomSignal));
