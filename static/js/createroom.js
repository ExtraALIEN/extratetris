import {secondsToMinutes} from './timing.js';

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
  short.innerHTML = type;
  text.innerHTML = DESCRIPTIONS[type];
}

function displayVolume(type){
  if (type in STANDARD_VOLUME){
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
  let total = (STANDARD_VOLUME[type]/100) * proc;
  if (type === 'CO'){
    total = secondsToMinutes(total);
  }
  else{
    total = parseInt(total);
  }
  vol.querySelector('p').innerHTML = `${MEASURE[type]}: ${total}`;
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

const STANDARD_VOLUME = {
  'LI' : 60,
  'CO' : 360,
  'SA' : 20000,
  'DR' : 4020,
  'AC' : 100,
};

const MEASURE = {
  'LI' : 'Линии',
  'CO' : 'Время',
  'SA' : 'Очки',
  'DR' : 'Пробег',
  'AC' : 'Скорость',
};

let conn = new WebSocket('ws://localhost/ws/create/');

conn.onmessage = function(event){
  let data = JSON.parse(event.data);
  console.log(data);
  let type = data.type;

};

conn.onopen = function(event){
  console.log('websocket open');
};

conn.onerror = function(error){
  console.log('websocket error');
  console.log(error);
};

conn.onclose = function(event){
  console.log('websocket closed');
  console.log(event);
};

const DESCRIPTIONS = {
  'CL' : 'Стандартный вариант игры в Тетрис. \
          Чтобы расчистить место для следующих фигур, нужно составлять полные линии, \
          после чего они уничтожаются. \
          Побеждает игрок, набравший больше всех очков.',
  'DM' : 'Битва. Расширенный вариант по сравнению со стандартным. \
          На поле могут появляться различные бонусы, которые можно собирать и использовать, \
          чтобы облегчать игру себе и осложнять соперникам. \
          Побеждает игрок, набравший больше всех очков. ',
  'SU' : 'Выживание. Побеждает игрок, продержавшийся в игре дольше всех по времени.',
  'LI' : 'Линии. Побеждает игрок, быстрее всех уничтожвиший заданное количество линий.',
  'CO' : 'Ограниченное время. Каждому дается одинаковое количество времени, по истечении которого \
          игра заканчивается, независимо от обстановки на поле. Побеждает игрок, набравший больше \
          всех очков за отведенное время.',
  'SA' : 'Скоростное покорение вершины. Необходимо как можно быстрее набрать определенное \
          количество очков, после чего игра заканчивается, независимо от обстановки на поле. \
          Побеждает игрок, набравший установленные очки быстрее всех.',
  'DR' : 'Заезд на определенную дистанцию. Необходимо как можно быстрее набрать определенный \
          пробег, после чего игра заканчивается, независимо от обстановки на поле. \
          Побеждает игрок, проехавший дистанцию быстрее всех.',
  'AC' : 'Максимальное ускорение. Необходимо как можно быстрее развить определенную скорость, \
          после чего игра заканчивается, независимо от обстановки на поле. Побеждает игрок, \
          достигший установленной скорости быстрее всех.',
  'CF' : 'Захват флага. Задача - взять флаг и принести его на свою базу. \
          Изначально флаг находится на определенной высоте. Чтобы его взять, нужно первым среди всех игроков \
          составить линию на высоте флага. После взятия, чтобы принести флаг на свою базу, \
          надо постепенно уничтожать линии до самого низа, после чего засчитывается очко, \
          новый флаг образуется на изначальной высоте. Соперники могут перехватить флаг, сжигая линии выше \
          чем он находится у игрока, который взял флаг и несет его на базу. \
          Побеждает игрок, захвативший флаг на базу наибольшее количество раз.',
  'HF' : 'Удержание флага. Необходимо захватить и продержать флаг у себя наибольшее время \
          по сравнению с остальными. Флаг образуется и перемещается по тем же правилам, \
          что и в режиме захвата флага. Каждому игроку засчитывается время удержания флага \
          с того момента, как он взял либо перехватил флаг. Приносить флаг на базу не обязательно. \
          В случае если игрок все же принес флаг на базу, образуется новый флаг на изначальной высоте, \
          при этом считается что его удерживает тот же игрок, до тех пор пока флаг \
          не будет взят или перехвачен другим игроком. Побеждает игрок, продержавший флаг дольше всех.',
  'RA' : 'Ралли. Задача игроков - пройти трассу при максимальном соответствии с заданным маршрутом. \
          Учитывается общее количество линий, уничтоженных в игре всеми игроками. \
          Маршрутные очки присуждаются либо отнимаются за уничтожение определенных линий. \
          За уничтожение каждой пятой линии в игре, дается +2 маршрутных очка. \
          За уничтожение каждой 10, 25, 100 линии даются дополнительные маршрутные очки.\
          Начиная с 11 линии, за уничтожение следующей линии после каждой пятой \
          (за линии 11, 16, 21, 26...), снимается -1 маршрутное очко. \
          За линии стоящими непосредственно перед каждой пятой, начиная с 14 линии (14, 19, 24...) \
          тоже снимается -1 маршрутное очко. За линии, стоящие перед каждой 10, 25, 100 линией, \
          снимаются дополнительные маршрутные очки. Побеждает игрок, набравший больше всех маршрутных очков.'


}

let btn = document.getElementById('create');
btn.addEventListener('click', sendInit);
let inputs = document.querySelectorAll('input');
let typeButtons = document.querySelectorAll('input[name="game_type"]');
let desc = document.getElementById('game-description');
let short = desc.querySelector('.short');
let text = desc.querySelector('.text');
let vol = document.querySelector('.vol');
vol.querySelector('input').addEventListener('input', calculateVolume);
for (let x of [...typeButtons]){
  x.addEventListener('change', changeGameType);
}
for (let x of [...inputs]){
  x.addEventListener('change', checkFilled);
}
let ranked = document.getElementById('id_ranked');
let crazy = document.getElementById('id_crazy');
crazy.addEventListener('change', checkCrazy);
checkFilled();
displayVolume(document.querySelector('[name="game_type"]:checked').value);
