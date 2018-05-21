import sys
from PyQt4 import QtGui, QtCore

class Main(QtGui.QMainWindow):
	def __init__(self):
		# initializing the window using the super constructor
		super(Main, self).__init__()
		self.setGeometry(50, 50, 800, 500)
		self._name = None
		self.setWindowTitle("%s * Kate Perry" % self._name)
		self.setWindowIcon(QtGui.QIcon("katePerryIcon.jpg"))
	
		# dirty trick ;)
		self.line = 1
		self.col = 1
		
		# variables for keyboard events
		self.keylist = []
		self.firstrelease = False
		
		# set the text editor object on the window
		self.editor = QtGui.QTextEdit()
		self.setCentralWidget(self.editor)
		
		self.editor.cursorPositionChanged.connect(self.changeCursor)
		
		self.home()
		
	def updateWindowTitle(self):
		self.setWindowTitle("%s --- Kate Perry" % self._name)
	
	def changeCursor(self):
		cursorPos = self.editor.textCursor()
		
		self.line = cursorPos.blockNumber() + 1
		self.col = cursorPos.columnNumber() + 1
		
		# needs fixing, when the mouse is on File or Edit... this message doesn't appear
		self.statusbar.showMessage("Line %d, Column %d" % (self.line, self.col))
	
	def fileSavingAs(self):
		name = QtGui.QFileDialog.getSaveFileName(self, "Save file")
		self._name = name
			
		# needs to know if the current version of the file is saved
		with open(name, "w+") as f:
			text = self.editor.toPlainText()
			f.write(text)
			
		# fetches file name from absolute path
		self._name = name.split("/")[-1]
		self.updateWindowTitle()
	
	def fileSaving(self):
		if self._name == None:
			self.fileSavingAs()
			return
			
		# needs to know if the current version of the file is saved
		with open(self._name, "w+") as f:
			text = self.editor.toPlainText()
			f.write(text)
			
		# fetches file name from absolute path
		self._name = self._name.split("/")[-1]
		self.updateWindowTitle()
	
	def fileOpening(self):
		name = QtGui.QFileDialog.getOpenFileName(self, "Open file")
		with open(name, "r") as f:
			text = f.read()
			self.editor.setText(text)
		# fetches file name from absolute path
		self._name = name.split("/")[-1]
		self.updateWindowTitle()
		
	def fileCreating(self):
		name = None
		self.editor.setText("")
		self._name = name
		self.updateWindowTitle()
	
	def home(self):
		self.initStatusBar()
		self.initMenu()

		self.initFormatbar()
		
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
	
	def newFileAction(self):
		# new file action
		newFileAction = QtGui.QAction("New", self)
		newFileAction.setIcon(QtGui.QIcon('55.png'))
		newFileAction.setShortcut("Ctrl+N")
		newFileAction.setStatusTip("New File")
		newFileAction.triggered.connect(self.fileCreating)
		return newFileAction
	
	def openFileAction(self):
		# open file action
		openFileAction = QtGui.QAction("Open", self)
		openFileAction.setIcon(QtGui.QIcon('open.jpg'))
		openFileAction.setShortcut("Ctrl+O")
		openFileAction.setStatusTip("Open File")
		openFileAction.triggered.connect(self.fileOpening)
		return openFileAction
	
	def saveAsFileAction(self):
		# save as file action
		saveAsFileAction = QtGui.QAction("Save As", self)
		saveAsFileAction.setIcon(QtGui.QIcon('save_as.png'))
		saveAsFileAction.setStatusTip("Save File")
		saveAsFileAction.triggered.connect(self.fileSavingAs)
		return saveAsFileAction
	
	def saveFileAction(self):
		# save file action
		saveFileAction = QtGui.QAction("Save", self)
		saveFileAction.setIcon(QtGui.QIcon('save.png'))
		saveFileAction.setStatusTip("Save File")
		saveFileAction.triggered.connect(self.fileSaving)
		return saveFileAction
		
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
		copyAction = QtGui.QAction("Copy", self)
		copyAction.setShortcut("Ctrl+C")
		copyAction.triggered.connect(self.editor.copy)
		return copyAction
	
	def pasteAction(self):
		pasteAction = QtGui.QAction("Paste", self)
		pasteAction.setShortcut("Ctrl+V")
		pasteAction.triggered.connect(self.editor.paste)
		return pasteAction
	
	def cutAction(self):
		cutAction = QtGui.QAction("Cut", self)
		cutAction.setShortcut("Ctrl+X")
		cutAction.triggered.connect(self.editor.cut)
		return cutAction
	
	def selectAllAction(self):
		selectAllAction = QtGui.QAction("Select All", self)
		selectAllAction.setShortcut("Ctrl+A")
		selectAllAction.triggered.connect(self.editor.selectAll)
		return selectAllAction
	
	# keyboard event handler
	def keyPressEvent(self, event):
		# closing
		if event.key() == QtCore.Qt.Key_Escape:
			qmessage = QtGui.QMessageBox.question(self, "Quit Kate Perry", "Are you sure you want to quit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
			if qmessage == QtGui.QMessageBox.Yes:
				self.close()
			else:
				pass
		# multiple event listening
		else:
			self.firstrelease = True
			self.keylist.append(event.key())

	def keyReleaseEvent(self, event):
		if self.firstrelease == True: 
			self.processmultikeys(self.keylist)

		self.firstrelease = False
	# solves the problem of an ambiguous shortcut
	def processmultikeys(self,keyspressed):
		if QtCore.Qt.Key_Shift in keyspressed and QtCore.Qt.Key_S in keyspressed and QtCore.Qt.Key_Control in keyspressed:
			self.fileSavingAs()
		elif QtCore.Qt.Key_S in keyspressed and QtCore.Qt.Key_Control in keyspressed:
			self.fileSaving()
		self.keylist = []
	
	def initMenu(self):        
		# create the file drop menu and push all the actions in
		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu("File")
		fileMenu.addAction(self.newFileAction())
		fileMenu.addAction(self.openFileAction())
		fileMenu.addAction(self.saveFileAction())
		fileMenu.addAction(self.saveAsFileAction())
		fileMenu.addAction(self.exitAction())
		
		editMenu = mainMenu.addMenu("Edit")
		editMenu.addAction(self.undoAction())
		editMenu.addAction(self.redoAction())
		editMenu.addAction(self.copyAction())
		editMenu.addAction(self.pasteAction())
		editMenu.addAction(self.cutAction())
		editMenu.addAction(self.selectAllAction())	
		
		# TODO
		viewMenu = mainMenu.addMenu("View")
		
		# TODO
		optionsMenu = mainMenu.addMenu("Options")
		
	def initFormatbar(self):
		toolbar = self.addToolBar("Format")
		toolbar.addAction(self.newFileAction())
		toolbar.addAction(self.openFileAction())
		toolbar.addAction(self.saveFileAction())
		toolbar.addAction(self.saveAsFileAction())
		
	def closeApp(self):
		if self.editor.toPlainText() != "":
			choice = QtGui.QMessageBox.question(self, "Please don't leave", "Are you sure you want to leave without saving",
											QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
			if choice == QtGui.QMessageBox.Yes:
				sys.exit()
		else:
			sys.exit()

app = QtGui.QApplication(sys.argv)
GUI = Main()
sys.exit(app.exec_())
