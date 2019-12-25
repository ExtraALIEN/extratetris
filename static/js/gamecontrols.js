console.log('script loaded');

function startFields(fields, conn){
  for(let x in fields){
    console.log(x);
    let data = fields[x];
    console.log(data);
    let fieldElem = document.getElementById(`field${x}`);
    let rows = fieldElem.querySelectorAll('.row').length-1;
    console.log(rows);
    let connectDiv = document.getElementById(`position${x}`);
    let disconnectButton = document.getElementById(`disconnect${x}`);
    connectDiv.remove();
    disconnectButton.remove();
    document.body.conn = conn;
    document.body.addEventListener('keydown', controlField);
    displayCells(fieldElem, rows, 0, data.surface);
    let changes = Object.assign({}, data.active_piece)
    for (let y in data.active_piece){
      for (let x in y){
        if (data.active_piece[y][x] === 0){
          delete changes[y][x];
        }
      }
    }
    updateField({'pos':x, 'changes':changes});
    updateQueue({'pos':x, 'queue':data.queue});

  }
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


function displayCells(elem, y, x, data){
  for(let yy = 0; yy<data.length; yy++){
    for (let xx = 0; xx<data[0].length; xx++){
      let selector = `.row[data-y="${y-yy}"] .cell[data-x="${x+xx}"]`;
      let cell = elem.querySelector(selector);
      let newClass = `color-${data[yy][xx]}`;
      setClass(cell,newClass);

    }
  }
}

function updateField(data){
  let pos = data.pos;
  let field = document.getElementById(`field${pos}`);
  for (let y in data.changes){
    for(let x in data.changes[y]){
      let selector = `.row[data-y="${y}"] .cell[data-x="${x}"]`;

      let cell = field.querySelector(selector);
      let cl = data.changes[y][x];
      setClass(cell, `color-${cl}`);
    }
  }
}

function updateQueue(data){
  let pos = data.pos;
  let qElem = document.querySelector(`#field${pos} .queue`);
  for(let i in data.queue){
    [...qElem.querySelectorAll(`[id="queue${i}"] .cell`)].forEach(a=> setClass(a, 'color-0'));
    for(let y in data.queue[i]){
      for(let x in data.queue[i][y]){
        let selector = `[id="queue${i}"] .queue-row[data-y="${y}"] .cell[data-x="${x}"]`;
        let cell = qElem.querySelector(selector);
        console.log(cell);
        let cl = data.queue[i][y][x];
        setClass(cell, `color-${cl}`);
      }
    }
  }
}



function setClass(elem, newClass){
  if(elem) {
    elem.className = "cell";
    elem.classList.add(newClass);
  }
}

function removeControls(){
  document.body.removeEventListener('keydown', controlField);
}

export {startFields, getReady, updateField, removeControls, updateQueue};
