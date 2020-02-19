function showInfoBlock({msg}){
  let info = document.getElementById('info');
  info.innerHTML = msg;
  info.classList.add('new-info');
}

export {showInfoBlock};
