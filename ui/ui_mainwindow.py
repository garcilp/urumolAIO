# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_2kHjtQA.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QButtonGroup, QFormLayout, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QMainWindow, QSizePolicy, QSpacerItem,
    QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 520)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName(u"mainLayout")
        self.player1Group = QGroupBox(self.centralwidget)
        self.player1Group.setObjectName(u"player1Group")
        font = QFont()
        font.setBold(False)
        self.player1Group.setFont(font)
        self.player1Group.setAutoFillBackground(False)
        self.player1Horizontal = QHBoxLayout(self.player1Group)
        self.player1Horizontal.setObjectName(u"player1Horizontal")
        self.player1Left = QVBoxLayout()
        self.player1Left.setObjectName(u"player1Left")
        self.hboxLayout = QHBoxLayout()
        self.hboxLayout.setObjectName(u"hboxLayout")
        self.label = QLabel(self.player1Group)
        self.label.setObjectName(u"label")

        self.hboxLayout.addWidget(self.label)

        self.deckId1 = QLineEdit(self.player1Group)
        self.deckId1.setObjectName(u"deckId1")
        self.deckId1.setMaximumSize(QSize(292, 16777215))

        self.hboxLayout.addWidget(self.deckId1)

        self.player1ManaLayout = QHBoxLayout()
        self.player1ManaLayout.setObjectName(u"player1ManaLayout")

        self.hboxLayout.addLayout(self.player1ManaLayout)

        self.hboxLayout1 = QHBoxLayout()
        self.hboxLayout1.setObjectName(u"hboxLayout1")
        self.scoreSpacer1 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hboxLayout1.addItem(self.scoreSpacer1)


        self.hboxLayout.addLayout(self.hboxLayout1)


        self.player1Left.addLayout(self.hboxLayout)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.label1 = QLabel(self.player1Group)
        self.label1.setObjectName(u"label1")
        self.label1.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label1)

        self.playerName1 = QLineEdit(self.player1Group)
        self.playerName1.setObjectName(u"playerName1")
        self.playerName1.setMaximumSize(QSize(460, 16777215))

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.playerName1)

        self.label2 = QLabel(self.player1Group)
        self.label2.setObjectName(u"label2")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label2)

        self.deckName1 = QLineEdit(self.player1Group)
        self.deckName1.setObjectName(u"deckName1")
        self.deckName1.setMaximumSize(QSize(460, 16777215))

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.deckName1)

        self.player1WinsLayout = QHBoxLayout()
        self.player1WinsLayout.setObjectName(u"player1WinsLayout")

        self.formLayout.setLayout(2, QFormLayout.ItemRole.SpanningRole, self.player1WinsLayout)


        self.player1Left.addLayout(self.formLayout)


        self.player1Horizontal.addLayout(self.player1Left)


        self.mainLayout.addWidget(self.player1Group)

        self.centerBar = QHBoxLayout()
        self.centerBar.setSpacing(9)
        self.centerBar.setObjectName(u"centerBar")
        self.centerBar.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.lineLeft = QFrame(self.centralwidget)
        self.lineLeft.setObjectName(u"lineLeft")
        self.lineLeft.setFrameShape(QFrame.Shape.HLine)

        self.centerBar.addWidget(self.lineLeft)

        self.bo3Button = QToolButton(self.centralwidget)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.bo3Button)
        self.bo3Button.setObjectName(u"bo3Button")
        self.bo3Button.setCheckable(True)
        self.bo3Button.setChecked(True)

        self.centerBar.addWidget(self.bo3Button)

        self.swapButton = QToolButton(self.centralwidget)
        self.swapButton.setObjectName(u"swapButton")
        font1 = QFont()
        font1.setPointSize(18)
        self.swapButton.setFont(font1)

        self.centerBar.addWidget(self.swapButton)

        self.bo5Button = QToolButton(self.centralwidget)
        self.buttonGroup.addButton(self.bo5Button)
        self.bo5Button.setObjectName(u"bo5Button")
        self.bo5Button.setCheckable(True)

        self.centerBar.addWidget(self.bo5Button)

        self.lineRight = QFrame(self.centralwidget)
        self.lineRight.setObjectName(u"lineRight")
        self.lineRight.setFrameShape(QFrame.Shape.HLine)

        self.centerBar.addWidget(self.lineRight)


        self.mainLayout.addLayout(self.centerBar)

        self.player2Group = QGroupBox(self.centralwidget)
        self.player2Group.setObjectName(u"player2Group")
        self.player2Horizontal = QHBoxLayout(self.player2Group)
        self.player2Horizontal.setObjectName(u"player2Horizontal")
        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.setObjectName(u"vboxLayout")
        self.hboxLayout2 = QHBoxLayout()
        self.hboxLayout2.setObjectName(u"hboxLayout2")
        self.label3 = QLabel(self.player2Group)
        self.label3.setObjectName(u"label3")

        self.hboxLayout2.addWidget(self.label3)

        self.deckId2 = QLineEdit(self.player2Group)
        self.deckId2.setObjectName(u"deckId2")
        self.deckId2.setMaximumSize(QSize(292, 16777215))

        self.hboxLayout2.addWidget(self.deckId2)

        self.player2ManaLayout = QHBoxLayout()
        self.player2ManaLayout.setObjectName(u"player2ManaLayout")

        self.hboxLayout2.addLayout(self.player2ManaLayout)

        self.hboxLayout3 = QHBoxLayout()
        self.hboxLayout3.setObjectName(u"hboxLayout3")
        self.scoreSpacer2 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hboxLayout3.addItem(self.scoreSpacer2)


        self.hboxLayout2.addLayout(self.hboxLayout3)


        self.vboxLayout.addLayout(self.hboxLayout2)

        self.formLayout1 = QFormLayout()
        self.formLayout1.setObjectName(u"formLayout1")
        self.formLayout1.setFormAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.label4 = QLabel(self.player2Group)
        self.label4.setObjectName(u"label4")

        self.formLayout1.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label4)

        self.playerName2 = QLineEdit(self.player2Group)
        self.playerName2.setObjectName(u"playerName2")
        self.playerName2.setMaximumSize(QSize(460, 16777215))

        self.formLayout1.setWidget(0, QFormLayout.ItemRole.FieldRole, self.playerName2)

        self.label5 = QLabel(self.player2Group)
        self.label5.setObjectName(u"label5")

        self.formLayout1.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label5)

        self.deckName2 = QLineEdit(self.player2Group)
        self.deckName2.setObjectName(u"deckName2")
        self.deckName2.setMaximumSize(QSize(460, 16777215))

        self.formLayout1.setWidget(1, QFormLayout.ItemRole.FieldRole, self.deckName2)

        self.player2WinsLayout = QHBoxLayout()
        self.player2WinsLayout.setObjectName(u"player2WinsLayout")

        self.formLayout1.setLayout(2, QFormLayout.ItemRole.SpanningRole, self.player2WinsLayout)


        self.vboxLayout.addLayout(self.formLayout1)


        self.player2Horizontal.addLayout(self.vboxLayout)


        self.mainLayout.addWidget(self.player2Group)

        self.mainLayout.setStretch(0, 1)
        self.mainLayout.setStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Urumol Stream Manager", None))
        self.player1Group.setTitle(QCoreApplication.translate("MainWindow", u"PLAYER 1", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Deck", None))
        self.label1.setText(QCoreApplication.translate("MainWindow", u"Player", None))
        self.label2.setText(QCoreApplication.translate("MainWindow", u"Deck", None))
        self.bo3Button.setText(QCoreApplication.translate("MainWindow", u"BO3", None))
        self.swapButton.setText(QCoreApplication.translate("MainWindow", u"\u21c5", None))
        self.bo5Button.setText(QCoreApplication.translate("MainWindow", u"BO5", None))
        self.player2Group.setTitle(QCoreApplication.translate("MainWindow", u"PLAYER 2", None))
        self.label3.setText(QCoreApplication.translate("MainWindow", u"Deck", None))
        self.label4.setText(QCoreApplication.translate("MainWindow", u"Player", None))
        self.label5.setText(QCoreApplication.translate("MainWindow", u"Deck", None))
    # retranslateUi

