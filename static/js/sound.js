import {randomNumberInRange} from './utils.js';

const ALL_SOUNDS = ['move', 'rotate'];
const UNC_SOUNDS = ['move', 'rotate'];

function createSoundSpace(){
  let fields = document.querySelectorAll('[id^="field"]');
  for(let x of fields){
    let pos = +x.dataset.pos;
    soundSpace[pos] = new AudioContext();
    uncontinousSound[pos] = null;
    let gainNode = soundSpace[pos].createGain();
    gainNode.gain.value = pos === 0 ? 1 : 0.333;
    gainNode.connect(soundSpace[pos].destination);
    soundSpace[pos].vol = gainNode;

  }
}


function loadSounds(){
  let bank = {};
  let tempCtx = new AudioContext();
  for (let x of ALL_SOUNDS){
    fetch(`/static/sound/${x}.ogg`)
      .then(response => response.arrayBuffer())
      .then(arrayBuffer => tempCtx.decodeAudioData(arrayBuffer))
      .then(buffer => {
        bank[x] = buffer;
      });
  }
  return bank;
}

function playSound(pos, type, speed=0){
  let node = new AudioBufferSourceNode(soundSpace[pos], {'detune' : speed*2.5});
  node.buffer = soundBank[type];
  node.connect(soundSpace[pos].vol);
  // console.log(node.detune);
  if(uncontinousSound[pos]){
      uncontinousSound[pos].stop(0.01);
  }
  node.start(0);
  if (type in UNC_SOUNDS){
    uncontinousSound[pos] = node;
  }
}
let soundSpace = {};
let uncontinousSound = {};
createSoundSpace();
let soundBank = loadSounds();

export {playSound};
