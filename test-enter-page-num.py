
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
import random
import os
import requests
browser = webdriver.Chrome(executable_path="./chromedriver")

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
# Read utl
# url = "http://vanban.chinhphu.vn/portal/page/portal/chinhphu/hethongvanban"
url = "http://vanban.chinhphu.vn/portal/page/portal/chinhphu/hethongvanban"
browser.get(url)

selector = Select(browser.find_element_by_id('d_category_id'))
list_selector = []
for k in selector.options:
    list_selector.append(k.get_attribute('value'))

for i in range(1,len(list_selector)):
    
    print("vao lan thu {}".format(i))
    selector = Select(browser.find_element_by_id('d_category_id'))
    selector.select_by_value(list_selector[i])
    try:

        sleep(random.randint(2,5))
        selector_pagenum = Select(browser.find_element_by_id('d_page_id'))
        #lay ra cac trang hien co
        list_pagenum = []
        for k in selector_pagenum.options:
            list_pagenum.append(k.text)
        print(len(list_pagenum))
        print(list_pagenum)
        print("Da vao categori thu {}".format(list_selector[i]))
    except Exception as e:

        raw_text = browser.find_element_by_class_name("doc_list_total").text
        res = [int(i) for i in raw_text.split() if i.isdigit()]
        total_doc = res[0]
        print("Da vao exception! Totel doc = {}".format(total_doc))
        # for j in range(2,total_doc+2):
        # 
        #     doc_link = browser.find_element_by_xpath("//*[@id='highlight']/tbody/tr["+str(j)+"]/td[3]/a").get_attribute('href')
        # 
        #     browser.get(str(doc_link))
        # 
        #     sleep(random.randint(2,3))
        # 
        #     link = []
        #     link = browser.find_element_by_xpath("//*[@id='vbpq_content']/div[1]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/a").get_attribute('href')
        #     download(str(link),dest_folder="./data/"+str(list_selector[3]))
        #     sleep(1)
        #     browser.execute_script("window.history.go(-1)")
        #     sleep(random.randint(2,3))
 # selector = Select(browser.find_element_by_id('d_category_id'))
# selector.select_by_value(str(856))
# selector_pagenum = Select(browser.find_element_by_id('d_page_id'))
# selector_pagenum.select_by_visible_text('843')
# raw_text = browser.find_elements_by_xpath('.//span[@class = "navigator"]')[0].text
#     
# res = [int(i) for i in raw_text.split() if i.isdigit()]
# total_doc = res[1]
# print(res)
# print(total_doc)
# raw_text = browser.find_element_by_class_name("doc_list_total").text
# res = [int(i) for i in raw_text.split() if i.isdigit()]
# print(res[0])
# print(type(res[0]))
# sleep(random.randint(2,4))
# list_pagenum = []
# selector_pagenum = Select(browser.find_element_by_id('d_page_id'))
# for k in selector_pagenum.options:
#     list_pagenum.append(k.text)
# 
# print(list_pagenum)
# for f in range(len(list_pagenum)):
#     selector_pagenum.select_by_visible_text(list_pagenum[f])
