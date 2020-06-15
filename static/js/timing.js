function secondsToMinutes(seconds, dec=false){
  if (dec){
    return (seconds/60).toFixed(2);
  }
  let s = parseInt(Math.floor(+seconds*10))/10;
  let sec = s % 60;
  let min = (s - sec)/60;
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
