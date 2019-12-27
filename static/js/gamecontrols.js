console.log('script loaded');

function startTetris(fields, conn){
  for(let x in fields){
    deactivateConnectButtons(x);
    if(conn){
      activateControls(conn);
    }    
    let data = fields[x];
    let fieldElem = document.getElementById(`field${x}`);
    refreshSurface(data.surface);
    refreshActivePiece(data.active_piece);
    refreshQueue(data.queue);
  }
}


function deactivateConnectButtons(x){
  let connectDiv = document.getElementById(`position${x}`);
  let disconnectButton = document.getElementById(`disconnect${x}`);
  connectDiv.remove();
  disconnectButton.remove();
}

function activateControls(conn){
  document.body.conn = conn;
  document.body.addEventListener('keydown', controlField);
}

function removeControls(){
  document.body.removeEventListener('keydown', controlField);
}


function controlField(event){
  let c = event.code;
  let msg = {'type': 'control'};
  if(c === 'KeyA' || c === 'ArrowLeft'){
    msg.command = 'move_left';
  }
  else if(c === 'KeyD' || c === 'ArrowRight'){
    msg.command = 'move_right';
  }else if(c === 'KeyS' || c === 'ArrowDown'){
    msg.command = 'move_down';
  }else if(c === 'KeyW' || c === 'ArrowUp'){
    msg.command = 'rotate';
  }
  if (msg.command){
    event.target.conn.send(JSON.stringify(msg));
  }
}



function getReady(conn){
  console.log('get ready signal received');
  conn.send(JSON.stringify({'type': 'ready'}))
}


function refreshSurface(data){
    let pos = data.pos;
    let field = document.getElementById(`field${pos}`);
    for(let y in data){
      if(y !== 'pos'){
        for (let x in data[y]){
          let selector = `.row[data-y="${y}"] .cell[data-x="${x}"]`;
          let cell = field.querySelector(selector);
          let cl = data[y][x];
          setClass(cell, `color-${cl}`);
        }
      }
    }
}

function refreshQueue(data){
  let pos = data.pos;
  let qElem = document.querySelector(`#field${pos} .queue`);
  for(let i in data){
    if (i!== 'pos'){
      [...qElem.querySelectorAll(`[id="queue${i}"] .cell`)].forEach(a=> setClass(a, 'color-0'));
      for(let y in data[i]){
        for(let x in data[i][y]){
          let selector = `[id="queue${i}"] .queue-row[data-y="${y}"] .cell[data-x="${x}"]`;
          let cell = qElem.querySelector(selector);
          let cl = data[i][y][x];
          setClass(cell, `color-${cl}`);
        }
      }
    }
  }
}

function refreshActivePiece(data){
  let pos = data.pos;
  for (let y in data){
    if(y !== 'pos'){
      for (let x in data[y]){
        if (data[y][x] > 0){
          let selector = `#field${pos} > .row[data-y="${y}"] .cell[data-x="${x}"]`;
          let cell = document.querySelector(selector);
          let newClass = `color-${data[y][x]}`;
          setClass(cell,newClass);
        }
      }
    }
  }
}

function updateTetris(data){
  let pos = data.pos;
  for (let prop in data){
    if(prop === 'current_piece'){
      updateCurrentPiece(pos, data.current_piece)
    }
  }
}

function refreshTetris(data){

    if (data.surface){
      refreshSurface(data.surface);
    }
    if (data.new_piece){
      refreshActivePiece(data.new_piece);
    }
    if (data.queue){
      refreshQueue(data.queue);
    }

}

function updateCurrentPiece(pos, data){
  for (let y in data){
    for(let x in data[y]){
        let selector = `#field${pos} > .row[data-y="${y}"] .cell[data-x="${x}"]`;
        let cell = document.querySelector(selector);
        let newClass = `color-${data[y][x]}`;
        setClass(cell,newClass);
    }
  }
}

function setClass(elem, newClass){
  if(elem) {
    elem.className = "cell";
    elem.classList.add(newClass);
  }
}



export {startTetris, getReady,  removeControls, updateTetris, refreshTetris};
