from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# import time
import requests
from bs4 import BeautifulSoup

# options
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument('--headless') # don't open browser

driver = webdriver.Chrome(options=options)


class scrap:

    def froxy_price(self):
        try:
            driver.get('https://froxy.com/en/prices')
            fast = driver.find_element(By.XPATH,'//*[@id="__layout"]/main/section/div/section[1]/div/div[1]/div[2]/div/div[1]/div/div/div[2]/span[1]').text.strip('$')

            driver.find_element(By.XPATH,'//*[@id="__layout"]/main/section/div/section[1]/div/ul/li[2]/button').click()
            residential = driver.find_element(By.XPATH,'//*[@id="__layout"]/main/section/div/section[1]/div/div[1]/div[2]/div/div[1]/div/div/div[2]/span[1]').text.strip('$')
            
            driver.find_element(By.XPATH,'//*[@id="__layout"]/main/section/div/section[1]/div/ul/li[3]/button').click()
            mobile = driver.find_elements(By.XPATH,'//*[@id="__layout"]/main/section/div/section[1]/div/div[1]/div[2]/div/div[1]/div/div/div[2]/span[1]')[0].text.strip('$')
                                                    
            return {'Fast': fast, 'Residential': residential, 'Mobile': mobile}

        except Exception as ex:
            print(ex)

        finally:
            driver.close()
            driver.quit()


    def proxy6_price(self):
        try:
            driver.get('https://proxy6.net/en/order')
            driver.find_element(By.XPATH,'//*[@id="form-order6"]/table/tbody/tr[6]/td[2]/div/select/option[4]').click() #period 1 month

            ipv6 = driver.find_element(By.XPATH,'//*[@id="form-order6"]/table/tbody/tr[8]/td[2]/b').text

            ipv4 = driver.find_element(By.XPATH,'//*[@id="form-order4"]/table/tbody/tr[8]/td[2]/b').text

            ipv4_shared = driver.find_element(By.XPATH,'//*[@id="form-order3"]/table/tbody/tr[8]/td[2]/b').text

            return {'Ipv6': ipv6, 'Ipv4': ipv4, 'Ipv4 shared': ipv4_shared}

        except Exception as ex:
            print(ex)

        finally:
            driver.close()
            driver.quit()


    def exchanger(self,curr):
        curr_dict = {
            'rub': [soup.find('input',{'class':"lWzCpb a61j6"})['value'], 'https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%B0%D1%80+%D1%80%D1%83%D0%B1%D0%BB%D1%8C&sxsrf=ALiCzsYWyLb3-ZkZedQ7-gplh17ZI53lIQ%3A1670941188340&ei=BIqYY7OlFMP2qwG0k6bIDQ&oq=%D0%B4%D0%BE%D0%BB%D0%B0%D1%80+&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAxgAMg8IABCxAxCDARBDEEYQggIyCggAELEDEIMBEEMyCAgAEIAEELEDMgQIABBDMggIABCABBCxAzIECAAQQzILCAAQgAQQsQMQyQMyBwgAELEDEEMyCAgAELEDEIMBMggIABCABBCxAzoKCAAQRxDWBBCwAzoHCAAQsAMQQzoRCC4QgAQQsQMQgwEQxwEQ0QM6CwgAEIAEELEDEIMBSgQIQRgASgQIRhgAUNINWLkkYJI7aAFwAXgAgAFciAHcA5IBATaYAQCgAQHIAQrAAQE&sclient=gws-wiz-serp']
        }

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

        full_page = requests.get(curr_dict[curr][1], headers=headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        answer = curr_dict[curr][0]

        return answer


    def answer_price(self,markets):
        price_dict = dict()

        for name in markets:
            if name == 'froxy':
                price_dict['froxy'] = self.froxy_price()
            elif name == 'proxy6':
                price_dict['proxy6'] = self.proxy6_price()

        return price_dict