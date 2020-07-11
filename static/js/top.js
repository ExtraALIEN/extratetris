import {secondsToMinutes, secondsToHours} from './utils.js';

function replaceInt(elem){
  elem.innerHTML = parseInt(+elem.dataset.val);
}

function replaceHours(elem){
  elem.innerHTML = secondsToHours(+elem.dataset.val);
}

function replaceTime(dec=false){
  return function(elem){
    elem.innerHTML = secondsToMinutes(+elem.dataset.val, dec);
  }
}

function round2(elem){
  elem.innerHTML = (+elem.dataset.val).toFixed(2);
}

let ints = document.querySelectorAll('[data-int]');
for (let x of [...ints]){
  replaceInt(x);
}

let mode = document.querySelector('h2').dataset.mode;
let proc = replaceInt;
if(mode === 'hours'){
  proc = replaceHours;
} else if (['survival_time'].includes(mode)){
  proc = replaceTime();
} else if (['time_acc', 'time_lines', 'time_drag', 'time_climb', 'hours'].includes(mode)){
  proc = replaceTime(true);
} else if (['speed'].includes(mode)){
  proc = round2;
}

for (let x of [...document.querySelectorAll('.result-rank[data-val]')]){
  proc(x);
}
