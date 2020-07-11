import {TETRIS_VALUES, secondsToMinutes} from './utils.js';

function sendInit(event){
  let starter = {
    'command' : 'init_room',
    'players' : document.querySelector('[name="players"]:checked').value,
    'game_type' : document.querySelector('[name="game_type"]:checked').value,
    'volume': document.querySelector('.vol input').value,
    'ranked': document.querySelector('#id_ranked').checked,
    'crazy': crazy.checked,
  }
  conn.send(JSON.stringify(starter));
}

function changeGameType(event){
  let type = event.target.value;
  showDescription(type);
  displayVolume(type);
}

function showDescription(type){
  document.querySelector('.short').innerHTML = type;
  document.querySelector('.text').innerHTML = `<div style="white-space:pre-wrap">${TETRIS_VALUES.descriptions[type]}</div>`;
}

function displayVolume(type){
  if (type in TETRIS_VALUES.standardVolume){
    vol.classList.remove('inactive');
    calculateVolume();
  }else{
    vol.classList.add('inactive');
    vol.querySelector('p').innerHTML = '';
  }
}

function calculateVolume(){
  let type = document.querySelector('[name="game_type"]:checked').value;
  let proc = vol.querySelector('input').value;
  if (proc > 250){
    proc = 250;
  }else if(proc < 25){
    proc = 25;
  }
  let total = (TETRIS_VALUES.standardVolume[type]/100) * proc;
  if (type === 'CO'){
    total = secondsToMinutes(total);
  }
  else{
    total = parseInt(total);
  }
  vol.querySelector('p').innerHTML = `${TETRIS_VALUES.measure[type]}: ${total}`;
}

function checkFilled(event){
  if (document.querySelector('[name="players"]:checked') &&
      document.querySelector('[name="game_type"]:checked') ){
        btn.classList.add('filled');
      }
  if (document.getElementById('id_players_0').checked){
    removeRanked();
  } else {
    showRanked();
  }
  if (document.getElementById('id_game_type_0').checked){
    removeCrazy();
  } else {
    showCrazy();
  }
}

function removeRanked(){
  ranked.checked = false;
  ranked.parentElement.style.display = 'none';
}

function showRanked(){
  ranked.parentElement.style.display = 'block';
  checkRanked();
}

function checkRanked(event){
  if (ranked.checked){
    vol.querySelector('input').value = 100;
    displayVolume(document.querySelector('[name="game_type"]:checked').value);
    removeCrazy();
  }
}

function removeCrazy(){
  crazy.checked = false;
  crazy.parentElement.style.display = 'none';
}

function showCrazy(){
  crazy.parentElement.style.display = 'block';
  checkCrazy();
  checkRanked();
}

function checkCrazy(event){
  if(crazy.checked){
    removeRanked();
  }
}

let conn = new WebSocket('ws://localhost/ws/create/');

conn.onmessage = function(event){
};

conn.onopen = function(event){
};

conn.onerror = function(error){
  console.log('websocket error');
  console.log(error);
};

conn.onclose = function(event){
};

let btn = document.getElementById('create');
btn.addEventListener('click', sendInit);
let inputs = document.querySelectorAll('input');
for (let x of [...inputs]){
  x.addEventListener('change', checkFilled);
}
let typeButtons = document.querySelectorAll('input[name="game_type"]');
for (let x of [...typeButtons]){
  x.addEventListener('change', changeGameType);
}
let vol = document.querySelector('.vol');
vol.querySelector('input').addEventListener('input', calculateVolume);
let ranked = document.getElementById('id_ranked');
let crazy = document.getElementById('id_crazy');
crazy.addEventListener('change', checkCrazy);
checkFilled();
displayVolume(document.querySelector('[name="game_type"]:checked').value);
