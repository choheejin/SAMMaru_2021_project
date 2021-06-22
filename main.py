################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
################################################################################
import datetime
import sys
import platform
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.uic import loadUi
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

# Crawling
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import csv
import requests
from selenium import webdriver


# GUI FILE
from ui_splash_screen import Ui_SplashScreen
from ui_main import Ui_MainWindow
from ui_m_bookTh import Ui_BookWindow
from ui_review import Ui_ReviewWindow

# GLOBALS
counter = 0
jumper = 10
global movieTitle

## ==> YOUR APPLICATION WINDOW
class ReviewWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui = Ui_ReviewWindow()
        self.ui.setupUi(self)
        self.ui.tableWidget.setColumnWidth(0, 10)
        self.ui.tableWidget.setColumnWidth(1, 150)
        self.ui.tableWidget.setColumnWidth(2, 60)
        self.ui.tableWidget.setColumnWidth(3, 110)
        self.ui.label.setText('\"'+ movieTitle + '\"')
        self.ui.btn_close.clicked.connect(lambda: self.buttonClose())
        self.ui.pushButton_3.clicked.connect(lambda: self.autoBook())
        self.ui.pushButton_4.clicked.connect(lambda: self.buttonClick())
        self.reviewMv()

    def reviewMv(self):
        URL = "https://movie.naver.com/movie/running/current.nhn"
        response = requests.get(URL)

        soup = BeautifulSoup(response.text, "html.parser")

        movie_data = []

        movies = soup.select('dt.tit a')
        for a_tag in movies:
            title = a_tag.text

            link_split = a_tag['href'].split('=')
            code = link_split[1]
            movie_tile_code = {
                'title': title,
                'code': code
            }
            movie_data.append(movie_tile_code)

        subBreak = True
        for movie in movie_data:
            if subBreak == False:
                break
            print()
            movie_code = movie['code']

            headers = {
                'authority': 'movie.naver.com',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-dest': 'iframe',
                'referer': 'https://movie.naver.com/movie/bi/mi/point.nhn?code=189069',
                'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'cookie': 'NRTK=ag#20s_gr#0_ma#-2_si#0_en#-1_sp#-1; ASID=731711cf0000017332744bcd0000005c; NM_THUMB_PROMOTION_BLOCK=Y; MM_NEW=1; NFS=2; MM_NOW_COACH=1; nx_ssl=2; NNB=HJOWCJ4MSYVF6; nid_inf=-1587872843; NID_AUT=ms/s8984xk6pp5LiYixmlL0IJ19FuO2FOm8M63dpFdlRQIer+58aNToXqSlELYWA; NID_JKL=9Vo5Vegco/eLv1m+6P1Kbt0bWcBm1Axn+OghbQooVbw=; BMR=s=1596694645166&r=https%3A%2F%2Fm.post.naver.com%2Fviewer%2FpostView.nhn%3FvolumeNo%3D29000825%26memberNo%3D15470144%26vType%3DVERTICAL&r2=https%3A%2F%2Fsearch.naver.com%2Fsearch.naver%3Fwhere%3Dnexearch%26sm%3Dtab_htk.nws%26ie%3Dutf8%26query%3D%25EB%25A5%2598%25ED%2598%25B8%25EC%25A0%2595%2B%25EC%259B%2590%25ED%2594%25BC%25EC%258A%25A4%2B%25EB%2585%25BC%25EB%259E%2580%25EC%2597%2590; page_uid=UyXlAlp0JywssPTkfEossssssYG-206097; NID_SES=AAABkPEddfvEDn4INl9+yjFY54DF1EAo9SXIt1ebEH/9DgMDSQwfatPgMGF/9beXBPUF1sun8XY4+EejzCKKpp+Mh2mooDsva1lg/m5Pg+4wpvJGDl9YwEPWuKCKOHqGaQK+mu0DSfA7rJvq6+tGjsNh52KPiszv8gxs2n4hX336qyFY+5LE0zkEjmVkbvJFfqCuX1sRpHCKSx5r7ql+/hwJUR1ckIVya6/XEheUE+fJcNeGFjaGR+FfCUVEQxRk8cRXkQ1NyCi1Hs487Eth02WVgXDYSBkJdL5DoYQMypX2NyxTbJoQqXX+SowjraC1GV+vw3j47tjiuvYK/IFUidW0Z4nF/wZCRq4J9ryiDvznMOfy0NO48fl5Vsw+P9FB3WIfOaXbjMDplKEcMTL4DpNxm3j+POHamQZ1qGRYhf8zYSu6aIWOrO8TnQ/KO9vrDhxJIVIYsFfZ96cq3qjwQ9WrcNRd1rLqZMNggXG5tImNVxn1m73Z2aJM/qqCu04G58ORcUW1u2TjjQ4ksyXzeOKo5IA=; REFERER_DOMAIN="d3d3Lmdvb2dsZS5jb20="; NM_VIEWMODE_AUTO=basic; csrf_token=5c41a00a-906f-450f-8594-970720a6feba',
            }

            params = (
                ('code', movie_code),
                ('type', 'after'),
                ('isActualPointWriteExecute', 'false'),
                ('isMileageSubscriptionAlready', 'false'),
                ('isMileageSubscriptionReject', 'false'),
            )

            response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', headers=headers,
                                    params=params)

            soup = BeautifulSoup(response.text, "html.parser")
            lis = soup.select('body > div > div > div.score_result > ul > li')
            # 우선 li 들을 리스트 형태로 받아오고 이를 반복문으로 돌린다.
            num = 1
            lists = []
            for li in lis:
                if num >= 10:
                    subBreak = False
                    break
                # li에서 별점정보를 찾는다.
                # 다만 성분이 단 하나임에도 이 역시 리스트형태로 반환됨이 확인되어
                # [0]로 값에 접근한 뒤 텍스트(별점)을 받아왔다
                star = li.select('div.star_score > em')[0].getText()
                # 이것도 리스트로 반환되서 [0] 처리
                p = li.select('div.score_reple > p > span')
                if len(p) == 2:
                    p = p[1]
                else:
                    p = p[0]
                # 내용이 길면 p안에 a태그가 존재한다
                # a가 존재할 경우 하나의 성분을, 없으면 [] 반환
                if movie['title'] == movieTitle:
                    strTitle = movie['title']
                    strStar = " [" + star + "점]"
                    strRe = p.text.strip()
                    self.ui.tableWidget.setItem(num, 0, QTableWidgetItem(str(num)))
                    self.ui.tableWidget.setItem(num, 1, QTableWidgetItem(strTitle))
                    self.ui.tableWidget.setItem(num, 2, QTableWidgetItem(strStar))
                    self.ui.tableWidget.setItem(num, 3, QTableWidgetItem(strRe))
                    num += 1


    def buttonClick(self):
        self.close()
        print("버튼클릭")
        self.main = MainWindow()
        self.main.show()

    def buttonClose(self):
        self.close()

    def autoBook(self):
        driver = webdriver.Chrome('c:/informs/chromedriver.exe')
        driver.implicitly_wait(3)
        url = "http://www.cgv.co.kr/ticket/"
        driver.get(url)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        now = datetime.datetime.now()
        self.ui.dateEdit.setDate(now.today())
        self.ui.btn_close.clicked.connect(lambda: self.buttonClose())
        self.ui.pushButton_2.clicked.connect(lambda: self.crawling())
        self.ui.pushButton_3.clicked.connect(lambda: self.buttonClick())
        self.ui.pushButton_4.clicked.connect(lambda: self.erase())
        self.ui.tableWidget.cellClicked.connect(lambda: self.celldoubleclicked_event())
        self.ui.tableWidget.cellDoubleClicked.connect(lambda: self.celldoubleclicked_event())

    def buttonClose(self):
        self.close()

    def buttonClick(self):
        print("버튼클릭")
        self.main = ReviewWindow()
        self.main.show()
        self.close()

    def celldoubleclicked_event(self):
        row = self.ui.tableWidget.currentIndex().row()
        data = self.ui.tableWidget.item(row, 0)
        global movieTitle
        movieTitle = data.text()
        print(movieTitle)
        print("셀 더블클릭 셀 값 : ", data.text())

    def erase(self):
        for i in range(1,16):
            Str = None
            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(Str))
            self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(Str))

    def crawling(self):
        def get_timetable(movie):
            lists = []
            timetables = movie.select('div > div.type-hall > div.info-timetable > ul > li')
            for timetable in timetables:
                time = timetable.select_one('em').get_text()
                seat = timetable.select_one('span').get_text()
                list = [time, seat]
                lists.append(list)
            answer = sum(lists, [])
            StrA = " ".join(answer)
            return StrA

        if self.ui.lineEdit_3.text() == 'CGV 용산아이파크몰':
            url_ = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0013&date='
            now = datetime.datetime.now()
            yea = now.year
            mon = now.month
            day = now.day
            add = str(yea) + '0' + str(mon) + str(day)
            url = url_+add
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'html.parser')
            movies = soup.select('body > div > div.sect-showtimes > ul > li')

            row = 1
            for movie in movies:
                title = movie.select_one('div>div.info-movie>a>strong').get_text().strip()
                timetable = get_timetable(movie)
                self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(title))
                self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(timetable))
                row=row+1

        if self.ui.lineEdit_3.text() == 'CGV 청주성안길':
            url_ = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=205&theatercode=0297&date='
            now = datetime.datetime.now()
            yea = now.year
            mon = now.month
            day = now.day
            add = str(yea) + '0' + str(mon) + str(day)
            url = url_ + add
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'html.parser')
            movies = soup.select('body > div > div.sect-showtimes > ul > li')

            row = 1
            for movie in movies:
                title = movie.select_one('div>div.info-movie>a>strong').get_text().strip()
                timetable = get_timetable(movie)
                self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(title))
                self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(timetable))
                row = row + 1



## ==> SPLASHSCREEN WINDOW
class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        ## ==> SET INITIAL PROGRESS BAR TO (0) ZERO
        self.progressBarValue(0)

        ## ==> REMOVE STANDARD TITLE BAR
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # Remove title bar
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # Set background to transparent

        ## ==> APPLY DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.ui.circularBg.setGraphicsEffect(self.shadow)

        ## QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(15)

        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##

    ## DEF TO LOANDING
    ########################################################################
    def progress (self):
        global counter
        global jumper
        value = counter

        # HTML TEXT PERCENTAGE
        htmlText = """<p><span style=" font-size:68pt;">{VALUE}</span><span style=" font-size:58pt; vertical-align:super;">%</span></p>"""

        # REPLACE VALUE
        newHtml = htmlText.replace("{VALUE}", str(jumper))

        if(value > jumper):
            # APPLY NEW PERCENTAGE TEXT
            self.ui.labelPercentage.setText(newHtml)
            jumper += 10

        # SET VALUE TO PROGRESS BAR
        # fix max value error if > than 100
        if value >= 100: value = 1.000
        self.progressBarValue(value)

        # CLOSE SPLASH SCREE AND OPEN APP
        if counter > 100:
            # STOP TIMER
            self.timer.stop()

            # SHOW MAIN WINDOW
            self.main = MainWindow()
            self.main.show()

            # CLOSE SPLASH SCREEN
            self.close()

        # INCREASE COUNTER
        counter += 0.5

    ## DEF PROGRESS BAR VALUE
    ########################################################################
    def progressBarValue(self, value):

        # PROGRESSBAR STYLESHEET BASE
        styleSheet = """
        QFrame{
        	border-radius: 150px;
        	background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} rgba(85, 170, 255, 255));
        }
        """

        # GET PROGRESS BAR VALUE, CONVERT TO FLOAT AND INVERT VALUES
        # stop works of 1.000 to 0.000
        progress = (100 - value) / 100.0

        # GET NEW VALUES
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)

        # SET VALUES TO NEW STYLESHEET
        newStylesheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2)

        # APPLY STYLESHEET WITH NEW VALUES
        self.ui.circularProgress.setStyleSheet(newStylesheet)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())
