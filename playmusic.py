#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging,time
from collections import deque
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

class PlayMusic:
  def __init__(self,login_id,password,playlist,driver=None):
    self.playlist = playlist
    self.login_id = login_id
    self.password = password
    self.logger = logging.getLogger('Play Music')
    self.logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    fh = logging.FileHandler("playmusic.log",mode="a")
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    self.logger.addHandler(ch)
    self.logger.addHandler(fh)

    self.logger.info("Initialize..")
    self.profile = webdriver.FirefoxProfile()

    self.driver = webdriver.PhantomJS(
      executable_path='/usr/local/bin/phantomjs',
      desired_capabilities={
        'phantomjs.page.settings.userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
      },
      service_args=['--ssl-protocol=tlsv1'],
    )
    if driver == "chrome":
      self.driver = webdriver.Chrome()
    self.logger.info("Play Music Login..")
    self.driver.get("https://accounts.google.com/")
    WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR,'#Email'))
    )
    self.driver.find_elements_by_css_selector('#Email')[0].send_keys(self.login_id)
    self.driver.find_elements_by_css_selector('#next')[0].send_keys('\n')
    WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR,'#Passwd'))
    )
    self.driver.find_elements_by_css_selector('#Passwd')[0].send_keys(self.password)
    self.driver.find_elements_by_css_selector('#signIn')[0].send_keys('\n')
    self.driver.get(self.playlist)
    WebDriverWait(self.driver, 30).until(
      EC.presence_of_element_located((By.CSS_SELECTOR,'.song-table'))
    )
    self.driver.find_elements_by_css_selector('th[data-col=duration]')[0].click()
    time.sleep(1)
    document = BeautifulSoup(self.driver.page_source,"lxml")
    songlen = int(document.select(".song-table tbody")[0].get("data-count"))
    self.logger.info(str(songlen)+"曲を編集します")
    for i in range(0,songlen):
      self.logger.info(str(i+1)+"曲目")
      song = None
      while not song:
        try:
          for tr in self.driver.find_elements_by_css_selector('[data-index]'):
            if tr.get_attribute('data-index') == str(i):
              song = tr
          if not song:
            self.driver.execute_script('document.getElementById("mainContainer").scrollTop += 64');
        except:
          song = None

      time.sleep(2)
      actions = webdriver.ActionChains(self.driver)
      actions.move_to_element(song)
      actions.context_click(song)
      actions.perform()

      edit = None
      while edit != ':e':
        actions = webdriver.ActionChains(self.driver)
        print(edit)
        try:
          edit = self.driver.find_elements_by_css_selector('.goog-menuitem-highlight')[0].get_attribute('id')
        except:
          edit = None
        if edit != ':e':
          actions.send_keys(u'\ue015')
        actions.perform()
        time.sleep(0.1)

      actions = webdriver.ActionChains(self.driver)
      actions.send_keys(u'\ue007')
      actions.perform()
      time.sleep(1.5)

      self.logger.info("おすすめを使用")
      self.driver.find_elements_by_css_selector('[data-action=use-suggestions]')[0].send_keys('\n')
      time.sleep(0.5)

      self.logger.info("保存")
      self.driver.find_elements_by_css_selector('[data-action=save]')[0].send_keys('\n')
      time.sleep(2)
