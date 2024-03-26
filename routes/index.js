var express = require('express');
const app = express();
const path = require('path');
const { spawn } = require('child_process');
const {PythonShell} = require('python-shell')


app.use(express.static(path.join(__dirname, 'views')));
/* GET the home page. */
app.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
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
  Token = req.body.authToken;
  res.render('welcome', { title: 'Welcome' });
});

module.exports = app;