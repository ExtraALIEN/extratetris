import {secondsToMinutes} from './timing.js';

let selector = `.game-results .time`;
let cells = document.querySelectorAll(selector);
for (let x of [...cells]){
  x.innerHTML = secondsToMinutes(x.dataset.time, x.classList.contains('dec'));
}

let graph = document.getElementById('graph');
let results = document.querySelectorAll('.for-graph');
let allTimes = [...document.querySelectorAll('.end + .time')]
                            .map(a => parseFloat(a.dataset.time));
let maxTime = allTimes.sort().reverse()[0];
let maxVal = 0;
let displayingStat = 'score';
let data = {'score': {},
            'lines': {},
            'speed': {},
            'distance': {},
          };
for (let x of [...results]){
  let [stat, pos] = x.id.split('-');
  let [times, vals] = [JSON.parse(x.dataset.times), JSON.parse(x.dataset.vals)];
  if (!(pos in data[stat])){
    data[stat][pos] = {};
  }
  data[stat][pos].times = times;
  data[stat][pos].vals = vals;
  if (!(maxTime in times)){
    data[stat][pos].times.push(maxTime);
    data[stat][pos].vals.push(vals[vals.length-1]);
  }
  if (stat === displayingStat && vals[vals.length-1] > maxVal){
    maxVal = vals[vals.length-1];
  }
}

let gWidth = graph.clientWidth;
let gHeight = graph.clientHeight;

let margin = {top: gHeight/10, right: gWidth/5, bottom: gHeight/10, left: gWidth/10};

let width = gWidth - margin.left - margin.right;
let height = gHeight - margin.top - margin.bottom;


let svg = d3.select("#graph")
      .append("svg")
      .attr("width", gWidth)
      .attr("height", gHeight)
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

function lineData(input){
  let result = [];
  for (let i = 0; i< input.times.length; i++){
    result.push({'x': input.times[i]/60, 'y': input.vals[i]});
  }
  return result;
}

let COLORS = ['#c61212', '#004bf1', '#e9a611', '#05db0e'];

for (let pos in data[displayingStat]){
let toDisplay = lineData(data[displayingStat][pos]);
svg.append("path")
      .datum(toDisplay)
      .attr("fill", "none")
      .attr("stroke", `${COLORS[pos]}`)
      .attr("stroke-width", 3.5)
      .attr("opacity", .9)
      .attr("d", d3.line()
        .x(d => timeScale(d.x))
        .y(d => valScale(d.y))
      )
}
