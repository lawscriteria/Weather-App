import sys
import requests
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit

from datetime import datetime, timezone, timedelta
from tzlocal import get_localzone

TIME = datetime.now(get_localzone())
tz = TIME.utcoffset().total_seconds()

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        #--> window comps

        self.setFixedSize(500, 400)
        self.setWindowTitle("Lawi's Weather App")
        self.setWindowIcon(QIcon("weathericon.png"))
        
        #--> background image

        self.bgimg = QLabel(self)
        self.pixmap = QPixmap("weatherbg.jpg")

        #--> Widgets

        #---> container widget and layout

        self.container = QWidget()
        self.layout = QVBoxLayout()

        #---> top widget and layout

        self.top_widget = QWidget()
        self.top_layout = QGridLayout()

        self.city_name = QLineEdit(self)
        self.submit_city_name = QPushButton(self)
        self.current_time = QLabel(f"{TIME.date()} \n {TIME.strftime('%H:%M:%S')}", self)
        
        self.temp = QLabel(self)
        self.hd = QLabel(self)
        self.dp = QLabel(self)
        self.vis = QLabel(self)

        self.feels_like = QLabel(self)
        self.desc_icon = QLabel(self)

        self.infos1 = QWidget()
        self.infos2 = QWidget()
        self.infos3 = QWidget()

        self.infos_layout1 = QHBoxLayout()
        self.infos_layout2 = QHBoxLayout()
        self.infos_layout3 = QHBoxLayout()

        self.infos_layout1.addWidget(self.temp)
        self.infos_layout2.addWidget(self.hd)
        self.infos_layout1.addWidget(self.dp)
        self.infos_layout2.addWidget(self.vis)

        self.infos_layout3.addWidget(self.feels_like)
        self.infos_layout3.addWidget(self.desc_icon)

        self.infos1.setLayout(self.infos_layout1)
        self.infos2.setLayout(self.infos_layout2)
        self.infos3.setLayout(self.infos_layout3)

        self.top_layout.addWidget(self.city_name, 0, 0)
        self.top_layout.addWidget(self.submit_city_name, 2, 1)
        self.top_layout.addWidget(self.current_time, 0, 1)

        self.top_layout.addWidget(self.infos1, 1, 0)
        self.top_layout.addWidget(self.infos2, 1, 1)
        self.top_layout.addWidget(self.infos3, 2, 0)

        self.top_widget.setLayout(self.top_layout)

        self.layout.addStretch()

        #--> adding to the layout

        self.layout.addWidget(self.top_widget)

        #--> setting fixed height for top wg

        self.top_widget.setFixedHeight(200)

        #--> setting the layout for the container widget

        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        #--> UI initialization

        self.UI()
        self.setFocus()

        #--> timer

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        #--> click events

        self.submit_city_name.clicked.connect(self.get_weather)
        self.city_name.installEventFilter(self)


    def UI(self):

        self.city_name.setPlaceholderText("Enter city name")
        self.submit_city_name.setText("Search")

        self.city_name.setAlignment(Qt.AlignCenter)
        self.current_time.setAlignment(Qt.AlignCenter)
        self.temp.setAlignment(Qt.AlignCenter)
        self.hd.setAlignment(Qt.AlignCenter)
        self.dp.setAlignment(Qt.AlignCenter)
        self.vis.setAlignment(Qt.AlignCenter)
        self.feels_like.setAlignment(Qt.AlignCenter)
        self.desc_icon.setAlignment(Qt.AlignCenter)

        self.bgimg.setGeometry(0, 0, 500, 400)
        self.bgimg.setPixmap(self.pixmap)
        self.bgimg.setScaledContents(True)

        self.city_name.setObjectName("city_name")
        self.submit_city_name.setObjectName("submit")
        self.current_time.setObjectName("time")

        self.temp.setObjectName("info")
        self.hd.setObjectName("info")
        self.dp.setObjectName("info")
        self.vis.setObjectName("info")

        self.desc_icon.setObjectName("emoji")

        self.top_widget.setObjectName("top_widget")
        self.infos1.setObjectName("infos_widget")
        self.infos2.setObjectName("infos_widget")
        self.infos3.setObjectName("infos_widget")

        self.setStyleSheet('''

                        * { font-family: 'Poppins'; color: black; margin: 0; }
                           
                        QWidget#top_widget { border: 1px solid white; padding: 1px; }

                        QLabel { border: 1px solid white; color: white; font-size: 15px; font-weight: bolder; padding: 0; }  
                           
                        QLabel#info { padding: 0; font-size: 15px; background-color: whitesmoke; color: black; border-radius: 15px; } 

                        QLineEdit { padding: 15px 50px; border-bottom-right-radius: 15px; border-top-right-radius: 15px; font-size: 15px; }
                           
                        QPushButton { padding: 10px 50px; background-color: rgb(19, 56, 158); color: white; border-bottom-left-radius: 15px; border-top-left-radius: 15px; font-size: 20px; text-transform: uppercase; }
                           
                        QLabel#time { padding: 0px; border: none; background-color: black; color: white; font-family: 'Courier New'; }
                           
                        QHBoxLayout { border: none; }
                           
                        #emoji { font-family: Segoe UI emoji; font-size: 30px; border: none; }

''')
        
    def update_time(self):
        self.current_time.setText(datetime.now(timezone(timedelta(seconds=tz))).strftime('%Y-%m-%d \n %H:%M:%S'))

    def get_weather(self):
        api_key = "63e2b6bee3ddf2e20758e780477bb687"
        city_name = self.city_name.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

        try:
            resp = requests.get(url)
            resp.raise_for_status()

            data = resp.json()

            if data['cod'] == 200:
                self.temp.setText(f"Temperature: \n {data['main']['temp']}°C")
                self.dp.setText(f"Pressure: \n {data['main']['pressure']}hPa")
                self.hd.setText(f"Humidity: \n {data['main']['humidity']}")
                self.vis.setText(f"Visibility: \n {data['visibility']}km")
                self.feels_like.setText(f"Feels like: \n {data['main']['feels_like']}°C")
                self.desc_icon.setText(f"{self.set_emoji(data['weather'][0]['id'])}")
                
                global tz
                tz = data['timezone']

                self.city_name.setStyleSheet("font-size: 20px; padding: 15px 50px; ")
        except requests.exceptions.HTTPError as e:
            match resp.status_code:
                case 400: self.display_error("Bad Request: Please check your input and try again")
                case 401: self.display_error("Unauthorized: Invalid API key")
                case 403: self.display_error("Forbidden: Access is denied")
                case 404: self.display_error("Not Found: City not found")
                case 500: self.display_error("Internal Server Error: Please try again later")
                case 502: self.display_error("Bad Gateway: Invalid response from server")
                case 503: self.display_error("Service Unavailable: Server is down")
                case 504: self.display_error("Gateway Timeout: No response from server")
                case _: self.display_error(f'HTTP Error Occurred: {e}')
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error: Please check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error: The request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects: Check the URL")
        except requests.exceptions.RequestException as re:
            self.display_error(f"Request Error: {re}")
    
    def display_error(self, msg):
        self.city_name.clear()
        self.city_name.setStyleSheet("font-size: 10px; padding: 15px 0px")
        self.city_name.setPlaceholderText(msg)

        self.temp.clear()
        self.dp.clear()
        self.hd.clear()
        self.vis.clear()
        self.feels_like.clear()
        self.desc_icon.clear()

        global tz
        tz = TIME.utcoffset().total_seconds()

        self.pixmap = QPixmap("weatherbg.jpg")
        self.bgimg.setPixmap(self.pixmap)

    def set_emoji(self, id):
        self.pixmap = QPixmap("weatherbg.jpg")
        emoji = ""
        if 200 <= id <= 232:
            self.pixmap = QPixmap("thunderstorm.jpg")
            emoji = "⛈"
        elif 300 <= id <= 321:
            self.pixmap = QPixmap("drizzle.jpg")
            emoji = "🌦"
        elif 500 <= id <= 531:
            self.pixmap = QPixmap("rain.jpg")
            emoji = "🌧"
        elif 600 <= id <= 622:
            self.pixmap = QPixmap("snowfall.jpg")
            emoji = "❄" 
        elif 701 <= id <= 731:
            self.pixmap = QPixmap("fog.jpg")
            emoji = "🌁"
        elif id == 762:
            self.pixmap = QPixmap("volcanic-ashes.jpg")
            emoji = "🌋"
        elif id == 771:
            self.pixmap = QPixmap("windy.jpg")
            emoji = "💨"
        elif id == 781:
            self.pixmap = QPixmap("tornado.jpg")
            emoji = "🌪"
        elif id == 800:
            self.pixmap = QPixmap("sunny.jpg")
            emoji = "☀"
        elif 801 <= id <= 804:
            self.pixmap = QPixmap("cloudy.jpg")
            emoji = "⛅"
        self.bgimg.setPixmap(self.pixmap)
        return emoji


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_app = App()
    my_app.show()

    # App Exit

    sys.exit(app.exec_())