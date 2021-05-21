from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
import random
import os
import requests

#function download file link
def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))

#function get link and download it
def preprocess_download(browser, list_selector,j,i):
    doc_link = browser.find_element_by_xpath("//*[@id='highlight']/tbody/tr["+str(j)+"]/td[3]/a").get_attribute('href')

    browser.get(str(doc_link))

    sleep(random.randint(2,3))

    link = []
    link = browser.find_element_by_xpath("//*[@id='vbpq_content']/div[1]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/a").get_attribute('href')
    download(str(link),dest_folder="./data/"+str(list_selector[i]))
    sleep(1)
    browser.execute_script("window.history.go(-1)")
    sleep(random.randint(2,3))

# 1. Khai bao bien browser
browser = webdriver.Chrome(executable_path="./chromedriver")

# Read utl
url = "http://vanban.chinhphu.vn/portal/page/portal/chinhphu/hethongvanban"
browser.get(url)

sleep(random.randint(2,4))

#find Linh Vuc, luu vao list_selector
selector = Select(browser.find_element_by_id('d_category_id'))
list_selector = []
for k in selector.options:
    list_selector.append(k.get_attribute('value'))

#duyet qua tat ca cac linh vuc, ngoai tru linh vuc 0 (tat ca)

for i in range(len(list_selector)):
    if(list_selector[i] == '0'):
        continue
    else:
        #chon tung linh vuc
        selector = Select(browser.find_element_by_id('d_category_id'))
        selector.select_by_value(list_selector[i])
        try:
            print("Process categori {}".format(list_selector[i]))
            sleep(random.randint(2,5))
            selector_pagenum = Select(browser.find_element_by_id('d_page_id'))
            #lay ra cac trang hien co
            list_pagenum = []
            for k in selector_pagenum.options:
                list_pagenum.append(k.text)
            #duyet cac trang
    
            for f in range(len(list_pagenum)):
                # print(list_pagenum[f])
                selector_pagenum = Select(browser.find_element_by_id('d_page_id'))
                selector_pagenum.select_by_visible_text(list_pagenum[f])

                #neu la trang cuoi cung
                if(list_pagenum[f]==list_pagenum[-1]):
                    raw_text_1 = browser.find_elements_by_xpath('.//span[@class = "navigator"]')[0].text
                    res = [int(i) for i in raw_text_1.split() if i.isdigit()]
                    temp_doc = res[1]
                    total_doc = temp_doc - 50*(len(list_pagenum)-1)
                    for j in range(2,total_doc+2):
                        preprocess_download(browser,list_selector,j,i)
                else:
                    #lay tat ca cac link trong trang thuoc linh vuc do
                    for j in range(2,52):
                        preprocess_download(browser,list_selector,j,i)
        except Exception as e:
            print("Process categori {}".format(list_selector[i]))
            raw_text = browser.find_element_by_class_name("doc_list_total").text
            res = [int(i) for i in raw_text.split() if i.isdigit()]
            total_doc = res[0]
            for j in range(2,total_doc+2):
                preprocess_download(browser,list_selector,j,i)

browser.close()

