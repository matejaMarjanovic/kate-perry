import sys
from PyQt4 import QtGui, QtCore

class Main(QtGui.QMainWindow):
    def __init__(self):
        # initializing the window using the super constructor
        super(Main, self).__init__()
        self.setGeometry(50, 50, 800, 500)
        self.setWindowTitle("Kate Perry")
        self.setWindowIcon(QtGui.QIcon("katePerryIcon.jpg"))
        
        
        self._name = None
        # dirty trick ;)
        self.line = 1
        self.col = 1
        
        # set the text editor object on the window
        self.editor = QtGui.QTextEdit()
        self.setCentralWidget(self.editor)
        
        self.editor.cursorPositionChanged.connect(self.changeCursor)
        
        self.home()
    
    def changeCursor(self):
        cursorPos = self.editor.textCursor()
        
        self.line = cursorPos.blockNumber() + 1
        self.col = cursorPos.columnNumber() + 1
        
        # needs fixing, when the mouse is on File or Edit... this message doesn't appear
        self.statusbar.showMessage("Line %d, Column %d" % (self.line, self.col))
    
    def fileSavingAs(self):
        name = QtGui.QFileDialog.getSaveFileName(self, "Save file")
            
        # needs to know if the current version of the file is saved
        with open(name, "w+") as f:
            text = self.editor.toPlainText()
            f.write(text)
    
    def fileSaving(self):
        if self._name == None:
            self.fileSavingAs()
            return
            
        # needs to know if the current version of the file is saved
        with open(self._name, "w+") as f:
            text = self.editor.toPlainText()
            f.write(text)
    
    def fileOpening(self):
        name = QtGui.QFileDialog.getOpenFileName(self, "Open file")
        with open(name, "r") as f:
            text = f.read()
            self.editor.setText(text)
        self._name = name
    
    def home(self):
        self.initStatusBar()
        self.initMenu()

        # nothing for now, maybe we will add icons like Open, New, Save...
        #self.formatbar = self.addToolBar("Format")
        
        self.show()
    
    def initStatusBar(self):
        self.statusbar = self.statusBar()
        # a dirty trick so that the program writes Line 1, Column 1 in the begging
        self.statusbar.showMessage("Line %d, Column %d" % (self.line, self.col))
        self.languageList = QtGui.QComboBox()
        self.languageList.addItems(["Plain Text", "C", "C++", "Java"])
        self.languageList.activated.connect(self.changeLanguage)
        self.statusbar.addPermanentWidget(self.languageList)
    
    # probably only one of these will have autocompletion for now
    def changeLanguage(self):
        # set the autocompletion for the chosen language
        print self.languageList.currentText()
    
    def openFileAction(self):
        # open file action
        openFileAction = QtGui.QAction("Open", self)
        openFileAction.setShortcut("Ctrl+O")
        openFileAction.setStatusTip("Open File")
        openFileAction.triggered.connect(self.fileOpening)
        return openFileAction
    
    def saveFileAction(self):
        # save file action
        saveFileAction = QtGui.QAction("Save", self)
        saveFileAction.setShortcut("Ctrl+S")
        saveFileAction.setStatusTip("Save File")
        saveFileAction.triggered.connect(self.fileSaving)
        return saveFileAction
    
    def saveAsFileAction(self):
        # save as file action
        saveAsFileAction = QtGui.QAction("Save As", self)
        saveAsFileAction.setStatusTip("Save File")
        saveAsFileAction.triggered.connect(self.fileSavingAs)
        return saveAsFileAction
        
    def exitAction(self):
        # exit Kate Perry
        exitAction = QtGui.QAction("Exit Kate Perry", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Leave")
        exitAction.triggered.connect(self.closeApp)
        return exitAction
    
    def undoAction(self):
        undoAction = QtGui.QAction("Undo", self)
        undoAction.setShortcut("Ctrl+Z")
        undoAction.triggered.connect(self.editor.undo)
        return undoAction
    
    def redoAction(self):
        redoAction = QtGui.QAction("Redo", self)
        redoAction.setShortcut("Ctrl+Shift+Z")
        redoAction.triggered.connect(self.editor.redo)
        return redoAction
    
    def copyAction(self):
        copyAction = QtGui.QAction("Copy to clipboard", self)
        copyAction.setShortcut("Ctrl+C")
        copyAction.triggered.connect(self.editor.copy)
        return copyAction
    
    def pasteAction(self):
        pasteAction = QtGui.QAction("Paste from clipboard", self)
        pasteAction.setShortcut("Ctrl+C")
        pasteAction.triggered.connect(self.editor.paste)
        return pasteAction
    
    def initMenu(self):        
        # create the file drop menu and push all the actions in
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        fileMenu.addAction(self.openFileAction())
        fileMenu.addAction(self.saveFileAction())
        fileMenu.addAction(self.saveAsFileAction())
        fileMenu.addAction(self.exitAction())
        
        editMenu = mainMenu.addMenu("Edit")
        editMenu.addAction(self.undoAction())
        editMenu.addAction(self.redoAction())
        editMenu.addAction(self.copyAction())
        editMenu.addAction(self.pasteAction())
        
        # TODO
        viewMenu = mainMenu.addMenu("View")
        
        # TODO
        optionsMenu = mainMenu.addMenu("Options")
        
    def closeApp(self):
        if self.editor.toPlainText() != "":
            choice = QtGui.QMessageBox.question(self, "Please don't leave", "Are you sure you want to leave without saving",
                                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if choice == QtGui.QMessageBox.Yes:
                print("You've just exited Kate Perry and didn't get no reward :(")
                sys.exit()
            else:
                print("Congratulations you didn't quit Kate Perry, now you can have your reward")
        else:
            sys.exit()

app = QtGui.QApplication(sys.argv)
GUI = Main()
sys.exit(app.exec_())
