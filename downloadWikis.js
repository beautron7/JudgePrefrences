const artoo = require("artoo-js");
const cheerio = require('cheerio');
const {readCSV} = require("./CSV");
const request = require('request-promise-native');
const http = require('http');
const fs = require('promisify-fs');
const sanitizeFilename = require('sanitize-filename');
artoo.bootstrap(cheerio);
// const fs = require('mz');

async function main() {
  //judges.csv can be downloaded off of the main page of the wiki. it's a list of all pages.
  sitemapCSV = await readCSV("judges.csv")
  //get a list of page names
  let pages = sitemapCSV.map(el=>el[1])

  //remove any pages that are attachments
  pages = pages.filter(item=>!~(//blacklisted extensions:
    ['.jpg','.gif','.png','.docx','.jpeg','.doc','.pdf','.xlsx','.pages','.webm']
      .findIndex(extension=>~item.toLowerCase().indexOf(extension))
  ))

  //Get URLS for each judge's page
  let judgeURLS = pages.map(name=>"https://judgephilosophies.wikispaces.com/"+encodeURIComponent(name.replace(" ","+")).replace("%2B","+"))


  let errors = 0;

  for (let i = 0; i < 10; i++) {
    let progPrct = ~~(100*i/judgeURLS)
    if(i % 10 == 0){
      console.log(`Progress is at (${progPrct})%.\n# completed: ${i}\n# fails    : ${errors}\n# queued   : ${judgeURLS.length-i}`)
    }

    let url = judgeURLS[i];
    request(url)
      .then(html=>{
        let $ = cheerio.load(html);
        let data = $("#content_view").text();
        return fs.writeFile(`./paradigms/${sanitizeFilename(pages[i])}.txt`,data,"utf8")
      })
      .catch(e=>{
        errors++;
        console.log("Failed to download or save "+url)
      });
  }
};main();

