let DESCRIPTIONS = {
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
};

let DESCRIPTIONS_STATS = {
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
};


let topics = document.querySelectorAll('[data-topic]');
for (let x of [...topics]){
  x.innerHTML = DESCRIPTIONS[x.dataset.topic];
}

let stats = document.querySelectorAll('[data-stat]');
for (let x of [...stats]){
  x.innerHTML = DESCRIPTIONS_STATS[x.dataset.stat];
}
