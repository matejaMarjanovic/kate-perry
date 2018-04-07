import sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):
    def __init__(self):
        # initializing the window using the super constructor
        super(Window, self).__init__()
        self.setGeometry(50, 50, 800, 500)
        self.setWindowTitle("Kate Perry")
        
        # set the text editor object on the window
        self.editor = QtGui.QTextEdit()
        self.setCentralWidget(self.editor)
        
        # add actions to the file drop menu
        
        # open file action
        openFileAction = QtGui.QAction("&Open File", self)
        openFileAction.setShortcut("Ctrl+O")
        openFileAction.setStatusTip("Open File")
        openFileAction.triggered.connect(self.fileOpening)
        
        # save file action
        saveFileAction = QtGui.QAction("&Save File", self)
        saveFileAction.setShortcut("Ctrl+S")
        saveFileAction.setStatusTip("Save File")
        saveFileAction.triggered.connect(self.fileSaving)
        
        # we don't need this
        resizeAction = QtGui.QAction("&Resize the window", self)
        resizeAction.setShortcut("Ctrl+R")
        resizeAction.setStatusTip("Change the window size")
        resizeAction.triggered.connect(self.resizeWindow)
        
        # exit Kate Perry
        exitAction = QtGui.QAction("&Exit Kate Perry", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Leave")
        exitAction.triggered.connect(self.closeApp)
        
        # now create the file drop menu and push all the actions in
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")
        fileMenu.addAction(openFileAction)
        fileMenu.addAction(saveFileAction)
        fileMenu.addAction(resizeAction)
        fileMenu.addAction(exitAction)
        
        self.home()
    
    def fileSaving(self):
        name = QtGui.QFileDialog.getSaveFileName(self, "Save file")
        # this needs fixing in case the file already exists 
        # we don't want to say '...yes overwrite...'
        # we just want to overwrite it
        with open(name, "w") as f:
            text = self.editor.toPlainText()
            f.write(text)
    
    def fileOpening(self):
        name = QtGui.QFileDialog.getOpenFileName(self, "Open file")
        with open(name, "r") as f:
            text = f.read()
            self.editor.setText(text)
    
    def home(self):
        self.progLang = QtGui.QLabel("Language", self)
        # looks nice doesn't do anything
        comboBox = QtGui.QComboBox(self)
        comboBox.addItem("C")
        comboBox.addItem("C++")
        comboBox.addItem("C#")
        comboBox.addItem("Java")
        comboBox.addItem("Python")
        
        # this also needs fixing in case of resining we don't want it to have a fixed position
        comboBox.move(650, 460)
        self.progLang.move(650, 440)
        comboBox.activated[str].connect(self.chosenLang)
        
        self.show()
    
    # NOTHING????? :(
    def chosenLang(self):
        print(self.progLang.selectedText())
        #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(text))
    
    # xD
    def resizeWindow(self):
        self.setGeometry(50, 50, 400, 400)
    
    def closeApp(self):
        choice = QtGui.QMessageBox.question(self, "Please don't leave", "Imala neko kuce gospodja se zvalo tako nesto?",
                                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.No:
            print("You've just exited Kate Perry and didn't get no reward :(")
            sys.exit()
        else:
            print("Congratulations you didn't quit Kate Perry, now you can have your reward")
            self.editor.setText("Imala neko kuče gospođa se zvalo tako nešto. I onda pošla pudlica ono u stan na vrata on pogleda šta će ona sad gola bila kupala se tako, pa uzne ogledalo, znaš ono providno, i stavi ispred nje i trči po ulicu. Gospodine si video tako nešto - ovaj pogleda ćutika, tep srela nekog ko mene gospodine si video tako nešto, kaže vido sam al tako uramljeno nesam.. i ona drži ogledalo ipred nju drži... hehehe")
            

app = QtGui.QApplication(sys.argv)
GUI = Window()
sys.exit(app.exec_())
