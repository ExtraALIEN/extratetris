function updateRoom(event){
  let data = JSON.parse(event.data);
  let type = data.type;
  switch (type) {
    case 'connect':
      let name = data.username;
      if (data.rating){
        name += `:${data.rating}`;
      }
      document.querySelector(`[data-number="${data.id}"] [data-pos="${data.pos}"]`)
              .innerHTML = name;
      break;
  case 'disconnect':
    document.querySelector(`[data-number="${data.id}"] [data-pos="${data.pos}"]`)
            .innerHTML = '---';
    break;
  case 'delete':
    document.querySelector(`.room[data-number="${data.id}"]`).remove();
    break;
  case 'room':
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
    break;
  }
}

let conn = new WebSocket(`ws://${location.host}/ws/lobby/`);

conn.onmessage = updateRoom;
