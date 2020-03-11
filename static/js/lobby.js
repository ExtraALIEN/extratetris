import {removeControls} from './controls.js';
import {secondsToMinutes} from './timing.js';

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

function updatePlayers({player, pos}){
  let selector = `#field${pos} .announce .player-name`;
  let span = document.querySelector(selector);
  span.innerHTML = player;
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
  let selector = `#field${pos} .announce .player-name`;
  let span = document.querySelector(selector);
  span.innerHTML = "";
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
  let selector = `#field${pos} .announce .message`;
  document.querySelector(selector).innerHTML = 'Player disconnected';
}

function showGameover({pos, stats, mode, username}){
  let myField = document.querySelector('.tetris-view.current');
  if (myField && +pos === +myField.dataset.pos){
    removeControls();
  }
  let selector = `#field${pos} .result .player-name`;
  let userSpan = document.querySelector(selector);
  userSpan.innerHTML = username;
  const STATS_SELECTOR = {
    'result' : '.primary .main-value',
    'score' : '.scores .total',
    'score-intermediate-st' : '.scores .inter-st',
    'score-sec' : '.scores .sec',
    'score-piece' : '.scores .piece',
    'score-action' : '.scores .action',
    'score-dist' : '.scores .dist',
    'time' : '.time .overall',
    'time-climb' : '.time .climb',
    'time-lines' : '.time .lines',
    'time-acc' : '.time .acc',
    'time-drag' : '.time .drag',
    'lines' : '.lines .total',
    'lines-min' : '.lines .min',
    'pieces-line' : '.lines .pieces',
    'dist-line' : '.lines .dist',
    'pieces' : '.figures .total',
    'pieces-min' : '.figures .min',
    'actions-piece' : '.figures .act',
    'max-speed': '.other .speed',
    'distance': '.other .dist',
    'apm':'.other .apm',
  };
  let resultTable = document.querySelector(`#field${pos} .result`);
  for (let elem of [...resultTable.querySelectorAll('.val')]){
    if (!elem.innerHTML) {
      elem.innerHTML = '-';
    }
  }
  for (let x in stats){
    let cell = resultTable.querySelector(`${STATS_SELECTOR[x]} .val`);
    let val = stats[x];
    if (val === null){
      continue;
    }
    else if (cell.classList.contains('timing')){
      val = secondsToMinutes(val, cell.classList.contains('dec'));
    }
    else if (cell.parentElement.classList.contains('main-value') &&
            ['SU', 'LI', 'SA', 'DR', 'AC', 'HF'].indexOf(mode) !== -1){
      val = secondsToMinutes(val, mode !== 'SU');
    }
    else if (val %1 !== 0){
      val = val.toFixed(2);
    }
    cell.innerHTML = val;
  }

  resultTable.classList.add('finished');
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
