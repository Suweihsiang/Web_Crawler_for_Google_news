import requests,bs4,re,docx
import jieba
from wordcloud import WordCloud
from collections import Counter
import traceback
import threading
from PyQt5.QtCore import QThread, pyqtSignal

class Utils(QThread):
    status_changed=pyqtSignal(str)                                              #signal of the status that send to GUI
    page_changed=pyqtSignal(str)                                                #signal of the page that send to GUI
    tree_changed=pyqtSignal(str)                                                #signal of the tree that send to GUI
    def __init__(self,parent=None):
        super().__init__(parent)

    def parser(self,url,path):
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
              AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/108.0.0.0 Safari/537.36',}
        newshtml=requests.get(url,headers=headers)                              #now we are at the google news page
        objSoup=bs4.BeautifulSoup(newshtml.text,'lxml')

        newsSoup=objSoup.find('div','MjjYud')
        news=newsSoup.find_all('div','SoaBEf')
        hrefs=[]                                                                #lists of news href
        nohrefs=[]                                                              #lists of news href that we not found
        for new in news:
            hrefs.append(new.find('a')['href'])

        pattern1=r'\d+-\d+-\d+'                                                 #the pattern of date,for example : YYYY-mm-dd
        pattern2=r'\d+/\d+/\d+'                                                 #the pattern of date,for example : YYYY/mm/dd
        camma=r'\W'                                                             #[^a-zA-Z0-9]
        count=0
        for href in hrefs:
            count+=1
            string=str(count)+'/'+str(len(hrefs))+' '+'  正在處理中'             #process status
            self.status_changed.emit(string)                                    #send status message to the GUI
            try:                                                                #the main part of this function
                if href.find('udn')>-1:                                         #UDN news
                    if href.find('money')>-1:
                        udnhtml=requests.get(href)
                        udnSoup=bs4.BeautifulSoup(udnhtml.text,'lxml')
                        title=udnSoup.find('h1','article-head__title').text
                        time=udnSoup.find('time','article-body__time').text
                        time=re.search(pattern2,time).group().replace('/','-')
                        content=''
                        paragraphs=udnSoup.find('section','article-body__editor').find_all('p')
                    else:
                        udnhtml=requests.get(href)
                        udnSoup=bs4.BeautifulSoup(udnhtml.text,'lxml')
                        title=udnSoup.find('h1','article-content__title').text
                        time=udnSoup.find('time','article-content__time').text
                        time=re.search(pattern1,time).group()
                        content=''
                        paragraphs=udnSoup.find('section','article-content__editor').find_all('p')
                elif href.find('cnyes')>-1:                                      #cnyes news
                    cnyeshtml=requests.get(href,headers=headers)
                    cnyesSoup=bs4.BeautifulSoup(cnyeshtml.text,'lxml')
                    title=cnyesSoup.find('section','t1el8oye').find('h1').text
                    time=cnyesSoup.find('p','alr4vq1').text
                    time=re.search(pattern1,time).group().replace('/','-')
                    content=''
                    paragraphs=cnyesSoup.find(id='article-container').find_all('p')
                elif href.find('chinatimes')>-1:                                #China times
                    if href.find('wantrich')>-1:
                        chinahtml=requests.get(href)
                        chinaSoup=bs4.BeautifulSoup(chinahtml.text,'lxml')
                        title=chinaSoup.find('h1','article-title').text
                        time=chinaSoup.find('time').find('span','date').text
                        content=''
                        paragraphs=chinaSoup.find('div','article-body').find_all('p')
                    else:
                        chinahtml=requests.get(href)
                        chinaSoup=bs4.BeautifulSoup(chinahtml.text,'lxml')
                        title=chinaSoup.find('h1','article-title').text
                        time=chinaSoup.find('time').find('span','date').text
                        time=re.search(pattern2,time).group().replace('/','-')
                        content=''
                        paragraphs=chinaSoup.find('div','main-figure').find_all('p')
                elif href.find('yahoo')>-1:                                     #Yahoo! news
                    if href.find('tw')>-1:                                      #Taiwan news
                        yahoohtml=requests.get(href)
                        yahooSoup=bs4.BeautifulSoup(yahoohtml.text,'lxml')
                        title=yahooSoup.find('div','caas-title-wrapper').find('h1').text
                        time=yahooSoup.find('time')['datetime']
                        time=re.search(pattern1,time).group()
                        content=''
                        paragraphs=yahooSoup.find('div','caas-body').find_all('p')
                    elif href.find('hk')>-1:                                    #Hong Kong news
                        yahoohtml=requests.get(href,headers=headers)
                        yahooSoup=bs4.BeautifulSoup(yahoohtml.text,'lxml')
                        title=yahooSoup.find('div','caas-title-wrapper').text
                        time=yahooSoup.find('time')['datetime']
                        time=re.search(pattern1,time).group()
                        content=''
                        paragraphs=yahooSoup.find('div','caas-body').find_all('p')
                elif href.find('blocktempo')>-1:                                #BlockTempo news
                    blocktempohtml=requests.get(href)
                    blocktempoSoup=bs4.BeautifulSoup(blocktempohtml.text,'lxml')
                    title=blocktempoSoup.find('h1','jeg_post_title').text
                    time=blocktempoSoup.find('div','jeg_meta_date').a.text
                    content=''
                    paragraphs=blocktempoSoup.find('div','content-inner').find_all('p')
                elif href.find('epochtimes')>-1:                                #Epoch times
                    epochtimeshtml=requests.get(href)
                    epochtimesSoup=bs4.BeautifulSoup(epochtimeshtml.text,'lxml')
                    title=epochtimesSoup.find('h1','blue18 title').text
                    time=epochtimesSoup.find('div','mbottom10 large-12 medium-12 small-12 columns').time.text
                    time=re.search(pattern1,time).group()
                    content=''
                    paragraphs=epochtimesSoup.find('div',itemprop='articleBody').find_all('p')
                elif href.find('dailyfxasia')>-1:                               #DailyFX news
                    dailyfxasiahtml=requests.get(href)
                    dailyfxasiaSoup=bs4.BeautifulSoup(dailyfxasiahtml.text,'lxml')
                    title=dailyfxasiaSoup.find('h1','dfx-articleHead__header m-0').text
                    time=dailyfxasiaSoup.find('div','dfx-articleHead__articleDetails').find('time')['data-time']
                    time=re.search(pattern1,time).group()
                    content=''
                    paragraphs=dailyfxasiaSoup.find('div','dfx-articleBody__content mt-4').find_all('p')
                elif href.find('ctee')>-1:                                      #ctee news
                    if href.find('policy')>-1 or href.find('view')>-1:
                        string=str(count)+'/'+str(len(hrefs))+' '+'無法產生word檔及文字雲'
                        self.status_changed.emit(string)
                        nohrefs.append(href)
                        continue   
                    else:
                        cteehtml=requests.get(href,headers=headers)
                        cteeSoup=bs4.BeautifulSoup(cteehtml.text,'lxml')
                        title=cteeSoup.find('h1','main-title ').text
                        time=cteeSoup.find('li','publish-date')['time']
                        time=re.search(pattern1,time).group()
                        content=''
                        paragraphs=cteeSoup.find('div','content__body').find_all('p')
                elif href.find('ltn')>-1:                                       #LTN news
                    ltnhtml=requests.get(href)
                    ltnSoup=bs4.BeautifulSoup(ltnhtml.text,'lxml')
                    title=ltnSoup.find('div','whitecon boxTitle boxText').h1.text
                    time=ltnSoup.find('span','time').text
                    time=re.search(pattern2,time).group().replace('/','-')
                    content=''
                    paragraphs=ltnSoup.find('div','text').find_all('p')
                elif href.find('ettoday')>-1:                                   #ETToday news
                    ethtml=requests.get(href)
                    etSoup=bs4.BeautifulSoup(ethtml.text,'lxml')
                    title=etSoup.find('h1','title').text
                    time=etSoup.find('time','date').text
                    time=re.search(pattern1,time).group()
                    content=''
                    paragraphs=etSoup.find('div','story').find_all('p')
                else:                                                           #not in the lists of the news network
                    string=str(count)+'/'+str(len(hrefs))+' '+'無法產生word檔及文字雲'
                    self.status_changed.emit(string)
                    nohrefs.append(href)
                    continue
            except:                                                             #some error occurs when we parse the href
                string=str(count)+'/'+str(len(hrefs))+' '+'  爬蟲失敗，請檢查爬蟲程式'
                self.status_changed.emit(string)
                tbmsgfn='tracebackmsg.txt'                                      #save the error message in the file
                tbfn=open(path+tbmsgfn,'a')
                tbfn.write(href+'  爬蟲失敗\n')
                traceback.print_exc(file=tbfn)
                tbfn.write('-'*70+'\n')
                tbfn.close()
                continue
            try:                                                                #try to generate the Word file and wordcolud of the news
                string=str(count)+'/'+str(len(hrefs))+' '+'%s  正在產生word檔及文字雲'%title
                self.status_changed.emit(string)
                for paragraph in paragraphs:                                    #write the news content
                    content+=paragraph.text+'\n'
                title=re.sub(camma,'',title)                                    #remove the special symbols of the news title
                fn=str(time)+title+'.docx'
                fnDoc=docx.Document()                                           #generate the Word file
                fnDoc.add_paragraph(content)
                fnDoc.save(path+fn)
                self.tree_changed.emit(fn)                                      #send message to GUI tree
                jieba.set_dictionary('dict.txt.big.txt')                        #cut the content using jieba
                jieba.load_userdict('user_dict.txt')
                words=jieba.cut(content)
                w=[]                                                            #the words in the content
                stops=[]                                                        #stop words
                with open('stopword.txt','r',encoding='utf-8') as stopObj:
                    stopwords=stopObj.readlines()
                    for stopword in stopwords:
                        stops.append(stopword.rstrip())
                for word in words:
                    if len(word)>1:
                        if word not in stops:
                            w.append(word)
                counts=Counter(w)                                               #frequency of all words in the content
                fnwc=str(time)+title+'.png'                                     #wordcloud file
                wc=WordCloud(font_path='mingliu',width=2160,height=1440)        #generate wordcloud
                wc.generate_from_frequencies(counts)
                wc.to_file(path+fnwc)
                self.tree_changed.emit(fnwc)
            except:                                                             #some error occurs when we generate wordcloud
                string=str(count)+'/'+str(len(hrefs))+' '+'  生成word檔及文字雲時發生錯誤'
                self.status_changed.emit(string)
                tbmsgfn='tracebackmsg.txt'
                tbfn=open(path+tbmsgfn,'a')
                tbfn.write(href+'  無法生成word檔或文字雲'+'\n')
                traceback.print_exc(file=tbfn)
                tbfn.write('-'*70+'\n')
                tbfn.close()
                continue
        nofn='find_href_yourself.txt'                                           #save the hrefs that we parse unsuccesefully in this file
        with open(path+nofn,'a') as nofnObj:
            for nohref in nohrefs:
                nofnObj.write(nohref+'\n')
            nofnObj.close()

    def hrefpage(self,url,totalPage):                                           #collections of google news page href
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
        AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/108.0.0.0 Safari/537.36',}
        newshtml=requests.get(url,headers=headers)
        objSoup=bs4.BeautifulSoup(newshtml.text,'lxml')
        pageSoup=objSoup.find('tr',jsname='TeSSVd')
        pageA=pageSoup.find_all('a')
        google='https://www.google.com'
        pages=[]
        for i in range(totalPage):
            pages.append(google+pageA[i]['href'])
        return pages
    
    def run(self,url,totalpage,path):
        self.parser(url,path)                                   #parse news in first page

        pages=self.hrefpage(url,int(totalpage)-1)               #collections of google news page href
        p=1
        for page in pages:                                      #parse news in other page
            p+=1
            string='第'+str(p)+'頁'+'/'+'共'+str(totalpage)+'頁'
            self.page_changed.emit(string)
            self.parser(page,path)
        string='爬蟲結束'
        self.status_changed.emit(string)