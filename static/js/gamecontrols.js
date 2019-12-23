console.log('script loaded');

function startFields(fields){
  for(let i in fields){
    let data = fields[i];
    let x = Object.keys(data)[0];
    let fieldElem = document.getElementById(`field${x}`);
    let connectDiv = document.getElementById(`position${x}`);
    let disconnectButton = document.getElementById(`disconnect${x}`);
    connectDiv.remove();
    disconnectButton.remove();
    displayCells(fieldElem, 24, 0, data[x].surface);
    displayCells(fieldElem, data[x].active_piece.y, data[x].active_piece.x,data[x].active_piece.shape);
  }

}

function getReady(conn){
  console.log('get ready signal received');
  conn.send(JSON.stringify({'type': 'ready'}))
}


function displayCells(elem, y, x, data){
  for(let yy = 0; yy<data.length; yy++){
    for (let xx = 0; xx<data[0].length; xx++){
      let selector = `.row[data-y="${y-yy}"] .cell[data-x="${x+xx}"]`;
      let cell = elem.querySelector(selector);
      let newClass = `color-${data[yy][xx]}`;
      cell.classList.add(newClass);
    }
  }
}

export {startFields, getReady}
