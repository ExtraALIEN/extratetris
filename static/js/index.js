if (document.querySelector('[data-waiting="waiting"]')){
  if (localStorage.getItem('reloaded') === 'true'){
  console.log(true);
  }
  else{
    localStorage.setItem('reloaded', true);
    window.location.reload(true);
  }
} else {
  console.log(false);
  localStorage.setItem('reloaded', false);
}
