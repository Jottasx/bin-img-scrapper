import os
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Carrega as variáveis de ambiente
load_dotenv()

# Variáveis ENV
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
smg13path = os.getenv('SMG13PATH')

# Variáveis globais
image_folder_path = "D:\\ATACAS\\"
smgoi13 = None
downloaded_images = []

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
    chrome_options.add_argument("--headless=new")
    chrome_prefs = {
        "download.default_directory": "D:\\ATACAS\\",  
        "download.prompt_for_download": False,       
        "safebrowsing.enabled": True,
        "safebrowsing.disable_download_protection": True                 
    }
    chrome_options.add_experimental_option("prefs", chrome_prefs)
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

# Função para atualizar as imagens que já foram baixadas na pasta
def update_downloaded_images():
    for image in get_folder_images():
        image_code = image.split(" ")[-1][:-4]
        downloaded_images.append(image_code)
        print(f"A imagem do produto {image_code} já existe na pasta")

def get_folder_images():
    return os.listdir(image_folder_path)

def get_image_name_by(product_code):
    for image_file in get_folder_images():
        if image_file.split(" ")[-1][:-4] == str(product_code):
            return image_file

def get_product_code_by(image_name):
    return image_name.split(" ")[-1][:-4]

# Função para baixar as imagens do site
def download_image(driver, product_code):
    try:
        driver.get(f"https://sistemabin.com.br/produtos?q={product_code}&qs=")
        wait_for_element(driver, By.XPATH, f"//a[contains(@href, '{product_code}')]").click()
        wait_for_element(driver, By.XPATH, '//div[@class="col-12 col-md-6"]').find_elements(By.XPATH, './/button')[0].click()
        # Espera o modal ficar visível
        WebDriverWait(driver, 15).until (
            EC.visibility_of_element_located((By.ID, "modal-download-image"))
        ).find_element(By.TAG_NAME, 'a').click()
        print(f"[OK] A imagem do produto {product_code} foi baixada com sucesso")
    except TimeoutException:
        print(f"[x] Erro ao baixar imagem do produto {product_code} pulando para a próxima imagem")

def rename_image_file(product_code):
    os.rename(f"{image_folder_path}{get_image_name_by(product_code)}", f"{image_folder_path}{product_code}.jpg")

        
def main():
    read_smgoi13(smg13path)
    update_downloaded_images()
    driver = start_selenium_driver()
    login(driver, email, password)

    filtered_codes = smgoi13[~smgoi13['Código'].isin(downloaded_images)]
    for product_code in filtered_codes['Código']:
        download_image(driver, product_code)

    # for image_file in get_folder_images():
    #     rename_image_file(get_product_code_by(image_file))
        

if __name__ == "__main__":
    main()
