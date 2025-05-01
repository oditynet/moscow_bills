import subprocess
import re
import threading
import queue
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

def get_adb_devices():
    try:
        result = subprocess.run(
            ['adb', 'devices'],
            capture_output=True,
            text=True,
            timeout=5
        )
        lines = [line.strip() for line in result.stdout.split('\n')[1:] if line.strip()]
        for line in lines:
            if re.match(r'^\S+\tdevice$', line):
                return line.split('\t')[0]
        return None
    except Exception as e:
        print(f"ADB error: {str(e)}")
        return None

def get_sms():
    try:
        result = subprocess.run(
            ['adb', 'shell', 'content', 'query', '--uri', 'content://sms/inbox'],
            capture_output=True,
            text=True,
            timeout=3
        )
        messages = []
        for line in result.stdout.split('\n'):
            if 'body=' in line and 'date=' in line:
                date_match = re.search(r'date=(\d+)', line)
                body_match = re.search(r'body=(.+?), service_center', line)
                #print(body_match)
                if date_match and body_match:
                    timestamp = int(date_match.group(1)) // 1000
                    dt = datetime.fromtimestamp(timestamp)
                    body = body_match.group(1).strip()
                    messages.append((dt, body))
        return messages
    except Exception as e:
        print(f"SMS error: {str(e)}")
        return []

def is_recent(msg_time):
    return (datetime.now() - msg_time) < timedelta(minutes=1)

def loopsms(output_queue, check_interval=10):
    while True:
        try:
            device = get_adb_devices()
            if device:
                #print(f"Устройство подключено: {device}")
                messages = get_sms()
                if messages:
                    latest_time, latest_body = messages[0]
                    if is_recent(latest_time):
                        print(f"Новое сообщение: {latest_body}")
                        output_queue.put(latest_body[-6:])
                        break
                        #return  latest_body[:5]
                #    else:
                #        print("Новых сообщений нет")
                else:
                    print("Сообщения не найдены")
            else:
                print("Устройство не обнаружено")
            
            time.sleep(check_interval)
            
        except KeyboardInterrupt:
            print("\nМониторинг остановлен")
            break
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            time.sleep(check_interval)

if __name__ == "__main__":



    #Мосводоканал
    log="+79771234567"
    passwd="pass"
    water="0.1"
    options = Options()
    options.set_preference("dom.webdriver.enabled", False)  # Скрываем автоматизацию  
    options.set_preference("useAutomationExtension", False)
    
    gecko_path="/home/odity/Downloads/geckodriver-v0.36.0-linux64/geckodriver"
    service = Service(executable_path=gecko_path,options=options)
    driver = webdriver.Firefox(service=service)
    driver.get(f"https://onewind.mosvodokanal.ru/#loginview")
    
    
    add = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "button-1016-btnInnerEl"))
    )
    
    #add = driver.find_element(By.ID, ".button-1016-btnInnerEl") #login
    add.click()
    time.sleep(1)
    
    #add = driver.find_element(By.CSS_SELECTOR, "input#login") #login
    
    add = driver.find_element(By.CSS_SELECTOR, "input[data-ref='inputEl'][name='login']") #login
    add.clear()
    add = add.send_keys(log)
    
    time.sleep(1)
    add = driver.find_element(By.CSS_SELECTOR, "input[data-ref='inputEl'][name='pass']") #passwd
    add.clear()
    add = add.send_keys(passwd)
    
    button = WebDriverWait(driver, 3).until( EC.element_to_be_clickable((   By.XPATH, 
            "//span[contains(@class, 'x-btn-inner-login-button-large') "
            "and contains(text(), 'ВОЙТИ В ЛИЧНЫЙ КАБИНЕТ')]" )) )
    
    # Кликнуть через JavaScript для обхода возможных перекрытий
    driver.execute_script("arguments[0].click();", button)  #button press
    
    time.sleep(3)
    button = WebDriverWait(driver, 2).until(
    EC.element_to_be_clickable((
        By.XPATH, 
        "//span[contains(@class, 'x-tab-inner') and text()='Передача показаний']"
    )))
    button.click()
    time.sleep(1) #кликается а дальше надо проверять
    
    
    element = WebDriverWait(driver, 2).until(
        lambda d: d.find_element(By.CSS_SELECTOR, "input[data-ref='inputEl']")
    )
    
    driver.execute_script("arguments[0].removeAttribute('readonly')", element)
    
    # Вводим значение
    element.clear()
    #element.send_keys("0")    #1
    
    input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR, 
            "div[data-ref='inputWrap'] > input[data-ref='inputEl']"
        ))
    )

    # Снять атрибут readonly (если требуется ввод)
    driver.execute_script("arguments[0].removeAttribute('readonly')", input_field)
    
    # Ввод значения
    input_field.clear() #2
    
    
    driver.close();




    # Мосэнергосбыт
    log="+79771234567"
    passwd="pass"
    water="0.1"
    options = Options()
    options.set_preference("dom.webdriver.enabled", False)  # Скрываем автоматизацию  
    options.set_preference("useAutomationExtension", False)
    
    gecko_path="/home/odity/Downloads/geckodriver-v0.36.0-linux64/geckodriver"
    service = Service(executable_path=gecko_path,options=options)
    driver = webdriver.Firefox(service=service)
    driver.get(f"https://my.mosenergosbyt.ru/auth")
    
    
    add = driver.find_element(By.CSS_SELECTOR, "input[testid='-login']") #login
    add.clear()
    add = add.send_keys(log)
    
    time.sleep(1)
    add = driver.find_element(By.CSS_SELECTOR, "input[testid='-password']") #passwd
    add.clear()
    add = add.send_keys(passwd)
    add = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][testid='loginButtonLogin']").click() #button 
    time.sleep(1)
    #авторизовались. дальше ждать 15 числа
    time.sleep(1200)
    
    driver.close();
    
    
    
    
    
    
    #МОС.РУ горячая вода
    
    
    log="+79771234567"
    passwd="pass"
    water="0.1"
    options = Options()
    options.set_preference("dom.webdriver.enabled", False)  # Скрываем автоматизацию  
    options.set_preference("useAutomationExtension", False)
    
    gecko_path="/home/odity/Downloads/geckodriver-v0.36.0-linux64/geckodriver"
    service = Service(executable_path=gecko_path,options=options)
    driver = webdriver.Firefox(service=service)
    driver.get(f"https://www.mos.ru/services/pokazaniya-vodi-i-tepla/")
    
    add = driver.find_element(By.CSS_SELECTOR, '.Button-children').click()
    #pyautogui.press('enter')      # Enter 
    time.sleep(1)
    add = driver.find_element(By.CSS_SELECTOR, "input#login") #login
    add = add.send_keys(log)
    
    time.sleep(1)
    add = driver.find_element(By.CSS_SELECTOR, "input#password") #passwd
    add = add.send_keys(passwd)

    time.sleep(1)
    add = driver.find_element(By.CSS_SELECTOR, 'button.form-login__button.button-base.button-accent').click() #MOS auth + 
    time.sleep(1)
    add = driver.find_element(By.CSS_SELECTOR, 'input.css-1jjcjge-Radiobutton[name="payerCode"]')
    driver.execute_script("arguments[0].click();", add)
    time.sleep(1)
    add = driver.find_element(By.CSS_SELECTOR, 'button.css-6xxhy1-Button-Text-Box').click() #next button
    time.sleep(1)
    add = driver.find_element(By.CSS_SELECTOR, "input[class='css-1452zdy-Field-Box-Text']")
    add.clear()
    add.send_keys(water)
    time.sleep(1)

    add = driver.find_element(By.CSS_SELECTOR, 'button.css-6xxhy1-Button-Text-Box').click() #next button
    time.sleep(1)
    driver.close();
    #PROFIT
    

    
    time.sleep(1200)

    # МОЭК
    chet="8001000177" #номер лицевого счета
    kv="11" #квартира
    #driver = webdriver.Firefox()
    options = Options()
    options.set_preference("dom.webdriver.enabled", False)  # Скрываем автоматизацию  
    options.set_preference("useAutomationExtension", False)
    
    gecko_path="/home/odity/Downloads/geckodriver-v0.36.0-linux64/geckodriver"
    service = Service(executable_path=gecko_path,options=options)
    driver = webdriver.Firefox(service=service)
    driver.get(f"https://online.moek.ru/person/peredacha-pokazaniya.html")
    #wait = WebDriverWait(driver, 15)

    #add = driver.find_element( By.ID, "bill")
    
    iframe = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "iframe")))
    driver.switch_to.frame(iframe)

    add = driver.find_element(By.CSS_SELECTOR, "input[class='form__input-number'][name='bill']")
    add = add.send_keys(chet)
    time.sleep(1)
    #pyautogui.press('enter')      # Enter+
    
    add = driver.find_element(By.CSS_SELECTOR, 'input.form__input-number[name="room"]')
    add = add.send_keys(kv)
    pyautogui.press('enter')      # Enter+
    time.sleep(1)
    
    #add = driver.find_element(By.ID, 'button button__pos_next button__col_blue').click()
    #pyautogui.press('enter')      # Enter+
    #time.sleep(1)
    
    
    #iframe = WebDriverWait(driver, 20).until(
    #EC.presence_of_element_located((By.CSS_SELECTOR, "iframe")))
    #driver.switch_to.frame(iframe)
    
    checkbox = driver.find_element(By.CSS_SELECTOR, "input[class='form__input-checkbox']").click() #галка
    #pyautogui.press('enter')      # Enter
    time.sleep(1)
    
    add = driver.find_element(By.CSS_SELECTOR, 'button.button.button__pos_next.button__col_blue').click()
    #pyautogui.press('enter')      # Enter 
    time.sleep(1)
    
    v1="0.316" #показания 1
    v2="0.0018"#показания 2
    
    add = driver.find_element(By.CSS_SELECTOR, 'input.form__input-number[name="currentValue0"]')
    #add = driver.find_element(By.ID, 'form__input-number')
    add = add.send_keys(v1)
    time.sleep(1)
    #pyautogui.press('enter')      # Enter

    add = driver.find_element(By.CSS_SELECTOR, 'input.form__input-number[name="currentValue1"]')
    #add = driver.find_element(By.ID, 'form__input-number')
    add = add.send_keys(v2)
    time.sleep(1)
    #pyautogui.press('enter')      # Enter

    #add = driver.find_element(By.ID, 'button button__pos_next button__col_blue').click() #отправить
    add = driver.find_element(By.CSS_SELECTOR, 'button.button.button__pos_next.button__col_blue').click()
    pyautogui.press('enter')      # Enter
    time.sleep(1)
    driver.close();
    
    #time.sleep(1200)


    #sms_read_code
    message_queue = queue.Queue()
    monitor_thread = threading.Thread(
        target=loopsms,
        args=(message_queue,10),
        daemon=True
    )
    monitor_thread.start()
    print(message_queue.get())
