import {playSound} from './sound.js';
import {randomNumberInRange} from './utils.js';

function activateControls(){
  document.body.addEventListener('keydown', controlField);
  activateSensorControls();
}

function removeControls(){
  document.body.removeEventListener('keydown', controlField);
  deactivateSensorControls();
}

function controlField(event, sensorData=''){
  let c = event.code;
  if (c){
    event.preventDefault();
  }
  if (sensorData !== ''){
    c = sensorData;
  }
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
    document.conn.send(JSON.stringify(msg));
  }
}

function sensorControlField(event){
  let elem = event.target;
  if (event.type === 'touchstart'){
    sendSensorCommand(elem);
    if (!elem.trackedTouch){
      elem.addEventListener('touchmove', detectLeave);
      elem.trackedTouch = true;
    }
  }
  else {
    elem.classList.remove('pressed');
    elem.removeEventListener('touchmove', detectLeave);
    elem.trackedTouch = false;
    clearTimeout(elem.timer);
    delete elem.timer;
  }
}

function detectLeave(event){
  let {pageX, pageY} = event.changedTouches[0];
  let currentElement = document.elementFromPoint(pageX, pageY);
  if (currentElement !== event.target){
    sensorControlField(event);
  }
}

function sendSensorCommand(elem){
  elem.classList.add('pressed');
  let sensorData = elem.dataset.command;
  if (elem.dataset.command === 'use') {
    let total = [...document.querySelectorAll('.tetris-view')].length;
    sensorData = `Numpad${Math.floor(randomNumberInRange(1,total+1))}`;
  }
  controlField({'code': null}, sensorData=sensorData);
  if(!elem.timer){
    elem.timer = setTimeout(function(){
      sendSensorCommand(elem);
    }, 400);
  } else {
    elem.timer = setTimeout(function(){
      sendSensorCommand(elem);
    }, 30);
  }
}


function activateSensorControls(){
  let sensorControls = document.querySelectorAll('.touchscreen-controls');
  for (let x of [...sensorControls]){
    x.addEventListener('touchstart', sensorControlField);
    x.addEventListener('touchend', sensorControlField);
  }
}

function deactivateSensorControls(){
  let sensorControls = document.querySelectorAll('.touchscreen-controls');
  for (let x of [...sensorControls]){
    x.removeEventListener('touchstart', sensorControlField);
    x.removeEventListener('touchend', sensorControlField);
  }
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
  playSound({pos: 0, file: 'select'});
}

export {activateControls, removeControls};
