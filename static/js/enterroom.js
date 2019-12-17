function sendInitRoomSignal(){
  conn.onopen = function(){
    let number = document.getElementById('room-number').dataset.roomNumber;
    let type = document.getElementById('room-type').dataset.roomType;
    let players = document.getElementById('room-players').dataset.roomPlayers;
    conn.send(JSON.stringify({type: 'init',
                              room: {
                                  type: type,
                                  id: number,
                                  players: players
                              }
                            })
              )
    };
  conn.onmessage = function(event){
    console.log(event.data);
  }
}

function sendConnectToRoomSignal(){
  let number = document.getElementById('room-number').dataset.roomNumber;
  let pos = this.dataset.pos;
  conn.send(JSON.stringify({type: 'connect',
                            room_id: number,
                            pos: pos,

                          }));
}


let conn = new WebSocket('ws://localhost:9000');

let player;
sendInitRoomSignal();
fields = document.querySelectorAll('.tetris-field');
[...fields].forEach(a=> a.addEventListener('click', sendConnectToRoomSignal));
