import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Carrega as variáveis de ambiente
load_dotenv()

# ENV variables
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

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
    driver.get('https://sistemabin.com.br/login')  # Abre a página de login
    # Aguarda o campo de email estar presente e preenche com o valor fornecido
    wait_for_element(driver, By.ID, 'email').send_keys(email)
    # Aguarda o campo de senha estar presente e preenche com o valor fornecido
    wait_for_element(driver, By.ID, 'password').send_keys(password)
    # Aguarda o botão de submit estar presente e clica nele
    wait_for_element(driver, By.XPATH, '//button[@type="submit"]').click()

# Função principal para executar o script
def main():
    # Solicita que o usuário insira o email e a senha
    #email = input("Please enter your email: ")
    #password = input("Please enter your password: ")
    # Inicia o Selenium e realiza o login
    driver = start_selenium_driver()
    login(driver, email, password)

if __name__ == "__main__":
    main()
