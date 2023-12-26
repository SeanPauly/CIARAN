from PyQt6.QtCore import QObject, QUrl, pyqtSlot
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
import shutil

class Backend(QObject):
    def __init__(self):
        super().__init__()

    @pyqtSlot(str)  # Define the slot to receive a string argument
    def processFile(self, fileUrl):
        file_path = fileUrl
        print(f"File selected: {file_path}")

        destination_folder = "./data/input/text"

        try:
            shutil.copy(file_path, destination_folder)
            print(f"File copied to {destination_folder}")
        except Exception as e:
            print(f"Error copying file: {e}")

if __name__ == "__main__":
    import sys

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)

    engine.load(QUrl.fromLocalFile("./modules/user_interaction/user_interface.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
