import {removeControls} from './controls.js';
import {secondsToMinutes} from './utils.js';
import {playSound} from './sound.js';
import {TETRIS_VALUES} from './utils.js';


function activateConnectButtons(){
  function sendConnectToRoomSignal(){
    let number = document.getElementById('room-number').dataset.roomNumber;
    let pos = this.dataset.pos;
    document.conn.send(JSON.stringify({type: 'connect',
                              room_id: number,
                              pos: pos,
                              player: document.player
                            }));
  }

  function sendDisconnectSignal(){
    let number = document.getElementById('room-number').dataset.roomNumber;
    let pos = this.dataset.pos;
    document.conn.send(JSON.stringify({type: 'disconnect',
                              room_id: number,
                              pos: pos,
                          }));
  }

  let connectButtons = document.querySelectorAll('button[id^="connect"]');
  [...connectButtons].forEach(a=> a.addEventListener('click', sendConnectToRoomSignal));
  let diss = document.querySelectorAll('[id^="disconnect"]');
  [...diss].forEach(a=> a.addEventListener('click', sendDisconnectSignal));
}

function deactivateConnectButtons(x){
  let connectDiv = document.getElementById(`position${x}`);
  let disconnectButton = document.getElementById(`disconnect${x}`);
  connectDiv.remove();
  disconnectButton.remove();
  let botHandle = document.querySelector(`#field${x} .bot-handle`);
  if (botHandle){
    botHandle.remove();
  }
}

function connectPlayer({pos}){
  let div = document.getElementById(`position${pos}`);
  let dis = document.getElementById(`disconnect${pos}`);
  let myField = document.getElementById(`field${pos}`);
  div.classList.add('connected');
  dis.classList.add('connected');
  myField.classList.add('current');
  let fields = document.querySelectorAll(`[id^="field"]`);
  for (let x of [...fields]){
    if (+x.dataset.pos !== +pos){
      x.classList.add('inactive');
    }
  }
}

function updatePlayers({player, pos, rating}){
  let span = document.querySelector(`#field${pos} .announce .player-name`);
  span.innerHTML = player;
  let ratingSpan = document.querySelector(`#field${pos} .announce .player-rating`);
  if (ratingSpan){
    ratingSpan.innerHTML = rating;
  }
  let dash = document.querySelector(`#field${pos} .stats`);
  dash.classList.add('ready');
  let conPos = document.querySelector(`#position${pos}`);
  if (conPos){
    conPos.classList.add('connected');
  }
  if (/\* bot level \d{1,3} \*/.test(player)){
    let botHandle = document.querySelector(`#field${pos} .bot-handle`);
    if (botHandle){
      botHandle.classList.add('bot');
      conPos.classList.add('bot');
    }
  }
}

function disconnectPlayer({pos}){
  let span = document.querySelector(`#field${pos} .announce .player-name`);
  span.innerHTML = "";
  let ratingSpan = document.querySelector(`#field${pos} .announce .player-rating`);
  if (ratingSpan){
    ratingSpan.innerHTML = "";
  }
  let dash = document.querySelector(`#field${pos} .stats`);
  document.querySelector(`#position${pos}`).classList.remove('connected');
  dash.classList.remove('ready');
  let botDivs = document.querySelectorAll(`#field${pos} .bot`);
  for (let x of [...botDivs]){
    x.classList.remove('bot');
  }
  let myDis = document.querySelector('.current .connected[id^="disconnect"]');
  if (myDis){
    let myPos = +myDis.id.replace('disconnect', '');
    if (+pos == myPos){
      myDis.classList.remove('connected');
      document.querySelector('.current').classList.remove('current');
      let inactives = document.querySelectorAll('.inactive');
      for (let x of [...inactives]){
        x.classList.remove('inactive');
      }
    }
  }
}

function kickRoom(){
  fetch(window.location.origin)
          .then(res => res.text())
          .then(function(text) {
          document.body.innerHTML = text;
          info.innerHTML = showInfoBlock('room deleted by author');
          nodeScriptReplace(document.getElementsByTagName("body")[0]);
          }
        );
}

function showDisconnect({pos}){
  document.querySelector(`#field${pos} .announce .message`).innerHTML = 'Player disconnected';
}

function showGameover({pos, stats, mode, username, silent}){
  let myField = document.querySelector('.tetris-view.current');
  if (myField && +pos === +myField.dataset.pos){
    removeControls();
  }
  let userSpan = document.querySelector(`#field${pos} .result .player-name`);
  userSpan.innerHTML = username;
  let resultTable = document.querySelector(`#field${pos} .result`);
  for (let elem of [...resultTable.querySelectorAll('.val')]){
    if (!elem.innerHTML) {
      elem.innerHTML = '-';
    }
  }
  for (let x in stats){
    let cell = resultTable.querySelector(`${TETRIS_VALUES.statsSelector[x]} .val`);
    let val = stats[x];
    if (val === null){
      continue;
    }
    else if (cell.classList.contains('timing')){
      val = secondsToMinutes(val, cell.classList.contains('dec'));
    }
    else if (cell.parentElement.classList.contains('main-value') &&
            ['SU', 'LI', 'SA', 'DR', 'AC', 'HF'].includes(mode)){
      val = secondsToMinutes(val, mode !== 'SU');
    }
    else if (val %1 !== 0){
      val = val.toFixed(2);
    }
    cell.innerHTML = val;
  }

  resultTable.classList.add('finished');
  if (!silent){
    playSound({pos, file: 'gameover'});
  }
}

function fillPlaces({places}){
  for (let x in places){
    for (let pos of places[x]){
      let elem = document.querySelector(`#field${pos} .result-place`);
      elem.innerHTML = x;
    }
  }
}

export {activateConnectButtons, deactivateConnectButtons, connectPlayer, disconnectPlayer,
updatePlayers, kickRoom, showDisconnect, showGameover, fillPlaces};
