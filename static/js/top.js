import {secondsToMinutes} from './timing.js';

function replaceInt(elem){
  elem.innerHTML = parseInt(+elem.dataset.val);
}

function replaceTime(elem){
  elem.innerHTML = secondsToMinutes(+elem.dataset.val);
}

function replaceDecTime(elem){
  elem.innerHTML = secondsToMinutes(+elem.dataset.val, true);
}

function round2(elem){
  elem.innerHTML = (+elem.dataset.val).toFixed(2);
}

let ints = document.querySelectorAll('[data-int]');
for (let x of [...ints]){
  replaceInt(x);
}

let mode = document.querySelector('h2').dataset.mode;
console.log(mode);
let proc = replaceInt;
if (['survival_time'].includes(mode)){
  proc = replaceTime;
} else if (['time_acc', 'time_lines', 'time_drag', 'time_climb', 'hours'].includes(mode)){
  proc = replaceDecTime;
} else if (['speed'].includes(mode)){
  proc = round2;
}

for (let x of [...document.querySelectorAll('.result-rank[data-val]')]){
  if(mode === 'hours'){
    x.dataset.val = +x.dataset.val/60;
  }
  proc(x);
}
