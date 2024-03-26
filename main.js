const {app, BrowserWindow} = require('electron')
const server = require('./app');
let mainWindow

function createWindow () {
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 800,
    webPreferences: {
      nodeIntegration: true
    }
  })

  mainWindow.loadURL('http://localhost:3000')  //ADD THIS
  mainWindow.on('closed', function () {
    mainWindow = null
  })
  mainWindow.webContents.openDevTools()

}

app.on('ready', createWindow)


app.on('resize', function(e,x,y){
  mainWindow.setSize(x, y);
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', function () {
  if (mainWindow === null) {
    createWindow()
  }
})
