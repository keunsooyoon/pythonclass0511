
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
# from PyQt5.QtCore import *

import requests                      # 파이썬으로 웹페이지 연결
from bs4 import BeautifulSoup as bs  # 분석을 용이하게 정제
import pandas as pd                  # 데이터 분석 관련 모듈
from selenium import webdriver     # 브라우저의 소스 읽어오기

form_class = uic.loadUiType("musicchart.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #버튼 클릭 인식해서 btn_clicked 매서드를 호출
        self.pushButton.clicked.connect(self.btn_clicked)  # 벅스 조회 단추
        self.pushButton_2.clicked.connect(self.btn_clicked2)  # 지니 조회 단추


    def btn_clicked(self):  #벅스 조회 매서드
        
        rank = 1

        html = requests.get('https://music.bugs.co.kr/chart')  # 페이지 소스 읽어오기
        soup = bs(html.text)     

        titles = soup.select('p.title > a')
        artists = soup.select('p.artist > a')



        for each in range(len(soup.select('p.title > a'))):  # 100번 반복

            self.tableWidget.resizeColumnsToContents()

            title = titles[each].text.strip()
            artist = artists[each].text.strip()
            
            self.tableWidget.setItem(each, 0, QTableWidgetItem("벅스"))
            self.tableWidget.setItem(each, 1, QTableWidgetItem(str(rank)))
            self.tableWidget.setItem(each, 2, QTableWidgetItem(title))
            self.tableWidget.setItem(each, 3, QTableWidgetItem(artist))
            rank += 1


    def btn_clicked2(self):  #지니 조회 매서드

        rank = 1

        driver = webdriver.Chrome('chromedriver.exe')  #크롬 브라우저 띄우기
        driver.get('https://www.genie.co.kr/chart/top200?ditc=D&ymd=20220513&hh=20&rtm=Y&pg=1')     #사이트 연결
        html = driver.page_source    
        soup = bs(html)

        songs = soup.select('tr.list')

        for song in songs:
            title = song.select('a.title.ellipsis')[0].text.strip()
            artist = song.select('a.artist.ellipsis')[0].text.strip()
            
            self.tableWidget.setItem(rank-1, 0, QTableWidgetItem("지니"))
            self.tableWidget.setItem(rank-1, 1, QTableWidgetItem(str(rank)))
            self.tableWidget.setItem(rank-1, 2, QTableWidgetItem(title))
            self.tableWidget.setItem(rank-1, 3, QTableWidgetItem(artist))            

            rank += 1



app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()


