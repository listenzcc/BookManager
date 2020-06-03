# %%
# Importing
# System
import os
import time
import threading

# Database
import pandas as pd

# Print
from pprint import pprint

# Web driver
import webbrowser
from selenium import webdriver

# Settings
# Init Options
OPT = webdriver.FirefoxOptions()
PROFILE = webdriver.firefox.options.Options()
PROFILE.binary = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
PROFILE.set_preference("browser.helperApps.neverAsk.saveToDisk",
                       "text/plain,application/octet-stream,application/pdf,application/x-pdf,application/vnd.pdf,application/zip")
PROFILE.set_preference('browser.download.manager.showWhenStarting', False)
# PROFILE.update_preferences()

# Get Paper Table
table_name = os.path.join('files', 'table.json')
TABLE = pd.read_json(table_name)
if 'Inventory' not in TABLE.columns:
    TABLE['Inventory'] = ''
TABLE

# %%


def open_click_close(src):
    # Open Firefox Browser
    print(f'Working on {src}')
    driver = webdriver.Firefox(options=OPT, firefox_options=PROFILE)
    driver.get(src)

    # Wait for open
    time.sleep(5)

    # Click
    print(f'Click on {src}')
    driver.find_elements_by_xpath(
        "//span[@class='button-alt-override-icon']")[1].click()

    # Close
    time.sleep(20)
    driver.close()
    print(f'Done on {src}')


# Get TABLE rows that have no inventory
table = TABLE.loc[TABLE['Inventory'] == '']

# Automatic load from table
threads = []
for src in table['Src']:
    # Where am I
    print(src)
    # continue

    webbrowser.open(src)
    continue

    # Operation
    t = threading.Thread(target=open_click_close, args=(src, ))
    t.start()

    # SLEEP 5 seconds,
    # VERY IMPORTANT !!!
    time.sleep(5)

    # Save the thread instance
    threads.append(t)

# Wait for unfinished threads
for t in threads:
    t.join()

# All done
input('All done. Press Enter to escape.')


# %%

# driver.get('https://www.baidu.com/')  # 打开网页

# # driver.maximize_window()                      #最大化窗口
# time.sleep(5)  # 加载等待

# # driver.find_element_by_xpath(
# # "./*//span[@class='bg s_ipt_wr quickdelete-wrap']/input").send_keys("魅族")  # 利用xpath查找元素进行输入文本
# driver.find_element_by_id('kw').send_keys("小米")  # 候选方法
# driver.find_element_by_xpath(
#     "//span[@class='bg s_btn_wr']/input").click()  # 点击按钮


# %%
