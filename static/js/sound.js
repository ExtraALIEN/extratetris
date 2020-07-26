import {randomNumberInRange, TETRIS_SOUNDS, TETRIS_SETTINGS} from './utils.js';

function createSoundSources(){
  vol['main'] = ctx.createGain();
  vol['main'].connect(ctx.destination);
  let fields = document.querySelectorAll('[id^="field"]');
  for(let x of fields){
    let pos = +x.dataset.pos;
    uncontinousSound[pos] = null;
    let gainNode = ctx.createGain();
    gainNode.gain.value = pos === 0 ? 1 : 0.5;
    gainNode.connect(vol['main']);
    vol[pos] = gainNode;
  }
}

function loadSounds(){
  let bank = {};
  for (let x of TETRIS_SOUNDS.allSounds){
    fetch(`/static/sound/${x}.ogg`)
      .then(response => response.arrayBuffer())
      .then(arrayBuffer => ctx.decodeAudioData(arrayBuffer))
      .then(buffer => {
          bank[x] = buffer;
        });
  }
  return bank;
}

function playSound({pos, file, speed=0}){
  let node = new AudioBufferSourceNode(ctx, {detune : speed});
  node.buffer = soundBank[file];
  node.connect(vol[pos]);
  if(uncontinousSound[pos]){
    uncontinousSound[pos].stop(0.01);
  }
  node.start();
  if (file in TETRIS_SOUNDS.uncSounds){
    uncontinousSound[pos] = node;
  }
}

function initSettingsControl(prop){
  let btn = document.querySelector(`.${prop}control`);
  btn.addEventListener('click', toggleMute(prop));
  document.body.addEventListener('keydown', function(event){
    if (event.code === TETRIS_SETTINGS[prop]) {
      toggleMute(event, prop);
    }
  });
  let stored = localStorage.getItem(prop);
  if (!stored){
    localStorage.setItem(prop, 'on');
  } else if (stored === 'off'){
    toggleMute(prop)(null, false);
  }
}

function toggleMute(prop){
  return function(event, manual=true){
    let btn = document.querySelector(`.${prop}control`);
    btn.classList.toggle('mute');
    if (prop === 'sound'){
      vol['main'].gain.setValueAtTime(+(!vol['main'].gain.value), ctx.currentTime);
    }
    if (manual) {
      localStorage.setItem(prop, localStorage.getItem(prop) === 'on' ? 'off': 'on');
    }
  }
}

let ctx = new AudioContext();
let vol = {};
let uncontinousSound = {};
createSoundSources();
let soundBank = loadSounds();
initSettingsControl('sound');
initSettingsControl('vib');

export {playSound};
