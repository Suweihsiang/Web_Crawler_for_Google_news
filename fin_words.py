from selenium import webdriver
from selenium.webdriver.common.by import By

url='https://www.fsc.gov.tw/ch/home.jsp?id=178&parentpath=0%2C6&mcustomize='                                    #FSC website

driver=webdriver.Firefox()                                                                                      #Firefox driver
driver.get(url)

pages=len(driver.find_element(By.CLASS_NAME,'select').find_elements(By.TAG_NAME,'option'))                      #total pages

word_list=[]                                                                                                    #save financial words

for page in range(pages-1):
    table=driver.find_element(By.XPATH,'//*[@id="messageform"]/div[2]/table').find_elements(By.TAG_NAME,'tr')   #all words in this page
    for t in table:
        word_list.append(t.text.split(' ')[2])
    driver.find_element(By.LINK_TEXT,'下一頁').click()
driver.quit()                                                                                                   #close all associated windoe

with open('word_list1.txt','w',encoding='utf-8') as f:
    for word in word_list:
        f.write(word)
        f.write('\n')
    f.close()