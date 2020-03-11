function updateRoom(event){
  let data = JSON.parse(event.data);
  let type = data.type;
  if (type === 'connect'){
    let selector = `[data-number="${data.id}"] [data-pos="${data.pos}"]`;
    document.querySelector(selector).innerHTML = data.username;
  } else if (type === 'disconnect'){
    let selector = `[data-number="${data.id}"] [data-pos="${data.pos}"]`;
    document.querySelector(selector).innerHTML = '---';
  } else if (type === 'delete'){
    let selector = `.room[data-number="${data.id}"]`;
    let li = document.querySelector(selector);
    li.remove();
  } else if (type === 'room'){
    let room = document.createElement('li');
    room.classList.add('room');
    room.dataset.number = data.id;
    let gameType = document.createElement('span');
    gameType.classList.add('type');
    gameType.innerHTML = data.game_type;
    room.appendChild(gameType);
    let players = document.createElement('span');
    players.classList.add('players');
    players.innerHTML = 'Игроков: ' + data.size;
    room.appendChild(players);
    let ul = document.createElement('ul');
    ul.classList.add('current-players');
    for (let x=0; x< data.size; x++){
      let li = document.createElement('li');
      li.dataset.pos = x;
      li.innerHTML = data.users[x].username;
      ul.appendChild(li);
    }
    room.appendChild(ul);
    let a = document.createElement('a');
    a.classList.add('flick');
    a.classList.add('enter');
    a.innerHTML = 'Подойти';
    a.href = data.url;
    room.appendChild(a);
    document.querySelector('.lobby').appendChild(room);
  }
}

let conn = new WebSocket('ws://localhost/ws/lobby/');

conn.onmessage = updateRoom;
