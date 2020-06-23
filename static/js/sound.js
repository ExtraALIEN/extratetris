import {randomNumberInRange} from './utils.js';

const ALL_SOUNDS = ['move', 'rotate', 'land', 'line', 'gameover', 'select',
            'chance_up',
            'chance_down',
            'speed_up',
            'speed_down',
            'line_add_1',
            'line_add_2',
            'line_add_3',
            'line_remove_1',
            'line_remove_2',
            'line_remove_3',
            'copy_figure',
            'duration_up',
            'duration_down',
            'thunder',
            'shield',
            'bomb',
            'trash',
            'blind',
            'blind_queue',
            'drink',
            'weak_signal',
            'flag',
            'goal'];
const UNC_SOUNDS = ['move', 'rotate', 'select'];
let ctx = new AudioContext();

function createSoundSources(){
  vol['main'] = ctx.createGain();
  vol['main'].connect(ctx.destination);
  let fields = document.querySelectorAll('[id^="field"]');
  for(let x of fields){
    let pos = +x.dataset.pos;
    uncontinousSound[pos] = null;
    let gainNode = ctx.createGain();
    gainNode.gain.value = pos === 0 ? 1 : 0.333;
    gainNode.connect(vol['main']);
    vol[pos] = gainNode;
  }
}


function loadSounds(){
  let bank = {};
  //let tempCtx = new OfflineAudioContext();

  for (let x of ALL_SOUNDS){
    fetch(`/static/sound/${x}.ogg`)
      .then(response => response.arrayBuffer())
      .then(arrayBuffer => ctx.decodeAudioData(arrayBuffer))
      .then(buffer => {
          // console.log(buffer);
          bank[x] = buffer;
          return null;
        });
  }

  return bank;
}

function playSound({pos, file, speed=0}){
  //console.log('playSound', ctx.getOutputTimestamp());
  let node = new AudioBufferSourceNode(ctx, {detune : speed});
  node.buffer = soundBank[file];
  node.connect(vol[pos]);
  if(uncontinousSound[pos]){
    uncontinousSound[pos].stop(0.01);
  }
  node.start();
  //console.log('started', ctx.getOutputTimestamp());
  if (file in UNC_SOUNDS){
    uncontinousSound[pos] = node;
  }
}

function initSoundControl(){
  let btn = document.querySelector('.soundcontrol');
  btn.addEventListener('click', toggleMute);
  document.body.addEventListener('keydown', function(event){
    if (event.code === 'KeyM') {
      toggleMute();
    }
  });
  let stored = localStorage.getItem('sound');
  if (!stored){
    localStorage.setItem('sound', 'on');
  } else if (stored === 'off'){
    toggleMute(null, false);
  }
}



function toggleMute(event, manual=true){
  let btn = document.querySelector('.soundcontrol');
  btn.classList.toggle('mute');
  vol['main'].gain.setValueAtTime(+(!vol['main'].gain.value), ctx.currentTime);
  if (manual) {
    localStorage.setItem('sound', localStorage.getItem('sound') === 'on' ? 'off': 'on');
  }
}


let vol = {};
let uncontinousSound = {};
createSoundSources();
console.log(ctx);

let soundBank = loadSounds();

console.log(soundBank);
initSoundControl();

export {playSound};
