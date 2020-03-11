function addBot(event){
  let pos = event.target.dataset.pos;
  let level = document.querySelector(`#field${pos} .bot-level input`).value;
  document.conn.send((JSON.stringify({'type': 'add-bot',
                                      'pos': pos,
                                      'level': level,
                                      'room_number': document.roomNumber})));
}

function delBot(event){
  let pos = event.target.dataset.pos;
  document.conn.send((JSON.stringify({'type': 'del-bot',
                                      'pos': pos,
                                      'room_number': document.roomNumber})));
}

export {addBot, delBot};
