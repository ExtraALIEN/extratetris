const TETRIS_VALUES = {
  'commands' : {
    'KeyA' : 'move_left',
    'ArrowLeft' : 'move_left',
    'KeyD' : 'move_right',
    'ArrowRight' : 'move_right',
    'KeyS' : 'move_down',
    'ArrowDown' : 'move_down',
    'KeyW' : 'rotate',
    'ArrowUp' : 'rotate',
    'Numpad1' : 'use_powerup',
    'Numpad2' : 'use_powerup',
    'Numpad3' : 'use_powerup',
    'Numpad4' : 'use_powerup',
    'Digit1' : 'use_powerup',
    'Digit2' : 'use_powerup',
    'Digit3' : 'use_powerup',
    'Digit4' : 'use_powerup'
  },
  'descriptions' : {
    'CL' : 'Тетрис: классический вариант. Расставляй фигуры в линии. \n \
            За фигуры и за линии присуждаются очки. \n \
            Набери как можно больше очков для победы в игре.',
    'DM' : 'Битва: тетрис + бонусы. \n \
            Устрой соперникам испытание и защищайся сам от их атак. \n \
            Набери как можно больше очков для победы в игре.',
    'SU' : 'Выживание: для победы останься в игре дольше всех.',
    'LI' : 'Линии: уничтожь заранее определенное количество линий. \n \
            После выполнения условия игра заканчивается, остальное не имеет значения. \n \
            Если не доживешь, результат не засчитывается, и присуждается последнее место. \n \
            Построй линии быстрее всех для победы в игре.' ,
    'CO' : 'Обратный отсчет: дается ограниченное время на игру. \n \
            Если не доживешь, результат не засчитывается, и присуждается последнее место. \n \
            Для победы набери больше всех очков за отведенное время.',
    'SA' : 'Покорение вершины: задача игры - набрать определенное количество очков. \n \
            После выполнения условия игра заканчивается, остальное не имеет значения. \n \
            Если не доживешь, результат не засчитывается, и присуждается последнее место. \n \
            Достигни нужного количества очков раньше всех для победы в игре.' ,
    'DR' : 'Заезд на ограниченную дистанцию: задача игры - набрать пробег определенный перед началом игры. \n \
            После выполнения условия игра заканчивается, остальное не имеет значения. \n \
            Если не доживешь, результат не засчитывается, и присуждается последнее место. \n \
            пройди дистанцию быстрее всех для победы в игре.',
    'AC' : 'Разгон с места: задача игры - достичь определенной скорости на спидометре. \n \
            После выполнения условия игра заканчивается, остальное не имеет значения. \n \
            Если не доживешь, результат не засчитывается, и присуждается последнее место. \n \
            Ускорься мощнее всех для победы в игре.' ,
    'CF' : 'Захват флага: возьми флаг с места хранения и принеси на свою базу. \n \
            Изначально флаг находится на определенной высоте. \n \
            Чтобы его взять, уничтожь линию на этой высоте флага. \n \
            После взятия, принеси флаг на свою базу, \n \
            для этого постепенно уничтожай линии до самого низа. \n \
            Новый флаг образуется на изначальной высоте. \n \
            Соперники могут перехватить флаг, сжигая линии выше \n \
            чем он находится у игрока, который его в данный момент несет. \n \
            Принеси на базу больше всех флагов для победы.',
    'HF' : 'Удержание флага: задача нести флаг как можно дольше. \n \
            Флаг образуется и перемещается по тем же правилам, что и в режиме захвата флага. \n \
            Время удержания флага отсчитывается с того момента, как игрок взял либо перехватил флаг. \n \
            В этом режиме не обязательно приносить флаг на базу. \n \
            В случае если игрок принес флаг на базу, образуется новый флаг на изначальной высоте, \n \
            при этом считается что им продолжает владеть тот же игрок, до тех пор пока флаг \n \
            не будет взят или перехвачен другим игроком. \n \
            Продержи флаг суммарно дольше всех за игру для победы.',
    'RA' : 'Ралли: задача - пройти трассу при максимальном соответствии с заданным маршрутом. \n \
            Маршрутные очки присуждаются либо отнимаются за уничтожение линий только в определенные моменты. \n \
            Учитывается общее количество линий, уничтоженных в игре всеми игроками на данный момент. \n \
            \n\
            Таблица очков: \n\
            Линии \t Маршрутные очки \n \
            005, 010, 015 ... \t +2 \n \
            010, 020, 030 ... \t +1 (дополнительно) \n\
            025, 050, 075 ... \t +1 (дополнительно) \n\
            100, 200, 300 ... \t +1 (дополнительно) \n\
            \n\
            Штрафы: \n\
            Линии \t Маршрутные очки \n \
            011, 016, 021 ... \t -1 \n \
            014, 019, 014 ... \t -1 (дополнительно) \n\
            024, 049, 074 ... \t -1 (дополнительно) \n\
            099, 199, 299 ... \t -1 (дополнительно) \n\
            \n\
            Внимательно выбирай моменты для уничтожения линий. \n\
            Для победы набери больше всех маршрутных очков, остальное не имеет значения.'
  },
  'standardVolume' : {
    'LI' : 60,
    'CO' : 360,
    'SA' : 20000,
    'DR' : 4020,
    'AC' : 100,
  },
  'measure' : {
    'LI' : 'Линии',
    'CO' : 'Время',
    'SA' : 'Очки',
    'DR' : 'Пробег',
    'AC' : 'Скорость',
  },
  'statsSelector' : {
    'result' : '.primary .main-value',
    'score' : '.scores .total',
    'score-intermediate-st' : '.scores .inter-st',
    'score-sec' : '.scores .sec',
    'score-piece' : '.scores .piece',
    'score-action' : '.scores .action',
    'score-dist' : '.scores .dist',
    'time' : '.time .overall',
    'time-climb' : '.time .climb',
    'time-lines' : '.time .lines',
    'time-acc' : '.time .acc',
    'time-drag' : '.time .drag',
    'lines' : '.lines .total',
    'lines-min' : '.lines .min',
    'pieces-line' : '.lines .pieces',
    'dist-line' : '.lines .dist',
    'pieces' : '.figures .total',
    'pieces-min' : '.figures .min',
    'actions-piece' : '.figures .act',
    'max-speed': '.other .speed',
    'distance': '.other .dist',
    'apm':'.other .apm',
  },
  'typeStats': {
    'best': 'Рекорды в игре',
    'user' : 'Игрок',
    'TOTAL' : 'TOTAL',
    'CL' : 'CL',
    'DM' : 'DM',
    'SU' : 'SU',
    'LI' : 'LI',
    'CO' : 'CO',
    'SA' : 'SA',
    'DR' : 'DR',
    'AC' : 'AC',
    'CF' : 'CF',
    'HF' : 'HF',
    'RA' : 'RA',
  },
  'statsDescriptions': {
    'speed': 'Максимальная скорость',
    'score' : 'Очки',
    'lines' : 'Линии',
    'distance' : 'Пробег',
    'survival_time' : 'Время выживания',
    'time_lines': 'Время 60 линий',
    'time_climb': 'Время 20000 очков',
    'time_drag': 'Прохожденеие 4020 дистанции',
    'time_acc': 'Разгон до 100',
    'countdown_score': 'Очки за 6 минут',
    'games' : 'Количество игр',
    'time' : 'Время в игре',
    'score_game' : 'Очков за игру',
    'lines_game' : 'Линий за игру',
    'distance_game' : 'Пробег за игру',
    'time_game' : 'Среднее время выживания',
    'distance_line' : 'Пробег за 1 линию',
    'figures_line' : 'Фигур на 1 линию',
    'actions_figure': 'Действий на 1 фигуру',
    'score_figure' : 'Очков за 1 фигуру',
    'score_actions' : 'Очков за 1 действие',
    'score_distance' : 'Очков за 1 шаг фигуры',
    'score_sec' : 'Очков в секунду',
    'lines_min' : 'Линий в минуту',
    'actions_min' :'Действий в минуту',
    'eff' : 'Эффективность % в играх с соперниками',
    'username' : 'Имя'
  },
};

const TETRIS_COLORS = {
  'record': ['#c61212', '#004bf1', '#e9a611', '#05db0e'],
};

const TETRIS_SOUNDS = {
  'allSounds' : ['move',
              'rotate',
              'land',
              'line',
              'gameover',
              'select',
              'chance_up',
              'chance_down',
              'speed_up',
              'speed_down',
              'line_add_1',
              'line_add_2',
              'line_add_3',
              'line_remove_1',
              'line_remove_2',
              'line_remove_3',
              'copy_figure',
              'duration_up',
              'duration_down',
              'thunder',
              'shield',
              'bomb',
              'trash',
              'blind',
              'blind_queue',
              'drink',
              'weak_signal',
              'flag',
              'goal',
              'block'],
    'uncSounds': ['move', 'rotate', 'select']
};

function addLeadingZeroes(num, digits){
  num = num + '';
  while(num.length < digits){
    num = '0' + num;
  }
  return num;
}

function randomNumberInRange(min, max) {
    return Math.random() * (max - min) + min;
}

function secondsToMinutes(seconds, dec=false){
  if (dec){
    return (seconds/60).toFixed(2);
  }
  let s = parseInt(Math.floor(+seconds*10))/10;
  let sec = s % 60;
  let min = (s - sec)/60;
  sec = sec.toFixed(1);

  if (min<10){
    min = '0' + min;
  }
  if (sec<10){
    sec = '0' + sec;
  }
  return `${min}:${sec}`;
}

function secondsToHours(seconds){
  return (seconds/3600).toFixed(2);
}



function deepUpdate(acc, cur){
  for (let x in cur){
    if (!(x in acc)){
      acc[x] = cur[x];
    }
    deepUpdate(acc[x], cur[x]);
    return acc;
  }
}

export {TETRIS_VALUES, TETRIS_COLORS, TETRIS_SOUNDS, addLeadingZeroes, randomNumberInRange, secondsToMinutes,
deepUpdate, secondsToHours};
