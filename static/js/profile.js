import {TETRIS_VALUES, secondsToMinutes} from './utils.js';

let topics = document.querySelectorAll('[data-topic]');
for (let x of [...topics]){
  x.innerHTML = TETRIS_VALUES.typeStats[x.dataset.topic];
}

let stats = document.querySelectorAll('[data-stat]');
for (let x of [...stats]){
  x.innerHTML = TETRIS_VALUES.statsDescriptions[x.dataset.stat];
}

let timeSurvival = document.querySelectorAll('.time');
for (let x of timeSurvival){
  let val = x.innerHTML;
  if (val !== '-'){
    x.innerHTML = secondsToMinutes(val);
  }
}
