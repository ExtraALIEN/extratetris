function secondsToMinutes(seconds, dec=false){
  if (dec){
    return (seconds/60).toFixed(2);
  }
  let sec = seconds%60;
  let min = (seconds - sec)/60;
  sec = sec.toFixed(1);
  if (min<10){
    min = '0' + min;
  }
  if (sec<10){
    sec = '0' + sec;
  }
  return `${min}:${sec}`;
}



export {secondsToMinutes};
