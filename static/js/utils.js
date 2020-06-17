function addLeadingZeroes(num, digits){
  num = num + '';
  while(num.length < digits){
    num = '0' + num;
  }
  return num;
}

function randomNumberInRange(min, max) {
    return Math.random() * (max - min) + min;
}

export {addLeadingZeroes, randomNumberInRange};
