from PyQt4.QtGui import *
from PyQt4.QtCore import *

class HighlightingRule():
	def __init__(self, pattern, format):
		self.pattern = pattern
		self.format = format

class Highlighter(QSyntaxHighlighter):
	def __init__(self, parent = None):
		QSyntaxHighlighter.__init__( self, parent )
		keyword = QTextCharFormat()
		types = QTextCharFormat()
		pds = QTextCharFormat()
		pdext = QTextCharFormat() 
		comments = QTextCharFormat()
		consts = QTextCharFormat()
		mlComments = QTextCharFormat()
		bb = QTextCharFormat()

		self.highlightingRules = []

		# keyword
		keyword.setForeground(QBrush(Qt.darkRed, Qt.SolidPattern))
		keyword.setFontWeight(QFont.Bold)
		keywords = QStringList(["break", "else", "for", "if", "return", "switch", "case", "goto", "break", "continue", "label", "static", "extern", "const", "while"])
		for word in keywords:
			pattern = QRegExp(r"\b%s\b" % word)
			rule = HighlightingRule(pattern, keyword)
			self.highlightingRules.append(rule)
		
		# types
		types.setForeground(QBrush(Qt.darkGreen, Qt.SolidPattern))
		types.setFontWeight(QFont.Bold)
		typeList = QStringList(["int", "float", "double", "void", "char", "unsigned", "long", "signed", "short"])
		for word in typeList:
			pattern = QRegExp(r"\b%s\b" % word)
			rule = HighlightingRule(pattern, types)
			self.highlightingRules.append(rule)
			
		# preprocesor directives etc
		pdext.setForeground(QBrush(Qt.darkCyan, Qt.SolidPattern))
		pdext.setFontWeight(QFont.Bold)
		pattern = QRegExp(r"#\w* <[\w.]*>|\"[\w.]*\"|__\w+__")
		rule = HighlightingRule(pattern, pdext)
		self.highlightingRules.append(rule)
		
		# preprocesor directives
		pds.setForeground(QBrush(Qt.darkMagenta, Qt.SolidPattern))
		pds.setFontWeight(QFont.Bold)
		pattern = QRegExp(r"#\w*")
		rule = HighlightingRule(pattern, pds)
		self.highlightingRules.append(rule)
		
		# comments
		comments.setForeground(QBrush(Qt.lightGray, Qt.SolidPattern))
		pattern = QRegExp(r"//[^\n]*")
		rule = HighlightingRule(pattern, comments)
		self.highlightingRules.append(rule)
		
		# multiline comments
		mlComments.setForeground(QBrush(Qt.lightGray, Qt.SolidPattern))
		pattern = QRegExp(r"/[*](.|\n)*[*]/")
		rule = HighlightingRule(pattern, mlComments)
		self.highlightingRules.append(rule)
		
		# block brackets
		bb.setForeground(QBrush(Qt.magenta, Qt.SolidPattern))
		bb.setFontWeight(QFont.Bold)
		pattern = QRegExp(r"[{}]")
		rule = HighlightingRule(pattern, bb)
		self.highlightingRules.append(rule)
		
		# constants
		consts.setForeground(QBrush(Qt.darkCyan, Qt.SolidPattern))
		consts.setFontWeight(QFont.Bold)
		pattern = QRegExp(r"[+-]?[0-9]+([.][0-9]*)?|[+-]?[0-9]*([.][0-9]+)|\'\w\'")
		rule = HighlightingRule(pattern, consts)
		self.highlightingRules.append(rule)

	def highlightBlock( self, text ):
		for rule in self.highlightingRules:
			expression = QRegExp( rule.pattern )
			index = expression.indexIn( text )
			while index >= 0:
				length = expression.matchedLength()
				self.setFormat( index, length, rule.format )
				index = text.indexOf( expression, index + length )
		self.setCurrentBlockState( 0 )
