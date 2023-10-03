import json
import time
import os
import urllib.request
import ssl


from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


context = ssl._create_unverified_context()
geourl = "https://sistema.wvetro.com.br/wvetro/rest/API/DPListLicencasVencidas" 

response = urllib.request.urlopen(geourl, context=context)
content = response.read()
data = json.loads(content.decode("utf-8"))


if __name__ == '__main__':
    
    service = Service(executable_path=ChromeDriverManager().install())
    dir_path = os.getcwd()
    profile = os.path.join(dir_path, "profile", "wpp")
    options = webdriver.ChromeOptions()
 
    options.add_argument(r"user-data-dir={}".format(profile))
    

    driver = webdriver.Chrome(service=service, options=options) 
    driver.minimize_window()
    time.sleep(3)
    driver.get("https://web.whatsapp.com")
    
    while len(driver.find_elements(By.ID, 'side')) < 1:
        time.sleep(2)
    time.sleep(4)

for i in data:

    licencaId = i['LicencaId']
    licencaNome = i['LicencaNome']
    licencaR = i['LicencaRespFinanceiro']
    licencaTDV = i['LicencaTitulosDtVencimento']
    licencaTVlr = i['LicencaTitulosVlr']
    licencaWpp = i['LicencaWhatsApp']
    licencaTLB = i['LicencaTitulosLinkBoleto']
    licencaTQR = i['LicencaTitulosQRCodeURL']
    licencaTCC = i['LicencaTitulosCopiaCola']
    
    
    dtstring = (f'{licencaTDV}')
    dt = dtstring.replace('-', '/')
    dtformat = datetime.strptime(dt, "%Y/%m/%d")
    dtven = datetime.strftime(dtformat, "%d/%m/%Y")
    
    dtnow = datetime.now()
    dtdate = dtnow.date()
    dtstr = (f"{dtdate}")
    dthj = dtstr.replace('-', '/')
    dthjformat = datetime.strptime(dthj, "%Y/%m/%d")
    dthoje = datetime.strftime(dtdate, "%d/%m/%Y")
    
    
    
    
    if licencaWpp != "":
        if licencaTCC !="":
            
            mensagem = (f"*WVETRO INFORMA:*\n\nNão identificamos o pagamento referente ao boleto do sistema com vencimento em: {dtven}\n\nAtualizamos e estamos encaminhando com vencimento para hoje: {dthoje}. Lembrando que 15 dias após o vencimento do título, caso o sistema não identifique o pagamento do boleto, seu sistema será bloqueado até a regularização.\n\nQualquer dúvida, estamos sempre a disposição.\n\nSeguem abaixo duas formas para pagamento:\n\nLink do boleto pix: {licencaTLB}\n\nPix copia e cola:" )
            
            chave_pix = (f"{licencaTCC}")
            
        else:
            mensagem = (f"Informamos que não identificamos o pagamento referente ao boleto do sistema com vencimento em: {dtven}\n\nAtualizamos e estamos encaminhando com vencimento para hoje: {dthoje}. Lembrando que 15 dias após o vencimento do título, caso o sistema não identifique o pagamento do boleto, seu sistema será bloqueado atá a regularização.\n\nSegue o boleto para realizar o pagamento:{licencaTLB}\n\nQualquer duvida estamos sempre a disposição.\n\nAtt.WVETRO")
            
        text = urllib.parse.quote(f"{mensagem}")
        link = f"https://web.whatsapp.com/send?phone=+55{licencaWpp}&text={text}"
        driver.get(link)
        
        while len(driver.find_elements(By.ID, 'side')) < 1:
            time.sleep(2)
        time.sleep(4)

        if len(driver.find_elements(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]')) < 1:
            driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click()
        time.sleep(4)

    if licencaTCC !="":
        pix = urllib.parse.quote(f"{chave_pix}")
        linkpix = f"https://web.whatsapp.com/send?phone=+55{licencaWpp}&text={pix}"
        driver.get(linkpix)
        
        while len(driver.find_elements(By.ID, 'side')) < 1:
            time.sleep(2)
        time.sleep(4)

        if len(driver.find_elements(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]')) < 1:
            driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click()
        time.sleep(4)
 
