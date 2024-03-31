import os
import sys
from PyQt5.QtCore import Qt
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton

requests_url = "http://geocode-maps.yandex.ru/1.x"
params = {'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
          'geocode': 'Саранск',
          'format': 'json'}
response = requests.get(requests_url, params=params)
if response:
    data = response.json()
    toponym = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
    # toponym_address = toponym['metaDataProperty']['GeocoderMetaData']['text']
    toponym_coordinates = toponym['Point']['pos']
    # lan, lat = map(float, toponym_coordinates.split())
    # print(f'{toponym_address} has coordinates: {toponym_coordinates}')
    razmer = [600, 450]


    class Example(QWidget):
        def __init__(self):
            super().__init__()
            self.maschtab = 0.002
            self.mnogitel = 0
            self.karta = 'map'
            self.toponym_coordinates = toponym_coordinates
            self.getImage()
            self.initUI()

        def getImage(self):
            url = 'http://static-maps.yandex.ru/1.x/?ll='
            map_request = f"{url}{','.join((self.toponym_coordinates).split())}&spn={str(self.maschtab)},{str(self.maschtab)}&l={self.karta}"
            response = requests.get(map_request)

            if not response:
                print("Ошибка выполнения запроса:")
                print(map_request)
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)
            self.map_file = "map.png"
            with open(self.map_file, "wb") as file:
                file.write(response.content)

        def initUI(self):
            self.setGeometry(100, 100, *razmer)
            self.setWindowTitle('Отображение карты')
            self.pixmap = QPixmap(self.map_file)
            self.image = QLabel(self)
            self.image.move(0, 0)
            self.image.resize(600, 450)
            self.image.setPixmap(self.pixmap)

            self.order_btn = QPushButton('Схема', self)
            self.order_btn.resize(100, 50)
            self.order_btn.move(0, 0)
            self.order_btn.clicked.connect(self.carta1)

            self.order_btn = QPushButton('Спутник', self)
            self.order_btn.resize(100, 50)
            self.order_btn.move(0, 50)
            self.order_btn.clicked.connect(self.carta2)

            self.order_btn = QPushButton('Гибрид', self)
            self.order_btn.resize(100, 50)
            self.order_btn.move(0, 100)
            self.order_btn.clicked.connect(self.carta3)

        def carta1(self):
            self.karta = 'map'
            self.getImage()
            self.izmenenie()

        def carta2(self):
            self.karta = 'sat'
            self.getImage()
            self.izmenenie()

        def carta3(self):
            self.karta = 'sat,skl'
            self.getImage()
            self.izmenenie()

        def closeEvent(self, event):
            os.remove(self.map_file)

        def keyPressEvent(self, event):
            if event.key() == Qt.Key_PageUp and self.maschtab < 30:
                self.maschtab += 0.005
                self.mnogitel += 1
            if event.key() == Qt.Key_PageDown and self.maschtab > 0.006:
                self.maschtab -= 0.005
                self.mnogitel -= 1
            if event.key() == Qt.Key_Up:
                self.toponym_coordinates = self.toponym_coordinates.split()
                if self.mnogitel != 0:
                    self.toponym_coordinates[1] = str(float(self.toponym_coordinates[1]) + 0.003 * self.mnogitel * 4)
                else:
                    self.toponym_coordinates[1] = str(float(self.toponym_coordinates[1]) + 0.003)
                self.toponym_coordinates = ' '.join(self.toponym_coordinates)
            if event.key() == Qt.Key_Down:
                self.toponym_coordinates = self.toponym_coordinates.split()
                if self.mnogitel != 0:
                    self.toponym_coordinates[1] = str(float(self.toponym_coordinates[1]) - 0.003 * self.mnogitel * 4)
                else:
                    self.toponym_coordinates[1] = str(float(self.toponym_coordinates[1]) - 0.003)
                self.toponym_coordinates = ' '.join(self.toponym_coordinates)
            if event.key() == Qt.Key_Right:
                self.toponym_coordinates = self.toponym_coordinates.split()
                if self.mnogitel != 0:
                    self.toponym_coordinates[0] = str(float(self.toponym_coordinates[0]) + 0.003 * self.mnogitel * 4)
                else:
                    self.toponym_coordinates[0] = str(float(self.toponym_coordinates[0]) + 0.003)
                self.toponym_coordinates = ' '.join(self.toponym_coordinates)
            if event.key() == Qt.Key_Left:
                self.toponym_coordinates = self.toponym_coordinates.split()
                if self.mnogitel != 0:
                    self.toponym_coordinates[0] = str(float(self.toponym_coordinates[0]) - 0.003 * self.mnogitel * 4)
                else:
                    self.toponym_coordinates[0] = str(float(self.toponym_coordinates[0]) - 0.003)
                self.toponym_coordinates = ' '.join(self.toponym_coordinates)
            self.getImage()
            self.izmenenie()

        def izmenenie(self):
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)


    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = Example()
        ex.show()
        sys.exit(app.exec())
else:
    print('Error:', requests_url)
    print('Satus:', response.status_code)
    print('Reason:', response.reason)