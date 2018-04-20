import webbrowser, sys, re, selenium, os, time, shutil
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

def run(uploadDirectory, daily_limit):

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    browser = webdriver.Chrome(chrome_options=options)
    browser.set_window_size(200,200)

    i = 0
    try:
        for filename in os.listdir(uploadDirectory):
            i += 1
            if i > daily_limit:
                break
            s = {}
            s['type'] = 'HOUSE_BRAND'
            s['brand'] = 'Cacophony Media'
            s['title'] = input('Enter title for ' + os.path.splitext(filename)[0] + ': ')
            s['feat1'] = input('Enter feature 1 for ' + s['title'] + ': ')
            s['feat2'] = input('Enter feature 2 for ' + s['title'] + ': ')
            s['color'] = 'black, dark heather, navy, baby blue, asphalt'.upper()
            s['fit'] = 'womens, men, kids'.upper()
            s['price'] = '12.99'
            s['file'] = uploadDirectory + '/' + filename
            s['desc'] = input('Enter description for ' + s['title'])

            if not bool(s['type'].strip()):
                print("Shirt type cannot be empty.")
                break
            elif not bool(s['brand'].strip()):
                print("Shirt brand cannot be empty.")
                break
            elif not bool(s['title'].strip()):
                print("Shirt title cannot be empty.")
                break
            elif not bool(s['color'].strip()):
                print("Shirt colors cannot be empty.")
                break
            elif not bool(s['fit'].strip()):
                print("Shirt fit cannot be empty.")
                break
            elif not bool(s['price'].strip()):
                print("Shirt price cannot be empty.")
                break
            elif not bool(s['file'].strip()):
                print("Shirt file name cannot be empty.")
                break

            if len(s['desc']) > 0 and len(s['desc']) < 75 or len(s['desc']) > 2000:
                print("Description must be either empty or between 75 and 2000 characters. Error for file - " + s['file'])
                break

            if not s['file'].endswith(".png"):
                print("Must provide a file name ending with '.png'. Filename given - " + s['file'])
                break

            if not os.path.exists(s['file']):
                print("This file does not exist in the this directory - " + s['file'])
                break

            try:
                integral, fractional = s['price'].split('.')
                n = float(s['price'])
                if len(fractional) == 2:
                    pass
                else:
                    raise ValueError
            except ValueError:
                print('Error with your price, please enter it as 4 digits, for example 19.99. You entered - ' + s['price'])
                break

            browser.get('http://merch.amazon.com/merch-tshirt/title-setup/new/upload_art')

            try:
                emailElem = browser.find_element_by_id('ap_email')
                userEmail = input('Enter your email: ')
                userPass = input('Enter your password: ')
                emailElem.send_keys(userEmail)
                passwordElem = browser.find_element_by_id('ap_password')
                passwordElem.send_keys(userPass)
                passwordElem.submit()
            except:
                pass

            #wait to get past login screen, either by automatic login or by user logging in
            WebDriverWait(
                        browser, 90
                ).until(EC.presence_of_element_located((By.ID, 'data-draft-tshirt-assets-front-image-asset-cas-shirt-art-image-file-upload-AjaxInput')))

            #upload file
            browser.find_element_by_id("data-draft-tshirt-assets-front-image-asset-cas-shirt-art-image-file-upload-AjaxInput").send_keys(os.getcwd()+"/"+s['file'])

            try:
                print("waiting for processing message to appear")
                WebDriverWait(
                        browser, 60
                ).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, '#data-draft-tshirt-assets-front-image-asset-cas-shirt-art-image-file-upload-uploading-message.a-hidden')))

                print("waiting for processing message to disappear")
                WebDriverWait(
                        browser, 60
                ).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#data-draft-tshirt-assets-front-image-asset-cas-shirt-art-image-file-upload-uploading-message.a-hidden')))

                time.sleep(4)

                print("clicking continue")
                browser.find_element_by_id("save-and-continue-upload-art-announce").click()
            except:
                print("timed out looking")

            WebDriverWait(
                        browser, 20
                ).until(EC.visibility_of_element_located((By.ID, 'data-draft-list-prices-marketplace-1-amount')))
            #new we must set price, shirt type, fit type, and colors
            #set Price
            priceElem = browser.find_element_by_id("data-draft-list-prices-marketplace-1-amount")
            priceElem.clear()
            priceElem.send_keys(s['price'])

            #fit type
            fits = s['fit'].split(",")
            fits = [x.strip(' ') for x in fits]

            WebDriverWait(
                        browser, 20
                ).until(EC.visibility_of_element_located((By.ID, 'data-shirt-configurations-fit-type-men')))
            #men and women selected by default, do opposite
            if not any(f in fits for f in ["MEN","MENS"]):
                browser.find_element_by_id("data-shirt-configurations-fit-type-men").send_keys(selenium.webdriver.common.keys.Keys.SPACE)
            if not any(f in fits for f in ["WOMEN","WOMENS"]):
                browser.find_element_by_id("data-shirt-configurations-fit-type-women").send_keys(selenium.webdriver.common.keys.Keys.SPACE)
            if any(f in fits for f in ["YOUTH","YOUTHS","KID","KIDS"]):
                browser.find_element_by_id("data-shirt-configurations-fit-type-youth").send_keys(selenium.webdriver.common.keys.Keys.SPACE)

            #do colors
            colors = s['color'].split(",")
            colors = [x.strip().replace(" ","_").replace("-","_").lower() for x in colors]

            #selected by default, remove
            browser.find_element_by_id("gear-checkbox-silver").click()

            for c in colors:
                browser.find_element_by_id("gear-tshirt-image").click()
                time.sleep(.25)
                n = c.lower()

                browser.find_element_by_id("gear-checkbox-"+n).click()

            #continue
            browser.find_element_by_id("save-and-continue-choose-variations-announce").click()

            WebDriverWait(
                        browser, 20
                ).until(EC.visibility_of_element_located((By.ID, 'data-draft-brand-name')))

            #text details
            browser.find_element_by_id('data-draft-brand-name').send_keys(s['brand'])
            browser.find_element_by_id('data-draft-name-en-us').send_keys(s['title'])
            browser.find_element_by_id('data-draft-bullet-points-bullet1-en-us').send_keys(s['feat1'])
            browser.find_element_by_id('data-draft-bullet-points-bullet2-en-us').send_keys(s['feat2'])
            browser.find_element_by_id('data-draft-description-en-us').send_keys(s['desc'])
            browser.find_element_by_id("save-and-continue-announce").click()

            WebDriverWait(
                        browser, 20
                ).until(EC.presence_of_element_located((By.ID, 'publish-announce')))

            #review and submit
            browser.find_element_by_xpath("//*[contains(text(), 'Sell - Public on Amazon')]").click()
            time.sleep(4)
            browser.find_element_by_id("publish-announce").click()
            time.sleep(4)
            browser.execute_script("document.getElementById('publish-confirm-button-announce').click();")

            WebDriverWait(
                        browser, 60
                ).until(EC.presence_of_element_located((By.ID, 'landing-page')))

    finally:
        browser.close()
