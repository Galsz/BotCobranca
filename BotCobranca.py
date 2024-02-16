# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------------------
# Created By   : Geovane A L Silva
# Created Date : 2023/09/03
# version = '1.6'  
# Last change date : 2024/02/16
# --------------------------------------------------------------------------------------------------------

import json
import time
import os
import urllib.request
import ssl


from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import UnexpectedAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


#fetches license data through an API
def get_data_license():

    context = ssl._create_unverified_context()
    geourl = os.environ.get('API_URL')

    response = urllib.request.urlopen(geourl, context=context)
    content = response.read()
    return json.loads(content.decode("utf-8"))


#initialize drivers and configure services
def initialize_driver():
    
    service = Service(executable_path=ChromeDriverManager().install())
    dir_path = os.getcwd()
    profile = os.path.join(dir_path, "profile", "wpp")
    options = webdriver.ChromeOptions()

    options.add_argument(r"user-data-dir={}".format(profile))
   
    driver = webdriver.Chrome(service=service, options=options) 
    driver.minimize_window()
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(30)

    return driver


#send text messages to license number
def send_message(driver, number, message):
    text = urllib.parse.quote(f"{message}")
    link = f"https://web.whatsapp.com/send?phone=+55{number}&text={text}"
    driver.get(link)

    while len(driver.find_elements(By.ID, 'side')) < 1:
        time.sleep(2)
    time.sleep(4)

    if len(driver.find_elements(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]')) < 1:
        driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click()
    time.sleep(4)


def main():
    
    try:
        
        driver = initialize_driver()
        data = get_data_license()

        for i in data:

            #********uncomment for use*********
            # licenseId = i['LicencaId']
            # licenseName = i['LicencaNome']
            # licenseR = i['LicencaRespFinanceiro']
            # licenseTQR = i['LicencaTitulosQRCodeURL']
            # licenseTVlr = i['LicencaTitulosVlr']
             
            licenseWpp = i['LicencaWhatsApp']
            licenseTLB = i['LicencaTitulosLinkBoleto']
            licenseTCC = i['LicencaTitulosCopiaCola']
            licenseTDV = i['LicencaTitulosDtVencimento']
            
            dtformat = datetime.strptime(licenseTDV, '%Y-%m-%d')
            dtven = dtformat.strftime("%d/%m/%Y")
        
            today = datetime.now().strftime("%d/%m/%Y")
            
            if licenseWpp != "":

                base_message = (
                        f"*WVETRO INFORMA:*\n\nNão identificamos o pagamento referente ao boleto do sistema "
                        f"com vencimento em: {dtven}\n\nAtualizamos e estamos encaminhando com vencimento "
                        f"para hoje: {today}. Lembrando que 15 dias após o vencimento do título, caso o "
                        f"sistema não identifique o pagamento do boleto, seu sistema será bloqueado até a regularização."
                        f"\n\nQualquer dúvida, estamos sempre à disposição."
                    )
                
                messages = []

                if licenseTCC !="":
                    
                    message = (f"{base_message}\n\nSeguem abaixo duas formas para pagamento:\n\nLink do boleto pix: {licenseTLB}\n\nPix copia e cola:" )
                    pix_key = (f"{licenseTCC}")
                    messages.extend([message, pix_key])
                else:
                    message = (f"{base_message}\n\nSegue o boleto para realizar o pagamento:{licenseTLB}\n\nQualquer duvida estamos sempre a disposição.\n\nAtt.WVETRO")
                    messages.append(message)

                for msg in messages:

                    send_message(driver=driver, number=licenseWpp,message=msg)
                

        print("************* Cobranças realizadas com sucesso ! *****************")
        time.sleep(5)

    except UnexpectedAlertPresentException as e:
        alert = driver.switch_to.alert
        alert.dismiss()
        print(f"Exception UnexpectedAlertPresentException: {e}")
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        if driver:
            driver.quit()
        time.sleep(4)

if __name__ == '__main__':
    main()

