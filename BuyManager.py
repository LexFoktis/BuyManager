# v.03.05.2019
# NOTE: Оптимизированно меню, убран лишний код.
# NOTE: Настроены атрибуты
# NOTE: ВОзможно загружать приложения
# NOTE: Все атрибуты выгружаются в Word шаблон
# NOTE: Все изображения выгружаются в Word документ последовательно
# NOTE: Добавлено окно с бюджетным планом
# NOTE: Коннект к базе

# TODO: Добавить механизм выбора элемента из таблицы и автоматического проставления в ячейки

from PyQt5 import QtCore, QtGui, QtWidgets
from docxtpl import DocxTemplate, InlineImage
from docx import Document
from docx.shared import Mm  # Размеры в Word документе в миллиметрах
from docx.enum.text import WD_ALIGN_PARAGRAPH  # выравнивание
import simplejson as json  # Серриализация данных
import collections  # Подключение коллекций для использования Counter()
import sqlite3  # Работа с базой данных SQLite
import xlrd
import sys
import io
import decimal


# ГЛАВНОЕ ОКНО
class Ui_MainWindow():
	# УСТАНОВКА ГРАФИКИ
	def setupUi(self, MainWindow):
		MainWindow.setWindowModality(QtCore.Qt.NonModal)
		MainWindow.setEnabled(True)
		MainWindow.resize(700, 700)
		MainWindow.setMinimumSize(QtCore.QSize(700, 700))

		# ПАРАМЕТРЫ ШРИФТА
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)

		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)

		# СОЗДАЕМ СКРУЛ БЛОК
		self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
		self.scrollArea.setWidgetResizable(True)
		self.scrollAreaWidgetContents = QtWidgets.QWidget()

		self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
		self.gridLayout_3 = QtWidgets.QGridLayout()
		self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
		self.gridLayout_3.setContentsMargins(5, 5, 5, 5)
		self.gridLayout_3.setHorizontalSpacing(20)
		self.gridLayout_3.setVerticalSpacing(10)
		self.gridLayout.addLayout(self.gridLayout_3, 0, 0, 1, 1)
		self.scrollArea.setWidget(self.scrollAreaWidgetContents)
		self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
		MainWindow.setCentralWidget(self.centralwidget)

		# РАЗДЕЛИТЕЛЬНЫЕ ЛИНИИ
		self.line = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line.setFrameShape(QtWidgets.QFrame.HLine)
		self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.gridLayout_3.addWidget(self.line, 6, 0, 1, 4)
		self.line_1 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.gridLayout_3.addWidget(self.line_1, 10, 0, 1, 4)
		self.line_2 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.gridLayout_3.addWidget(self.line_2, 16, 0, 1, 4)

		# ВКЛАДКИ ДЛЯ ФИН. АНАЛИТИК--------------------------------------------
		self.finTabs = []
		self.tabWidget = QtWidgets.QTabWidget(self.scrollAreaWidgetContents)
		self.gridLayout_3.addWidget(self.tabWidget, 11, 0, 5, 4)
		n = 0

		for tab in range(1):
			self.finTabs.append((
				QtWidgets.QWidget(), QtWidgets.QLabel(), QtWidgets.QLabel(),
				QtWidgets.QLabel(), QtWidgets.QLabel(), QtWidgets.QLabel(),
				QtWidgets.QPlainTextEdit(), QtWidgets.QPlainTextEdit(),
				QtWidgets.QPlainTextEdit(), QtWidgets.QPlainTextEdit(),
				QtWidgets.QPlainTextEdit(), QtWidgets.QPushButton()))
		for item in self.finTabs:
			n += 1
			self.tabWidget.addTab(item[0], "№" + str(n))
			self.fingridLayout = QtWidgets.QGridLayout(item[0])

			item[1].setParent(item[0])
			item[1].setMinimumSize(QtCore.QSize(190, 25))
			item[1].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
			self.fingridLayout.addWidget(item[1], 0, 0, 1, 1)
			item[1].setText("Источник финансирования")
			item[1].setFont(font)

			item[2].setParent(item[0])
			item[2].setMinimumSize(QtCore.QSize(190, 25))
			item[2].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
			self.fingridLayout.addWidget(item[2], 1, 0, 1, 1)
			item[2].setText("ЦФО")
			item[2].setFont(font)

			item[3].setParent(item[0])
			item[3].setMinimumSize(QtCore.QSize(190, 25))
			item[3].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
			self.fingridLayout.addWidget(item[3], 2, 0, 1, 1)
			item[3].setText("МВЗ")
			item[3].setFont(font)

			item[4].setParent(item[0])
			item[4].setMinimumSize(QtCore.QSize(190, 25))
			item[4].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
			self.fingridLayout.addWidget(item[4], 3, 0, 1, 1)
			item[4].setText("Проект")
			item[4].setFont(font)

			item[5].setParent(item[0])
			item[5].setMinimumSize(QtCore.QSize(190, 25))
			item[5].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
			self.fingridLayout.addWidget(item[5], 4, 0, 1, 1)
			item[5].setText("Статья ДДС")
			item[5].setFont(font)

			item[6].setParent(item[0])
			item[6].setObjectName("Tab_1_Источник_финансирования")
			item[6].setMinimumSize(QtCore.QSize(0, 25))
			item[6].setMaximumSize(QtCore.QSize(16777215, 25))
			self.fingridLayout.addWidget(item[6], 0, 1, 1, 3)

			item[7].setParent(item[0])
			item[7].setObjectName("Tab_1_ЦФО")
			item[7].setMinimumSize(QtCore.QSize(0, 25))
			item[7].setMaximumSize(QtCore.QSize(16777215, 25))
			self.fingridLayout.addWidget(item[7], 1, 1, 1, 3)

			item[8].setParent(item[0])
			item[8].setObjectName("Tab_1_МВЗ")
			item[8].setMinimumSize(QtCore.QSize(0, 75))
			item[8].setMaximumSize(QtCore.QSize(16777215, 75))
			self.fingridLayout.addWidget(item[8], 2, 1, 1, 1)

			item[9].setParent(item[0])
			item[9].setObjectName("Tab_1_Проект")
			item[9].setMinimumSize(QtCore.QSize(0, 25))
			item[9].setMaximumSize(QtCore.QSize(16777215, 25))
			self.fingridLayout.addWidget(item[9], 3, 1, 1, 3)

			item[10].setParent(item[0])
			item[10].setObjectName("Tab_1_Статья_ДДС")
			item[10].setMinimumSize(QtCore.QSize(0, 25))
			item[10].setMaximumSize(QtCore.QSize(16777215, 25))
			self.fingridLayout.addWidget(item[10], 4, 1, 1, 3)

			item[11].setParent(item[0])
			item[11].setMinimumSize(QtCore.QSize(0, 25))
			item[11].setMaximumSize(QtCore.QSize(16777215, 25))
			self.fingridLayout.addWidget(item[11], 2, 3, 1, 1)
			item[11].setText("Выбрать")
			item[11].clicked.connect(MVZWindow.show)
		# ----------------------------------------------------------------------

		# ЧЕК БОКС
		self.checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
		self.gridLayout_3.addWidget(self.checkBox, 17, 3, 2, 1)

		# КОМБО БОКСЫ
		self.comboBox_0 = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
		self.comboBox_0.addItem("")
		self.comboBox_0.addItem("")
		self.gridLayout_3.addWidget(self.comboBox_0, 0, 1, 1, 3)

		self.comboBox_1 = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
		self.comboBox_1.addItem("")
		self.comboBox_1.addItem("")
		self.gridLayout_3.addWidget(self.comboBox_1, 7, 1, 1, 3)
		self.comboBox_2 = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
		self.comboBox_2.setMaximumSize(QtCore.QSize(50, 16777215))
		self.comboBox_2.addItem("")
		self.comboBox_2.addItem("")
		self.comboBox_2.addItem("")
		self.gridLayout_3.addWidget(self.comboBox_2, 17, 2, 2, 1)

		self.comboBox_3 = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
		self.comboBox_3.addItem("")
		self.comboBox_3.addItem("")
		self.comboBox_3.addItem("")
		self.gridLayout_3.addWidget(self.comboBox_3, 9, 1, 1, 3)

		# ГРУПП БОКС ДЛЯ ПРИЛОЖЕНИЙ
		self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
		self.groupBox.setMinimumSize(QtCore.QSize(0, 200))
		self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
		self.gridLayout_3.addWidget(self.groupBox, 23, 0, 1, 4)

		# ВЫПАДАЮЩЕЕ МЕНЮ
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menu = QtWidgets.QMenu(self.menubar)
		self.filemenu = QtWidgets.QMenu(self.menubar)
		MainWindow.setMenuBar(self.menubar)

		self.action_Word = QtWidgets.QAction(MainWindow)
		self.action_Word.triggered.connect(self.exportToWord)
		self.action_PDF = QtWidgets.QAction(MainWindow)
		self.action_load = QtWidgets.QAction(MainWindow)
		self.action_save = QtWidgets.QAction(MainWindow)

		self.action_Exit = QtWidgets.QAction(MainWindow)
		self.action_Exit.triggered.connect(MainWindow.close)
		self.open_PPV = QtWidgets.QAction(MainWindow)
		self.open_PPV.triggered.connect(self.openppv)
		self.action_save.triggered.connect(self.saveFile)

		# ПРИВЯЗЫВАЕМ КОМАНДЫ К МЕНЮ
		self.menu.addAction(self.action_Word)
		self.menu.addAction(self.action_PDF)
		self.menu.addAction(self.open_PPV)
		self.filemenu.addAction(self.action_load)
		self.filemenu.addAction(self.action_save)
		self.filemenu.addSeparator()
		self.filemenu.addAction(self.action_Exit)
		self.menubar.addAction(self.filemenu.menuAction())
		self.menubar.addAction(self.menu.menuAction())

		# СОЗДАЕМ КНОПКИ
		self.pushButton_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
		self.gridLayout_3.addWidget(self.pushButton_2, 3, 3, 1, 1)
		self.pushButton_2.clicked.connect(LotWindow.show)  # открываем окно с лотами в бюджете

		self.pushButton_3 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
		self.gridLayout_3.addWidget(self.pushButton_3, 4, 3, 1, 1)
		self.pushButton_3.clicked.connect(ContactsWindow.show)  # открываем окно с контактами контрагентов

		self.pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
		self.pushButton.clicked.connect(self.showDialog)  # открываем диалоговое меню загрузки приложений
		self.gridLayout_3.addWidget(self.pushButton, 22, 0, 1, 4)

		# СОЗДАЕМ ЛЕЙБЛЫ
		n = 0
		self.labels = []
		while n <= 19:
			self.labels.append(QtWidgets.QLabel(self.scrollAreaWidgetContents))
			self.labels[n - 1].setFont(font)
			self.labels[n - 1].setLayoutDirection(QtCore.Qt.LeftToRight)
			self.labels[n - 1].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
			self.labels[n - 1].setMaximumSize(QtCore.QSize(190, 16777215))
			self.gridLayout_3.addWidget(self.labels[n - 1], (n - 1), 0, 1, 1)
			n += 1
		{  # Позиция для labels
			self.gridLayout_3.addWidget(self.labels[0], 0, 0, 1, 1),
			self.gridLayout_3.addWidget(self.labels[1], 1, 0, 1, 1),
			self.gridLayout_3.addWidget(self.labels[2], 2, 0, 1, 1),
			self.gridLayout_3.addWidget(self.labels[3], 3, 0, 1, 1),
			self.gridLayout_3.addWidget(self.labels[4], 4, 0, 1, 1),
			self.gridLayout_3.addWidget(self.labels[5], 5, 0, 1, 1),
			self.gridLayout_3.addWidget(self.labels[6], 7, 0, 1, 1),
			self.gridLayout_3.addWidget(self.labels[7], 8, 0, 1, 1),
			self.gridLayout_3.addWidget(self.labels[8], 9, 0, 1, 1),
			self.gridLayout_3.addWidget(self.labels[9], 11, 0, 1, 1),
			self.gridLayout_3.addWidget(self.labels[10], 12, 0, 1, 1),
			self.gridLayout_3.addWidget(self.labels[11], 13, 0, 1, 1),
			self.gridLayout_3.addWidget(self.labels[12], 14, 0, 1, 1),
			self.gridLayout_3.addWidget(self.labels[13], 15, 0, 1, 1),
			self.gridLayout_3.addWidget(self.labels[14], 17, 0, 1, 1),
			self.gridLayout_3.addWidget(self.labels[15], 18, 0, 1, 1),
			self.gridLayout_3.addWidget(self.labels[16], 19, 0, 1, 1),
			self.gridLayout_3.addWidget(self.labels[17], 20, 0, 1, 1),
			self.gridLayout_3.addWidget(self.labels[18], 21, 0, 1, 1)}

		self.labels[9].setVisible(0)
		self.labels[10].setVisible(0)
		self.labels[11].setVisible(0)
		self.labels[12].setVisible(0)
		self.labels[13].setVisible(0)

		# СОЗДАЕМ ТЕКСТОВЫЕ ПОЛЯ
		n2 = 0
		self.texts = []
		while n2 <= 17:
			self.texts.append(QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents))
			n2 += 1
		{  # Позиция для texts
			self.gridLayout_3.addWidget(self.texts[0], 0, 1, 1, 3),
			self.gridLayout_3.addWidget(self.texts[1], 1, 1, 1, 3),
			self.gridLayout_3.addWidget(self.texts[2], 2, 1, 1, 3),
			self.gridLayout_3.addWidget(self.texts[3], 3, 1, 1, 2),
			self.gridLayout_3.addWidget(self.texts[4], 4, 1, 1, 2),
			self.gridLayout_3.addWidget(self.texts[5], 5, 1, 1, 3),
			self.gridLayout_3.addWidget(self.texts[6], 8, 1, 1, 3),
			self.gridLayout_3.addWidget(self.texts[7], 16, 1, 1, 3),
			self.gridLayout_3.addWidget(self.texts[8], 11, 1, 1, 3),
			self.gridLayout_3.addWidget(self.texts[9], 12, 1, 1, 3),
			self.gridLayout_3.addWidget(self.texts[10], 13, 1, 1, 2),
			self.gridLayout_3.addWidget(self.texts[11], 14, 1, 1, 3),
			self.gridLayout_3.addWidget(self.texts[12], 15, 1, 1, 3),
			self.gridLayout_3.addWidget(self.texts[13], 17, 1, 1, 1),
			self.gridLayout_3.addWidget(self.texts[14], 18, 1, 1, 1),
			self.gridLayout_3.addWidget(self.texts[15], 19, 1, 1, 3),
			self.gridLayout_3.addWidget(self.texts[16], 20, 1, 1, 3),
			self.gridLayout_3.addWidget(self.texts[17], 21, 1, 1, 3)}
		{  # Размер для texts
			self.texts[0].setMinimumSize(QtCore.QSize(0, 25)),
			self.texts[1].setMinimumSize(QtCore.QSize(0, 25)),
			self.texts[2].setMinimumSize(QtCore.QSize(0, 25)),
			self.texts[3].setMinimumSize(QtCore.QSize(0, 25)),
			self.texts[4].setMinimumSize(QtCore.QSize(0, 25)),
			self.texts[5].setMinimumSize(QtCore.QSize(0, 50)),
			self.texts[6].setMinimumSize(QtCore.QSize(0, 25)),
			self.texts[7].setMinimumSize(QtCore.QSize(0, 25)),
			self.texts[8].setMinimumSize(QtCore.QSize(0, 25)),
			self.texts[9].setMinimumSize(QtCore.QSize(0, 25)),
			self.texts[10].setMinimumSize(QtCore.QSize(0, 75)),
			self.texts[11].setMinimumSize(QtCore.QSize(0, 25)),
			self.texts[12].setMinimumSize(QtCore.QSize(0, 25)),
			self.texts[13].setMinimumSize(QtCore.QSize(0, 25)),
			self.texts[14].setMinimumSize(QtCore.QSize(0, 25)),
			self.texts[15].setMinimumSize(QtCore.QSize(0, 25)),
			self.texts[16].setMinimumSize(QtCore.QSize(0, 25)),
			self.texts[17].setMinimumSize(QtCore.QSize(0, 80))}
		self.texts[0].setVisible(0)
		self.texts[7].setVisible(0)
		for item in self.texts:
			item.setPlainText(str(self.texts.index(item)))

		self.texts[8].setVisible(0)
		self.texts[9].setVisible(0)
		self.texts[10].setVisible(0)
		self.texts[11].setVisible(0)
		self.texts[12].setVisible(0)

		# СОЗДАЕМ ЛЕЙБЛЫ ДЛЯ ПРИЛОЖЕЙНИ
		n3 = 0
		self.AppLabels = []
		while n3 < 5:
			self.AppLabels.append(QtWidgets.QPlainTextEdit(self.groupBox))
			# self.AppLabels[n3-1].setScaledContents(True)
			self.gridLayout_4.addWidget(self.AppLabels[n3], (n3), 0, 1, 1)
			n3 += 1

		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		# ЗАПУСКАЕМ КОНТЕКСТНОЕ МЕНЮ
		self.tabWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.tabWidget.customContextMenuRequested.connect(self.showMenu)

	# ЗАПУСКАЕМ КОНТЕКСТНОЕ МЕНЮ
	def showMenu(self, event):
		contextMenu = QtWidgets.QMenu(MainWindowMC)
		contextMenu.addAction("Добавить аналитики", self.addTabFin)
		contextMenu.addAction("Удалить аналитики", self.deletTabFin)
		action = contextMenu.exec_(self.tabWidget.mapToGlobal(event))

	# ДОБАВЛЯЕМ ВКЛАДКУ АНАЛИТИКОВ ИЗ КОНТЕКСТНОГО МЕНЮ
	def addTabFin(self):
		# ВКЛАДКИ ДЛЯ ФИН. АНАЛИТИК

		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		n = 0
		TabNumber = 1
		ui.finTabs.append((
			QtWidgets.QWidget(), QtWidgets.QLabel(), QtWidgets.QLabel(),
			QtWidgets.QLabel(), QtWidgets.QLabel(), QtWidgets.QLabel(),
			QtWidgets.QPlainTextEdit(), QtWidgets.QPlainTextEdit(),
			QtWidgets.QPlainTextEdit(), QtWidgets.QPlainTextEdit(),
			QtWidgets.QPlainTextEdit(), QtWidgets.QPushButton()))

		for item in ui.finTabs:
			n += 1
			if n == len(ui.finTabs):
				TabNumber += 1
				ui.tabWidget.addTab(item[0], "№" + str(n))
				self.fingridLayout = QtWidgets.QGridLayout(item[0])

				item[1].setParent(item[0])
				item[1].setMinimumSize(QtCore.QSize(190, 25))
				item[1].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
				ui.fingridLayout.addWidget(item[1], 0, 0, 1, 1)

				item[1].setText("Источник финансирования")
				item[1].setFont(font)

				item[2].setParent(item[0])
				item[2].setMinimumSize(QtCore.QSize(190, 25))
				item[2].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
				ui.fingridLayout.addWidget(item[2], 1, 0, 1, 1)
				item[2].setText("ЦФО")
				item[2].setFont(font)

				item[3].setParent(item[0])
				item[3].setMinimumSize(QtCore.QSize(190, 25))
				item[3].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
				ui.fingridLayout.addWidget(item[3], 2, 0, 1, 1)
				item[3].setText("МВЗ")
				item[3].setFont(font)

				item[4].setParent(item[0])
				item[4].setMinimumSize(QtCore.QSize(190, 25))
				item[4].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
				ui.fingridLayout.addWidget(item[4], 3, 0, 1, 1)
				item[4].setText("Проект")
				item[4].setFont(font)

				item[5].setParent(item[0])
				item[5].setMinimumSize(QtCore.QSize(190, 25))
				item[5].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
				ui.fingridLayout.addWidget(item[5], 4, 0, 1, 1)
				item[5].setText("Статья ДДС")
				item[5].setFont(font)

				item[6].setParent(item[0])
				item[6].setObjectName("Tab_" + str(n) + "_Источник_финансирования")
				item[6].setMinimumSize(QtCore.QSize(0, 25))
				item[6].setMaximumSize(QtCore.QSize(16777215, 25))
				ui.fingridLayout.addWidget(item[6], 0, 1, 1, 3)

				item[7].setParent(item[0])
				item[7].setObjectName("Tab_" + str(n) + "_ЦФО")
				item[7].setMinimumSize(QtCore.QSize(0, 25))
				item[7].setMaximumSize(QtCore.QSize(16777215, 25))
				ui.fingridLayout.addWidget(item[7], 1, 1, 1, 3)

				item[8].setParent(item[0])
				item[8].setObjectName("Tab_" + str(n) + "_МВЗ")
				item[8].setMinimumSize(QtCore.QSize(0, 75))
				item[8].setMaximumSize(QtCore.QSize(16777215, 75))
				ui.fingridLayout.addWidget(item[8], 2, 1, 1, 1)

				item[9].setParent(item[0])
				item[9].setObjectName("Tab_" + str(n) + "_Проект")
				item[9].setMinimumSize(QtCore.QSize(0, 25))
				item[9].setMaximumSize(QtCore.QSize(16777215, 25))
				ui.fingridLayout.addWidget(item[9], 3, 1, 1, 3)

				item[10].setParent(item[0])
				item[10].setObjectName("Tab_" + str(n) + "_Статья_ДДС")
				item[10].setMinimumSize(QtCore.QSize(0, 25))
				item[10].setMaximumSize(QtCore.QSize(16777215, 25))
				ui.fingridLayout.addWidget(item[10], 4, 1, 1, 3)

				item[11].setParent(item[0])
				item[11].setMinimumSize(QtCore.QSize(0, 25))
				item[11].setMaximumSize(QtCore.QSize(16777215, 25))
				ui.fingridLayout.addWidget(item[11], 2, 3, 1, 1)
				item[11].setText("Выбрать")
				item[11].clicked.connect(MVZWindow.show)
				ui.tabWidget.setCurrentIndex(n - 1)

				# self.finTabs[2][6].setObjectName("adfdfsd")

				for item in self.finTabs:
					print(item[6].objectName())

	# УДАЛЯЕМ ВКЛАДКУ АНАЛИТИКОВ ИЗ КОНТЕКСТНОГО МЕНЮ
	def deletTabFin(self):

		index = ui.tabWidget.currentIndex()
		if index != 0:
			for item in self.finTabs[index]:
				item.deleteLater()

			self.finTabs.pop(index)

	# ПРИСВАЕВАЕМ ТЕКСТ ОБЪЕКТАМ
	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle("Менеджер закупок")
		self.checkBox.setText("НДС 20%")

		self.comboBox_2.setItemText(0, "RUB")
		self.comboBox_2.setItemText(1, "USD")
		self.comboBox_2.setItemText(2, "EUR")
		self.comboBox_1.setItemText(0, "Да")
		self.comboBox_1.setItemText(1, "Нет")
		self.comboBox_0.setItemText(0, "НИПИГАЗ")
		self.comboBox_0.setItemText(1, "СИБУР")
		self.comboBox_3.setItemText(0, "Не требуются")
		self.comboBox_3.setItemText(1, "Требуютя")
		self.comboBox_3.setItemText(2, "Требуются (см. Приложения)")

		self.labels[16].setText("<html><head/><body><p>Уровень цен</p></body></html>")
		self.labels[18].setText("<html><head/><body><p>Решение о выборе</p></body></html>")
		self.labels[15].setText("<html><head/><body><p>Цена после переговоров</p></body></html>")
		self.labels[17].setText("<html><head/><body><p>Условия оплаты</p></body></html>")
		self.labels[6].setText(
			"<html><head/><body><p><span style=\" font-size:10pt;\">Соответствие требованиям </span></p></body></html>")
		self.labels[9].setText(
			"<html><head/><body><p><span style=\" font-size:10pt;\">Источник финансирования</span></p></body></html>")
		self.labels[3].setText(
			"<html><head/><body><p><span style=\" font-size:10pt;\">Лот из плана закупок </span></p></body></html>")
		self.labels[0].setText(
			"<html><head/><body><p><span style=\" font-size:10pt;\">Наименование предприятия / <br/>подразделения </span></p></body></html>")
		self.labels[4].setText(
			"<html><head/><body><p><span style=\" font-size:10pt;\">Контрагент </span></p></body></html>")
		self.labels[5].setText(
			"<html><head/><body><p><span style=\" font-size:10pt;\">Реквизиты контрагента </span></p></body></html>")
		self.labels[10].setText("<html><head/><body><p><span style=\" font-size:10pt;\">ЦФО</span></p></body></html>")
		self.labels[2].setText(
			"<html><head/><body><p><span style=\" font-size:10pt;\">Предмет закупки </span></p></body></html>")
		self.labels[1].setText(
			"<html><head/><body><p><span style=\" font-size:10pt;\">Функциональный заказчик </span></p></body></html>")
		self.labels[8].setText(
			"<html><head/><body><p><span style=\" font-size:10pt;\">Гарантийные обязательства</span></p></body></html>")
		self.labels[13].setText("<html><head/><body><p>Статья ДДС</p></body></html>")
		self.labels[14].setText("<html><head/><body><p>Цена до переговоров</p></body></html>")
		self.labels[11].setText("<html><head/><body><p><span style=\" font-size:10pt;\">МВЗ</span></p></body></html>")
		self.labels[7].setText(
			"<html><head/><body><p><span style=\" font-size:10pt;\">Срок поставки</span></p></body></html>")
		self.labels[12].setText("<html><head/><body><p>Проект</p></body></html>")

		self.filemenu.setTitle("Файл")
		self.action_load.setText("Открыть")
		self.action_save.setText("Сохранить")
		self.action_Exit.setText("Выход")
		self.menu.setTitle("Паспорт")
		self.action_Word.setText("Экспорт в Word")
		self.action_PDF.setText("Экспорт в PDF")
		self.open_PPV.setText("Паспорт прямого выбора")
		self.groupBox.setTitle("Приложения")
		self.pushButton_2.setText("Выбрать")
		self.pushButton_3.setText("Выбрать")
		self.pushButton.setText("Загрузить приложения")

	# ОТКРЫВАЕМ ДИАЛОГОВОЕ ОКНО ВЫБОРА ПРИЛОЖЕНИЙ
	def showDialog(self, MainWindow):
		filter = "Image (*.jpeg *.jpg *.png *.bmp)"  # определяем формат приложения
		fname = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', '/home', filter)
		for item in self.AppLabels:  # перебераем доступные лейблы для вставки приложения
			if item.toPlainText() == "":  # если лейбл доступен, вставляем приложение
				item.setPlainText(str(fname[0]))
				break

	# ЭКСПОРТ В WORD
	def exportToWord(self):

		# ВЫБИРАЕМ ШАБЛОН
		if ui.tabWidget.count() == 1:
			pmz = DocxTemplate("PMZ_template_1.docx")
		elif ui.tabWidget.count() == 2:
			pmz = DocxTemplate("PMZ_template_2.docx")
		elif ui.tabWidget.count() == 3:
			pmz = DocxTemplate("PMZ_template_3.docx")
		elif ui.tabWidget.count() == 4:
			pmz = DocxTemplate("PMZ_template_4.docx")
		elif ui.tabWidget.count() == 5:
			pmz = DocxTemplate("PMZ_template_5.docx")

		# ДОБАВЛЯЕМ ПОЛЯ
		pmz_variables = {
			'comboBox_0': self.comboBox_0.currentText(), 'comboBox_1': self.comboBox_1.currentText(),
			'comboBox_2': self.comboBox_2.currentText(), 'comboBox_3': self.comboBox_3.currentText(),
			'text_2': self.texts[1].toPlainText(), 'text_3': self.texts[2].toPlainText(),
			'text_4': self.texts[3].toPlainText(), 'text_5': self.texts[4].toPlainText(),
			'text_6': self.texts[5].toPlainText(), 'text_7': self.texts[6].toPlainText(),
			'text_8': self.texts[7].toPlainText(), 'text_9': self.texts[8].toPlainText(),
			'text_10': self.texts[9].toPlainText(), 'text_11': self.texts[10].toPlainText(),
			'text_12': self.texts[11].toPlainText(), 'text_13': self.texts[12].toPlainText(),
			'text_14': self.texts[13].toPlainText(), 'text_15': self.texts[14].toPlainText(),
			'text_16': self.texts[15].toPlainText(), 'text_17': self.texts[16].toPlainText(),
			'text_18': self.texts[17].toPlainText(),
		}  # создаем все переменные которые будем зановить в шаблон
		# создаем множество перем енных, которые будем заносить в шаблон
		for item in ui.finTabs:
			pmz_variables[item[6].objectName()] = item[6].toPlainText()
			pmz_variables[item[7].objectName()] = item[7].toPlainText()
			pmz_variables[item[8].objectName()] = item[8].toPlainText()
			pmz_variables[item[9].objectName()] = item[9].toPlainText()
			pmz_variables[item[10].objectName()] = item[10].toPlainText()

		pmz.render(pmz_variables)  # заносим в шаблон множество

		# ДОБАВЛЯЕМ ПРИЛОЖЕНИЯ
		nApp = 0  # создаем счетчик вставленных приложений
		for item in self.AppLabels:  # берем по очереди все поля в которые загружаются приложения
			if item.toPlainText() != "":  # Если поле не пустое:
				nApp += 1  # прибавляем +1 к счетчику приложений
				p = pmz.add_page_break()  # переходим на новую страницу
				p.alignment = WD_ALIGN_PARAGRAPH.RIGHT  # делаем выравнивание по правому краю
				r = p.add_run()  # создаем бегунок
				r.bold = True  # жирный шрифт у бегунка
				r.add_text('ПРИЛОЖЕНИЕ' + ' ' + str(nApp))  # вводим текст
				r.add_picture(item.toPlainText(), width=Mm(170))  # вставляем приложение
		pmz.save("PMZ.docx")  # сохранчем полученный документ

	# СОХРАНЯЕМ ДОКУМЕНТ
	def saveFile(self):
		fname = QtWidgets.QFileDialog.getSaveFileName(None, 'Сохранить', 'Паспорт малоценной закупки', 'txt(*.txt)')
		myfile = open(fname[0], 'w', encoding='utf-8')
		allTextBox = {
			'self.texts[0]': self.texts[0].toPlainText(),
			'self.texts[1]': self.texts[1].toPlainText(),
			'self.texts[2]': self.texts[2].toPlainText(),
			'self.texts[3]': self.texts[3].toPlainText(),
			'self.texts[4]': self.texts[4].toPlainText(),
			'self.texts[5]': self.texts[5].toPlainText(),
			'self.texts[6]': self.texts[6].toPlainText(),
			'self.texts[7]': self.texts[7].toPlainText(),
			'self.texts[8]': self.texts[8].toPlainText(),
			'self.texts[9]': self.texts[9].toPlainText(),
			'self.texts[10]': self.texts[10].toPlainText(),
			'self.texts[11]': self.texts[11].toPlainText(),
			'self.texts[12]': self.texts[12].toPlainText(),
			'self.texts[13]': self.texts[13].toPlainText(),
			'self.texts[14]': self.texts[14].toPlainText(),
			'self.texts[15]': self.texts[15].toPlainText(),
			'self.texts[16]': self.texts[16].toPlainText(),
			'self.texts[17]': self.texts[17].toPlainText(),
			'self.comboBox_0': self.comboBox_0.currentText(),
			'self.comboBox_1': self.comboBox_1.currentText(),
			'self.comboBox_2': self.comboBox_2.currentText(),
			'self.comboBox_3': self.comboBox_3.currentText(),
			'self.AppLabels[0]': self.AppLabels[0].toPlainText(),
			'self.AppLabels[1]': self.AppLabels[1].toPlainText(),
			'self.AppLabels[2]': self.AppLabels[2].toPlainText(),
			'self.AppLabels[3]': self.AppLabels[3].toPlainText(),
			'self.AppLabels[4]': self.AppLabels[4].toPlainText(),
		}
		json.dump(allTextBox, myfile)

		myfile.close()

	def openppv(self):
		MainWindowPPV.show()
		MainWindowMC.hide()


# ОКНО С БЮДЖЕТОМ, КОНТРАГЕНТАМИ
class Ui_Dialog():

	# УСТАНОВКА ГРАФИКИ ДЛЯ ЛОТА
	def setupUi(self, Dialog):
		Dialog.resize(1550, 600)
		self.gridLayout = QtWidgets.QGridLayout(Dialog)
		self.tableWidget = QtWidgets.QTableWidget(Dialog)
		self.tableWidget.setRowCount(147)
		self.tableWidget.setColumnCount(8)
		self.tableWidget.horizontalHeader().setDefaultSectionSize(185)
		self.tableWidget.verticalHeader().setDefaultSectionSize(50)
		self.tableWidget.setAlternatingRowColors(True)
		self.tableWidget.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Тип"))
		self.tableWidget.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Локация"))
		self.tableWidget.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("Функциональный заказчик"))
		self.tableWidget.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem("Проект"))
		self.tableWidget.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem("Наименование"))
		self.tableWidget.setHorizontalHeaderItem(5, QtWidgets.QTableWidgetItem("Статья"))
		self.tableWidget.setHorizontalHeaderItem(6, QtWidgets.QTableWidgetItem("Лот"))
		self.tableWidget.setHorizontalHeaderItem(7, QtWidgets.QTableWidgetItem("ЦФО"))
		self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
		self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
		self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

		# NOTE: ЧТО ЗА КОНТРУКЦИЯ С lambda?
		self.buttonBox.accepted.connect(lambda: self.laccept(Dialog))  # передаем параметр Dialog через lambda
		self.buttonBox.rejected.connect(Dialog.reject)

		self.textbox = QtWidgets.QPlainTextEdit(Dialog)
		self.gridLayout.addWidget(self.textbox, 1, 0, 1, 1)
		self.textbox.setMaximumSize(QtCore.QSize(600, 25)),
		self.textbox.textChanged.connect(lambda: self.filter("ЛОТ"))

		QtCore.QMetaObject.connectSlotsByName(Dialog)
		self.loadData("LOT")

	# УСТАНОВКА ГРАФИКИ ДЛЯ КОНТРАГЕНТА
	def setupUi2(self, Dialog2):
		Dialog2.resize(750, 501)
		self.gridLayout2 = QtWidgets.QGridLayout(Dialog2)
		self.tableWidget2 = QtWidgets.QTableWidget(Dialog2)
		self.tableWidget2.setRowCount(10)
		self.tableWidget2.setColumnCount(4)
		self.tableWidget2.horizontalHeader().setDefaultSectionSize(185)
		self.tableWidget2.verticalHeader().setDefaultSectionSize(50)
		self.tableWidget2.setAlternatingRowColors(True)
		self.tableWidget2.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("АСВНСИ"))
		self.tableWidget2.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Наименование"))
		self.tableWidget2.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("ИНН"))
		self.tableWidget2.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem("КПП"))
		self.tableWidget2.setColumnWidth(0, 80)
		self.tableWidget2.setColumnWidth(1, 400)
		self.tableWidget2.setColumnWidth(2, 80)
		self.tableWidget2.setColumnWidth(3, 80)
		self.gridLayout2.addWidget(self.tableWidget2, 0, 0, 1, 4)
		QtCore.QMetaObject.connectSlotsByName(Dialog2)

		self.textbox_cont = QtWidgets.QPlainTextEdit(Dialog2)
		self.gridLayout2.addWidget(self.textbox_cont, 1, 0, 1, 1)
		self.textbox_cont.setMaximumSize(QtCore.QSize(110, 25)),
		self.textbox_cont.textChanged.connect(lambda: self.filter("Контакт_АСВН"))

		self.textbox_cont2 = QtWidgets.QPlainTextEdit(Dialog2)
		self.gridLayout2.addWidget(self.textbox_cont2, 1, 1, 1, 1)
		self.textbox_cont2.setMaximumSize(QtCore.QSize(390, 25)),
		self.textbox_cont2.textChanged.connect(lambda: self.filter("Контакт_Наименование"))

		self.textbox_cont3 = QtWidgets.QPlainTextEdit(Dialog2)
		self.gridLayout2.addWidget(self.textbox_cont3, 1, 2, 1, 1)
		self.textbox_cont3.setMaximumSize(QtCore.QSize(95, 25)),
		self.textbox_cont3.textChanged.connect(lambda: self.filter("Контакт_ИНН"))

		self.buttonBox4 = QtWidgets.QDialogButtonBox(Dialog2)
		self.buttonBox4.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox4.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
		self.gridLayout2.addWidget(self.buttonBox4, 2, 0, 1, 4)
		self.buttonBox4.accepted.connect(lambda: self.getContacts(Dialog2))  # передаем параметр Dialog через lambda
		self.buttonBox4.rejected.connect(Dialog2.reject)

		self.statusbar_cont = QtWidgets.QStatusBar(Dialog2)
		self.statusbar_cont.setObjectName("statusbar")

		self.loadData("CONTACT")

	# УСТАНОВКА ГРАФИКИ ДЛЯ МВЗ
	def setupMVZ(self, Dialog3):
		Dialog3.resize(750, 642)
		self.gridLayout_mvz = QtWidgets.QGridLayout(Dialog3)
		self.buttonBox_mvz = QtWidgets.QDialogButtonBox(Dialog3)
		self.buttonBox_mvz.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox_mvz.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)

		self.gridLayout_mvz.addWidget(self.buttonBox_mvz, 6, 0, 1, 4)
		self.frame_mvz = QtWidgets.QFrame(Dialog3)
		self.frame_mvz.setMinimumSize(QtCore.QSize(0, 25))
		self.frame_mvz.setFrameShape(QtWidgets.QFrame.StyledPanel)
		self.frame_mvz.setFrameShadow(QtWidgets.QFrame.Raised)

		self.radioButton1_mvz = QtWidgets.QRadioButton(Dialog3)
		self.gridLayout_mvz.addWidget(self.radioButton1_mvz, 0, 0, 1, 1)
		self.radioButton1_mvz.setText("Выбор по фамилиям")
		self.radioButton1_mvz.setChecked(1)
		self.radioButton1_mvz.clicked.connect(self.SearchByFIO)

		self.radioButton2_mvz = QtWidgets.QRadioButton(Dialog3)
		self.gridLayout_mvz.addWidget(self.radioButton2_mvz, 0, 1, 1, 1)
		self.radioButton2_mvz.setText("Выбор по МВЗ")
		self.radioButton2_mvz.clicked.connect(self.SearchByMVZ)

		self.buttonBox1_mvz = QtWidgets.QPushButton(self.frame_mvz)
		self.buttonBox1_mvz.setGeometry(QtCore.QRect(630, 0, 25, 25))
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/icons8-down-button-40.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.buttonBox1_mvz.setIcon(icon)
		self.buttonBox1_mvz.clicked.connect(self.pickMVZ)

		self.buttonBox2_mvz = QtWidgets.QPushButton(self.frame_mvz)
		self.buttonBox2_mvz.setGeometry(QtCore.QRect(680, 0, 25, 25))
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/icons8-slide-up-40.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.buttonBox2_mvz.setIcon(icon)
		self.buttonBox2_mvz.clicked.connect(self.removePickMVZ)

		self.gridLayout_mvz.addWidget(self.frame_mvz, 3, 0, 1, 4)
		self.tableWidget_mvz = QtWidgets.QTableWidget(Dialog3)
		self.tableWidget_mvz.setStyleSheet(" background-color: #dae6e8;")
		self.tableWidget_mvz.setLineWidth(2)
		self.tableWidget_mvz.setMidLineWidth(2)
		self.tableWidget_mvz.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		self.tableWidget_mvz.setProperty("showDropIndicator", False)
		self.tableWidget_mvz.setDragDropOverwriteMode(False)
		self.tableWidget_mvz.setAlternatingRowColors(True)
		self.tableWidget_mvz.setRowCount(2600)
		self.tableWidget_mvz.setColumnCount(2)
		self.tableWidget_mvz.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("ФИО"))
		self.tableWidget_mvz.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("МВЗ"))

		self.tableWidget_mvz.horizontalHeader().setCascadingSectionResizes(True)
		self.tableWidget_mvz.horizontalHeader().setDefaultSectionSize(250)
		self.tableWidget_mvz.horizontalHeader().setSortIndicatorShown(True)
		self.tableWidget_mvz.horizontalHeader().setStretchLastSection(True)
		self.tableWidget_mvz.verticalHeader().setCascadingSectionResizes(True)
		self.tableWidget_mvz.verticalHeader().setSortIndicatorShown(True)
		self.tableWidget_mvz.verticalHeader().setStretchLastSection(False)
		self.tableWidget_mvz.setSortingEnabled(True)
		self.gridLayout_mvz.addWidget(self.tableWidget_mvz, 2, 0, 1, 4)

		self.tableWidget_mvz2 = QtWidgets.QTableWidget(Dialog3)
		self.tableWidget_mvz2.setAlternatingRowColors(True)
		self.tableWidget_mvz2.setRowCount(0)
		self.tableWidget_mvz2.setColumnCount(3)
		self.tableWidget_mvz2.horizontalHeader().setDefaultSectionSize(230)
		self.tableWidget_mvz2.setSortingEnabled(True)
		self.gridLayout_mvz.addWidget(self.tableWidget_mvz2, 5, 0, 1, 4)
		self.tableWidget_mvz2.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("ФИО"))
		self.tableWidget_mvz2.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("МВЗ"))
		self.tableWidget_mvz2.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("%"))

		self.plainTextEdit_mvz = QtWidgets.QPlainTextEdit(Dialog3)
		self.plainTextEdit_mvz.setMaximumHeight(25)
		# self.plainTextEdit_mvz.setMaximumSize(QtCore.QSize(200, 25))
		self.gridLayout_mvz.addWidget(self.plainTextEdit_mvz, 1, 0, 1, 3)
		self.plainTextEdit_mvz.textChanged.connect(lambda: self.filter("МВЗ"))

		self.label_mvz = QtWidgets.QLabel(Dialog3)
		self.gridLayout_mvz.addWidget(self.label_mvz, 1, 3, 1, 1)

		self.buttonBox_mvz.accepted.connect(self.mvzOK)
		self.buttonBox_mvz.rejected.connect(Dialog3.reject)

		QtCore.QMetaObject.connectSlotsByName(Dialog3)

		_translate = QtCore.QCoreApplication.translate
		Dialog3.setWindowTitle(_translate("Dialog", "Dialog"))

		self.label_mvz.setText(_translate("Dialog", "Фильтр по ФИО"))
		self.loadData("MVZ")

	# ПЕРЕКЛЮЧАЕМ (RADIOBUTTON) НА ПОИСК МВЗ ПО НАЗВАНИЮ МВЗ
	def SearchByMVZ(self):
		self.tableWidget_mvz.clear()
		self.tableWidget_mvz.setColumnCount(1)
		self.tableWidget_mvz.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("МВЗ"))
		self.tableWidget_mvz.setRowCount(0)

		self.tableWidget_mvz2.setColumnCount(2)
		self.tableWidget_mvz2.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("МВЗ"))
		self.tableWidget_mvz2.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("%"))
		self.tableWidget_mvz2.setRowCount(0)

		connection = sqlite3.connect('Plan2019.db')
		query = "SELECT * FROM МВЗ_2"
		result = connection.execute(query)
		for row_number, row_data in enumerate(result):
			self.tableWidget_mvz.insertRow(row_number)
			for colum_number, data in enumerate(row_data):
				self.tableWidget_mvz.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))
		connection.close()

	# ПЕРЕКЛЮЧАЕМ (RADIOBUTTON) НА ПОИСК МВЗ ПО ФАМИЛИЯМ
	def SearchByFIO(self):
		self.tableWidget_mvz.setRowCount(2600)
		self.tableWidget_mvz.setColumnCount(2)
		self.tableWidget_mvz.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("ФИО"))
		self.tableWidget_mvz.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("МВЗ"))

		self.tableWidget_mvz2.setColumnCount(3)
		self.tableWidget_mvz2.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("ФИО"))
		self.tableWidget_mvz2.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("МВЗ"))
		self.tableWidget_mvz2.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("%"))
		self.tableWidget_mvz2.setRowCount(0)
		connection = sqlite3.connect('Plan2019.db')
		query = "SELECT * FROM МВЗ"
		result = connection.execute(query)
		for row_number, row_data in enumerate(result):
			self.tableWidget_mvz.insertRow(row_number)
			for colum_number, data in enumerate(row_data):
				self.tableWidget_mvz.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))
		connection.close()

	# ЗАГРУЖАЕМ БЮДЖЕТ ИЗ SQL БАЗЫ
	def loadData(self, window):
		connection = sqlite3.connect('Plan2019.db')
		if window == "LOT":
			query = "SELECT * FROM Plan"
			result = connection.execute(query)
			self.tableWidget.setRowCount(0)
			for row_number, row_data in enumerate(result):
				self.tableWidget.insertRow(row_number)
				for colum_number, data in enumerate(row_data):
					self.tableWidget.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))
		elif window == "CONTACT":
			query = "SELECT * FROM Contacts"
			result = connection.execute(query)
			self.tableWidget2.setRowCount(0)
			for row_number, row_data in enumerate(result):
				self.tableWidget2.insertRow(row_number)
				for colum_number, data in enumerate(row_data):
					self.tableWidget2.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))
		elif window == "MVZ":
			query = "SELECT * FROM МВЗ"
			result = connection.execute(query)
			self.tableWidget_mvz.setRowCount(0)
			for row_number, row_data in enumerate(result):
				self.tableWidget_mvz.insertRow(row_number)
				for colum_number, data in enumerate(row_data):
					self.tableWidget_mvz.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))
		connection.close()

	# СООТНОСИМ ЯЧЕЙКИ ИЗ ГЛАВНОГО ОКНА С ЯЧЕЙКАМИ В ТАБЛИЦЕ ЛОТ
	def laccept(self, Dialog):
		index = ui.tabWidget.currentIndex()
		index2 = PPV.tabWidget.currentIndex()
		if MainWindowMC.isVisible():
			ui.texts[1].setPlainText(self.tableWidget.item(self.tableWidget.currentItem().row(), 2).text())
			ui.texts[2].setPlainText(self.tableWidget.item(self.tableWidget.currentItem().row(), 4).text())
			ui.texts[3].setPlainText(self.tableWidget.item(self.tableWidget.currentItem().row(), 6).text())
			ui.finTabs[index][7].setPlainText(self.tableWidget.item(self.tableWidget.currentItem().row(), 7).text())
			ui.finTabs[index][9].setPlainText(self.tableWidget.item(self.tableWidget.currentItem().row(), 3).text())
			ui.finTabs[index][10].setPlainText(self.tableWidget.item(self.tableWidget.currentItem().row(), 5).text())

		elif MainWindowPPV.isVisible():
			PPV.plainTextEdit_2.setPlainText(self.tableWidget.item(self.tableWidget.currentItem().row(), 2).text())
			PPV.plainTextEdit_3.setPlainText(self.tableWidget.item(self.tableWidget.currentItem().row(), 6).text())
			PPV.textEdit_2.setPlainText(self.tableWidget.item(self.tableWidget.currentItem().row(), 4).text())
			if index2 == 0:
				PPV.plainTextEdit_6.setPlainText(self.tableWidget.item(self.tableWidget.currentItem().row(), 7).text())
				PPV.plainTextEdit_7.setPlainText(self.tableWidget.item(self.tableWidget.currentItem().row(), 3).text())
				PPV.plainTextEdit_8.setPlainText(self.tableWidget.item(self.tableWidget.currentItem().row(), 5).text())
			else:
				PPV.finTabs[index][9].setPlainText(
					self.tableWidget.item(self.tableWidget.currentItem().row(), 7).text())
				PPV.finTabs[index][11].setPlainText(
					self.tableWidget.item(self.tableWidget.currentItem().row(), 3).text())
				PPV.finTabs[index][12].setPlainText(
					self.tableWidget.item(self.tableWidget.currentItem().row(), 5).text())
		Dialog.hide()

	# СООТНОСИМ ЯЧЕЙКИ ИЗ ГЛАВНОГО ОКНА С ЯЧЕЙКАМИ В ТАБЛИЦЕ КОНТРАГЕНТ
	def getContacts(self, Dialog2):
		if MainWindowMC.isVisible():
			ui.texts[4].setPlainText(self.tableWidget2.item(self.tableWidget2.currentItem().row(), 1).text())
			ui.texts[5].setPlainText("ИНН: " + self.tableWidget2.item(self.tableWidget2.currentItem().row(), 2).text() +
			                         "  КПП: " + self.tableWidget2.item(self.tableWidget2.currentItem().row(),
			                                                            3).text())
		elif MainWindowPPV.isVisible():
			PPV.textEdit_3.setPlainText(self.tableWidget2.item(self.tableWidget2.currentItem().row(), 1).text() + "\n" +
			                            "ИНН: " + self.tableWidget2.item(self.tableWidget2.currentItem().row(),
			                                                             2).text() +
			                            "  КПП: " + self.tableWidget2.item(self.tableWidget2.currentItem().row(),
			                                                               3).text())
		Dialog2.hide()

	# ДОБАВЛЯЕМ ФИЛЬТРАЦИЮ В ЛОТ ЧЕРЕЗ SQL ЗАПРОСЫ
	def filter(self, filterBox):
		connection = sqlite3.connect('Plan2019.db')
		if filterBox == "ЛОТ":
			filter = '%' + self.textbox.toPlainText() + '%'
			result = connection.execute("SELECT * FROM Plan WHERE ЛОТ LIKE '%s'" % filter)
			self.tableWidget.setRowCount(0)
			for row_number, row_data in enumerate(result):
				self.tableWidget.insertRow(row_number)
				for colum_number, data in enumerate(row_data):
					self.tableWidget.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))
		# ДОБАВЛЯЕМ ФИЛЬТРАЦИЮ В МВЗ ПО ФАМИЛИИ ЧЕРЕЗ SQL ЗАПРОС
		elif filterBox == "МВЗ":
			if self.radioButton1_mvz.isChecked():
				filter = self.plainTextEdit_mvz.toPlainText() + '%'
				result = connection.execute("SELECT * FROM МВЗ WHERE ФИО LIKE '%s'" % filter)
				self.tableWidget_mvz.setRowCount(0)
				for row_number, row_data in enumerate(result):
					self.tableWidget_mvz.insertRow(row_number)
					for colum_number, data in enumerate(row_data):
						self.tableWidget_mvz.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))
			elif self.radioButton2_mvz.isChecked():
				filter = '%' + self.plainTextEdit_mvz.toPlainText() + '%'
				result = connection.execute("SELECT * FROM МВЗ_2 WHERE МВЗ LIKE '%s'" % filter)
				self.tableWidget_mvz.setRowCount(0)
				for row_number, row_data in enumerate(result):
					self.tableWidget_mvz.insertRow(row_number)
					for colum_number, data in enumerate(row_data):
						self.tableWidget_mvz.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))
		elif filterBox == "Контакт_АСВН":
			filter = self.textbox_cont.toPlainText() + '%'
			result = connection.execute("SELECT * FROM Contacts WHERE КодАСВНСИ LIKE '%s'" % filter)
			self.tableWidget2.setRowCount(0)
			for row_number, row_data in enumerate(result):
				self.tableWidget2.insertRow(row_number)
				for colum_number, data in enumerate(row_data):
					self.tableWidget2.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))
		elif filterBox == "Контакт_Наименование":
			filter = '%' + self.textbox_cont2.toPlainText() + '%'
			result = connection.execute("SELECT * FROM Contacts WHERE Наименование LIKE '%s'" % filter)
			self.tableWidget2.setRowCount(0)
			for row_number, row_data in enumerate(result):
				self.tableWidget2.insertRow(row_number)
				for colum_number, data in enumerate(row_data):
					self.tableWidget2.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))
		elif filterBox == "Контакт_ИНН":
			filter = self.textbox_cont3.toPlainText() + '%'
			result = connection.execute("SELECT * FROM Contacts WHERE ИНН LIKE '%s'" % filter)
			self.tableWidget2.setRowCount(0)
			for row_number, row_data in enumerate(result):
				self.tableWidget2.insertRow(row_number)
				for colum_number, data in enumerate(row_data):
					self.tableWidget2.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))
		connection.close()

	# ПЕРЕНОСИМ МВЗ ИЗ ВЕРХНЕЙ ТАБЛИЦЫ В НИЖНЮЮ
	def pickMVZ(self):
		# ЕСЛИ ВКЛЮЧЕН ПОИСК ПО ФАМИЛИЯМ
		if self.radioButton1_mvz.isChecked():
			FIO = self.tableWidget_mvz.item(self.tableWidget_mvz.currentRow(), 0)
			MVZ = self.tableWidget_mvz.item(self.tableWidget_mvz.currentRow(), 1)
			self.tableWidget_mvz2.insertRow(self.tableWidget_mvz2.rowCount())
			self.tableWidget_mvz2.setItem(self.tableWidget_mvz2.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(FIO))
			self.tableWidget_mvz2.setItem(self.tableWidget_mvz2.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(MVZ))
			# СЧИТАЕМ %
			try:  # проверка деления на 0
				persent = 100 / self.tableWidget_mvz2.rowCount()
			except ZeroDivisionError:
				persent = 100
			n = 0
			persent2 = 100/6
			tg ="s%" % persent2
			tg2 = str(tg)
			print(tg)

			
			while n <= self.tableWidget_mvz2.rowCount()-1:  # считаем для всех заполненных ячеек
				
				self.tableWidget_mvz2.setItem(n, 2, QtWidgets.QTableWidgetItem(str(round(persent,3))))
				self.tableWidget_mvz2.setItem(0, 2, QtWidgets.QTableWidgetItem(str(round(persent,3))))  # присваиваем остаток первой ячейке
				n += 1
			self.tableWidget_mvz.setFocus()
			self.tableWidget_mvz.selectRow(self.tableWidget_mvz.currentRow())

		# ЕСЛИ ВКЛЮЧЕН ПОИСК ПО МВЗ
		elif self.radioButton2_mvz.isChecked():
			MVZ = self.tableWidget_mvz.item(self.tableWidget_mvz.currentRow(), 0)

			self.tableWidget_mvz2.insertRow(self.tableWidget_mvz2.rowCount())
			self.tableWidget_mvz2.setItem(self.tableWidget_mvz2.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(MVZ))
			self.tableWidget_mvz.removeRow(self.tableWidget_mvz.currentRow())
			self.tableWidget_mvz.setFocus()
			self.tableWidget_mvz.selectRow(self.tableWidget_mvz.currentRow())

	# УДАЛЯЕМ МВЗ ИЗ НИЖНЕЙ ТАБЛИЦЫ
	def removePickMVZ(self):
		if self.radioButton1_mvz.isChecked():
			self.tableWidget_mvz2.removeRow(self.tableWidget_mvz2.currentRow())
			self.tableWidget_mvz2.setFocus()
			self.tableWidget_mvz2.selectRow(self.tableWidget_mvz2.currentRow())
			# СЧИТАЕМ %
			try:  # проверка деления на 0
				persent = 100 / self.tableWidget_mvz2.rowCount()
			except ZeroDivisionError:
				persent = 100
			n = 0
			while n <= self.tableWidget_mvz2.rowCount():  # считаем для всех заполненных ячеек
				# self.tableWidget_mvz2.setItem(n,2,QtWidgets.QTableWidgetItem(str(persent)))
				self.tableWidget_mvz2.setItem(n, 2, QtWidgets.QTableWidgetItem(str(int(persent))))
				self.tableWidget_mvz2.setItem(0, 2, QtWidgets.QTableWidgetItem(
					str(int(persent) + 100 % self.tableWidget_mvz2.rowCount())))  # присваиваем остаток первой ячейке
				n += 1
			self.tableWidget_mvz2.setFocus()
			self.tableWidget_mvz2.selectRow(self.tableWidget_mvz.currentRow())
		elif self.radioButton2_mvz.isChecked():
			MVZ = self.tableWidget_mvz2.item(self.tableWidget_mvz2.currentRow(), 0)
			self.tableWidget_mvz.insertRow(self.tableWidget_mvz.rowCount())
			self.tableWidget_mvz.setItem(self.tableWidget_mvz.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(MVZ))
			self.tableWidget_mvz2.removeRow(self.tableWidget_mvz2.currentRow())
			self.tableWidget_mvz2.setFocus()
			self.tableWidget_mvz2.selectRow(self.tableWidget_mvz2.currentRow())

	# ПЕРЕНОСИМ ВСЕ МВЗ В ГЛАВНОЕ МЕНЮ
	def mvzOK(self):
		# ЕСЛИ ВКЛЮЧЕН ПОИСК ПО ФАМИЛИЯМ
		if self.radioButton1_mvz.isChecked():
			index = ui.tabWidget.currentIndex()
			ui.finTabs[index][8].setPlainText("")  # Очищаем текстовое поле для вставки

			allMVZ = []  # создаем двумерный масив, для записис всех пар

			# Запускаем цикл длинной равной колличеству строк в таблице МВЗ
			for i1 in range(self.tableWidget_mvz2.rowCount()):
				# Добавляем пару МВЗ + процент, символ $ является указателем для обрезания (Start)
				# символ # является указателем для обрезания (Finish)
				mvz = (self.tableWidget_mvz2.item(i1, 1).text(), '$' + self.tableWidget_mvz2.item(i1, 2).text() + '#')
				# Заполняем двумерный массив нашими парами
				allMVZ.append(mvz)
			# вызываем оператор collections.Counter(),
			# который счиает повторяющиеся значения в двумерном массиве, и убирает их
			# после подсчета повторений сразу переводим полученные результаты в Словарь
			# ((МВЗ,процент):кол-во повторений)
			Re = dict(collections.Counter(allMVZ))
			ui.finTabs[index][8].setPlainText("")
			# берем по очереди все ключи в словаре '(МВЗ,процент)'- ключь
			for item in Re.keys():
				test = str(item)  # переводим в строку
				mvz2 = str(test[2:test.find(",") - 1])  # находим в строке название МВЗ (со 2 символа до ",")
				persent = test[test.find("$") + 1:test.find("#")]  # находим в строке процент (от $ до #)
				factor = Re.get(item)  # берем значение из Re (нашь множитель),
				# на текущей итерации мы имеем item, который является ключем
				result = float(factor) * float(persent)  # Перемножаем множитель и процент
				if MainWindowMC.isVisible():  # Вставляем в окно паспорта малоценки
					ui.finTabs[index][8].setPlainText(
						ui.finTabs[index][8].toPlainText() + mvz2 + " " + str(int(result)) + "%;" + "\n")
				elif MainWindowPPV.isVisible():  # Вставляем в окно паспорта прямого выбора
					PPV.textEdit.setPlainText(PPV.textEdit.toPlainText() + mvz2 + " " + str(int(result)) + "%;" + "\n")

		# ЕСЛИ ВКЛЮЧЕН ПОИСК ПО МВЗ
		elif self.radioButton2_mvz.isChecked():
			index = ui.tabWidget.currentIndex()  # Определяем открытую вкладку фин аналитик Для малоценки
			index2 = PPV.tabWidget.currentIndex()  # Определяем открытую вкладку фин аналитик Для ППВ
			ui.finTabs[index][8].setPlainText("")  # Очищаем текстовое поле МВЗ паспорта малоценки
			PPV.finTabs[index2][10].setPlainText("")  # Очищаем текстовое поле МВЗ паспорта прямого выбора

			for i1 in range(self.tableWidget_mvz2.rowCount()): # Перебираем все строки в таблице МВЗ
				mvz = self.tableWidget_mvz2.item(i1, 0).text() # Присваиваем ячейку (i1,0) в строке переменной mvz
				temp_persent = self.tableWidget_mvz2.item(i1, 1)

				if temp_persent == None: persent = ""
				else: persent = " " + self.tableWidget_mvz2.item(i1, 1).text() + "%"  # Присваиваем ячейку (i1,1) в строке переменной persent

				if MainWindowMC.isVisible():  # Вставляем в окно паспорта малоценки
					ui.finTabs[index][8].setPlainText(ui.finTabs[index][8].toPlainText() + mvz + str(persent) + "\n")
				elif MainWindowPPV.isVisible():  # Вставляем в окно паспорта прямого выбора
					PPV.finTabs[index2][10].setPlainText(PPV.finTabs[index2][10].toPlainText() + mvz + str(persent) + "\n")
		MVZWindow.hide()


# ОКНО ПАСПОРТ ПРЯМОГО ВЫБОРА
class Ui_MainWindowPPV(object):

	def setupUiPPV(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(767, 705)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setObjectName("scrollArea")
		self.scrollAreaWidgetContents = QtWidgets.QWidget()
		self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 730, 2141))
		self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
		self.gridLayout_5 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
		self.gridLayout_5.setObjectName("gridLayout_5")
		self.gridLayout = QtWidgets.QGridLayout()
		self.gridLayout.setObjectName("gridLayout")
		self.tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
		self.tableWidget.setMinimumSize(QtCore.QSize(0, 90))
		self.tableWidget.setAlternatingRowColors(True)
		self.tableWidget.setRowCount(0)
		self.tableWidget.setObjectName("tableWidget")
		self.tableWidget.setColumnCount(1)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(0, item)
		self.tableWidget.horizontalHeader().setMinimumSectionSize(0)
		self.tableWidget.horizontalHeader().setStretchLastSection(True)
		self.tableWidget.verticalHeader().setDefaultSectionSize(25)
		self.tableWidget.verticalHeader().setStretchLastSection(True)
		self.gridLayout.addWidget(self.tableWidget, 51, 0, 1, 8)
		self.line_7 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_7.setObjectName("line_7")
		self.gridLayout.addWidget(self.line_7, 52, 0, 1, 8)
		self.line_5 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_5.setObjectName("line_5")
		self.gridLayout.addWidget(self.line_5, 47, 0, 1, 8)
		self.pushButton_5 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
		self.pushButton_5.setObjectName("pushButton_5")
		self.gridLayout.addWidget(self.pushButton_5, 50, 0, 1, 8)
		self.pushButton_4 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		self.pushButton_4.setFont(font)
		self.pushButton_4.setObjectName("pushButton_4")
		self.gridLayout.addWidget(self.pushButton_4, 48, 0, 1, 8)
		self.textEdit_20 = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
		self.textEdit_20.setMinimumSize(QtCore.QSize(0, 90))
		self.textEdit_20.setMaximumSize(QtCore.QSize(16777215, 90))
		self.textEdit_20.setObjectName("textEdit_20")
		self.gridLayout.addWidget(self.textEdit_20, 46, 2, 1, 6)
		self.label_91 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_91.setFont(font)
		self.label_91.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_91.setObjectName("label_91")
		self.gridLayout.addWidget(self.label_91, 44, 0, 1, 1)
		self.label_90 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_90.setFont(font)
		self.label_90.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_90.setObjectName("label_90")
		self.gridLayout.addWidget(self.label_90, 42, 0, 1, 1)
		self.line_26 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_26.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_26.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_26.setObjectName("line_26")
		self.gridLayout.addWidget(self.line_26, 33, 0, 1, 8)
		self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents)
		self.plainTextEdit_3.setMaximumSize(QtCore.QSize(16777215, 25))
		self.plainTextEdit_3.setObjectName("plainTextEdit_3")
		self.gridLayout.addWidget(self.plainTextEdit_3, 2, 2, 1, 5)
		self.comboBox_26 = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
		self.comboBox_26.setEditable(True)
		self.comboBox_26.setObjectName("comboBox_26")
		self.comboBox_26.addItem("")
		self.comboBox_26.addItem("")
		self.comboBox_26.addItem("")
		self.comboBox_26.addItem("")
		self.comboBox_26.addItem("")
		self.gridLayout.addWidget(self.comboBox_26, 22, 2, 1, 6)
		self.line_31 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_31.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_31.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_31.setObjectName("line_31")
		self.gridLayout.addWidget(self.line_31, 43, 0, 1, 8)
		self.line_23 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_23.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_23.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_23.setObjectName("line_23")
		self.gridLayout.addWidget(self.line_23, 31, 0, 1, 8)
		self.line_27 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_27.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_27.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_27.setObjectName("line_27")
		self.gridLayout.addWidget(self.line_27, 35, 0, 1, 8)
		self.plainTextEdit_54 = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents)
		self.plainTextEdit_54.setMaximumSize(QtCore.QSize(16777215, 75))
		self.plainTextEdit_54.setObjectName("plainTextEdit_54")
		self.gridLayout.addWidget(self.plainTextEdit_54, 42, 2, 1, 6)
		self.line_28 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_28.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_28.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_28.setObjectName("line_28")
		self.gridLayout.addWidget(self.line_28, 39, 0, 1, 8)
		self.line_30 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_30.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_30.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_30.setObjectName("line_30")
		self.gridLayout.addWidget(self.line_30, 45, 0, 1, 8)
		self.line_29 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_29.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_29.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_29.setObjectName("line_29")
		self.gridLayout.addWidget(self.line_29, 41, 0, 1, 8)
		self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_3.setFont(font)
		self.label_3.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_3.setObjectName("label_3")
		self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
		self.label_92 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_92.setFont(font)
		self.label_92.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_92.setObjectName("label_92")
		self.gridLayout.addWidget(self.label_92, 46, 0, 1, 1)
		self.line_24 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_24.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_24.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_24.setObjectName("line_24")
		self.gridLayout.addWidget(self.line_24, 29, 0, 1, 8)
		self.plainTextEdit_55 = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents)
		self.plainTextEdit_55.setMaximumSize(QtCore.QSize(16777215, 75))
		self.plainTextEdit_55.setObjectName("plainTextEdit_55")
		self.gridLayout.addWidget(self.plainTextEdit_55, 44, 2, 1, 6)
		self.line_6 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_6.setObjectName("line_6")
		self.gridLayout.addWidget(self.line_6, 49, 0, 1, 8)
		self.line_25 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_25.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_25.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_25.setObjectName("line_25")
		self.gridLayout.addWidget(self.line_25, 27, 0, 1, 8)
		self.comboBox_25 = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
		self.comboBox_25.setObjectName("comboBox_25")
		self.comboBox_25.addItem("")
		self.comboBox_25.addItem("")
		self.gridLayout.addWidget(self.comboBox_25, 0, 2, 1, 6)
		self.plainTextEdit_12 = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents)
		self.plainTextEdit_12.setMaximumSize(QtCore.QSize(16777215, 25))
		self.plainTextEdit_12.setObjectName("plainTextEdit_12")
		self.gridLayout.addWidget(self.plainTextEdit_12, 24, 2, 1, 6)
		self.pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
		self.pushButton.setObjectName("pushButton")
		self.gridLayout.addWidget(self.pushButton, 2, 7, 1, 1)
		self.comboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
		self.comboBox.setEditable(True)
		self.comboBox.setObjectName("comboBox")
		self.comboBox.addItem("")
		self.comboBox.addItem("")
		self.comboBox.addItem("")
		self.gridLayout.addWidget(self.comboBox, 6, 2, 1, 6)
		self.textEdit_3 = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
		self.textEdit_3.setObjectName("textEdit_3")
		self.gridLayout.addWidget(self.textEdit_3, 18, 2, 1, 5)
		self.textEdit_2 = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
		self.textEdit_2.setMaximumSize(QtCore.QSize(16777215, 75))
		self.textEdit_2.setObjectName("textEdit_2")
		self.gridLayout.addWidget(self.textEdit_2, 10, 2, 1, 6)
		self.line_3 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_3.setObjectName("line_3")
		self.gridLayout.addWidget(self.line_3, 17, 0, 1, 8)
		self.line_14 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_14.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_14.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_14.setObjectName("line_14")
		self.gridLayout.addWidget(self.line_14, 21, 0, 1, 8)
		self.label_86 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_86.setFont(font)
		self.label_86.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_86.setObjectName("label_86")
		self.gridLayout.addWidget(self.label_86, 32, 0, 1, 1)
		self.comboBox_2 = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
		self.comboBox_2.setEditable(True)
		self.comboBox_2.setObjectName("comboBox_2")
		self.comboBox_2.addItem("")
		self.comboBox_2.addItem("")
		self.comboBox_2.addItem("")
		self.gridLayout.addWidget(self.comboBox_2, 8, 2, 1, 6)
		self.line_4 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_4.setObjectName("line_4")
		self.gridLayout.addWidget(self.line_4, 25, 0, 1, 8)
		self.line = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line.setFrameShape(QtWidgets.QFrame.HLine)
		self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line.setObjectName("line")
		self.gridLayout.addWidget(self.line, 15, 0, 1, 8)
		self.plainTextEdit_53 = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents)
		self.plainTextEdit_53.setMaximumSize(QtCore.QSize(16777215, 25))
		self.plainTextEdit_53.setObjectName("plainTextEdit_53")
		self.gridLayout.addWidget(self.plainTextEdit_53, 30, 2, 1, 6)
		self.textEdit_17 = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
		self.textEdit_17.setMaximumSize(QtCore.QSize(16777215, 75))
		self.textEdit_17.setObjectName("textEdit_17")
		self.gridLayout.addWidget(self.textEdit_17, 34, 2, 1, 6)
		self.line_22 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_22.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_22.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_22.setObjectName("line_22")
		self.gridLayout.addWidget(self.line_22, 13, 0, 1, 8)
		self.tabWidget = QtWidgets.QTabWidget(self.scrollAreaWidgetContents)
		self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 275))
		self.tabWidget.setObjectName("tabWidget")
		self.tab_1 = QtWidgets.QWidget()
		self.tab_1.setObjectName("tab_1")
		self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_1)
		self.gridLayout_4.setObjectName("gridLayout_4")
		self.gridLayout_3 = QtWidgets.QGridLayout()
		self.gridLayout_3.setObjectName("gridLayout_3")
		self.label_4 = QtWidgets.QLabel(self.tab_1)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_4.setFont(font)
		self.label_4.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_4.setObjectName("label_4")
		self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)
		self.plainTextEdit_5 = QtWidgets.QPlainTextEdit(self.tab_1)
		self.plainTextEdit_5.setMaximumSize(QtCore.QSize(16777215, 25))
		self.plainTextEdit_5.setObjectName("plainTextEdit_5")
		self.gridLayout_3.addWidget(self.plainTextEdit_5, 1, 1, 1, 2)
		self.plainTextEdit_4 = QtWidgets.QPlainTextEdit(self.tab_1)
		self.plainTextEdit_4.setMaximumSize(QtCore.QSize(16777215, 25))
		self.plainTextEdit_4.setObjectName("plainTextEdit_4")
		self.gridLayout_3.addWidget(self.plainTextEdit_4, 0, 1, 1, 2)
		self.label_5 = QtWidgets.QLabel(self.tab_1)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_5.setFont(font)
		self.label_5.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_5.setObjectName("label_5")
		self.gridLayout_3.addWidget(self.label_5, 1, 0, 1, 1)
		self.label_6 = QtWidgets.QLabel(self.tab_1)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_6.setFont(font)
		self.label_6.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_6.setObjectName("label_6")
		self.gridLayout_3.addWidget(self.label_6, 2, 0, 1, 1)
		self.pushButton_2 = QtWidgets.QPushButton(self.tab_1)
		self.pushButton_2.setObjectName("pushButton_2")
		self.gridLayout_3.addWidget(self.pushButton_2, 3, 2, 1, 1)
		self.plainTextEdit_6 = QtWidgets.QPlainTextEdit(self.tab_1)
		self.plainTextEdit_6.setMaximumSize(QtCore.QSize(16777215, 25))
		self.plainTextEdit_6.setObjectName("plainTextEdit_6")
		self.gridLayout_3.addWidget(self.plainTextEdit_6, 2, 1, 1, 2)
		self.label_8 = QtWidgets.QLabel(self.tab_1)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_8.setFont(font)
		self.label_8.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_8.setObjectName("label_8")
		self.gridLayout_3.addWidget(self.label_8, 4, 0, 1, 1)
		self.textEdit = QtWidgets.QTextEdit(self.tab_1)
		self.textEdit.setMaximumSize(QtCore.QSize(16777215, 75))
		self.textEdit.setObjectName("textEdit")
		self.gridLayout_3.addWidget(self.textEdit, 3, 1, 1, 1)
		self.plainTextEdit_7 = QtWidgets.QPlainTextEdit(self.tab_1)
		self.plainTextEdit_7.setMaximumSize(QtCore.QSize(16777215, 25))
		self.plainTextEdit_7.setObjectName("plainTextEdit_7")
		self.gridLayout_3.addWidget(self.plainTextEdit_7, 4, 1, 1, 2)
		self.plainTextEdit_8 = QtWidgets.QPlainTextEdit(self.tab_1)
		self.plainTextEdit_8.setMaximumSize(QtCore.QSize(16777215, 25))
		self.plainTextEdit_8.setObjectName("plainTextEdit_8")
		self.gridLayout_3.addWidget(self.plainTextEdit_8, 5, 1, 1, 2)
		self.label_7 = QtWidgets.QLabel(self.tab_1)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_7.setFont(font)
		self.label_7.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_7.setObjectName("label_7")
		self.gridLayout_3.addWidget(self.label_7, 3, 0, 1, 1)
		self.label_9 = QtWidgets.QLabel(self.tab_1)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_9.setFont(font)
		self.label_9.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_9.setObjectName("label_9")
		self.gridLayout_3.addWidget(self.label_9, 5, 0, 1, 1)
		self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
		self.tabWidget.addTab(self.tab_1, "")
		self.gridLayout.addWidget(self.tabWidget, 4, 0, 1, 8)
		self.line_33 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_33.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_33.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_33.setObjectName("line_33")
		self.gridLayout.addWidget(self.line_33, 7, 0, 1, 8)
		self.label_15 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_15.setFont(font)
		self.label_15.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_15.setObjectName("label_15")
		self.gridLayout.addWidget(self.label_15, 14, 0, 1, 1)
		self.label_21 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_21.setFont(font)
		self.label_21.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_21.setObjectName("label_21")
		self.gridLayout.addWidget(self.label_21, 26, 0, 1, 1)
		self.label_12 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_12.setFont(font)
		self.label_12.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_12.setObjectName("label_12")
		self.gridLayout.addWidget(self.label_12, 10, 0, 1, 1)
		self.line_37 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_37.setFrameShape(QtWidgets.QFrame.VLine)
		self.line_37.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_37.setObjectName("line_37")
		self.gridLayout.addWidget(self.line_37, 36, 1, 1, 1)
		self.label_87 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_87.setFont(font)
		self.label_87.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_87.setObjectName("label_87")
		self.gridLayout.addWidget(self.label_87, 34, 0, 1, 1)
		self.label_13 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_13.setFont(font)
		self.label_13.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_13.setObjectName("label_13")
		self.gridLayout.addWidget(self.label_13, 12, 0, 1, 1)
		self.label_18 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_18.setFont(font)
		self.label_18.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_18.setObjectName("label_18")
		self.gridLayout.addWidget(self.label_18, 20, 0, 1, 1)
		self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label.setFont(font)
		self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label.setObjectName("label")
		self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
		self.label_19 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_19.setFont(font)
		self.label_19.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_19.setObjectName("label_19")
		self.gridLayout.addWidget(self.label_19, 22, 0, 1, 1)
		self.comboBox_6 = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
		self.comboBox_6.setMinimumSize(QtCore.QSize(150, 0))
		self.comboBox_6.setObjectName("comboBox_6")
		self.comboBox_6.addItem("")
		self.comboBox_6.addItem("")
		self.gridLayout.addWidget(self.comboBox_6, 28, 4, 1, 2)
		self.line_32 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_32.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_32.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_32.setObjectName("line_32")
		self.gridLayout.addWidget(self.line_32, 9, 0, 1, 8)
		self.label_16 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_16.setFont(font)
		self.label_16.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_16.setObjectName("label_16")
		self.gridLayout.addWidget(self.label_16, 16, 0, 1, 1)
		self.line_40 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_40.setFrameShape(QtWidgets.QFrame.VLine)
		self.line_40.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_40.setObjectName("line_40")
		self.gridLayout.addWidget(self.line_40, 36, 3, 1, 1)
		self.label_11 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_11.setFont(font)
		self.label_11.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_11.setObjectName("label_11")
		self.gridLayout.addWidget(self.label_11, 8, 0, 1, 1)
		self.line_35 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_35.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_35.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_35.setObjectName("line_35")
		self.gridLayout.addWidget(self.line_35, 3, 0, 1, 8)
		self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_2.setFont(font)
		self.label_2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_2.setObjectName("label_2")
		self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
		self.label_10 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_10.setFont(font)
		self.label_10.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_10.setObjectName("label_10")
		self.gridLayout.addWidget(self.label_10, 6, 0, 1, 1)
		self.line_34 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_34.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_34.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_34.setObjectName("line_34")
		self.gridLayout.addWidget(self.line_34, 5, 0, 1, 8)
		self.label_20 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_20.setFont(font)
		self.label_20.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_20.setObjectName("label_20")
		self.gridLayout.addWidget(self.label_20, 24, 0, 1, 1)
		self.label_17 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_17.setFont(font)
		self.label_17.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_17.setObjectName("label_17")
		self.gridLayout.addWidget(self.label_17, 18, 0, 1, 1)
		self.line_36 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_36.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_36.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_36.setObjectName("line_36")
		self.gridLayout.addWidget(self.line_36, 37, 2, 1, 6)
		self.pushButton_3 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
		self.pushButton_3.setObjectName("pushButton_3")
		self.gridLayout.addWidget(self.pushButton_3, 18, 7, 1, 1)
		self.checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
		self.checkBox.setObjectName("checkBox")
		self.gridLayout.addWidget(self.checkBox, 36, 2, 1, 1)
		self.checkBox_2 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
		self.checkBox_2.setObjectName("checkBox_2")
		self.gridLayout.addWidget(self.checkBox_2, 38, 2, 1, 1)
		self.label_22 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_22.setFont(font)
		self.label_22.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_22.setObjectName("label_22")
		self.gridLayout.addWidget(self.label_22, 30, 0, 1, 1)
		self.plainTextEdit_9 = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents)
		self.plainTextEdit_9.setMaximumSize(QtCore.QSize(16777215, 25))
		self.plainTextEdit_9.setObjectName("plainTextEdit_9")
		self.gridLayout.addWidget(self.plainTextEdit_9, 16, 2, 1, 6)
		self.label_85 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_85.setFont(font)
		self.label_85.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_85.setObjectName("label_85")
		self.gridLayout.addWidget(self.label_85, 28, 0, 1, 1)
		self.line_38 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_38.setFrameShape(QtWidgets.QFrame.VLine)
		self.line_38.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_38.setObjectName("line_38")
		self.gridLayout.addWidget(self.line_38, 38, 1, 1, 1)
		self.comboBox_3 = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
		self.comboBox_3.setEditable(True)
		self.comboBox_3.setObjectName("comboBox_3")
		self.comboBox_3.addItem("")
		self.comboBox_3.addItem("")
		self.comboBox_3.addItem("")
		self.gridLayout.addWidget(self.comboBox_3, 12, 2, 1, 6)
		self.line_21 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_21.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_21.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_21.setObjectName("line_21")
		self.gridLayout.addWidget(self.line_21, 23, 0, 1, 8)
		self.label_88 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_88.setFont(font)
		self.label_88.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_88.setObjectName("label_88")
		self.gridLayout.addWidget(self.label_88, 36, 0, 3, 1)
		self.comboBox_4 = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
		self.comboBox_4.setEditable(True)
		self.comboBox_4.setObjectName("comboBox_4")
		self.comboBox_4.addItem("")
		self.comboBox_4.addItem("")
		self.gridLayout.addWidget(self.comboBox_4, 14, 2, 1, 6)
		self.line_13 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_13.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_13.setObjectName("line_13")
		self.gridLayout.addWidget(self.line_13, 19, 0, 1, 8)
		self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents)
		self.plainTextEdit_2.setMaximumSize(QtCore.QSize(16777215, 25))
		self.plainTextEdit_2.setObjectName("plainTextEdit_2")
		self.gridLayout.addWidget(self.plainTextEdit_2, 1, 2, 1, 6)
		self.plainTextEdit = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents)
		self.plainTextEdit.setMaximumSize(QtCore.QSize(75, 25))
		self.plainTextEdit.setObjectName("plainTextEdit")
		self.gridLayout.addWidget(self.plainTextEdit, 28, 2, 1, 1)
		self.line_39 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_39.setFrameShape(QtWidgets.QFrame.VLine)
		self.line_39.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_39.setObjectName("line_39")
		self.gridLayout.addWidget(self.line_39, 38, 3, 1, 1)
		self.comboBox_7 = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
		self.comboBox_7.setMinimumSize(QtCore.QSize(200, 0))
		self.comboBox_7.setEditable(True)
		self.comboBox_7.setMaxVisibleItems(10)
		self.comboBox_7.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
		self.comboBox_7.setMinimumContentsLength(0)
		self.comboBox_7.setObjectName("comboBox_7")
		self.comboBox_7.addItem("")
		self.comboBox_7.addItem("")
		self.gridLayout.addWidget(self.comboBox_7, 28, 6, 1, 2)
		self.label_89 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_89.setFont(font)
		self.label_89.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
		self.label_89.setObjectName("label_89")
		self.gridLayout.addWidget(self.label_89, 40, 0, 1, 1)
		self.textEdit_4 = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
		self.textEdit_4.setMaximumSize(QtCore.QSize(16777215, 75))
		self.textEdit_4.setObjectName("textEdit_4")
		self.gridLayout.addWidget(self.textEdit_4, 32, 2, 1, 6)
		self.toolBox_2 = QtWidgets.QToolBox(self.scrollAreaWidgetContents)
		self.toolBox_2.setEnabled(False)
		self.toolBox_2.setObjectName("toolBox_2")
		self.page_6 = QtWidgets.QWidget()
		self.page_6.setGeometry(QtCore.QRect(0, 0, 407, 69))
		self.page_6.setObjectName("page_6")
		self.gridLayout_18 = QtWidgets.QGridLayout(self.page_6)
		self.gridLayout_18.setObjectName("gridLayout_18")
		self.plainTextEdit_11 = QtWidgets.QPlainTextEdit(self.page_6)
		self.plainTextEdit_11.setMaximumSize(QtCore.QSize(16777215, 50))
		self.plainTextEdit_11.setObjectName("plainTextEdit_11")
		self.gridLayout_18.addWidget(self.plainTextEdit_11, 0, 0, 1, 1)
		self.toolBox_2.addItem(self.page_6, "")
		self.page_7 = QtWidgets.QWidget()
		self.page_7.setGeometry(QtCore.QRect(0, 0, 511, 69))
		self.page_7.setObjectName("page_7")
		self.gridLayout_19 = QtWidgets.QGridLayout(self.page_7)
		self.gridLayout_19.setObjectName("gridLayout_19")
		self.plainTextEdit_56 = QtWidgets.QPlainTextEdit(self.page_7)
		self.plainTextEdit_56.setMaximumSize(QtCore.QSize(16777215, 50))
		self.plainTextEdit_56.setObjectName("plainTextEdit_56")
		self.gridLayout_19.addWidget(self.plainTextEdit_56, 0, 0, 1, 1)
		self.toolBox_2.addItem(self.page_7, "")
		self.page_8 = QtWidgets.QWidget()
		self.page_8.setGeometry(QtCore.QRect(0, 0, 511, 69))
		self.page_8.setObjectName("page_8")
		self.gridLayout_20 = QtWidgets.QGridLayout(self.page_8)
		self.gridLayout_20.setObjectName("gridLayout_20")
		self.plainTextEdit_57 = QtWidgets.QPlainTextEdit(self.page_8)
		self.plainTextEdit_57.setMaximumSize(QtCore.QSize(16777215, 50))
		self.plainTextEdit_57.setObjectName("plainTextEdit_57")
		self.gridLayout_20.addWidget(self.plainTextEdit_57, 0, 0, 1, 1)
		self.toolBox_2.addItem(self.page_8, "")
		self.gridLayout.addWidget(self.toolBox_2, 36, 4, 1, 4)
		self.textEdit_19 = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
		self.textEdit_19.setMaximumSize(QtCore.QSize(16777215, 75))
		self.textEdit_19.setObjectName("textEdit_19")
		self.gridLayout.addWidget(self.textEdit_19, 40, 2, 1, 6)
		self.toolBox = QtWidgets.QToolBox(self.scrollAreaWidgetContents)
		self.toolBox.setEnabled(False)
		self.toolBox.setObjectName("toolBox")
		self.page_3 = QtWidgets.QWidget()
		self.page_3.setGeometry(QtCore.QRect(0, 0, 407, 69))
		self.page_3.setObjectName("page_3")
		self.gridLayout_15 = QtWidgets.QGridLayout(self.page_3)
		self.gridLayout_15.setObjectName("gridLayout_15")
		self.plainTextEdit_58 = QtWidgets.QPlainTextEdit(self.page_3)
		self.plainTextEdit_58.setMaximumSize(QtCore.QSize(16777215, 50))
		self.plainTextEdit_58.setObjectName("plainTextEdit_58")
		self.gridLayout_15.addWidget(self.plainTextEdit_58, 0, 0, 1, 1)
		self.toolBox.addItem(self.page_3, "")
		self.page_4 = QtWidgets.QWidget()
		self.page_4.setGeometry(QtCore.QRect(0, 0, 511, 69))
		self.page_4.setObjectName("page_4")
		self.gridLayout_16 = QtWidgets.QGridLayout(self.page_4)
		self.gridLayout_16.setObjectName("gridLayout_16")
		self.plainTextEdit_59 = QtWidgets.QPlainTextEdit(self.page_4)
		self.plainTextEdit_59.setMaximumSize(QtCore.QSize(16777215, 50))
		self.plainTextEdit_59.setObjectName("plainTextEdit_59")
		self.gridLayout_16.addWidget(self.plainTextEdit_59, 0, 0, 1, 1)
		self.toolBox.addItem(self.page_4, "")
		self.page_5 = QtWidgets.QWidget()
		self.page_5.setGeometry(QtCore.QRect(0, 0, 511, 69))
		self.page_5.setObjectName("page_5")
		self.gridLayout_17 = QtWidgets.QGridLayout(self.page_5)
		self.gridLayout_17.setObjectName("gridLayout_17")
		self.plainTextEdit_60 = QtWidgets.QPlainTextEdit(self.page_5)
		self.plainTextEdit_60.setMaximumSize(QtCore.QSize(16777215, 50))
		self.plainTextEdit_60.setObjectName("plainTextEdit_60")
		self.gridLayout_17.addWidget(self.plainTextEdit_60, 0, 0, 1, 1)
		self.toolBox.addItem(self.page_5, "")
		self.gridLayout.addWidget(self.toolBox, 38, 4, 1, 4)
		self.line_2 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
		self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_2.setObjectName("line_2")
		self.gridLayout.addWidget(self.line_2, 11, 0, 1, 8)
		self.plainTextEdit_10 = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents)
		self.plainTextEdit_10.setMaximumSize(QtCore.QSize(16777215, 25))
		self.plainTextEdit_10.setObjectName("plainTextEdit_10")
		self.gridLayout.addWidget(self.plainTextEdit_10, 20, 2, 1, 6)
		self.plainTextEdit_13 = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents)
		self.plainTextEdit_13.setMaximumSize(QtCore.QSize(16777215, 25))
		self.plainTextEdit_13.setObjectName("plainTextEdit_13")
		self.gridLayout.addWidget(self.plainTextEdit_13, 26, 2, 1, 4)
		self.comboBox_5 = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
		self.comboBox_5.setObjectName("comboBox_5")
		self.comboBox_5.addItem("")
		self.comboBox_5.addItem("")
		self.comboBox_5.addItem("")
		self.gridLayout.addWidget(self.comboBox_5, 26, 6, 1, 1)
		self.checkBox_3 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
		self.checkBox_3.setObjectName("checkBox_3")
		self.gridLayout.addWidget(self.checkBox_3, 26, 7, 1, 1)
		self.gridLayout_5.addLayout(self.gridLayout, 1, 0, 1, 1)
		self.scrollArea.setWidget(self.scrollAreaWidgetContents)
		self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 767, 21))
		self.menubar.setObjectName("menubar")
		self.menu = QtWidgets.QMenu(self.menubar)
		self.menu.setObjectName("menu")
		self.menu_2 = QtWidgets.QMenu(self.menubar)
		self.menu_2.setObjectName("menu_2")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		self.action = QtWidgets.QAction(MainWindow)
		self.action.setObjectName("action")
		self.action_2 = QtWidgets.QAction(MainWindow)
		self.action_2.setObjectName("action_2")
		self.action_4 = QtWidgets.QAction(MainWindow)
		self.action_4.setObjectName("action_4")
		self.action_Word = QtWidgets.QAction(MainWindow)
		self.action_Word.setObjectName("action_Word")
		self.action_5 = QtWidgets.QAction(MainWindow)
		self.action_5.setObjectName("action_5")
		self.action_7 = QtWidgets.QAction(MainWindow)
		self.action_7.setObjectName("action_7")
		self.action_8 = QtWidgets.QAction(MainWindow)
		self.action_8.setObjectName("action_8")
		self.action_9 = QtWidgets.QAction(MainWindow)
		self.action_9.setObjectName("action_9")
		self.menu.addAction(self.action)
		self.menu.addAction(self.action_2)
		self.menu.addSeparator()
		self.menu.addAction(self.action_4)
		self.menu_2.addAction(self.action_Word)
		self.menu_2.addAction(self.action_5)
		self.menu_2.addSeparator()
		self.menu_2.addAction(self.action_7)
		self.menu_2.addAction(self.action_8)
		self.menu_2.addAction(self.action_9)
		self.menubar.addAction(self.menu.menuAction())
		self.menubar.addAction(self.menu_2.menuAction())

		self.retranslateUi(MainWindow)
		self.tabWidget.setCurrentIndex(0)
		self.toolBox_2.setCurrentIndex(0)
		self.toolBox.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

		# КОНТЕКСТНОЕ МЕНЮ
		self.tabWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.tabWidget.customContextMenuRequested.connect(self.showMenu)

		self.finTabs = []
		self.finTabs.append((self.tabWidget, self.label_4, self.label_5, self.label_6,
		                     self.label_7, self.label_8, self.label_9,
		                     self.plainTextEdit_4, self.plainTextEdit_5, self.plainTextEdit_6,
		                     self.textEdit, self.plainTextEdit_7,
		                     self.plainTextEdit_8, self.pushButton_2))

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Паспорт прямого выбора"))
		self.pushButton_5.setText(_translate("MainWindow", "Загрузить приложения"))
		self.pushButton_4.setText(_translate("MainWindow", "ФОРМА 1"))
		self.label_91.setText(_translate("MainWindow", "Опишите имеющиеся \n""меры по снижению рисков."))
		self.label_90.setText(
			_translate("MainWindow", "Опишите риски,\n""связанные с использованием \n""единственного поставщика."))
		self.comboBox_26.setItemText(0, _translate("MainWindow", "Акционерное общество"))
		self.comboBox_26.setItemText(1, _translate("MainWindow", "Общество с ограниченной ответственностью"))
		self.comboBox_26.setItemText(2, _translate("MainWindow", "Закрытое акционерное общество"))
		self.comboBox_26.setItemText(3, _translate("MainWindow", "Публичное акционерное обество"))
		self.comboBox_26.setItemText(4, _translate("MainWindow", "Индивидуальный предприниматель"))
		self.label_3.setText(_translate("MainWindow", "Лот из плана закупок"))
		self.label_92.setText(
			_translate("MainWindow", "Краткое обоснование \n""прямого выбора \n""(с приложением Формы 1)"))
		self.comboBox_25.setItemText(0, _translate("MainWindow", "НИПИГАЗ"))
		self.comboBox_25.setItemText(1, _translate("MainWindow", "СИБУР"))
		self.plainTextEdit_12.setPlainText(_translate("MainWindow", "Проверка не проводилась"))
		self.pushButton.setText(_translate("MainWindow", "Выбрать"))
		self.comboBox.setItemText(0, _translate("MainWindow", "Закупка МТР"))
		self.comboBox.setItemText(1, _translate("MainWindow", "Закупка услуг"))
		self.comboBox.setItemText(2, _translate("MainWindow", "Закупка МТР и услуг"))
		self.label_86.setText(_translate("MainWindow", "Объем закупки"))
		self.comboBox_2.setItemText(0, _translate("MainWindow", "Поставке лицензий на ПО"))
		self.comboBox_2.setItemText(1, _translate("MainWindow", "Услуги по оказанию технической поддержки"))
		self.comboBox_2.setItemText(2, _translate("MainWindow",
		                                          "Поставке лицензий на ПО и услуги по оказанию технической поддержки"))
		self.plainTextEdit_53.setPlainText(_translate("MainWindow", "-"))
		self.textEdit_17.setHtml(_translate("MainWindow", "-"))
		self.label_4.setText(_translate("MainWindow", "Источник финансирования"))
		self.label_5.setText(_translate("MainWindow", "Номенклатурная группа"))
		self.label_6.setText(_translate("MainWindow", "ЦФО"))
		self.pushButton_2.setText(_translate("MainWindow", "Выбрать"))
		self.label_8.setText(_translate("MainWindow", "Проект"))
		self.label_7.setText(_translate("MainWindow", "МВЗ"))
		self.label_9.setText(_translate("MainWindow", "Статья"))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "Аналитики"))
		self.label_15.setText(
			_translate("MainWindow", "Техническое предложение\n""рассматривалось \n""профильными экспертами?"))
		self.label_21.setText(_translate("MainWindow", "Сумма закупки"))
		self.label_12.setText(_translate("MainWindow", "Предмет закупки"))
		self.label_87.setText(_translate("MainWindow", "Условия доставки"))
		self.label_13.setText(_translate("MainWindow", "Требования"))
		self.label_18.setText(_translate("MainWindow",
		                                 "Включен ли претендент \n""в перечень \n""квалифицированных \n""контрагентов? \n""Статус квалификации?"))
		self.label.setText(_translate("MainWindow", "Наименование предприятия"))
		self.label_19.setText(
			_translate("MainWindow", "Структура собственности \n""и аффилированность \n""предлагаемого поставщика. "))
		self.comboBox_6.setItemText(0, _translate("MainWindow", "календарных дней"))
		self.comboBox_6.setItemText(1, _translate("MainWindow", "рабочих дней"))
		self.label_16.setText(_translate("MainWindow", "Требования к претенденту "))
		self.label_11.setText(_translate("MainWindow", "Направление закупки"))
		self.label_2.setText(_translate("MainWindow", "Функциональный заказчик"))
		self.label_10.setText(_translate("MainWindow", "Тип закупки"))
		self.label_20.setText(_translate("MainWindow", "Результаты аудиторской \n""проверки."))
		self.label_17.setText(_translate("MainWindow", "Название.\n""Контактная информация"))
		self.pushButton_3.setText(_translate("MainWindow", "Выбрать"))
		self.checkBox.setText(_translate("MainWindow", "Лицензии"))
		self.checkBox_2.setText(_translate("MainWindow", "Услуги"))
		self.label_22.setText(_translate("MainWindow", "Срок поставки МТР"))
		self.plainTextEdit_9.setPlainText(_translate("MainWindow", "Не применимо"))
		self.label_85.setText(_translate("MainWindow", "Срок поставки"))
		self.comboBox_3.setItemText(0, _translate("MainWindow", "В соответствии с техническим заданием "))
		self.comboBox_3.setItemText(1, _translate("MainWindow", "Не применимо"))
		self.comboBox_3.setItemText(2, _translate("MainWindow", "В приложении к паспорту"))
		self.label_88.setText(_translate("MainWindow", "Условия оплаты"))
		self.comboBox_4.setItemText(0, _translate("MainWindow", "Нет"))
		self.comboBox_4.setItemText(1, _translate("MainWindow", "Да"))
		self.comboBox_7.setItemText(0, _translate("MainWindow", "с даты подписания договора"))
		self.comboBox_7.setItemText(1,
		                            _translate("MainWindow", "с даты поступления денежных средств на расчетный счет"))
		self.label_89.setText(_translate("MainWindow",
		                                 "Укажите, проведены ли \n""переговоры с поставщиком. \n""Если да, укажите, \n""результат переговоров"))
		self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_6), _translate("MainWindow", "Вариант 1"))
		self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_7), _translate("MainWindow", "Вариант 2"))
		self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_8), _translate("MainWindow", "Вариант 3"))
		self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), _translate("MainWindow", "Вариант 1"))
		self.toolBox.setItemText(self.toolBox.indexOf(self.page_4), _translate("MainWindow", "Вариант 2"))
		self.toolBox.setItemText(self.toolBox.indexOf(self.page_5), _translate("MainWindow", "Вариант 3"))
		self.comboBox_5.setItemText(0, _translate("MainWindow", "RUB"))
		self.comboBox_5.setItemText(1, _translate("MainWindow", "USD"))
		self.comboBox_5.setItemText(2, _translate("MainWindow", "EUR"))
		self.checkBox_3.setText(_translate("MainWindow", "НДС 20%"))
		self.menu.setTitle(_translate("MainWindow", "Файл"))
		self.menu_2.setTitle(_translate("MainWindow", "Паспорт"))
		self.action.setText(_translate("MainWindow", "Открыть"))
		self.action_2.setText(_translate("MainWindow", "Сохранить"))
		self.action_4.setText("Выйти")
		self.action_Word.setText("Экспорт в Word")
		self.action_5.setText(_translate("MainWindow", "Экспорт в ПДФ"))
		self.action_7.setText(_translate("MainWindow", "Паспорт малоценной закупки"))
		self.action_8.setText(_translate("MainWindow", "Паспорт прямого выбора"))
		self.action_9.setText(_translate("MainWindow", "Паспорт закупки"))

		self.action_7.triggered.connect(MainWindowPPV.hide)
		self.action_7.triggered.connect(MainWindowMC.show)
		# self.action_Word.triggered.connect(self.exportToWord)
		self.action_4.triggered.connect(MainWindow.close)

		self.pushButton.clicked.connect(LotWindow.show)
		self.pushButton_2.clicked.connect(MVZWindow.show)
		self.pushButton_3.clicked.connect(ContactsWindow.show)
		self.pushButton_4.clicked.connect(self.Forma1Show)

		self.checkBox.stateChanged.connect(self.checkLicenseOn)
		self.checkBox_2.stateChanged.connect(self.checkServiseOn)
		self.pushButton_5.clicked.connect(self.showDialog)

		self.tableWidget.setColumnCount(1)

	# ЗАПУСКАЕМ КОНТЕКСТНОЕ МЕНЮ
	def showMenu(self, event):
		contextMenu = QtWidgets.QMenu(MainWindowPPV)
		contextMenu.addAction("Добавить аналитики", self.addTabFin)
		contextMenu.addAction("Удалить аналитики", self.deletTabFin)
		action = contextMenu.exec_(self.tabWidget.mapToGlobal(event))

	# ДОБАВЛЯЕМ ВКЛАДКУ АНАЛИТИКОВ ИЗ КОНТЕКСТНОГО МЕНЮ
	def addTabFin(self):
		# ВКЛАДКИ ДЛЯ ФИН. АНАЛИТИК

		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		n = 0
		TabNumber = 1
		PPV.finTabs.append((
			QtWidgets.QWidget(), QtWidgets.QLabel(), QtWidgets.QLabel(), QtWidgets.QLabel(),
			QtWidgets.QLabel(), QtWidgets.QLabel(), QtWidgets.QLabel(),
			QtWidgets.QPlainTextEdit(), QtWidgets.QPlainTextEdit(), QtWidgets.QPlainTextEdit(),
			QtWidgets.QPlainTextEdit(), QtWidgets.QPlainTextEdit(),
			QtWidgets.QPlainTextEdit(), QtWidgets.QPushButton()))

		for item in PPV.finTabs:
			n += 1
			if n == len(PPV.finTabs):
				TabNumber += 1
				PPV.tabWidget.addTab(item[0], "№" + str(n))
				self.gridLayout_3 = QtWidgets.QGridLayout(item[0])

				item[1].setParent(item[0])
				item[1].setMinimumSize(QtCore.QSize(190, 25))
				item[1].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
				PPV.gridLayout_3.addWidget(item[1], 0, 0, 1, 1)

				item[1].setText("Источник финансирования")
				item[1].setFont(font)

				item[2].setParent(item[0])
				item[2].setMinimumSize(QtCore.QSize(190, 25))
				item[2].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
				PPV.gridLayout_3.addWidget(item[2], 1, 0, 1, 1)
				item[2].setText("Номенклатурная группа")
				item[2].setFont(font)

				item[3].setParent(item[0])
				item[3].setMinimumSize(QtCore.QSize(190, 25))
				item[3].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
				PPV.gridLayout_3.addWidget(item[3], 2, 0, 1, 1)
				item[3].setText("ЦФО")
				item[3].setFont(font)

				item[4].setParent(item[0])
				item[4].setMinimumSize(QtCore.QSize(190, 25))
				item[4].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
				PPV.gridLayout_3.addWidget(item[4], 3, 0, 1, 1)
				item[4].setText("МВЗ")
				item[4].setFont(font)

				item[5].setParent(item[0])
				item[5].setMinimumSize(QtCore.QSize(190, 25))
				item[5].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
				PPV.gridLayout_3.addWidget(item[5], 4, 0, 1, 1)
				item[5].setText("Проект")
				item[5].setFont(font)

				item[6].setParent(item[0])
				item[6].setMinimumSize(QtCore.QSize(190, 25))
				item[6].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
				PPV.gridLayout_3.addWidget(item[6], 5, 0, 1, 1)
				item[6].setText("Статья ДДС")
				item[6].setFont(font)

				item[7].setParent(item[0])
				item[7].setObjectName("Tab_" + str(TabNumber) + "_Источник_финансирования")
				item[7].setMinimumSize(QtCore.QSize(0, 25))
				item[7].setMaximumSize(QtCore.QSize(16777215, 25))
				PPV.gridLayout_3.addWidget(item[7], 0, 1, 1, 3)

				item[8].setParent(item[0])
				item[8].setObjectName("Tab_" + str(TabNumber) + "_Номенклатурная_группа")
				item[8].setMinimumSize(QtCore.QSize(0, 25))
				item[8].setMaximumSize(QtCore.QSize(16777215, 25))
				PPV.gridLayout_3.addWidget(item[8], 1, 1, 1, 3)

				item[9].setParent(item[0])
				item[9].setObjectName("Tab_" + str(TabNumber) + "_ЦФО")
				item[9].setMinimumSize(QtCore.QSize(0, 25))
				item[9].setMaximumSize(QtCore.QSize(16777215, 25))
				PPV.gridLayout_3.addWidget(item[9], 2, 1, 1, 3)

				item[10].setParent(item[0])
				item[10].setObjectName("Tab_" + str(TabNumber) + "_МВЗ")
				item[10].setMinimumSize(QtCore.QSize(0, 75))
				item[10].setMaximumSize(QtCore.QSize(16777215, 75))
				PPV.gridLayout_3.addWidget(item[10], 3, 1, 1, 1)

				item[11].setParent(item[0])
				item[11].setObjectName("Tab_" + str(TabNumber) + "_Проект")
				item[11].setMinimumSize(QtCore.QSize(0, 25))
				item[11].setMaximumSize(QtCore.QSize(16777215, 25))
				PPV.gridLayout_3.addWidget(item[11], 4, 1, 1, 3)

				item[12].setParent(item[0])
				item[12].setObjectName("Tab_" + str(TabNumber) + "_Статья_ДДС")
				item[12].setMinimumSize(QtCore.QSize(0, 25))
				item[12].setMaximumSize(QtCore.QSize(16777215, 25))
				PPV.gridLayout_3.addWidget(item[12], 5, 1, 1, 3)

				item[13].setParent(item[0])
				item[13].setMinimumSize(QtCore.QSize(0, 25))
				item[13].setMaximumSize(QtCore.QSize(16777215, 25))
				PPV.gridLayout_3.addWidget(item[13], 3, 3, 1, 1)
				item[13].setText("Выбрать")
				item[13].clicked.connect(MVZWindow.show)
				PPV.tabWidget.setCurrentIndex(n - 1)

	# УДАЛЯЕМ ВКЛАДКУ АНАЛИТИКОВ ИЗ КОНТЕКСТНОГО МЕНЮ
	def deletTabFin(self):
		index = PPV.tabWidget.currentIndex()
		if index != 0:
			for item in self.finTabs[index]:
				item.deleteLater()
			self.finTabs.pop(index)

	def checkLicenseOn(self, state):
		if state == QtCore.Qt.Checked:
			self.toolBox_2.setEnabled(1)
			self.plainTextEdit_11.setPlainText("Лицензии условие 1")
			self.plainTextEdit_56.setPlainText("Лицензии условие 2")
			self.plainTextEdit_57.setPlainText("Лицензии условие 3")
		else:
			self.toolBox_2.setEnabled(0)
			self.plainTextEdit_11.setPlainText("")
			self.plainTextEdit_56.setPlainText("")
			self.plainTextEdit_57.setPlainText("")

	def checkServiseOn(self, state):
		if state == QtCore.Qt.Checked:
			self.toolBox.setEnabled(1)
			self.plainTextEdit_58.setPlainText("Услуги условие 1")
			self.plainTextEdit_59.setPlainText("Услуги условие 2")
			self.plainTextEdit_60.setPlainText("Услуги условие 3")
		else:
			self.toolBox.setEnabled(0)
			self.plainTextEdit_58.setPlainText("")
			self.plainTextEdit_59.setPlainText("")
			self.plainTextEdit_60.setPlainText("")

	def Forma1Show(self):
		Forma1.show()

	def showDialog(self, MainWindow):
		filter = "Image (*.jpeg *.jpg *.png *.bmp)"  # определяем формат приложения
		fname = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', '/home', filter)
		print(fname)
		if fname[0]:
			self.tableWidget.insertRow(self.tableWidget.rowCount())
			self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QtWidgets.QTableWidgetItem())
			self.tableWidget.item(self.tableWidget.rowCount() - 1, 0).setText(fname[0])


# ОКНО С ФОРМОЙ 1
class Ui_DialogForma1(object):

	def setupUi(self, Dialog):
		Dialog.setObjectName("Dialog")
		Dialog.resize(990, 700)
		self.gridLayout = QtWidgets.QGridLayout(Dialog)
		self.gridLayout.setObjectName("gridLayout")
		self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
		self.buttonBox.setObjectName("buttonBox")
		self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
		self.buttonBox2 = QtWidgets.QPushButton(Dialog)
		self.gridLayout.addWidget(self.buttonBox2, 0, 0, 1, 1)
		self.buttonBox2.clicked.connect(self.loadContragent)

		self.tableWidget = QtWidgets.QTableWidget(Dialog)
		font = QtGui.QFont()
		font.setPointSize(10)
		self.tableWidget.setFont(font)
		self.tableWidget.setStyleSheet("QWidget {background-color: rgb(255, 255, 204);"
		                               "color: black;}"
		                               "QHeaderView::section {"
		                               "background-color:rgb(255, 255, 255);"
		                               "padding: 5px;"
		                               "font-size: 10pt;}"
		                               "QTableWidget {gridline-color: black;"
		                               "font-size: 10pt;}")
		self.tableWidget.setObjectName("tableWidget")
		self.tableWidget.setColumnCount(6)
		self.tableWidget.setRowCount(11)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setVerticalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setVerticalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setVerticalHeaderItem(2, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setVerticalHeaderItem(3, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setVerticalHeaderItem(4, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setVerticalHeaderItem(5, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setVerticalHeaderItem(6, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setVerticalHeaderItem(7, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setVerticalHeaderItem(8, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setVerticalHeaderItem(9, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setVerticalHeaderItem(10, item)
		item = QtWidgets.QTableWidgetItem()
		item.setTextAlignment(QtCore.Qt.AlignCenter)
		item.setBackground(QtGui.QColor(255, 255, 204))
		self.tableWidget.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(2, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(3, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(4, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(5, item)
		item = QtWidgets.QTableWidgetItem()
		item.setTextAlignment(QtCore.Qt.AlignCenter)
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		item.setFont(font)
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(0, 0, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		item.setFont(font)
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(0, 1, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		item.setFont(font)
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(0, 2, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		item.setFont(font)
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(0, 3, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		item.setFont(font)
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(0, 4, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		item.setFont(font)
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(0, 5, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		item.setFont(font)
		brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(1, 0, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		item.setFont(font)
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(1, 1, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		item.setFont(font)
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(1, 2, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setItalic(True)
		font.setWeight(75)
		item.setFont(font)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 204))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(1, 3, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(1, 4, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(1, 5, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(2, 0, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(2, 1, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(2, 2, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setItalic(True)
		font.setWeight(75)
		item.setFont(font)
		self.tableWidget.setItem(2, 3, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(2, 4, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(2, 5, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(3, 0, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(3, 1, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(3, 2, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setItalic(True)
		font.setWeight(75)
		item.setFont(font)
		self.tableWidget.setItem(3, 3, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(3, 4, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(3, 5, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(4, 0, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(4, 1, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(4, 2, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setItalic(True)
		font.setWeight(75)
		item.setFont(font)
		self.tableWidget.setItem(4, 3, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(4, 4, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(4, 5, item)
		item = QtWidgets.QTableWidgetItem()
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(5, 0, item)
		item = QtWidgets.QTableWidgetItem()
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(5, 1, item)
		item = QtWidgets.QTableWidgetItem()
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(5, 2, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setItalic(True)
		font.setWeight(75)
		item.setFont(font)
		self.tableWidget.setItem(5, 3, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(False)
		item.setFont(font)
		self.tableWidget.setItem(5, 4, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(5, 5, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		item.setFont(font)
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setForeground(brush)
		self.tableWidget.setItem(6, 0, item)
		item = QtWidgets.QTableWidgetItem()
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(6, 1, item)
		item = QtWidgets.QTableWidgetItem()
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(6, 2, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		item.setFont(font)
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(6, 3, item)
		item = QtWidgets.QTableWidgetItem()
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(6, 4, item)
		item = QtWidgets.QTableWidgetItem()
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(6, 5, item)
		item = QtWidgets.QTableWidgetItem()
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(7, 0, item)
		item = QtWidgets.QTableWidgetItem()
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(7, 1, item)
		item = QtWidgets.QTableWidgetItem()
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(7, 2, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setItalic(True)
		font.setWeight(75)
		item.setFont(font)
		self.tableWidget.setItem(7, 3, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(7, 4, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(7, 5, item)
		item = QtWidgets.QTableWidgetItem()
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(8, 0, item)
		item = QtWidgets.QTableWidgetItem()
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(8, 1, item)
		item = QtWidgets.QTableWidgetItem()
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(8, 2, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setItalic(True)
		font.setWeight(75)
		item.setFont(font)
		self.tableWidget.setItem(8, 3, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(8, 4, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(8, 5, item)
		item = QtWidgets.QTableWidgetItem()
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(9, 0, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setItalic(True)
		font.setWeight(75)
		item.setFont(font)
		self.tableWidget.setItem(9, 3, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(9, 4, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(9, 5, item)
		item = QtWidgets.QTableWidgetItem()
		brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
		brush.setStyle(QtCore.Qt.SolidPattern)
		item.setBackground(brush)
		self.tableWidget.setItem(10, 0, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setItalic(True)
		font.setWeight(75)
		item.setFont(font)
		self.tableWidget.setItem(10, 3, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(10, 4, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setItalic(True)
		item.setFont(font)
		self.tableWidget.setItem(10, 5, item)
		self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
		self.tableWidget.verticalHeader().setDefaultSectionSize(70)
		self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 1)

		self.retranslateUi(Dialog)
		self.buttonBox.accepted.connect(Dialog.accept)
		self.buttonBox.rejected.connect(Dialog.reject)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		_translate = QtCore.QCoreApplication.translate
		Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
		__sortingEnabled = self.tableWidget.isSortingEnabled()
		self.buttonBox2.setText("Загрузить предлагаемого контрагента")
		self.tableWidget.setSortingEnabled(False)
		item = self.tableWidget.item(0, 0)
		item.setText(_translate("Dialog", "Описание требования"))
		item = self.tableWidget.item(0, 1)
		item.setText(_translate("Dialog", "Обоснование требования"))
		item = self.tableWidget.item(0, 2)
		item.setText(_translate("Dialog", "Требование является обязательным? По какой причине?"))
		item = self.tableWidget.item(0, 3)
		item.setText(_translate("Dialog", "Предлагаемый претендент"))
		item = self.tableWidget.item(0, 4)
		item.setText(_translate("Dialog", "Альтернатива 1"))
		item = self.tableWidget.item(0, 5)
		item.setText(_translate("Dialog", "Альтернатива 2"))
		item = self.tableWidget.item(2, 0)
		item.setText(_translate("Dialog", "Условия оплаты "))
		item = self.tableWidget.item(2, 1)
		item.setText(_translate("Dialog", "Стандартные условия договоров образца НИПИгаз"))
		item = self.tableWidget.item(2, 2)
		item.setText(_translate("Dialog", "Да"))
		item = self.tableWidget.item(3, 0)
		item.setText(_translate("Dialog", "Срок поставки"))
		item = self.tableWidget.item(3, 1)
		item.setText(_translate("Dialog", "Стандартные условия закупки процедур НИПИгаз"))
		item = self.tableWidget.item(3, 2)
		item.setText(_translate("Dialog", "Да"))
		item = self.tableWidget.item(4, 0)
		item.setText(_translate("Dialog", "Согласие работы по стандартной форме договора"))
		item = self.tableWidget.item(4, 1)
		item.setText(_translate("Dialog", "Стандартные условия закупки процедур НИПИгаз"))
		item = self.tableWidget.item(4, 2)
		item.setText(_translate("Dialog", "Да"))
		item = self.tableWidget.item(5, 0)
		item.setText(_translate("Dialog", "Источник информации об альтернативных предложениях:"))
		item = self.tableWidget.item(5, 3)
		item.setText(_translate("Dialog", "Запрос КП"))
		item = self.tableWidget.item(5, 4)
		item.setText(_translate("Dialog", "Запрос КП"))
		item = self.tableWidget.item(5, 5)
		item.setText(_translate("Dialog", "Запрос КП"))
		item = self.tableWidget.item(6, 0)
		item.setText(_translate("Dialog", "Стоимость альтернатив:"))
		item = self.tableWidget.item(7, 0)
		item.setText(_translate("Dialog", "Стоимость предложения:"))
		item = self.tableWidget.item(8, 0)
		item.setText(_translate("Dialog", "Прочие коммерческие условия:"))
		item = self.tableWidget.item(8, 3)
		item.setText(_translate("Dialog", "Нет"))
		item = self.tableWidget.item(8, 4)
		item.setText(_translate("Dialog", "Нет"))
		item = self.tableWidget.item(8, 5)
		item.setText(_translate("Dialog", "Нет"))
		item = self.tableWidget.item(9, 0)

		item.setText(_translate("Dialog", "Дополнительные издержки при выборе альтернативных вариантов:"))
		item = self.tableWidget.item(10, 0)
		item.setText(_translate("Dialog", "Возможные потери при выборе альтернативных вариантов:"))
		item = self.tableWidget.item(10, 4)
		item.setText(
			_translate("Dialog", " Увеличение ожидания сроков и качества предоставления технической поддержки"))
		item = self.tableWidget.item(10, 5)
		item.setText(
			_translate("Dialog", " Увеличение ожидания сроков и качества предоставления технической поддержки"))
		self.tableWidget.setSortingEnabled(__sortingEnabled)
		for x in range(5):
			for y in range(6):
				self.tableWidget.item(x, y).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.item(5, 3).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.item(5, 4).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.item(5, 5).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.item(6, 3).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.item(6, 4).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.item(6, 5).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.item(7, 3).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.item(7, 4).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.item(7, 5).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.item(8, 3).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.item(8, 4).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.item(8, 5).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.item(9, 3).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.item(9, 4).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.item(9, 5).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.item(10, 3).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.item(10, 4).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.item(10, 5).setTextAlignment(QtCore.Qt.AlignCenter)

		self.tableWidget.setSpan(0, 0, 2, 1)
		self.tableWidget.setSpan(0, 1, 2, 1)
		self.tableWidget.setSpan(0, 2, 2, 1)

		self.tableWidget.setSpan(5, 0, 1, 3)
		self.tableWidget.setSpan(6, 0, 1, 5)

		self.tableWidget.setSpan(7, 0, 1, 3)
		self.tableWidget.setSpan(8, 0, 1, 3)
		self.tableWidget.setSpan(9, 1, 1, 2)
		self.tableWidget.setSpan(10, 1, 1, 2)

		self.tableWidget.setRowHeight(0, 40)
		self.tableWidget.setRowHeight(1, 40)
		self.tableWidget.setRowHeight(2, 70)
		self.tableWidget.setRowHeight(3, 70)
		self.tableWidget.setRowHeight(4, 70)

		self.tableWidget.setRowHeight(5, 25)
		self.tableWidget.setRowHeight(6, 25)
		self.tableWidget.setRowHeight(7, 25)
		self.tableWidget.setRowHeight(8, 25)
		self.tableWidget.setRowHeight(9, 80)
		self.tableWidget.setRowHeight(10, 80)
		self.tableWidget.resizeRowsToContents()

	def loadContragent(self):
		self.tableWidget.item(1, 3).setText(PPV.textEdit_3.toPlainText())
		price_1 = PPV.plainTextEdit_13.toPlainText()
		self.tableWidget.item(7, 3).setText(price_1 + " " + PPV.comboBox_5.itemText(PPV.comboBox_5.currentIndex()))

		self.tableWidget.item(2, 3).setText("")
		if PPV.toolBox_2.currentIndex() == 0:
			self.tableWidget.item(2, 3).setText("Лицензии: " + PPV.plainTextEdit_11.toPlainText())
		elif PPV.toolBox_2.currentIndex() == 1:
			self.tableWidget.item(2, 3).setText("Лицензии: " + PPV.plainTextEdit_56.toPlainText())
		elif PPV.toolBox_2.currentIndex() == 2:
			self.tableWidget.item(2, 3).setText("Лицензии: " + PPV.plainTextEdit_57.toPlainText())

		if PPV.toolBox.currentIndex() == 0:
			self.tableWidget.item(2, 3).setText(
				self.tableWidget.item(2, 3).text() + "\n""Услуги: " + PPV.plainTextEdit_58.toPlainText())
		elif PPV.toolBox.currentIndex() == 1:
			self.tableWidget.item(2, 3).setText(
				self.tableWidget.item(2, 3).text() + "\n""Услуги: " + PPV.plainTextEdit_59.toPlainText())
		elif PPV.toolBox.currentIndex() == 2:
			self.tableWidget.item(2, 3).setText(
				self.tableWidget.item(2, 3).text() + "\n""Услуги: " + PPV.plainTextEdit_60.toPlainText())

		self.tableWidget.item(3, 3).setText(
			PPV.plainTextEdit.toPlainText() + " " + PPV.comboBox_6.currentText() + " " + PPV.comboBox_7.currentText())
		self.tableWidget.resizeRowsToContents()


# МЕНЮ ВЫБОРА ПАСПОРТОВ
class Ui_Form(object):

	def setupUi(self, Form):
		Form.setObjectName("Form")
		Form.resize(318, 135)
		Form.setMinimumSize(QtCore.QSize(318, 135))
		Form.setMaximumSize(QtCore.QSize(318, 135))
		Form.setWindowTitle("Менеджер закупочной документации")
		self.gridLayout = QtWidgets.QGridLayout(Form)
		self.gridLayout.setObjectName("gridLayout")
		self.pushButton_3 = QtWidgets.QPushButton(Form)
		self.pushButton_3.setText("")
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("D:/BuyManager/icons/icons8-documents-folder-80.png"), QtGui.QIcon.Normal,
		               QtGui.QIcon.Off)
		self.pushButton_3.setIcon(icon)
		self.pushButton_3.setIconSize(QtCore.QSize(80, 80))
		self.pushButton_3.setObjectName("pushButton_3")
		self.gridLayout.addWidget(self.pushButton_3, 0, 3, 1, 1)
		self.pushButton = QtWidgets.QPushButton(Form)
		self.pushButton.setText("")
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap("D:/BuyManager/icons/icons8-document-80.png"), QtGui.QIcon.Normal,
		                QtGui.QIcon.Off)
		self.pushButton.setIcon(icon1)
		self.pushButton.setIconSize(QtCore.QSize(80, 80))
		self.pushButton.setObjectName("pushButton")
		self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)
		self.pushButton_2 = QtWidgets.QPushButton(Form)
		self.pushButton_2.setText("")
		icon2 = QtGui.QIcon()
		icon2.addPixmap(QtGui.QPixmap("D:/BuyManager/icons/icons8-documents-80.png"), QtGui.QIcon.Normal,
		                QtGui.QIcon.Off)
		self.pushButton_2.setIcon(icon2)
		self.pushButton_2.setIconSize(QtCore.QSize(80, 80))
		self.pushButton_2.setObjectName("pushButton_2")
		self.gridLayout.addWidget(self.pushButton_2, 0, 2, 1, 1)
		spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
		spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem1, 0, 4, 1, 1)
		self.pushButton_4 = QtWidgets.QPushButton(Form)
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		self.pushButton_4.setFont(font)
		self.pushButton_4.setObjectName("pushButton_4")
		self.gridLayout.addWidget(self.pushButton_4, 1, 1, 1, 3)
		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)
		Form.setWindowFlag(QtCore.Qt.CustomizeWindowHint, False)
		Form.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, False)
		Form.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
		Form.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
		Form.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
		Form.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
		Form.setWindowFlag(QtCore.Qt.WindowTitleHint, False)
		Form.setWindowFlag(QtCore.Qt.WindowSystemMenuHint, False)
		Form.setWindowFlag(QtCore.Qt.WindowStaysOnBottomHint, False)
		Form.setWindowFlag(QtCore.Qt.BypassWindowManagerHint, False)

	def retranslateUi(self, Form):
		_translate = QtCore.QCoreApplication.translate
		self.pushButton_4.setText(_translate("Form", "Выход"))
		self.pushButton_4.clicked.connect(Form.close)
		self.pushButton.clicked.connect(MainWindowMC.show)
		self.pushButton.clicked.connect(FirstWindow.hide)
		self.pushButton_2.clicked.connect(MainWindowPPV.show)
		self.pushButton_2.clicked.connect(FirstWindow.hide)


app = QtWidgets.QApplication(sys.argv)
MainWindowMC = QtWidgets.QMainWindow()
LotWindow = QtWidgets.QDialog()
ContactsWindow = QtWidgets.QDialog()
MVZWindow = QtWidgets.QDialog()

ui = Ui_MainWindow()
ui.setupUi(MainWindowMC)

di = Ui_Dialog()
di.setupUi(LotWindow)
di.setupUi2(ContactsWindow)
di.setupMVZ(MVZWindow)

MainWindowPPV = QtWidgets.QMainWindow()
PPV = Ui_MainWindowPPV()
PPV.setupUiPPV(MainWindowPPV)

Forma1 = QtWidgets.QDialog()
f1 = Ui_DialogForma1()
f1.setupUi(Forma1)

FirstWindow = QtWidgets.QWidget()
FW = Ui_Form()
FW.setupUi(FirstWindow)

FirstWindow.show()

# MainWindowPPV.show()


sys.exit(app.exec_())
