import {secondsToMinutes} from './timing.js';

function startTetris(fields, conn){
  for(let x in fields){
    deactivateConnectButtons(x);
    if(conn){
      activateControls(conn);
    }
    let data = fields[x];
    let fieldElem = document.getElementById(`field${x}`);
    if (fieldElem.classList.contains('current')){
      fieldElem.querySelector('.powerups .place').classList.add('active');
    }
    refreshSurface(data.surface);
    refreshActivePiece(data.active_piece);
    refreshQueue(data.queue);
    for (let s of ['score', 'lines', 'speed', 'distance', 'time']){
      {
        updateStats(x, s, data[s]);
      }
    }
  }
}


function deactivateConnectButtons(x){
  let connectDiv = document.getElementById(`position${x}`);
  let disconnectButton = document.getElementById(`disconnect${x}`);
  connectDiv.remove();
  disconnectButton.remove();
}

function activateControls(conn){
  document.body.conn = conn;
  document.body.addEventListener('keydown', controlField);
}

function removeControls(){
  document.body.removeEventListener('keydown', controlField);
  console.log('control removed');
}

function changePowerup(next){
  let activePowerup = document.querySelector('.current .powerups .active');
  let num = +activePowerup.dataset.pos;
  let newNum;
  activePowerup.classList.remove('active');
  if(next){
    newNum = num < 3 ? num + 1 : 1;
  }
  else{
    newNum = num > 1 ? num - 1 : 3;
  }
  document.querySelector(`.current .powerups .place[data-pos="${newNum}"]`).classList.add('active');
}


function updatePowerup(data){
  let selector = `#field${data.pos} .powerups .place[data-pos="${data.num}"]`;
  let place = document.querySelector(selector);
  if (data.powerup){
    place.classList.add(`powerup-${data.powerup}`);

  } else if (data.time){
    for (let x of [...place.classList]){
      if (x.startsWith('time-')){
        place.classList.remove(x);
      }
    }
    place.classList.add(`time-${data.time}`);
  } else {
    for (let x of [...place.classList]){
      if (x.startsWith('time-')){
        place.classList.remove(x);
      }
      else if (x.startsWith('powerup-')){
        place.classList.remove(x);
      }
    }
    place.classList.add(`time-00`);
  }
}

function controlField(event){
  let c = event.code;
  let msg = {'type': 'control'};
  if(c === 'KeyA' || c === 'ArrowLeft'){
    msg.command = 'move_left';
  }
  else if(c === 'KeyD' || c === 'ArrowRight'){
    msg.command = 'move_right';
  }else if(c === 'KeyS' || c === 'ArrowDown'){
    msg.command = 'move_down';
  }else if(c === 'KeyW' || c === 'ArrowUp'){
    msg.command = 'rotate';
  } else if (c === 'Numpad0' || c === 'KeyQ'){
    changePowerup(false);
  } else if (c === 'KeyE' || c === 'NumpadDecimal'){
    changePowerup(true);
  } else if (c === 'Digit1' || c === 'Numpad1'){
    msg.command = 'use_powerup';
    msg.place = document.querySelector('.powerups .active').dataset.pos;
    msg.target_field = 1;
  } else if (c === 'Digit2' || c === 'Numpad2'){
    msg.command = 'use_powerup';
    msg.place = document.querySelector('.powerups .active').dataset.pos;
    msg.target_field = 2;
  } else if (c === 'Digit3' || c === 'Numpad3'){
    msg.command = 'use_powerup';
    msg.place = document.querySelector('.powerups .active').dataset.pos;
    msg.target_field = 3;
  } else if (c === 'Digit4' || c === 'Numpad4'){
    msg.command = 'use_powerup';
    msg.place = document.querySelector('.powerups .active').dataset.pos;
    msg.target_field = 4;
  }
  if (msg.command){
    event.target.conn.send(JSON.stringify(msg));
  }
}



function getReady(conn){
  console.log('get ready signal received');
  conn.send(JSON.stringify({'type': 'ready'}))
}

function blind(data){
  console.log('blind', data)
  let field = document.querySelector(`#field${data.pos}`);
  console.log(field);
  if (data.cols){
    for (let x of data.cols){
      let selector = `.row .cell[data-x="${x}"]`;
      for (let elem of field.querySelectorAll(selector)){
        elem.classList.add('blind');

      }
    }
  }
  else{
    let queue = field.querySelector('.queue');
    queue.classList.add('blind');
  }
}

function removeBlind(data){
  let field = document.querySelector(`#field${data.pos}`);
  if (data.x !== undefined){
    for (let elem of [...field.querySelectorAll(`.row .cell[data-x="${data.x}"]`)]){
      elem.classList.remove('blind');
    }
  } else {
      let queue = field.querySelector('.queue');
    queue.classList.remove('blind');
  }
}


function refreshSurface(data){
    let pos = data.pos;
    let field = document.getElementById(`field${pos}`);
    for(let y in data){
      if(y !== 'pos'){
        for (let x in data[y]){
          let selector = `.row[data-y="${y}"] .cell[data-x="${x}"]`;
          let cell = field.querySelector(selector);
          let total = +data[y][x];
          let color = total % 100;
          let powerup = (total - color) / 100;
          let newColor = `color-${color}`;
          setColor(cell,newColor);
          if (powerup){
            showPowerup(cell, powerup);
          }

        }
      }
    }
}

function refreshQueue(data){
  let pos = data.pos;
  let qElem = document.querySelector(`#field${pos} .queue`);
  for(let i in data){
    if (i!== 'pos'){
      [...qElem.querySelectorAll(`[id="queue${i}"] .cell`)].forEach(a=> setColor(a, 'color-0'));
      for(let y in data[i]){
        for(let x in data[i][y]){
          let selector = `[id="queue${i}"] .queue-row[data-y="${y}"] .cell[data-x="${x}"]`;
          let cell = qElem.querySelector(selector);
          let cl = data[i][y][x];
          setColor(cell, `color-${cl>0? 10:0}`);
        }
      }
    }
  }
}

function refreshActivePiece(data){
  let pos = data.pos;
  for (let y in data){
    if(y !== 'pos'){
      for (let x in data[y]){
        if (data[y][x] > 0){
          let selector = `#field${pos} > .row[data-y="${y}"] .cell[data-x="${x}"]`;
          let cell = document.querySelector(selector);
          let total = +data[y][x];
          let color = total % 100;
          let powerup = (total - color) / 100;
          let newColor = `color-${color}`;
          setColor(cell,newColor);
          if (powerup){
            showPowerup(cell, powerup);
          }
        }
      }
    }
  }
}

function updateTetris(data){
  let pos = data.pos;
  if(data.current_piece){
    updateCurrentPiece(pos, data.current_piece);
  }
  for (let x of ['score', 'lines', 'speed', 'distance', 'time']){
    if(data[x]){
      updateStats(pos, x, data[x]);
    }
  }

}

function refreshTetris(data){

    if (data.surface){
      refreshSurface(data.surface);
    }
    if (data.new_piece){
      refreshActivePiece(data.new_piece);
    }
    if (data.queue){
      refreshQueue(data.queue);
    }

}

function updateCurrentPiece(pos, data){
  for (let y in data){
    for(let x in data[y]){
        let selector = `#field${pos} > .row[data-y="${y}"] .cell[data-x="${x}"]`;
        let cell = document.querySelector(selector);
        let total = +data[y][x];
        let color = total % 100;
        let powerup = (total - color) / 100;
        let newClass = `color-${color}`;
        setColor(cell,newClass);
        if (powerup){
          showPowerup(cell, powerup);
        }

    }
  }
}

function updateStats(pos, type, value){
  let selector = `#field${pos} .stats .${type} .val`;
  if (type === 'time'){
    value = secondsToMinutes(value);
  }
  else if (value%1 != 0){
    value = value.toFixed(1);
  }
  document.querySelector(selector).innerHTML = value;
}

function setColor(elem, newColor){
  if(elem) {
    for (let x of [...elem.classList]){
      if (x.startsWith('color-')){
        elem.classList.remove(x);
      }
      if (x.startsWith('powerup-')){
        elem.classList.remove(x);
      }
    }
    elem.classList.add(newColor);
  }
}

function showPowerup(cell, powerup){
  cell.classList.add(`powerup-${powerup}`);
}



export {startTetris, getReady,  removeControls, updateTetris, refreshTetris, updatePowerup, blind, removeBlind};
