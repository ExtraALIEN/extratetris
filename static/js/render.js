import {activateControls} from './controls.js';
import {deactivateConnectButtons} from './lobby.js';
import {addLeadingZeroes, secondsToMinutes} from './utils.js';
import {playSound} from './sound.js';

function startTetris({fields}){
  activateControls();
  renderTetris({fields});
}

function renderTetris({fields}){
  for(let x in fields){
    deactivateConnectButtons(x);
    let data = fields[x];
    let fieldElem = document.getElementById(`field${x}`);
    if (fieldElem.classList.contains('current')){
      fieldElem.querySelector('.powerups .place').classList.add('active');
    }
    let surface = data.surface;
    let new_piece = data.active_piece;
    let queue = data.queue;
    refreshSurface({surface});
    refreshActivePiece({new_piece}, true);
    refreshQueue({queue});
    let pos = x;
    let {score, lines, speed, distance, time} = data;
    updateScore({pos, score});
    updateLines({pos, lines});
    updateSpeed({pos, speed});
    updateDistance({pos, distance});
    updateTime({pos, time});

  }
}

function updateTetris({pos, current_piece, speed, time, score, distance, lines, silent, rotate}){
  if(current_piece){
    updateCurrentPiece({pos, current_piece});
  }
  if (score){
    updateScore({pos, score});
  }
  if (lines){
    updateLines({pos, lines});
    playSound({pos, file: 'line'});
  }
  if (speed){
    updateSpeed({pos, speed});
  }
  if (distance){
    updateDistance({pos, distance});
  }
  if (time){
    updateTime({pos, time});
  }
  if (!silent){
    if(rotate){
      playSound({pos, file: 'rotate'});
    }
    else {
      let currentSpeed = +document.querySelector(`#field${pos} .stats .speed .val`).innerHTML;
      playSound({pos, file : 'move', speed: currentSpeed});
    }
  }
}

function updateScore({pos, score}){
  document.querySelector(`#field${pos} .stats .score .val`).innerHTML = `${addLeadingZeroes(score, 7)}`;
}

function updateLines({pos, lines}){
  document.querySelector(`#field${pos} .stats .lines .val`).innerHTML = `${addLeadingZeroes(lines, 3)}`;
}

function updateSpeed({pos, speed}){
  speed = speed.toFixed(1);
  let deg = ((360/320) * speed).toFixed(0);
  let arrow = document.querySelector(`#field${pos} .arrow`);
  arrow.style.transform = `rotate(${deg}deg)`;
  document.querySelector(`#field${pos} .stats .speed .val`).innerHTML = speed - speed % 1;
}

function updateDistance({pos, distance}){
  distance = `${addLeadingZeroes(distance, 7)}`;
  let d = distance.slice(-1);
  distance = distance.slice(0,-1);
  document.querySelector(`#field${pos} .stats .distance .last`).innerHTML = d;
  document.querySelector(`#field${pos} .stats .distance .val`).innerHTML = distance;
}

function updateTime({pos, time}){
  document.querySelector(`#field${pos} .stats .time .val`).innerHTML = secondsToMinutes(time);
}

function updateRoomLines({lines}){
  for (let x of [...document.querySelectorAll('.room-lines')]){
    x.classList.add('visible');
    x.innerHTML = `${addLeadingZeroes(lines, 3)}`;
  }
}

function updateGoals({goals}){
  let myField = document.querySelector('.tetris-view.current');
  for (let x in goals){
    let res = goals[x];
    let elem = document.querySelector(`#field${x} .goals`);
    let prev = +elem.innerHTML;
    elem.innerHTML = res;
    if (myField && +x === +myField.dataset.pos && res !== prev){
      playSound({pos: x, file: 'goal', speed: (res-prev-2)*100});
    }
  }
}

function updateCurrentPiece({pos, current_piece}){
  for (let y in current_piece){
    for(let x in current_piece[y]){
        let cell = document.querySelector(`#field${pos} > .row[data-y="${y}"] .cell[data-x="${x}"]`);
        let total = +current_piece[y][x];
        updateCell(cell, total);
    }
  }
}

function updateCell(cell, total){
  let color = total % 100;
  let powerup = (total - color) / 100;
  let newClass = `color-${color}`;
  setColor(cell,newClass);
  if (powerup){
    showPowerup(cell, powerup);
  }
}

function updateFlag({pos, y}){
  let flagElement = document.querySelector(`#field${pos} .flag`);
  if (flagElement){
    flagElement.classList.remove('flag');
  }
  document.querySelector(`#field${pos} .row[data-y="${y}"]`).classList.add('flag');
  let myField = document.querySelector('.tetris-view.current');
  if (myField && +pos === +myField.dataset.pos && +myField.querySelector(`.stats .speed .val`).innerHTML > 0 && !myField.querySelector('.result.finished')){
    playSound({pos, file: 'flag', speed: (5-y)*100});
  }
}

function refreshTetris({new_piece, queue, surface}){
  if (surface){
    refreshSurface({surface});
  }
  if (new_piece){
    refreshActivePiece({new_piece});
  }
  if (queue){
    refreshQueue({queue});
  }
}

function updatePowerup({pos, num, powerup, time}){
  let place = document.querySelector(`#field${pos} .powerups .place[data-pos="${num}"]`);
  if (powerup){
    place.classList.add(`powerup-${powerup}`);
  } else if (time) {
    for (let x of [...place.classList]){
      if (x.startsWith('time-')){
        place.classList.remove(x);
      }
    }
    place.classList.add(`time-${time}`);
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

function refreshSurface({surface}){
  let pos = surface.pos;
  let field = document.getElementById(`field${pos}`);
  for(let y in surface){
    if(y !== 'pos'){
      for (let x in surface[y]){
        let cell = field.querySelector(`.row[data-y="${y}"] .cell[data-x="${x}"]`);
        let total = +surface[y][x];
        updateCell(cell, total);
      }
    }
  }
}

function refreshQueue({queue}){
  let pos = queue.pos;
  let qElem = document.querySelector(`#field${pos} .queue`);
  for(let i in queue){
    if (i!== 'pos'){
      [...qElem.querySelectorAll(`[id="queue${i}"] .cell`)].forEach(a=> setColor(a, 'color-0'));
      for(let y in queue[i]){
        for(let x in queue[i][y]){
          let cell = qElem.querySelector(`[id="queue${i}"] .queue-row[data-y="${y}"] .cell[data-x="${x}"]`);
          let cl = queue[i][y][x];
          setColor(cell, `color-${cl>0? 10:0}`);
        }
      }
    }
  }
}

function refreshActivePiece({new_piece}, silent=false){
  let pos = new_piece.pos;
  for (let y in new_piece){
    if(y !== 'pos'){
      for (let x in new_piece[y]){
        if (new_piece[y][x] > 0){
          let cell = document.querySelector(`#field${pos} > .row[data-y="${y}"] .cell[data-x="${x}"]`);
          let total = +new_piece[y][x];
          updateCell(cell, total);
        }
      }
    }
  }
  if(!silent){
    playSound({pos, file: 'land'});
  }
}

function blind({pos, cols}){
  let field = document.querySelector(`#field${pos}`);
  if (cols){
    for (let x of cols){
      for (let elem of field.querySelectorAll(`.row .cell[data-x="${x}"]`)){
        elem.classList.add('blind');
      }
    }
  }
  else{
    let queue = field.querySelector('.queue');
    queue.classList.add('blind');
  }
}

function removeBlind({pos, x}){
  let field = document.querySelector(`#field${pos}`);
  if (x !== undefined){
    for (let elem of [...field.querySelectorAll(`.row .cell[data-x="${x}"]`)]){
      elem.classList.remove('blind');
    }
  } else {
      let queue = field.querySelector('.queue');
    queue.classList.remove('blind');
  }
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

function showInfoBlock({msg}){
  let info = document.getElementById('info');
  info.innerHTML = msg;
  info.classList.add('js-new-info');
}

export {startTetris, renderTetris, updateTetris, refreshTetris, updateRoomLines,
updateGoals, updateFlag, updatePowerup, blind, removeBlind, showInfoBlock}
