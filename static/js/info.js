function showInfoBlock({msg}){
  let info = document.getElementById('info');
  info.innerHTML = msg;
  info.classList.add('js-new-info');
}

export {showInfoBlock};
