#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
driver = webdriver.Chrome(executable_path="/home/oni/Music/project01/drivers/chromedriver")

driver.maximize_window()
driver.get("http://127.0.0.1:8000/")
time.sleep(3)
# Register a user
'''driver.find_element_by_name("firstname").send_keys("Anisul")
driver.find_element_by_name("lastname").send_keys("Islam")
driver.find_element_by_id("username").send_keys("Bitsbee")
driver.find_element_by_name("email").send_keys("anisulislam@gmail.com")

# Does not interactable
driver.find_element_by_name("password").send_keys("JaniNaAmiKichui")
driver.find_element_by_name("confpassword").send_keys("JaniNaAmiKichui")


driver.find_element_by_xpath("//*[text()='Sign Up']").send_keys(Keys.ENTER)'''

# For successfull sign in

driver.find_element_by_class_name("btn-outline-primary").send_keys(Keys.ENTER)
time.sleep(3)
driver.find_element_by_id("email").send_keys("omg")
driver.find_element_by_id("password").send_keys("omg12345")
driver.find_element_by_class_name("btn-primary").send_keys(Keys.ENTER)

time.sleep(5)
print(driver.current_url)
alr = driver.find_element_by_name("mesg")
print(alr.text)

driver.find_element_by_xpath("//*[text()='Sign Out']").send_keys(Keys.ENTER)
alr = driver.find_element_by_name("mesg")
print(alr.text)

time.sleep(5)
# For unsuccessfull sign in

driver.find_element_by_class_name("btn-outline-primary").send_keys(Keys.ENTER)
time.sleep(3)
driver.find_element_by_id("email").send_keys("hackerX")
driver.find_element_by_id("password").send_keys("hackerXtream")
driver.find_element_by_class_name("btn-primary").send_keys(Keys.ENTER)

time.sleep(5)
print(driver.current_url)
alr = driver.find_element_by_name("mesg")
print(alr.text)


#driver.close()
print("Test has been run successfully")
