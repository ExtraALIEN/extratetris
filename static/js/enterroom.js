import {nodeScriptReplace} from './nodescript.js';
import {secondsToMinutes} from './utils.js';
import {activateConnectButtons, connectPlayer, disconnectPlayer, updatePlayers, kickRoom, showDisconnect,
showGameover, fillPlaces} from './lobby.js';
import {startTetris, renderTetris, updateTetris, refreshTetris, updateRoomLines,
updateGoals, updateFlag, updatePowerup, blind, removeBlind, showInfoBlock} from './render.js';
import {addBot, delBot} from './bot.js';
import {playSound} from './sound.js';

function initConnection(event){
  document.conn = conn;
  sendRoomNumber(event);
  activateConnectButtons();
}

function sendRoomNumber(event){
  let number = document.getElementById('room-number').dataset.roomNumber;
  document.roomNumber = number;
  conn.send(JSON.stringify({
    'type': 'init',
    'room_id': number
  }));
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

function copyURL(event){
  let textArea = document.createElement("textarea");
  textArea.value = event.target.dataset.url;
  textArea.style.color = 'transparent';
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  document.execCommand('copy');
  document.body.removeChild(textArea);
}

function formatTimeLimit(){
  let type = document.getElementById('room-type').dataset.roomType;
  if (type === 'CO'){
    let lim = document.getElementById('room-limit');
    lim.innerHTML = `Limit: ${secondsToMinutes(+lim.dataset.limit)}`;
  }
}

const MESSAGE_HANDLERS = {
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
  'powerup-sound': playSound,
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
  'update-players': ['player', 'pos', 'rating'],
  'disconnect-player': ['pos'],
  'room-deleted' : [],
  'start-game': [],
  'get-ready': [],
  'start-tetris': ['fields'],
  'watch-tetris': ['fields'],
  'update-tetris': ['pos', 'current_piece', 'speed', 'time', 'score', 'distance', 'lines', 'silent', 'rotate'],
  'refresh-tetris': ['new_piece', 'queue', 'surface'],
  'room-lines' : ['lines'],
  'goal' : ['goals'],
  'flag' : ['pos', 'y'],
  'powerup' : ['pos', 'num', 'powerup', 'time'],
  'powerup-sound': ['pos', 'file'],
  'blind' : ['pos', 'cols'],
  'remove-blind': ['pos', 'x'],
  'game-disconnect': ['pos'],
  'game-over' : ['pos', 'stats', 'mode', 'username', 'silent'],
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

function limitLevel(event){
  let field = event.target;
  let inp = field.value;
  if (inp === ''){
    field.value = 50;
  }
  if (field.value > 100){
    field.value = 100;
  }
  else if (field.value < 1) {
    field.value = 1;
  }
  field.value = (+field.value).toFixed(0);
}

let ready = false;
let copier = document.getElementById('copy-url');
copier.addEventListener('click', copyURL);
formatTimeLimit();
let buttonsAddBot = document.querySelectorAll('[id^="addbot"]');
for (let x of [...buttonsAddBot]){
  x.addEventListener('click', addBot);
}
let buttonsDelBot = document.querySelectorAll('[id^="delbot"]');
for (let x of [...buttonsDelBot]){
  x.addEventListener('click', delBot);
}
let botLevels = document.querySelectorAll('.bot-level input');
for (let x of [...botLevels]){
  x.addEventListener('change', limitLevel);
}
let conn = new WebSocket(`ws://${location.host}/ws/connect/`);



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
