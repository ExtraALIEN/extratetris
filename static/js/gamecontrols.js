console.log('script loaded');

function startFields(fields){
  for(let x in fields){
    let fieldElem = document.getElementById(`field${x}`);
    let connectDiv = document.getElementById(`position${x}`);
    connectDiv.remove();
  }

}

function getReady(conn){
  console.log('get ready signal received');
  conn.send(JSON.stringify({'type': 'ready'}))
}

export {startFields, getReady}
