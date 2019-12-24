console.log('script loaded');

function startFields(fields, conn){
  console.log('conn', conn);
  for(let i in fields){
    let data = fields[i];
    let x = Object.keys(data)[0];
    let fieldElem = document.getElementById(`field${x}`);
    let connectDiv = document.getElementById(`position${x}`);
    let disconnectButton = document.getElementById(`disconnect${x}`);
    connectDiv.remove();
    disconnectButton.remove();
    document.body.addEventListener('keydown', controlField);
    displayCells(fieldElem, 24, 0, data[x].surface);
    displayCells(fieldElem, data[x].active_piece.y, data[x].active_piece.x,data[x].active_piece.shape);
  }

  function controlField(event){
    console.log('listener,' , conn);
    let c = event.code;
    let msg = {'type': 'control'};
    if(c === 'KeyA'){
      msg.command = 'move_left';
    }
    else if(c === 'KeyD'){
      msg.command = 'move_right';
    }else if(c === 'KeyS'){
      msg.command = 'move_down';
    }else if(c === 'KeyW'){
      msg.command = 'rotate';
    }
    conn.send(JSON.stringify(msg));
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



export {startFields, getReady};
