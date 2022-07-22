from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os
import time
from flask import Flask, render_template, request, make_response, Response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", data="https://i.pinimg.com/originals/b0/68/5b/b0685b0e8c16e8cb57534de738f446a0.gif")


@app.route('/generate', methods=['POST', 'GET'])
def generate():

    output = request.form.to_dict()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

    # options = webdriver.ChromeOptions()
    # options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    # chrome_driver_binary = r"C:\Users\princ\OneDrive\Documents\zulfi\AI Sapien\chromedriver.exe"
    # options.headless = True
    # driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)


    driver.get("https://replicate.com/kuprel/min-dalle")  

    time.sleep(1)  

    # Finding textbox and changing value
    # value = "arguments[0].value = " + output["text"] + ';'
    
    textBox = driver.find_element(By.XPATH, '//*[@id="tabs--1--panel--0"]/div/div/div[1]/form/div[1]/input')
    textBox.send_keys(Keys.CONTROL + "a")      
    textBox.send_keys(Keys.BACK_SPACE)
    textBox.send_keys(output["text"])
    # driver.execute_script(value, textBox)

    # Unchecking Progressive Images
    driver.find_element(By.XPATH, '//*[@id="tabs--1--panel--0"]/div/div/div[1]/form/div[3]/div/input').click()

    # Submit Button
    driver.find_element(By.XPATH, '//*[@id="tabs--1--panel--0"]/div/div/div[1]/form/button[1]/span').click()

    def finder():
        try:
            if driver.find_element(By.XPATH, '//*[@id="tabs--1--panel--0"]/div/div/div[2]/div/div[1]/div/div/a/img').is_displayed():
                print('------ found ------')
        except NoSuchElementException:
            time.sleep(3)
            finder()

    finder()

    # time.sleep(3)

    # get the image source
    img = driver.find_element(By.XPATH, '//*[@id="tabs--1--panel--0"]/div/div/div[2]/div/div[1]/div/div/a/img')

    src = img.get_attribute('src')

    print(src)

    driver.close()

    return render_template("index.html", data=src)

if __name__ == '__main__':
    app.run(debug=True)