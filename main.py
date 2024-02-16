import os
import sys
from PyQt5.QtCore import Qt
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

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
            self.getImage()
            self.initUI()

        def getImage(self):
            url = 'http://static-maps.yandex.ru/1.x/?ll='
            map_request = f"{url}{','.join((toponym_coordinates).split())}&spn={str(self.maschtab)},{str(self.maschtab)}&l=map"
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

        def closeEvent(self, event):
            os.remove(self.map_file)

        def keyPressEvent(self, event):
            if event.key() == Qt.Key_PageUp and self.maschtab < 10:
                self.maschtab += 0.005
            if event.key() == Qt.Key_PageDown and self.maschtab > 0.006:
                self.maschtab -= 0.005
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