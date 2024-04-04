var express = require('express');
const app = express();
const path = require('path');
const { spawn } = require('child_process');
const {PythonShell} = require('python-shell')
const fs = require('fs');

app.use(express.static(path.join(__dirname, 'views')));
/* GET the home page. */
app.get('/', function(req, res, next) {
  res.render('index', { title: 'Express',Errormessage:false });
});

app.get('/export', function(req, res, next) {
    console.log("export function");
    // collect data from script
    PythonShell.run('excel.py',  function  (err, results)  {
        if  (err)  throw err;
        console.log('hello.py finished.');
        console.log('results', results);
       });
    
  });

/***
 * Form transformation - inject data into a word document
 */
app.post('/form-submit', function(req, res, next) {

  var password, Token, email;
  email = req.body.typeEmailX;
  password = req.body.typePasswordX;
  fs.readFile('./user.json', 'utf8', function (err, data) {
    if (err) throw err;
    obj = JSON.parse(data);
    for(let i=0;i<obj.length;i++){
      for(var value in obj[i]){
        if(email == obj[i]["email"] && password==obj[i]["password"]){
          //console.log("email",email,obj[i]["email"])
          return res.render('dashboard', { title: 'Welcome' });
        }
      }
  }
  return res.render('index', { title: 'Welcome',Errormessage:"Error in user credentials"  });
  });
 
});

module.exports = app;