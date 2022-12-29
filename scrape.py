import os
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from readPDF import get_text_from_any_pdf
# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# driver = webdriver.Chrome(executable_path=os.environ.get(
#     "CHROMEDRIVER_PATH"), options=chrome_options)

options = Options()
options.headless = False
driver = webdriver.Chrome(
    ChromeDriverManager().install(), options=options)
notificationDat = "NA"
address = "NA"
Status = "NA"
currencies = []
removelist = []
thisval = ""


def main(num):
    irnis = num
    data = {
        'IRN': irnis,
        'Name & Address': '',
        'Notification Date': '',
        'Status': '',
        'Link': ''
    }
    address = ''
    notificationDate = ''
    href = ''

    try:
        driver.get("https://www3.wipo.int/madrid/monitor/en/")
        driver.find_element_by_id("AUTO_input").send_keys(irnis)
        driver.find_element_by_id(
            "AUTO_input").send_keys(Keys.ENTER)
        time.sleep(2)
    except:
        print("    Page loading Error....")
        print(".......Close and Run Again..........")
    try:
        driver.find_element_by_id("gridForsearch_pane").click()
        time.sleep(2)
        page_src = driver.page_source
        soup = BeautifulSoup(page_src, "html.parser")
        time.sleep(2)
        containers = soup.findAll('div', {"class": "p"})

        for item in containers:
            # print(item)
            try:
                name = item.find('div', {"class": "inidText"})
                # print(name.text)
                textis = item.find('div', {"class": "text"})
                if (name.text == "Name and address of the representative"):
                    address = (textis.text)
                    address = address.strip()
            except Exception as e:
                pass

        indian = soup.find_all("div", {"class": "text"})
        datecheck = 0
        for p in indian:
            if ('<span title="India">IN</span>' in str(p)):
                divTag = p.find_all("a", {"class": "pdfDocLink"})
                for div in divTag:
                    href = div['href']
                    link = (div['href'])
                datecheck = 1
            if (datecheck == 1):
                if (len(p.text) == 10):
                    if ("." in p.text):
                        notificationDate = p.text
                        datecheck = 0
        # address = address.encode('ascii', 'ignore').decode('ascii')
        # notificationDate = notificationDate.encode(
        #     'ascii', 'ignore').decode('ascii')
        # response = requests.get(link)
        # soup = BeautifulSoup(response.text, 'html.parser')
        # pdf = open("temp.pdf", 'wb')
        # pdf_path = (os.getcwd() + "/" + "temp.pdf")
        # pdf.write(response.content)
        # pdf.close()

        # thispdf = get_text_from_any_pdf(pdf_path)
        # thispdf = ''
        # word = "The Grounds are mentioned as per the Notice(es) of Opposition attached herewith"
        # second_word = "of filling TM-M"
        # second_word2 = "of filing TM-M"
        # # print(findings)
        # if thispdf.find(word) != -1:
        #     Status = "Opposition"
        # elif thispdf.find(second_word) != -1:
        #     Status = "Opposition"
        # elif thispdf.find(second_word2) != -1:
        #     Status = "Opposition"
        # else:
        #     Status = "Refusal"

        data['Name & Address'] = address
        data['Notification Date'] = notificationDate
        data['Status'] = ""
        data['Link'] = href
        # print(data)

        # {'IRN': irnis, 'Name & Address': address, 'Notification Date': notificationDate, 'Status': Status, 'Link': link})
        #print("!...Extraction Process completed...!")
        #print("!...Extraction Process completed...!")

    except Exception as e:
        print(e)
        for c in removelist:
            currencies.remove(c)
        print("    Page did not load properly     ")
        print(".......Close and Run Again..........")
    return data


if __name__ == '__main__':
    print(main(1616369))
