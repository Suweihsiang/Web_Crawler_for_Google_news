from PyQt5.QtWidgets import QApplication
from myMainWindow import QmyMainWindow
import sys

if __name__=="__main__":
    app=QApplication(sys.argv)
    form=QmyMainWindow()
    form.show()
    sys.exit(app.exec_())