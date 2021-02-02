import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, JavascriptException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import jsonlines


class Scraping:
    
    def __init__(self):
        option = Options()
        option.headless = False

    def getDriver(self):
        return webdriver.Chrome(ChromeDriverManager().install())

    @staticmethod
    def main(uf, self):
        if(uf == ''):
            driver = self.getDriver()
            driver.get(
                'http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm')
            select = driver.find_element_by_xpath(
                '//*[@id="Geral"]/div/div/span[2]/label/select')
            options = select.find_elements_by_tag_name("option")

            total = 0

            for x in options:
                total += 1

            for x in range(total):
                if(x == 0):
                    indice = x + 2
                else:
                    indice = x + 1

                uf = driver.find_element_by_xpath(
                    '//*[@id="Geral"]/div/div/span[2]/label/select/option[{0}]'.format(indice))

                ufName = uf.get_attribute('value')

                uf.click()

                button = driver.find_element_by_xpath(
                    '//*[@id="Geral"]/div/div/div[4]/input')
                button.click()

                time.sleep(2)

                table = driver.find_element_by_xpath(
                    '/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table[2]').get_attribute('outerHTML')

                next = True

                soup = BeautifulSoup(table, 'html.parser')
                beautifulTable = soup.find(name='table')
                df = pd.read_html(str(beautifulTable))[0]

                while next:
                    try:
                        driver.execute_script(
                            "document.Proxima.submit('Proxima')")

                        time.sleep(2)

                        nextTable = driver.find_element_by_xpath(
                            '/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table').get_attribute('outerHTML')

                        soup = BeautifulSoup(nextTable, 'html.parser')
                        beautifulTable = soup.find(name='table')
                        dfNext = pd.read_html(str(beautifulTable))[0]
                        df = df.append(dfNext)

                    except JavascriptException as x:
                        next = False
                        pass

                df.insert(0, 'Id', range(len(df)))

                tableDict = {}
                tableDict = df.to_dict('records')

                with jsonlines.open('{0}.jsonl'.format(ufName), 'w') as writer:
                    writer.write_all(tableDict)

                back = driver.find_element_by_xpath(
                    '/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div[3]/a')
                back.click()

                time.sleep(2)
        else:
            driver = self.getDriver()
            driver.get(
                'http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm')

            select = driver.find_element_by_xpath(
                '//*[@id="Geral"]/div/div/span[2]/label/select')

            selected = select.find_element_by_xpath(
                "//option[@value='{0}']".format(uf))

            selected.click()

            button = driver.find_element_by_xpath(
                '//*[@id="Geral"]/div/div/div[4]/input')
            button.click()

            time.sleep(2)

            table = driver.find_element_by_xpath(
                '/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table[2]').get_attribute('outerHTML')

            next = True

            soup = BeautifulSoup(table, 'html.parser')
            beautifulTable = soup.find(name='table')
            df = pd.read_html(str(beautifulTable))[0]

            while next:
                try:
                    driver.execute_script(
                        "document.Proxima.submit('Proxima')")

                    time.sleep(2)

                    nextTable = driver.find_element_by_xpath(
                        '/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table').get_attribute('outerHTML')

                    soup = BeautifulSoup(nextTable, 'html.parser')
                    beautifulTable = soup.find(name='table')
                    dfNext = pd.read_html(str(beautifulTable))[0]
                    df = df.append(dfNext)

                except JavascriptException as x:
                    next = False
                    pass

            df.insert(0, 'Id', range(len(df)))

            tableDict = {}
            tableDict = df.to_dict('records')

            with jsonlines.open('{0}.jsonl'.format(uf), 'w') as writer:
                writer.write_all(tableDict)