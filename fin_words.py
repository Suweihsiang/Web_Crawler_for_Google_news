from selenium import webdriver
from selenium.webdriver.common.by import By

url='https://www.fsc.gov.tw/ch/home.jsp?id=178&parentpath=0%2C6&mcustomize='                                        #FSC website

driver=webdriver.Firefox()                                                                                          #Firefox driver
driver.get(url)

pages=len(driver.find_element(By.CLASS_NAME,'select').find_elements(By.TAG_NAME,'option'))                          #total pages

with open('word_list.txt','w',encoding='utf-8') as f:                                                               #save all words to the file
    for page in range(pages):
        table=driver.find_element(By.XPATH,'//*[@id="messageform"]/div[2]/table').find_elements(By.TAG_NAME,'tr')   #all words in this page
        i = 0
        for t in table:
            if(i == 0) :                                                                                            #first row is not we want
                i += 1
                continue
            f.write(t.text.split(' ')[2])                                                                           #the third column is chinese vocabulary
            f.write('\n')
        driver.find_element(By.LINK_TEXT,'下一頁').click()
    driver.quit() 
    f.close()