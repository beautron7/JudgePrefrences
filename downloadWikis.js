const cheerio = require('cheerio');
const {readCSV} = require("./CSV");
const http = require('http');
const request = require('request');
const rq = require('request-promise-native');
const fs = require('promisify-fs');
const sanitizeFilename = require('sanitize-filename');
const wait = require('./wait').default;

let errors = 0,
    defaultRequestOptions,
    pages;

readCSV("judges.csv").then(sitemapCSV=>{
  pages = sitemapCSV.map(el=>el[1])//get first col of each row
  
  
  //remove pages that are files.
  let blacklisted_extensions = ['.jpg','.gif','.png','.docx','.jpeg','.doc','.pdf','.xlsx','.pages','.webm']
  pages = pages.filter(item=>!~(blacklisted_extensions.findIndex(extension=>~item.toLowerCase().indexOf(extension))))
  
  //set default options for requests
  defaultRequestOptions = {
    transform: cheerio.load,//when html is received, run cheerio.load(html), and pass to fcn.
  };

  getJudge(0);//start the loop
})

function getNextJudge(i){
  setTimeout(() => {//disassocaite with the callstack
    getJudge(i+1)
  }, 1000);//delay betwn. reqs.
}

function getJudge(i) {
  if(i >= pages.length) {//TODO
    return;
  }

  let progPrct = ~~(100*i/pages.length)
  let judgeName = pages[i]
  let judgeUrl = "https://judgephilosophies.wikispaces.com/"+encodeURIComponent(judgeName.replace(" ","+")).replace("%2B","+");
  let requestOptions = Object.assign({
    url:judgeUrl,
  },defaultRequestOptions)
  
  console.log(`Progress is at (${progPrct})%.\n# attempted: ${i-errors}\n# fails    : ${errors}\n# queued   : ${pages.length-i}`)
  
  rq(requestOptions)
    .then(function ($) {    
      let data = $("#content_view").text();
      fs.writeFile(`./paradigms/${sanitizeFilename(judgeName)}.txt`,data,"utf8")
        .then(()=>{
          getNextJudge(i);//FIXED?
        });
    })
    .catch(function (e) {
      errors++;
      console.log("Failed to download or save "+judgeName)
      getNextJudge(i);

      e = JSON.stringify(e)
      if(e.length > 100){
        console.log(e.slice(0,50)+" ... "+e.slice(-50));
      } else {
        console.log(e)
      }
    })
}



process.on('SIGINT', function() {//doesn't work.
  console.log("Saving progress to ./paradigms/progress.txt");
  getNextJudge =(i)=>{
    fs.writeFile("./paradigms/progress.txt",i,"utf8").then(()=>{
      setTimeout(() => {
        process.exit(1);
      }, 1000);
    })
  };
  
});


