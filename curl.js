const http = require("http")
defaultOptions = {
  port:80,
  method:"GET",
}

module.exports.default = function curl(url,options) {
  let [_,host,path] = url.match(/(?:https?:\/\/)?(.+?)(?=\/)(.*)/);
  let requestOptions = Object.assign(options ||{},{'host':host,'path':path}, defaultOptions );
  console.log(requestOptions);

  return new Promise(function(resolve, reject) {
    let req = http.request(requestOptions, function(res) {
      res.setEncoding('utf8');
      console.log(`Request Loaded!
        STATUS: ${res.statusCode}
        HEADERS: ${JSON.stringify(res.headers)}
      `);


      if(res.statusCode == "302") {
        console.log("Redirecting to "+res.headers.location);
        return curl(res.headers.location,{cookie:((options && options.cookie) || "")+(res.headers["set-cookie"] || "")});
      } else {
        res.on('data', resolve)
      }
    });
    req.on("error",reject)
    req.end()
  })
}