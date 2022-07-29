from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from flask import Flask, render_template, request, make_response, Response, jsonify
from urllib.parse import unquote
import pymysql
import os

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def generate():

    # output = request.form.to_dict()

    #  --- PRODUCTION --- #

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

    #  --- DEVELOPMENT --- #

#     options = webdriver.ChromeOptions()
#     options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
#     chrome_driver_binary = r"C:\Users\princ\OneDrive\Documents\zulfi\AI Sapien\chromedriver.exe"
#     options.headless = True
#     driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)

    #  --- ----------- --- #

    text = request.args.get('q', default = 'A mango tree on moon, 4k, Photorealetic', type = str)
    text = unquote(text)
    print('-----------')
    print(text)
    print('-----------')
    driver.get("https://www.craiyon.com/")  

    time.sleep(1)
    
    print('----- URL LOADED -----')

    driver.execute_script("document.querySelector('#prompt').innerHTML = '" + text + "';")
        
    print('----- TEXT INPUT -----')

    driver.execute_script("document.querySelector('#app > div > div > div.mt-4.flex.w-full.justify-center.rounded-lg.rounded-b-none > button').click();")
    
    print('----- SUBMIT CLICK -----')

    def finder():
        try:
            if driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div/div[1]/div[1]/img').is_displayed():
                print('----- FOUND IMAGES -----')
        except NoSuchElementException:
            time.sleep(5)
            finder()

    finder()

    # get the image source
    p1 = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div/div[1]/div[1]/img').get_attribute('src')
    p2 = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div/div[1]/div[2]/img').get_attribute('src')
    p3 = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div/div[1]/div[3]/img').get_attribute('src')
    p4 = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div/div[1]/div[4]/img').get_attribute('src')
    p5 = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div/div[1]/div[5]/img').get_attribute('src')
    p6 = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div/div[1]/div[6]/img').get_attribute('src')
    p7 = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div/div[1]/div[7]/img').get_attribute('src')
    p8 = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div/div[1]/div[8]/img').get_attribute('src')
    p9 = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div/div[1]/div[9]/img').get_attribute('src')
    
    # Delete record
    conn = pymysql.connect(host="zulfi.me", port=3306, user="zulfi_public", passwd="Qwerty@007", db="zulfi_ai-sapien")
    myCursor = conn.cursor()
    print(myCursor)

    sql = """delete from `table` where 1
        """
    myCursor.execute(sql)
    conn.commit()
    print(myCursor.rowcount, "record deleted.")

    # Add record
    sql = """insert into `table` (title, data1, data2, data3, data4, data5, data6, data7, data8, data9)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
        """
    val = (text, p1, p2, p3, p4, p5, p6, p7, p8, p9)
    myCursor.execute(sql, val)
    conn.commit()
    print(myCursor.rowcount, "record inserted.")

    driver.close()

    return "SUCCESS"

if __name__ == '__main__':
    app.run(debug=True)
