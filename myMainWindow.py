import sys,os,threading
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import QApplication, QHeaderView, QLabel,QMainWindow,QTreeWidgetItem,QFileDialog
from PyQt5.QtCore import Qt, pyqtSlot,QThread

from ui_MainWindow import Ui_MainWindow                             #GUI
from utils import Utils                                             #web  crawler utils
class QmyMainWindow(QMainWindow):                                   #this class is inherit from QMainWindow
    global curDirPath                                               #current directory path
    curDirPath=os.getcwd()
    global save_path                                                #save files to the deirectory
    save_path=curDirPath+'\\'
    def __init__(self,parent=None):
        super().__init__(parent)                                    #use QMainWindow inititialize function 
        self.ui=Ui_MainWindow()                                     #construct GUI
        self.ui.setupUi(self)
        curDirName=os.path.basename(curDirPath)                     #current directory's name
        curFiles=os.listdir(curDirPath)                             #lists of files in the current directory
        self.setRootChild(curDirName,curDirPath,curFiles,curDirPath)#construct the tree of this directory
        self.label_page=QLabel()                                    #show the page that we currently in
        self.ui.statusbar.addWidget(self.label_page)
        self.label_news=QLabel()                                    #show the current news title
        self.ui.statusbar.addWidget(self.label_news)
        self.pix_wordcloud=QPixmap()                                #show the wordcloud of the news
    
#=====================================由connectSlotByName()自動連結的槽函數===================================================
    @pyqtSlot()
    def on_actionOpen_triggered(self):
        Dir=QFileDialog.getExistingDirectory(self,'請選擇資料夾')
        if Dir!="":
            self.ui.tree_Text.clear()
            DirName=os.path.basename(Dir)
            Files=os.listdir(Dir)
            self.setRootChild(DirName,Dir,Files,curDirPath)
            global save_path
            save_path=Dir+'/'

    @pyqtSlot()
    def on_btn_Browse_clicked(self):
        self.ut=Utils()                                                             #web crawler utils
        q=str(self.ui.KeyWord.text())                                               #the news that we want to query
        start_month=str(self.ui.date_Start.date().month())                          #the date of query interval
        start_day=str(self.ui.date_Start.date().day())
        start_year=str(self.ui.date_Start.date().year())
        end_month=str(self.ui.date_End.date().month())
        end_day=str(self.ui.date_End.date().day())
        end_year=str(self.ui.date_End.date().year())
        totalpage=self.ui.combo_Page.currentText()                                  #the number of page that we want to query
        url='https://www.google.com/search?q='+q+'&rlz=1C1CHBF_zh-TWTW971TW971&biw=1280&bih=625&source=lnt&tbs=cdr%3A1%2Ccd_min%3A'+start_month+'%2F'+start_day+'%2F'+start_year+'%2Ccd_max%3A'+end_month+'%2F'+end_day+'%2F'+end_year+'&tbm=nws'           #google news url
        self.ut.status_changed.connect(self.do_statuschanged)                       #currently status
        self.ut.page_changed.connect(self.do_pageChanged)                           #the page we currently in
        self.ut.tree_changed.connect(self.do_treeChanged)                           #update the tree
        self.label_page.setText('第1頁/共'+str(totalpage)+'頁')                      #show the page 
        thread=threading.Thread(target=self.ut.run,args=(url,totalpage,save_path))  #synchronousln run web crawler function
        thread.start()
    @pyqtSlot(QTreeWidgetItem,int)
    def on_tree_Text_itemDoubleClicked(self,item,column):                           #double click the item of the tree
        file_name=item.text(column)
        file_path=save_path+file_name
        _,extension=os.path.splitext(file_name)
        if extension=='.png':                                                       #show the picture
            self.pix_wordcloud.load(file_path)
            label_height=self.ui.WordCloud.height()
            label_width=self.ui.WordCloud.width()
            scaled_pix_wordcloud=self.pix_wordcloud.scaled(label_width-5,label_height-5)
            self.ui.WordCloud.setPixmap(scaled_pix_wordcloud)


#============================================自定義槽函數===================================================================

    def do_statuschanged(self,string):                  #show current news title
        self.label_news.setText(string)

    def do_pageChanged(self,string):                    #show current page we are in
        self.label_page.setText(string)

    def do_treeChanged(self,string):                    #update tree
        if os.path.exists(save_path+string):            #the file is exist
            Child=QTreeWidgetItem()
            Child.setText(0,string)
            _,extension=os.path.splitext(string)
            self.setChildIcon(Child,extension,string,curDirPath)
            self.ui.tree_Text.topLevelItem(0).addChild(Child)
            self.ui.tree_Text.topLevelItem(0).sortChildren(0,Qt.SortOrder.AscendingOrder)

#==========================================自訂函數========================================================================
    def setRootChild(self,rootname,rootpath,rootfiles,curpath):                         #construct the tree widget
        Root=QTreeWidgetItem()
        Root.setText(0,rootname)                                                        #top of the tree
        Root.setIcon(0,QIcon(curpath+'\\images\\folder.png'))
        if len(rootfiles) != 0:                                                         #all of files in the directory
            for i in range(len(rootfiles)):
                Child=QTreeWidgetItem()
                Child.setText(0,rootfiles[i])
                _,extension=os.path.splitext(rootfiles[i])
                self.setChildIcon(Child,extension,rootfiles[i],curpath)
                Root.addChild(Child)
        self.ui.tree_Text.addTopLevelItem(Root)
        self.ui.tree_Text.topLevelItem(0).sortChildren(0,Qt.SortOrder.AscendingOrder)
        self.ui.tree_Text.expandAll()

    def setChildIcon(self,Child,extension,file,curpath):                                #set the file's icon
        if extension == ".py":
            Child.setIcon(0,QIcon(curpath+'\\images\\py.png'))
        elif extension=='.txt':
            Child.setIcon(0,QIcon(curpath+'\\images\\text.png'))
        elif extension=='.png':
            Child.setIcon(0,QIcon(curpath+'\\images\\photo.png'))
        elif extension=='.docx':
            Child.setIcon(0,QIcon(curpath+'\\images\\docx.png'))
        elif extension=='':
            Child.setIcon(0,QIcon(curpath+'\\images\\folder.png'))
        else:
            Child.setIcon(0,QIcon(curpath+'\\images\\other.png'))
    
    def resizeEvent(self,event):
        label_height=self.ui.WordCloud.height()
        label_width=self.ui.WordCloud.width()
        if not self.pix_wordcloud.isNull():
            scaled_pix_wordcloud=self.pix_wordcloud.scaled(label_width-5,label_height-5)
            self.ui.WordCloud.setPixmap(scaled_pix_wordcloud)

#==========================================表單測試程式=====================================================================
if __name__=="__main__":
    app=QApplication(sys.argv)
    form=QmyMainWindow()
    form.show()
    sys.exit(app.exec_())