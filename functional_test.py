from selenium import webdriver
import os
chrome_driver_path = "/home/yang/Downloads"
os.environ["PATH"] += os.pathsep + chrome_driver_path
browser = webdriver.Chrome()
browser.get('http://localhost:8080')

assert 'Django' in browser.title
