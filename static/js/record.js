import {secondsToMinutes} from './timing.js';

let selector = `.game-results .time`;
let cells = document.querySelectorAll(selector);
for (let x of [...cells]){
  x.innerHTML = secondsToMinutes(x.dataset.time, x.classList.contains('dec'));
}

console.log(d3);
