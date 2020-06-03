# %%
from selenium import webdriver
import time
import re

# opt = webdriver.EdgeOptions()
# options.use_chromium = True
# driver = webdriver.Edge()

# %%
opt = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=opt)

driver.get('https://www.baidu.com/')  # 打开网页

# driver.maximize_window()                      #最大化窗口
time.sleep(5)  # 加载等待

# driver.find_element_by_xpath(
# "./*//span[@class='bg s_ipt_wr quickdelete-wrap']/input").send_keys("魅族")  # 利用xpath查找元素进行输入文本
driver.find_element_by_id('kw').send_keys("小米")  # 候选方法
driver.find_element_by_xpath(
    "//span[@class='bg s_btn_wr']/input").click()  # 点击按钮


# %%
