import {startTetris, getReady, removeControls, updateTetris, refreshTetris, updatePowerup} from './gamecontrols.js';
import {nodeScriptReplace} from './nodescript.js';
import {secondsToMinutes} from './timing.js';

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

function showGameover(data){
  let STATS_SELECTOR = {
    'result' : '.primary .main-value',
    'score' : '.scores .total',
    'score-intermediate' : '.scores .intermediate',
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
  let resultTable = document.querySelector(`#field${data.pos} .result`);
  for (let elem of [...resultTable.querySelectorAll('.val')]){
    if (!elem.innerHTML) {
      elem.innerHTML = '-';
    }
  }
  for (let x in data.stats){
    let cell = resultTable.querySelector(`${STATS_SELECTOR[x]} .val`);
    let val = data.stats[x];
    if (val === null){
      continue;
    }
    else if (cell.classList.contains('timing')){
      val = secondsToMinutes(val, cell.classList.contains('dec'));
    }
    else if (cell.parentElement.classList.contains('main-value') &&
            ['SU', 'LI', 'SA', 'DR', 'AC'].indexOf(data.mode) !== -1){
      val = secondsToMinutes(val, data.mode !== 'SU');
    }
    else if (val %1 !== 0){
      val = val.toFixed(2);
    }
    cell.innerHTML = val;
  }

  resultTable.classList.add('finished');
}

function fillPlaces(places){
  for (let x in places){
    for (let pos of places[x]){
      console.log(pos,x);
      let elem = document.querySelector(`#field${pos} .result-place`);
      elem.innerHTML = x;
    }
  }
}


function showDisconnect(pos){
  let selector = `#field${pos} .announce .message`;
  console.log(selector);
  document.querySelector(selector).innerHTML = 'Player disconnected';
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
    let myField = document.getElementById('field'+pos);
    myField.classList.add('current');
  } else if (type === 'update-players'){
    let new_player = data.player;
    let pos = data.pos;
    let selector = `#field${pos} .announce .player-name`;
    let span = document.querySelector(selector);
    span.innerHTML = new_player;
    let conPos = document.querySelector(`#position${pos}`);
    if (conPos){
      conPos.classList.add('connected');
    }
  } else if (type === 'disconnect-player'){
    let pos = data.pos;
    let selector = `#position${pos} + .announce .player-name`;
    let span = document.querySelector(selector);
    span.innerHTML = "";
    let myDis = document.querySelector('.current .connected[id^="disconnect"]');
    let myPos = +myDis.id.replace('disconnect', '');
    if (+pos == myPos){
      myDis.classList.remove('connected');
      document.querySelector(`#position${pos}`).classList.remove('connected');
      document.querySelector('.current').classList.remove('current');
    }


  }else if (type === 'room-deleted'){
    console.log('room deleted');
    fetch(window.location.origin)
            .then(res => res.text())
            .then(function(text) {
              console.log('fetched');
            document.body.innerHTML = text;
            let info = document.getElementById('info')
            info.innerHTML = 'room deleted by author';
            info.classList.add('new-info');
            nodeScriptReplace(document.getElementsByTagName("body")[0]);
            }
            );


  } else if (type === 'start-game'){
    console.log('start game');
    console.log(window.location.href);
    fetch(window.location.href)
                   .then(res => res.text())
                   .then(function(text) {
                      if(!ready){
                        document.body.innerHTML = text;
                        nodeScriptReplace(document.getElementsByTagName("body")[0]);
                      }
                    });
  } else if (type === 'get-ready'){
    getReady(conn);
    ready = true;
  }
    else if (type === 'start-tetris') {
    startTetris(data.fields, conn);
  } else if (type === 'watch-tetris'){
    startTetris(data.fields);
  } else if (type === 'update-tetris'){
    updateTetris(data);
  } else if (type === 'refresh-tetris'){
    refreshTetris(data);
  } else if (type === 'game-over'){
    showGameover(data);
    let myField = document.querySelector('.tetris-view.current');
    console.log(myField);
    if (myField && +data.pos === +myField.dataset.pos){
      removeControls();
    }
    console.log(data);
  } else if (type === 'queue-update'){
    updateQueue(data);
  } else if(type === 'game-disconnect'){
    showDisconnect(data.pos);
  } else if (type ==='places'){
      fillPlaces(data.places);
  } else if (type === 'powerup'){
    updatePowerup(data);
  } else{
      console.log(data);
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
let ready = false;
let connectButtons = document.querySelectorAll('button[id^="connect"]');
[...connectButtons].forEach(a=> a.addEventListener('click', sendConnectToRoomSignal));
let diss = document.querySelectorAll('[id^="disconnect"]');
[...diss].forEach(a=> a.addEventListener('click', sendDisconnectSignal));
