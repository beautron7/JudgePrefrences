const {readCSV} = require('basic-csv');

exports.readCSV = function(){
  return new Promise((y,n)=>{
    readCSV(...arguments,(e,x)=>{
      if(e) {
        n(x)
      } else {
        y(x)
      }
    })
  })
}
