import os
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Carrega as variáveis de ambiente
load_dotenv()

# Variáveis ENV
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
smg13path = os.getenv('SMG13PATH')

# Variáveis globais
smgoi13 = None

# Lê a planilha smgoi13 e cria um dataframe 
def read_smgoi13(path):
    global smgoi13
    if smgoi13 == None:
        smgoi13 = pd.read_excel(path)
        # Formata a coluna de códigos para o formato (5 digitos)
        smgoi13['Código'] = smgoi13['Código'].str.split('-').str.get(0)

# Função para iniciar o driver do Selenium com as opções configuradas
def start_selenium_driver():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")  
    chrome_options.add_argument("--start-maximized")
    service = Service('C:\\Program Files\\Google\\chromedriver-win64\\chromedriver.exe')  
    return webdriver.Chrome(service=service, options=chrome_options)

# Função para esperar que um elemento esteja disponível no DOM
def wait_for_element(driver, by, element):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((by, element))
    )

# Função para realizar o login
def login(driver, email, password):
    driver.get('https://sistemabin.com.br/login')
    wait_for_element(driver, By.ID, 'email').send_keys(email)
    wait_for_element(driver, By.ID, 'password').send_keys(password)
    wait_for_element(driver, By.XPATH, '//button[@type="submit"]').click()

# Função para baixar as imagens do site
def download_image(driver, product_code):
    driver.get(f"https://sistemabin.com.br/produtos?q={product_code}&qs=")
    wait_for_element(driver, By.XPATH, f"//a[contains(@href, '{product_code}')]").click()
    wait_for_element(driver, By.XPATH, '//div[@class="col-12 col-md-6"]').find_elements(By.XPATH, './/button')[0].click()
    # Espera o modal ficar visível
    WebDriverWait(driver, 10).until (
        EC.visibility_of_element_located((By.ID, "modal-download-image"))
    ).find_element(By.TAG_NAME, 'a').click()
    time.sleep(5)
         

def main():
    read_smgoi13(smg13path)
    driver = start_selenium_driver()
    login(driver, email, password)
    download_image(driver, smgoi13['Código'][0])
    

if __name__ == "__main__":
    main()
