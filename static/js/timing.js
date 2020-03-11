function secondsToMinutes(seconds, dec=false){
  if (dec){
    return (seconds/60).toFixed(2);
  }
  let sec = seconds % 60;
  let min = (seconds - sec)/60;
  sec = sec.toFixed(1);
  if (min<10){
    min = '0' + min;
  }
  if (sec<10){
    sec = '0' + sec;
  }
  if(sec == 60){
    sec = 0;
    min += 1;
  }
  return `${min}:${sec}`;
}



export {secondsToMinutes};
