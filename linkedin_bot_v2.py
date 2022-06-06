# Import the libraries to handle the work
# if the libraries were not installed, they will be installed automatically
try:
    import pandas as pd
    import numpy as np
    import openpyxl
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    import time
    import warnings
    import re
    from selenium import webdriver
except ImportError:
    import pip
    pip.main(['install', '--user', 'selenium'])
    pip.main(['install', '--user', 'webdriver_manager'])
    pip.main(['install', '--user', 'openpyxl'])
    import pandas as pd
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium import webdriver
    import time
    import warnings
    import re

warnings.filterwarnings('ignore')

def scroll_down_page(driver, speed=8):
        current_scroll_position, new_height= 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = driver.execute_script("return document.body.scrollHeight")

"""
    - Util Functions to scrap all the connections :
"""

MY_CONNECTIONS_LINK = 'https://www.linkedin.com/mynetwork/invite-connect/connections/'

def scrape_connections(driver, wait):

    driver.get(MY_CONNECTIONS_LINK)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.mn-connection-card')))

    number_of_connections = driver.find_element_by_css_selector("#ember30 .t-black.t-normal").text
    print("\nThere are ",number_of_connections)
    print("--> Collecting Connections ...")

    total_connections_text = driver.find_element_by_css_selector('.mn-connections').text
    total_connections = int(re.search(r'(\d+)', total_connections_text).group(1))

    scroll_to_bottom(total_connections,driver)
    return get_all_connections(driver,wait)


def get_all_connections(driver,wait):
    connections = []
    for el in visible_connections(driver):
        connection = {}
        connection['name'] = el.find_element_by_css_selector(
            '.mn-connection-card__name').text
        #connection['connected_time'] = el.find_element_by_css_selector('time').text
        connection_link = el.find_element_by_css_selector(
            '.mn-connection-card__link').get_attribute('href')
        connection['Profile link'] = connection_link
        connection['id'] = re.search(
            r'/in/(.*?)/', connection_link).group(1)
        print('\t',connection['name'],' is collected')
        connections.append(connection)

    return connections

def scroll_to_bottom(total_connections,driver):
    num_visible_connections = 0
    consecutive_same_num = 1
    MAX_CONSECUTIVE = 20
    while num_visible_connections < total_connections and consecutive_same_num < MAX_CONSECUTIVE:
        prev_visible_connections = num_visible_connections
        num_visible_connections = len(visible_connections(driver))
        if (prev_visible_connections == num_visible_connections):
            consecutive_same_num += 1
        else:
            consecutive_same_num = 1
        driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(0.1)
        try:
            button_scroll = driver.find_element_by_css_selector(".scaffold-finite-scroll__load-button")
            button_scroll.click()
            time.sleep(2)
        except:
            pass

def visible_connections(driver):
    return driver.find_elements_by_css_selector('.mn-connection-card')

if __name__ == '__main__':

    print("\nOpening the browser...")
    try:
        # Initilaize selenium
        PATH = ChromeDriverManager(version='90.0.4430.24').install()
        service = Service(PATH)
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('-disable-gpu')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.24 Safari/537.36")

        #options.add_argument("--disable-popup-blocking")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        d = webdriver.DesiredCapabilities.CHROME
        d['loggingPrefs'] = {'performance': 'ALL'}
        #driver = Chrome(options=options,desired_capabilities=d)

        driver = Chrome(PATH,  options=options,desired_capabilities=d)
        wait = WebDriverWait(driver, 10)
        time.sleep(1)
    except:
        # Initilaize selenium
        PATH = ChromeDriverManager().install()
        service = Service(PATH)
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('-disable-gpu')
        driver = Chrome(PATH, options=options)
        wait = WebDriverWait(driver, 10)


    time.sleep(2)
    action = ActionChains(driver)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    print("Browser opened succefully")
    time.sleep(1)

    # Linkedin account info
    print("\n\t *** Linkedin account information : ***")
    
    email = 'touzani.zakari@gmail.com'
    password = 'TouzaniZa2113'
    #email = input("\n\t ---> Enter the email/user account : ")
    #password = input("\t ---> Enter the password : ")


    time.sleep(2)
    print("\nLogin to linkedIn ...")
    driver.get('https://www.linkedin.com/uas/login')
    driver.find_element(By.CSS_SELECTOR, '#username').send_keys(email)
    driver.find_element(By.CSS_SELECTOR, '#password').send_keys(password)
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '.from__button--floating').click()
    time.sleep(5)


    try :
        driver.find_element_by_id("input__email_verification_pin")

        print("\n\t *** Verification Alert *** \nthere is a verification security step due to IP changing ! \nYou will receive a pin code in your email adress now. ")
        pin_code = int(input("\n\t-->Enter the PIN code you received in your email ): "))
        time.sleep(60)

        pin_area = driver.find_element_by_id("input__email_verification_pin")
        pin_area.send_keys(pin_code)
        time.sleep(2)

        submit_pin_button = driver.find_element_by_id("email-pin-submit-button")
        submit_pin_button.click()
        time.sleep(6)

        print("\n Verfication step was succefully passed !")

        driver.get("https://www.linkedin.com/")
        time.sleep(3)
    except:
        pass

    print("\nLogin succefully !\n")


    connections_info = scrape_connections(driver,wait)
    print("\nConnections infos are collected succefully !")
    print(len(connections_info)," connections collected !")
  
    # convert data to an excel file
    connection_data = pd.DataFrame(connections_info)
    print(connection_data)
    #connection_data.to_excel("Connection_data.xlsx")
    connection_data.to_csv("Connection_data.txt",sep=' | ', index=False)
    #np.savetxt(r'data_v1.txt',connection_data.values, fmt='%d')
    driver.close()
    




