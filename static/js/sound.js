import {randomNumberInRange, TETRIS_SOUNDS} from './utils.js';

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

let ctx = new AudioContext();
let vol = {};
let uncontinousSound = {};
createSoundSources();
let soundBank = loadSounds();
initSoundControl();

export {playSound};
