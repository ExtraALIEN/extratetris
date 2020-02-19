function addLeadingZeroes(num, digits){
  num = num + '';
  while(num.length < digits){
    num = '0' + num;
  }
  return num;
}

export {addLeadingZeroes};
