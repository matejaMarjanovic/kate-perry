import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from pyqterm import TerminalWidget
from highlight import *

class Main(QMainWindow):
	def __init__(self):
		# standard initialization
		super(Main, self).__init__()
		self.setGeometry(50, 50, 800, 500)
		self._name = None
		self.setWindowTitle("%s * Kate Perry" % self._name)
		self.setWindowIcon(QIcon("katePerryIcon.jpg"))
		
		# initial theme
		self.setBasic()
		
		# for the staus bar
		self.line = 1
		self.col = 1
		
		# so the user can exit the app before he starts writing text
		self._currentSavedText = ""
		
		# set the text editor object on the window
		self.editor = QTextEdit()
		self.setCentralWidget(self.editor)
		self.editor.cursorPositionChanged.connect(self.changeCursor)
		
		self.highlighter = Highlighter(self.editor)
		
		self.home()
		
	def updateWindowTitle(self):
		self.setWindowTitle("%s --- Kate Perry" % self._name.split("/")[-1])
	
	def changeCursor(self):
		cursorPos = self.editor.textCursor()
		
		self.line = cursorPos.blockNumber() + 1
		self.col = cursorPos.columnNumber() + 1
		
		# needs fixing, when the mouse is on File or Edit... this message doesn't appear
		self.statusbar.showMessage("Line %d, Column %d" % (self.line, self.col))
	
	def fileSavingAs(self):
		name = QFileDialog.getSaveFileName(self, "Save file")
		self._name = name
			
		# needs to know if the current version of the file is saved
		with open(name, "w+") as f:
			text = self.editor.toPlainText()
			f.write(text)
			
		# fetches file name path
		self._currentSavedText = self.editor.toPlainText()
		self.updateWindowTitle()
	
	def fileSaving(self):
		if self._name == None:
			self.fileSavingAs()
			return
			
		# needs to know if the current version of the file is saved
		with open(self._name, "w+") as f:
			text = self.editor.toPlainText()
			f.write(text)
			
		self.updateWindowTitle()
		self._currentSavedText = self.editor.toPlainText()
	
	def fileOpening(self):
		name = QFileDialog.getOpenFileName(self, "Open file")
		with open(name, "r") as f:
			text = f.read()
			self.editor.setText(text)
		# fetches file name from absolute path
		self._currentSavedText = self.editor.toPlainText()
		self._name = name
		self.updateWindowTitle()
		
	def fileCreating(self):
		name = None
		self.editor.setText("")
		self._name = name
		self.updateWindowTitle()
		
	def htmlConversion(self):
		if self._name != None:
            # create a new file with a html extension
			htmlFileName = self._name.split(".")[0] + ".html"
			with open(htmlFileName, "w") as f:
				f.write(self.editor.toHtml())

	# go to console mode
	def termMode(self):
		self.terminal = TerminalWidget()
		self.setCentralWidget(self.terminal)
	
	# go to initial text edit mode
	def editMode(self):	
		self.editor = QTextEdit()
		self.setCentralWidget(self.editor)
		self.editor.cursorPositionChanged.connect(self.changeCursor)
		self.highlighter = Highlighter(self.editor)
	
	# theme
	def setDark(self):
		with open("./styles/dark.css", "r") as f:
			self.setStyleSheet(f.read())
	
	# theme
	def setSky(self):
		with open("./styles/sky.css", "r") as f:
			self.setStyleSheet(f.read())
	
	# theme
	def setBasic(self):
		with open("./styles/basic.css", "r") as f:
			self.setStyleSheet(f.read())
	
	# add the main features
	def home(self):
		self.initStatusBar()
		self.initMenu()
		self.initFormatbar()	
		self.show()
	
	def initStatusBar(self):
		self.statusbar = self.statusBar()
		# a dirty trick so that the program writes Line 1, Column 1 in the begging
		self.statusbar.showMessage("Line %d, Column %d" % (self.line, self.col))
		
		# does nothing :(
		self.languageList = QComboBox()
		self.languageList.addItems(["Plain Text", "C", "C++", "Java"])
		self.languageList.activated.connect(self.changeLanguage)
		self.statusbar.addPermanentWidget(self.languageList)
	
	def changeLanguage(self):
		# set the autocompletion for the chosen language
		print self.languageList.currentText()
	
	def newFileAction(self):
		# new file action
		newFileAction = QAction("New", self)
		newFileAction.setIcon(QIcon('./icons/55.png'))
		newFileAction.setShortcut("Ctrl+N")
		newFileAction.setStatusTip("New File")
		newFileAction.triggered.connect(self.fileCreating)
		return newFileAction
	
	def openFileAction(self):
		# open file action
		openFileAction = QAction("Open", self)
		openFileAction.setIcon(QIcon('./icons/open.jpg'))
		openFileAction.setShortcut("Ctrl+O")
		openFileAction.setStatusTip("Open File")
		openFileAction.triggered.connect(self.fileOpening)
		return openFileAction
	
	def saveAsFileAction(self):
		# save as file action
		saveAsFileAction = QAction("Save As", self)
		saveAsFileAction.setIcon(QIcon('./icons/save_as.png'))
		saveAsFileAction.setShortcut("Ctrl+Shift+S")
		saveAsFileAction.setStatusTip("Save As File")
		saveAsFileAction.triggered.connect(self.fileSavingAs)
		return saveAsFileAction
	
	def saveFileAction(self):
		# save file action
		saveFileAction = QAction("Save", self)
		saveFileAction.setIcon(QIcon('./icons/save.png'))
		saveFileAction.setShortcut("Ctrl+S")
		saveFileAction.setStatusTip("Save File")
		saveFileAction.triggered.connect(self.fileSaving)
		return saveFileAction
		
	def exitAction(self):
		# exit Kate Perry
		exitAction = QAction("Exit Kate Perry", self)
		exitAction.setShortcut("Ctrl+Q")
		exitAction.setStatusTip("Leave")
		exitAction.triggered.connect(self.closeApp)
		return exitAction
	
	def undoAction(self):
		undoAction = QAction("Undo", self)
		undoAction.setShortcut("Ctrl+Z")
		undoAction.setIcon(QIcon('./icons/undo.png'))
		undoAction.triggered.connect(self.editor.undo)
		return undoAction
	
	def redoAction(self):
		redoAction = QAction("Redo", self)
		redoAction.setShortcut("Ctrl+Shift+Z")
		redoAction.setIcon(QIcon('./icons/redo.png'))
		redoAction.triggered.connect(self.editor.redo)
		return redoAction
	
	def copyAction(self):
		copyAction = QAction("Copy", self)
		copyAction.setShortcut("Ctrl+C")
		copyAction.triggered.connect(self.editor.copy)
		return copyAction
	
	def pasteAction(self):
		pasteAction = QAction("Paste", self)
		pasteAction.setShortcut("Ctrl+V")
		pasteAction.triggered.connect(self.editor.paste)
		return pasteAction
	
	def cutAction(self):
		cutAction = QAction("Cut", self)
		cutAction.setShortcut("Ctrl+X")
		cutAction.triggered.connect(self.editor.cut)
		return cutAction
	
	def selectAllAction(self):
		selectAllAction = QAction("Select All", self)
		selectAllAction.setShortcut("Ctrl+A")
		selectAllAction.triggered.connect(self.editor.selectAll)
		return selectAllAction
	
	def htmlAction(self):
		htmlAction = QAction("Export to HTML", self)
		htmlAction.triggered.connect(self.htmlConversion)
		return htmlAction
	
	def terminalAction(self):
		terminalAction = QAction("Terminal Mode", self)
		terminalAction.triggered.connect(self.termMode)
		return terminalAction
    
	def editAction(self):
		editAction = QAction("Edit Mode", self)
		editAction.triggered.connect(self.editMode)
		return editAction
	
	def darkAction(self):
		darkAction = QAction("Dark", self)
		darkAction.triggered.connect(self.setDark)
		return darkAction
	
	def skyAction(self):
		skyAction = QAction("Sky Blue", self)
		skyAction.triggered.connect(self.setSky)
		return skyAction
	
	def basicAction(self):
		basicAction = QAction("Basic", self)
		basicAction.triggered.connect(self.setBasic)
		return basicAction
	
	def initMenu(self):        
		# create the file drop menu and push all the actions in
		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu("File")
		self._newFile = self.newFileAction()
		self._openFile = self.openFileAction()
		self._saveFile = self.saveFileAction()
		self._saveAsFile = self.saveAsFileAction()
		fileMenu.addAction(self._newFile)
		fileMenu.addAction(self._openFile)
		fileMenu.addAction(self._saveFile)
		fileMenu.addAction(self._saveAsFile)
		fileMenu.addAction(self.exitAction())
		
		editMenu = mainMenu.addMenu("Edit")
		self._undo = self.undoAction()
		self._redo = self.redoAction()
		editMenu.addAction(self._undo)
		editMenu.addAction(self._redo)
		editMenu.addAction(self.copyAction())
		editMenu.addAction(self.pasteAction())
		editMenu.addAction(self.cutAction())
		editMenu.addAction(self.selectAllAction())	
		
		optionsMenu = mainMenu.addMenu("Options")
		optionsMenu.addAction(self.htmlAction())
		optionsMenu.addAction(self.terminalAction())
		optionsMenu.addAction(self.editAction())
		
		appearancesMenu = mainMenu.addMenu("Appearances")
		appearancesMenu.addAction(self.basicAction())
		appearancesMenu.addAction(self.darkAction())
		appearancesMenu.addAction(self.skyAction())
		
	def initFormatbar(self):
		toolbar = self.addToolBar("Format")
		# the same variables like in the initMenu function, so shortcuts wouldn't be ambigous
		toolbar.addAction(self._newFile)
		toolbar.addAction(self._openFile)
		toolbar.addSeparator()
		toolbar.addAction(self._saveFile)
		toolbar.addAction(self._saveAsFile)
		toolbar.addSeparator()
		toolbar.addAction(self._undo)
		toolbar.addAction(self._redo)
		
	def closeApp(self):
		if self.editor.toPlainText() != self._currentSavedText:
			choice = QMessageBox.question(self, "Please don't leave", "Are you sure you want to leave without saving",
											QMessageBox.Yes, QMessageBox.No)
			if choice == QMessageBox.Yes:
				sys.exit()
		else:
			sys.exit()

app = QApplication(sys.argv)
GUI = Main()
sys.exit(app.exec_())
