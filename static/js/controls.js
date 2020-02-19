function activateControls(){
  document.body.addEventListener('keydown', controlField);
}

function removeControls(){
  document.body.removeEventListener('keydown', controlField);
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
    document.conn.send(JSON.stringify(msg));
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
}

export {activateControls, removeControls};
