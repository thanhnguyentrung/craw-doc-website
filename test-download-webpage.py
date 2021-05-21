import os
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import pandas as pd
import requests
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



# 1. Khai bao bien browser
browser = webdriver.Chrome(executable_path="./chromedriver")

# Read utl
url = "http://vanban.chinhphu.vn/portal/page/portal/chinhphu/hethongvanban?class_id=1&_page=1&mode=detail&document_id=15381"

browser.get(url)
# link = browser.find_elements_by_css_selector(".doc_detail_file_link [href]")
link = browser.find_element_by_xpath("//*[@id='vbpq_content']/div[1]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/a").get_attribute('href')
# print(link)
download(str(link),dest_folder="./data/mydirtest")
