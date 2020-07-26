function makeVibrate(duration){
  if ('vibrate' in navigator && localStorage.getItem('vib') === 'on'){
    navigator.vibrate(duration);
  }
}

export {makeVibrate};
