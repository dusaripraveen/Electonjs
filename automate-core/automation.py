from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def login_to_dynatrace(driver, email, password):
    # login
    login = driver.find_element(By.CSS_SELECTOR, "[type='email']")
    login.send_keys(email)
    login.send_keys(Keys.RETURN)

    time.sleep(2)

    # password
    password_data = driver.find_element(By.CSS_SELECTOR, "[type='password']")
    password_data.send_keys(password)
    password_data.send_keys(Keys.RETURN)
    time.sleep(2)


def automate_chrome(website, driver, email, password):
    report = website['report_name']
    url = website['data']['url']

    if website['data']['new_tab']:

        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(url)
    else:

        driver.get(url)

    if not website['data']['new_tab']:
        login_to_dynatrace(driver, email, password)

    try:
        back_to_login = driver.find_element(By.CSS_SELECTOR, "[type='button']")
        back_to_login.click()
    except Exception as e:
        print('login exception not thrown - ', e)

    time.sleep(2)

    try:
        print('trying to scroll towards right')
        # scroll to right
        try:
            print(f'report ---> {report}')
            if report == 'acom_online' or report == 'online_store_monthly':
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            else:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
            time.sleep(5)
            try:
                ribbon_button_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "ribbon-buttons")))
                dexp_actions_element = ribbon_button_element.find_element(By.TAG_NAME, 'dexp-actions')
                button_element = dexp_actions_element.find_element(By.TAG_NAME, 'button')
                button_element.click()
                print('clicking button popup')
                try:
                    print('accessing popup')
                    export_CSV = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//button/span[text()=' Export CSV ']")))
                    print('clicking download')
                    export_CSV.click()
                    print('download started')
                except Exception as e:
                    print('Exception while handling csv', e)

            except Exception as e:
                print('exception while clicking - ', e)
        except Exception as e:
            print('Error scrolling or loading tables: ', e)
    except Exception as e:
        print('Error occurred: ', e)
    finally:
        time.sleep(5)
        print(f'close activate --> {website['data']['close']}')
        if website['data']['close']:
            print('closing !!!!')
            driver.quit()
            
