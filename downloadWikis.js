const artoo = require("artoo-js");
const cheerio = require('cheerio');
const {readCSV} = require("./CSV");
const curl = require('./curl').default;
const https = require('https');
artoo.bootstrap(cheerio);
// const fs = require('mz');

async function main() {

  data = await readCSV("judges.csv")
  let judges = data.map(el=>el[1])//judges is a simple array of file names.

  judges = judges.filter(item=>!~(//blacklisted extensions:
    ['.jpg','.gif','.png','.docx','.jpeg','.doc','.pdf','.xlsx','.pages','.webm']
      .findIndex(extension=>~item.toLowerCase().indexOf(extension))
  ))

  ///*Use this to show all potential attachments */console.log(judges.filter(item=> (typeof item === "string" && /\.\w{1,4}/.test(item))));
  
  let judgeURLS = judges.map(name=>"https://judgephilosophies.wikispaces.com/"+encodeURIComponent(name.replace(" ","+")).replace("%2B","+"))
  // console.log(judgeURLS[1])
  https.get("https://judgephilosophies.wikispaces.com/Anda%2C+Michael")
};main();

