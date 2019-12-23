import {startFields, getReady} from './gamecontrols.js';

function nodeScriptReplace(node) {
        if ( nodeScriptIs(node) === true ) {
                node.parentNode.replaceChild( nodeScriptClone(node) , node );
        }
        else {
                var i        = 0;
                var children = node.childNodes;
                while ( i < children.length ) {
                        nodeScriptReplace( children[i++] );
                }
        }

        return node;
}
function nodeScriptIs(node) {
        return node.tagName === 'SCRIPT';
}
function nodeScriptClone(node){
        var script  = document.createElement("script");
        script.text = node.innerHTML;
        for( var i = node.attributes.length-1; i >= 0; i-- ) {
                script.setAttribute( node.attributes[i].name, node.attributes[i].value );
        }
        return script;
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


function sendDisconnectSignal(){
  let number = document.getElementById('room-number').dataset.roomNumber;
  let pos = this.dataset.pos;
  conn.send(JSON.stringify({type: 'disconnect',
                            room_id: number,
                            pos: pos,
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
  } else if (type === 'info'){
    console.log(data.msg);
    let info = document.getElementById('info')
    info.innerHTML = data.msg;
    info.classList.add('new-info');
  } else if (type === 'connected'){
    let pos = data.pos;
    let div = document.getElementById('position'+pos);
    div.classList.add('connected');
    let dis = document.getElementById('disconnect'+pos);
    dis.classList.add('connected');
  } else if (type === 'update-players'){
    let new_player = data.player;
    let pos = data.pos;
    let selector = `#position${pos} .player-name`;
    let span = document.querySelector(selector);
    span.innerHTML = new_player;
  } else if (type === 'disconnect-player'){
    let pos = data.pos;
    let selector = `#position${pos} .player-name`;
    let span = document.querySelector(selector);
    span.innerHTML = "";
    let dis = document.querySelector('.connected[id^="disconnect"]');
    let myField = document.querySelector('.connect.connected')
    if (myField && +pos === +myField.dataset.pos){
      myField.classList.remove('connected');
      dis.classList.remove('connected');
    }
  } else if (type === 'start-game'){
    console.log('start game');
    console.log(window.location.href);
    fetch(window.location.href)
                   .then(res => res.text())
                   .then(function(text) {
                      document.body.innerHTML = text;
                      nodeScriptReplace(document.getElementsByTagName("body")[0]);
                    });
  } else if (type === 'get-ready'){
    getReady(conn);
  }
    else if (type === 'start-tetris') {
    startFields(data.fields);
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

let connectButtons = document.querySelectorAll('button[id^="connect"]');
[...connectButtons].forEach(a=> a.addEventListener('click', sendConnectToRoomSignal));
let diss = document.querySelectorAll('[id^="disconnect"]');
[...diss].forEach(a=> a.addEventListener('click', sendDisconnectSignal));
