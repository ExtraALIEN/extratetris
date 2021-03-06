import {secondsToMinutes, deepUpdate, TETRIS_COLORS} from './utils.js';

function displaySeconds(){
  let cells = document.querySelectorAll(`.game-results .time`);
  for (let x of [...cells]){
    if(x.dataset.time){
      x.innerHTML = secondsToMinutes(x.dataset.time, x.classList.contains('dec'))
    } else{
      x.innerHTML = '-';
    };
  }
}

function detectMaxTime(){
  let allTimes = [...document.querySelectorAll('.end + .time')]
                              .map(a => parseFloat(a.dataset.time));
  return allTimes.sort((a,b) => a-b ).reverse()[0];
}

function primaryData(result){
  let output = {};
  let [stat, pos] = result.dataset.stat.split('-');
  output[stat] = {};
  output[stat][pos] = {};
  let [times, vals] = [JSON.parse(result.dataset.times), JSON.parse(result.dataset.vals)];
  output[stat][pos].times = times;
  output[stat][pos].vals = vals;
  let finishTime = playerTime(pos);
  if (finishTime > times[times.length-1]){
    output[stat][pos].times.push(finishTime);
    output[stat][pos].vals.push(vals[vals.length-1]);
  }
  return output;
}

function buildMultipleDataObj(results){
  let data = {'score': {},
              'speed': {},
              'distance': {},
              'lines': {},
              'figures': {}};
  let times = {};
  let maxTimes = {};
  for (let x of [...results]){
    let [stat, pos, vals] = [x.dataset.stat, x.dataset.pos, x.dataset.vals];
    if (stat === 'max_times') {
      let t = JSON.parse(vals);
      t.sort((a,b)=> b-a);
      maxTimes[pos] = JSON.parse(vals);
      times[pos] = [];
      for(let i=0; i< t[0]; i++){
        times[pos].push(i);
      }
    }
  }
  for (let x of [...results]){
    let [stat, pos, vals] = [x.dataset.stat, x.dataset.pos, x.dataset.vals];
    if (stat !== 'max_times'){
      let v = JSON.parse(vals).map(a => a/maxTimes[pos].length);
      data[stat][pos] = {'times': times[pos],
                        'vals': v
                        };
    }
  }
  return data;
}

function overallAvg(data, stat){
  let output = {};
  for (let x in data[stat]){
    output[x] = {};
    let player = data[stat][x];
    output[x].times = player.times;
    output[x].vals = [0];
    for (let i=1; i<player.times.length; i++){
      if(player.times[i] !== 0){
        output[x].vals.push(player.vals[i]/(player.times[i]));
      }
    }
  }
  return output;
}

function currentAvg(data, stat, range, delta){
  let output = {};
  for (let x in data[stat]){
    output[x]= {};
    let player = data[stat][x];
    output[x].times = [];
    output[x].vals = [];
    let time = range/2;
    while(time < player.times[player.times.length-1]){
      output[x].times.push(time);
      let indexes = [];
      for(let i=0; i<player.times.length; i++){
        if( (player.times[i] <= time+range/2) && (player.times[i] >= time-range/2)){
          indexes.push(i);
        }
      }
      let fact = 0;
      if (indexes.length > 0){
        fact = (player.vals[indexes[indexes.length-1]]-player.vals[indexes[0]])/
            (player.times[indexes[indexes.length-1]]-player.times[indexes[0]]);
      }
      if(isNaN(fact)){
        output[x].times.pop();
      }else{
        output[x].vals.push(fact);
      }
      time += delta;
    }

  }
  return output;
}

function crossAvg(data, stat1, stat2, delta){
  let output = {};
  let data1 = {};
  let data2 = {};
  let time;
  for (let x in data[stat1]){
    output[x] = {'times': [], 'vals': []};
    data1[x] = [];
    let player = data[stat1][x];
    time = delta;
    while(time < player.times[player.times.length-1]){
      output[x].times.push(time);
      let indexes = [];
      for(let i=0; i<player.times.length; i++){
        if(player.times[i] <= time){
          indexes.push(i);
        }
      }
      let temp = 0;
      if (indexes.length > 0){
        temp = player.vals[indexes[indexes.length-1]];
      }
      data1[x].push(temp);
      time += delta;
    }
    output[x].times.push(player.times[player.times.length-1]);
    data1[x].push(player.vals[player.vals.length-1]);
  }
  for (let x in data[stat2]){
    data2[x] = [];
    let player = data[stat2][x];
    let time1 = player.times[player.times.length-1];
    time = delta;
    while(time < time1){
      let indexes = [];
      for(let i=0; i<player.times.length; i++){
        if(player.times[i] <= time){
          indexes.push(i);
        }
      }
      let temp = 0;
      if (indexes.length > 0){
        temp = player.vals[indexes[indexes.length-1]];
      }
      data2[x].push(temp);
      time += delta;
    }
    data2[x].push(player.vals[player.vals.length-1]);
  }
  for(let x in data1){
    for (let i in data1[x]){
      if (data2[x][i] > 0){
        output[x].vals.push(data1[x][i] / data2[x][i]);
      } else {
        output[x].vals.push(0);
      }
    }
  }
  return output;
}

function currentCrossAvg(data, stat1, stat2, range, delta){
  let output = {};
  let data1 = {};
  let data2 = {};
  let time;
  for (let x in data[stat1]){
    output[x] = {'times': [], 'vals': []};
    data1[x] = [];
    let player = data[stat1][x];
    time = range/2;
    while(time < player.times[player.times.length-1]){
      output[x].times.push(time);
      let indexes = [];
      for(let i=0; i<player.times.length; i++){
        if( (player.times[i] <= time+range/2) && (player.times[i] >= time-range/2)){
          indexes.push(i);
        }
      }
      let fact = 0;
      if (indexes.length > 0){
        fact = (player.vals[indexes[indexes.length-1]]-player.vals[indexes[0]])/
            (player.times[indexes[indexes.length-1]]-player.times[indexes[0]]);
      }
      data1[x].push(fact);
      time += delta;
    }
  }
  for (let x in data[stat2]){
    data2[x] = [];
    let player = data[stat2][x];
    time = range/2;
    while(time < player.times[player.times.length-1]){
      output[x].times.push(time);
      let indexes = [];
      for(let i=0; i<player.times.length; i++){
        if( (player.times[i] <= time+range/2) && (player.times[i] >= time-range/2)){
          indexes.push(i);
        }
      }
      let fact = 0;
      if (indexes.length > 0){
        fact = (player.vals[indexes[indexes.length-1]]-player.vals[indexes[0]])/
            (player.times[indexes[indexes.length-1]]-player.times[indexes[0]]);
      }
      data2[x].push(fact);
      time += delta;
    }
  }
  for(let x in data1){
    for (let i in data1[x]){
      if (data2[x][i] > 0){
        output[x].vals.push(data1[x][i] / data2[x][i]);
      } else {
        output[x].times.splice(i,1);
      }
    }
  }
  return output;
}

function valsMul(input, mul){
  let output = {};
  for (let x in input){
    output[x] = {'times': input[x].times,
                 'vals': input[x].vals.map(a => a*mul)};
  }
  return output;
}

function detectData(results, ready=true){
  let data = {};
  if (ready){
    for (let x of [...results]){
      let prim = primaryData(x);
      data = deepUpdate(data, prim);
    }
  } else {
    data = buildMultipleDataObj(results);
  }
  data['score-sec'] = overallAvg(data, 'score');
  data['score-fact'] = currentAvg(data, 'score', 60, 1);
  data['score-figure'] = crossAvg(data, 'score', 'figures', 1);
  data['score-figure-fact'] = currentCrossAvg(data, 'score', 'figures', 60, 10);
  data['score-distance'] = crossAvg(data, 'score', 'distance', 1);
  data['score-distance-fact'] = currentCrossAvg(data, 'score', 'distance', 60, 10);
  data['lines-min'] = valsMul(overallAvg(data, 'lines'), 60);
  data['lines-fact'] = valsMul(currentAvg(data, 'lines', 60, 10), 60);
  data['speed-min'] = valsMul(overallAvg(data, 'speed'), 60);
  data['speed-fact'] = valsMul(currentAvg(data, 'speed', 60, 10), 60);
  data['figures-min'] = valsMul(overallAvg(data, 'figures'), 60);
  data['figures-fact'] = valsMul(currentAvg(data, 'figures', 60, 10), 60);
  data['figures-line'] = crossAvg(data, 'figures', 'lines', 1);
  data['figures-line-fact'] = currentCrossAvg(data, 'figures', 'lines', 60, 10);
  data['dist-min'] = valsMul(overallAvg(data, 'distance'), 60);
  data['dist-fact'] = valsMul(currentAvg(data, 'distance', 60, 10), 60);
  data['dist-line'] = crossAvg(data, 'distance', 'lines', 1);
  data['dist-line-fact'] = currentCrossAvg(data, 'distance', 'lines', 60, 10);
  data['dist-figure'] = crossAvg(data, 'distance', 'figures', 1);
  data['dist-figure-fact'] = currentCrossAvg(data, 'distance', 'figures', 60, 10);
  return data;
}

function playerTime(pos){
  return [...document.querySelectorAll('.end + .time')]
                     .map(a => parseFloat(a.dataset.time))[pos];
}

function lineData(input){
  let result = [];
  for (let i = 0; i< input.times.length; i++){
    result.push({'x': input.times[i]/60, 'y': input.vals[i]});
  }
  return result;
}

function displayGraph(data, stat){
  let maxVal = 0;
  for (let x in data.game[stat]){
    for (let val of data.game[stat][x].vals){
      if (val > maxVal){
        maxVal = val;
      }
    }
  }
  maxVal *= 1.02;
  let gWidth = graph.clientWidth;
  let gHeight = graph.clientHeight;
  let margin = {top: gHeight/10, right: gWidth/5, bottom: gHeight/10, left: gWidth/10};
  let width = gWidth - margin.left - margin.right;
  let height = gHeight - margin.top - margin.bottom;

  let svg = d3.select("#graph")
        .append("svg")
        .attr("viewBox", `0 0 ${gWidth} ${gHeight}`)
        .append('g')
        .attr("transform",`translate(${margin.left}, ${margin.top})`);
  let timeScale = d3.scaleLinear()
                    .domain([0, maxTime/60])
                    .range([0, width]);
  let valScale = d3.scaleLinear()
                   .domain([0, maxVal])
                   .range([height, 0]);
  let xAxis = d3.axisBottom()
                .scale(timeScale);
  let yAxis = d3.axisLeft()
                .scale(valScale);

  svg.append('g')
     .call(xAxis)
     .attr("transform", `translate(0, ${height})`)
     .call(g => g.selectAll(".tick line").clone()
          .attr("y2", -height)
          .attr("stroke-opacity", 0.2));

  svg.append('g')
     .call(yAxis)
     .call(g => g.selectAll(".tick line").clone()
          .attr("x2", width)
          .attr("stroke-opacity", 0.2));
  for(let x in data){
    for (let pos in data[x][stat]){
        let toDisplay = lineData(data[x][stat][pos]);
        svg.append("path")
           .datum(toDisplay)
           .attr("fill", "none")
           .attr("stroke", `${TETRIS_COLORS.record[pos]}`)
           .attr("stroke-width", x === 'last' ? 1 : 4)
           .attr("stroke-dasharray", x === 'best' ? [5,5] : null)
           .attr("opacity", x === 'best' ? .4 : x === 'last' ? .95 : .95)
           .attr("d", d3.line()
                        .x(d => timeScale(d.x))
                        .y(d => valScale(d.y))
                  )
            }
    }
}

function clearGraph(){
  document.querySelector('svg').remove();
}

function changeMode(event){
  document.querySelector('.displaying').classList.remove('displaying');
  event.target.classList.add('displaying');
  clearGraph();
  displayGraph(data, event.target.dataset.mode);
}

displaySeconds();
let graph = document.getElementById('graph');
let maxTime = detectMaxTime();
let data = {
  'game': detectData(document.querySelectorAll('.for-graph')),
  'best': detectData(document.querySelectorAll('.best-graph')),
  'last': detectData(document.querySelectorAll('.last-graph'), false)
};
displayGraph(data,'score');
let modes = document.querySelectorAll('#graph .modes > li');
for (let x of [...modes]){
  x.addEventListener('click', changeMode);
}
