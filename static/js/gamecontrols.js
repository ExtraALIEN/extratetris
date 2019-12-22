function sendCheck(){
  conn.send(JSON.stringify({'type': 'check'}));
}


console.log(conn);
let check = document.getElementById('check');
check.addEventListener('click', sendCheck);
