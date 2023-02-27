import os
import sys
import requests
import subprocess

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QThread, pyqtSignal, QUrl

import time




class FlaskThread(QThread):
    started_signal = pyqtSignal()
    finished_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        subprocess.Popen(['python', 'back_flask.py'], cwd=os.path.abspath("./back"), shell=True)
        self.started_signal.emit()

        time.sleep(1)

        self.finished_signal.emit()

class AngularThread(QThread):
    started_signal = pyqtSignal()
    finished_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        angular_dir = os.path.abspath("IA_parle_moi_front")
        subprocess.Popen(['ng', 'serve', '--port', '4200'], cwd=angular_dir, shell=True)
        self.started_signal.emit()

        self.wait_until_angular_server_started()

        self.finished_signal.emit()

    def wait_until_angular_server_started(self):
        while True:
            try:
                response = requests.get("http://localhost:4200")
                if response.status_code == 200:
                    break
            except:
                pass

            time.sleep(0.1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assistant Virtuel")
        self.setGeometry(100, 100, 800, 600)

        self.flask_thread = FlaskThread(self)
        self.angular_thread = AngularThread(self)

        self.flask_thread.started_signal.connect(self.on_flask_thread_started)
        self.angular_thread.started_signal.connect(self.on_angular_thread_started)
        self.angular_thread.finished_signal.connect(self.on_angular_thread_finished)

        self.flask_thread.start()
        self.angular_thread.start()

    def on_flask_thread_started(self):
        print("Flask thread started.")

    def on_angular_thread_started(self):
        print("Angular thread started.")

    def on_angular_thread_finished(self):
        print("Angular thread finished.")

        # Attendre que les threads Flask et Angular soient tous deux terminés
        while self.flask_thread.isRunning() or self.angular_thread.isRunning():
            time.sleep(0.1)

        # Ajouter une vue de page Web à la fenêtre principale
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        # Charger le projet Angular dans la vue de la fenêtre principale
        url = QUrl("http://localhost:4200/accueil")
        self.browser.load(url)
        self.browser.loadFinished.connect(self.on_load_finished)

    def on_load_finished(self, ok):
        if ok:
            # La page a été chargée avec succès, on peut continuer avec le reste du code
            print("Page loaded successfully!")
        else:
            # Il y a eu une erreur lors du chargement de la page
            print("Page loading failed.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
