console.log('script loaded');

function updateSurface(data){
  for(let y=data.y; y<data.height; y++)  {
    for(let x=data.x; y<data.width; x++){
      let selector = `#field${data.pos} .row[data-y=${y}] .cell[data-x=${x}]`;
      document.querySelector(selector).classlist.add('color-1');
    }
  }
}

export {updateSurface}
