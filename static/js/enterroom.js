import {nodeScriptReplace} from './nodescript.js';
import {showInfoBlock} from './info.js';
import {activateConnectButtons, connectPlayer, disconnectPlayer, updatePlayers, kickRoom, showDisconnect,
showGameover, fillPlaces} from './lobby.js';
import {startTetris, renderTetris, updateTetris, refreshTetris, updateRoomLines,
updateGoals, updateFlag, updatePowerup, blind, removeBlind} from './render.js';


function initConnection(event){
  document.conn = conn;
  sendRoomNumber(event);
  activateConnectButtons();
}


function sendRoomNumber(event){
  let number = document.getElementById('room-number').dataset.roomNumber;
  conn.send(JSON.stringify({
    'type': 'init',
    'room_id': number
  }));
}

function setPlayer({name}){
  document.player = name;
}

function prepareToGame(){
  fetch(window.location.href)
       .then(res => res.text())
       .then(function(text) {
          if(!ready){
            document.body.innerHTML = text;
            nodeScriptReplace(document.getElementsByTagName("body")[0]);
          }
        });
}

function getReady(){
  ready = true;
  conn.send(JSON.stringify({'type': 'ready'}));
}

let MESSAGE_HANDLERS = {
  'player' : setPlayer,
  'info' : showInfoBlock,
  'connected': connectPlayer,
  'update-players' : updatePlayers,
  'disconnect-player' : disconnectPlayer,
  'room-deleted' : kickRoom,
  'start-game' : prepareToGame,
  'get-ready' : getReady,
  'start-tetris': startTetris,
  'watch-tetris': renderTetris,
  'update-tetris' : updateTetris,
  'refresh-tetris' : refreshTetris,
  'room-lines' : updateRoomLines,
  'goal' : updateGoals,
  'flag' : updateFlag,
  'powerup' : updatePowerup,
  'blind' : blind,
  'remove-blind': removeBlind,
  'game-disconnect': showDisconnect,
  'game-over' : showGameover,
  'places' : fillPlaces
};

const HANDLER_PARAMS = {
  'player' : ['player'],
  'info' : ['msg'],
  'connected' : ['pos'],
  'update-players': ['player', 'pos'],
  'disconnect-player': ['pos'],
  'room-deleted' : [],
  'start-game': [],
  'get-ready': [],
  'start-tetris': ['fields'],
  'watch-tetris': ['fields'],
  'update-tetris': ['pos', 'current_piece', 'speed', 'time', 'score', 'distance', 'lines'],
  'refresh-tetris': ['new_piece', 'queue', 'surface'],
  'room-lines' : ['lines'],
  'goal' : ['goals'],
  'flag' : ['pos', 'y'],
  'powerup' : ['pos', 'num', 'powerup', 'time'],
  'blind' : ['pos', 'cols'],
  'remove-blind': ['pos', 'x'],
  'game-disconnect': ['pos'],
  'game-over' : ['pos', 'stats', 'mode'],
  'places' : ['places']
};

function processMessage(event){
  let data = JSON.parse(event.data);
  let type = data.type;
  let params = {};
  for (let x of HANDLER_PARAMS[data.type]){
    params[x] = data[x];
  }
  MESSAGE_HANDLERS[data.type](params);
}

let ready = false;
let conn = new WebSocket('ws://localhost/ws/connect/');

conn.onopen = initConnection;

conn.onerror = function(error){
  console.log('websocket error');
  console.log(error);
};

conn.onclose = function(event){
  console.log('websocket closed');
  console.log(event);
};

conn.onmessage = processMessage;
