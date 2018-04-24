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
        
        # set the text editor object on the window
        self.editor = QtGui.QTextEdit()
        self.setCentralWidget(self.editor)
        
        self.editor.cursorPositionChanged.connect(self.changeCursor)
        
        self.home()
    
    def changeCursor(self):
        cursorPos = self.editor.textCursor()
        
        line = cursorPos.blockNumber() + 1
        col = cursorPos.columnNumber() + 1
        
        self.statusbar.showMessage("Line %d, Column %d" % (line, col))
    
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
        self.initMenu()
        self.statusbar = self.statusBar()
        
        self.formatbar = self.addToolBar("Format")
        
        self.show()
    
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
    
    def initMenu(self):
        # add actions to the file drop menu
        
        # file actions
        openFileAction = self.openFileAction()
        saveFileAction = self.saveFileAction()
        saveAsFileAction = self.saveAsFileAction()
        exitAction = self.exitAction()
        
        # edit actions
        undoAction = self.undoAction()
        redoAction = self.redoAction()
        
        # now create the file drop menu and push all the actions in
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        fileMenu.addAction(openFileAction)
        fileMenu.addAction(saveFileAction)
        fileMenu.addAction(saveAsFileAction)
        fileMenu.addAction(exitAction)
        
        editMenu = mainMenu.addMenu("Edit")
        editMenu.addAction(undoAction)
        editMenu.addAction(redoAction)
        
        viewMenu = mainMenu.addMenu("View")
        
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
