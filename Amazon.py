from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from lxml.html import parse
from io import StringIO 
import pyperclip, time, json, traceback, requests

class Amazon:
    def __init__(self, path, window_size="1920x1080", headless_mode ="headless"):     #chromedriver의 기본 옵션 적용 
        options = webdriver.ChromeOptions()
        options.add_argument(headless_mode)
        options.add_argument(window_size)
        options.add_argument("disable-gpu")
        # options.add_argument("no-sandbox")
        # options.add_argument("disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        self.driver = webdriver.Chrome(path, chrome_options=options)
    
    def url_page(self, url):    #사용자가 입력한 제품 URL 
        try:                    #사용자가 선택한 제품옵션을 처리하는 함수 
            self.driver.get(url)
            myElem = WebDriverWait(self.driver, 8).until(EC.presence_of_element_located((By.TAG_NAME, 'div')))#8초 동안 url load 기다림
            print ("Page is ready!")
            right_product = self.driver.find_element_by_xpath("//*[@id='twisterContainer']")    #제품 옵션 틀 Element
            right_product2 = self.driver.find_element_by_xpath("//*[@id='twisterContainer']").find_element_by_tag_name("form").find_elements_by_xpath("div")
            #div 개수를 통해서 options이  몇개인지 확인하기 위한 product2

            count = 0   #똑같은 tag 와 classname의 구별을 위해 사용
            for k in right_product2:    #사용자가 선택할 옵션의 right_product2 list형태의 변수
                if k.get_attribute('class') == "a-section a-spacing-base variation-dropdown":   #콤보box형태의 ElementClass일경우 처리
                    right_title = right_product.find_element_by_xpath("//span[@class='a-button a-button-dropdown aui-variation  a-fastclick-disable']")
                    right_title.click()
                    right_elementList = self.driver.find_element_by_xpath("//div[@data-action='a-popover-a11y']").find_elements_by_tag_name("li")
                    right_list = []
                    for x in right_elementList:
                        right_list.append(x.text)
                    if right_list[0] == "Select":   #Select가 옵션에 있을경우 제거한후 처리
                        right_list.pop(0)
                        right_elementList.pop(0)
                        print(right_list)       #옵션 list를 보여주기 윈한 print 추후 바꿀예정
                        value = input("번호를 입력하세요 1 ~ "+str(len(right_list))+" : ")
                        right_elementList[int(value)-1].click()
                    else:
                        print(right_list)
                        value = input("번호를 입력하세요 1 ~ "+str(len(right_list))+" : ")
                        right_elementList[int(value)].click()
                else:
                    right_elementList = k.find_elements_by_xpath("//ul[@role='radiogroup']")
                    right_list = []
                    try:        #해당 Element가 img tag 일경우
                        test_element = right_elementList[count].find_element_by_tag_name("img")
                    except:
                        right_test = right_elementList[count].find_elements_by_tag_name("li")
                        count += 1
                        for x in right_test:
                            right_list.append(x.text)

                        print(right_list)
                        value = input("번호를 입력하세요 1 ~ "+str(len(right_test))+" : ")
                        right_test[int(value)-1].click()
                    else:       #제품의 길이만큼의 번호를 클릭할수 있게 처리
                        right_test = right_elementList[count].find_elements_by_tag_name("li")
                        value = input("번호를 입력하세요 1 ~ "+str(len(right_test))+" : ")
                        right_test[int(value)-1].click()
            time.sleep(3)
            no_ment = self.driver.find_element_by_xpath("//*[@id='delivery-message']").text.split(".")[0]   #한국으로 배송이되지 않을 경우 예외처리를 위한 ment
            if no_ment in "This item does not ship to Korea; Republic of (South Korea)":
                print("이제품은 한국으로 배송이 되지 않습니다.")
                self.driver.close() #종료
                return
            
            # amount = right_product.find_element_by_xpath("//*[@id='quantity']") #수량 클릭 
            # ActionChains(self.driver).click(amount).perform()

            #해당부분이 클릭시 Element가 다르게? 나옵니다. 질문에 적어놨습니다. 
            ######################################################################
            # amount_wait = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, "//div[@data-action='a-popover-a11y']")))
            # test1 = amount_wait.find_elements_by_tag_name("li")
            # amount_list = self.driver.find_element_by_xpath("//div[@data-action='a-popover-a11y']").find_elements_by_tag_name("li") #수량 가능 갯수
            # +str(len(amount_list))+
            amount_count = input("수량을 입력하세요 1 ~ 6 : ")    #사용자 수량 입력
            self.driver.execute_script("quantity.value = %d;" % (int(amount_count)))
            #test1[int(amount_count)-1].click() #수량 클릭
            ######################################################################
            buy_button = right_product.find_element_by_xpath("//*[@id='submit.buy-now']/span")  #구매 버튼
            buy_button.click()
            #전부 return 값 로그인 성공여부, 결제성공여부, 제품배송번호
        except:
            traceback.print_exc()

    def login(self):    #로그인 함수
        self.driver.find_element_by_xpath("//div[@class='a-section a-spacing-base']").find_element_by_xpath("//form[@class='auth-validate-form auth-real-time-validation a-spacing-none fwcim-form']").find_element_by_xpath("//div[@class='a-box-inner a-padding-extra-large']")

        input_id = self.driver.find_element_by_xpath("//input[@type='email']")  #id_Element
        input_id.send_keys("gill1994@naver.com")
        next_button = self.driver.find_element_by_xpath("//input[@class='a-button-input']")
        next_button.click()
        
        input_pw = self.driver.find_element_by_xpath("//*[@id='ap_password']")  #Pw_Element
        input_pw.send_keys("as14736945025")
        next_button2 = self.driver.find_element_by_xpath("//*[@id='signInSubmit']")
        next_button2.click()
    
    def payment(self): #결제방식선택 함수 
        # ttt = self.driver.find_elements_by_xpath("//input[@class='enterAddressFormField validateInputCharactersOnBlur']")
        
        information_next = self.driver.find_element_by_xpath("//form[@class='a-nostyle']").find_element_by_xpath("//div[@id='address-book-entry-0']").find_elements_by_tag_name("a")
        information_next[0].click()
        krw = self.driver.find_element_by_xpath("//input[@value='KRW']").click()
        # last_button = self.driver.find_element_by_xpath("//input[@aria-labelledby='pp-RH-59-announce']").click()


if __name__ == "__main__":
    test_case = Amazon("C:\\Users\\sin\\Desktop\\chrome\\chromedriver_win32\\chromedriver.exe")
    # test_case.url_page("https://www.amazon.com/VATI-Compatible-Silicone-Replacement-iWatch/dp/B07P3V71MR/ref=gbps_img_m-9_f108_f0a02e9b?smid=A1LP7IJ3L9195V&pf_rd_p=5f0e22ee-4642-4df0-8c17-21aae098f108&pf_rd_s=merchandised-search-9&pf_rd_t=101&pf_rd_i=15529609011&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=W8MSSRKAXGCA05QQG2Z7")
    # test_case.url_page("https://www.amazon.com/Amazon-Essentials-Standard-Regular-Fit-Short-Sleeve/dp/B07J6HXCFS/ref=sr_1_1_sspa?keywords=shirt&qid=1569942273&s=gateway&sr=8-1-spons&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzOTE0SjNLQ0NNWDFJJmVuY3J5cHRlZElkPUEwMTE2NjgxMjdRSkFVNVRONjJTRSZlbmNyeXB0ZWRBZElkPUEwMDg1Njg5NFVHTkg3S1FOMFpFJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ&th=1&psc=1")
    test_case.url_page("https://www.amazon.com/QuickBooks-Desktop-Pro-2019-Disc/dp/B07FYMWZ76/ref=lp_16225008011_1_3?s=software-intl-ship&ie=UTF8&qid=1570520843&sr=1-3")
    # test_case.url_page("https://www.amazon.com/Motor-Trend-MT-923-BK-FlexTough-Contour/dp/B01A5TLGJ4/ref=sr_1_1?keywords=Accessories&qid=1570543724&sr=8-1")
    # test_case.login()
    # test_case.payment()

#Page Wait 방법 2가지
#Implicitly wait
#: 지정해둔 HTML(Element)가 나타날떄 까지 기다려주는 코드. (Implicitly wait(3) 을 하게 된다면 3초를 기다린다.)
#Explicitly wait
#: 기본적으로 Implicitly wait의 값은 0초입니다. 즉, 요소를 찾는 코드를 실행시킨 때 요소가 없다면 전혀 기다리지 않고 Exception을 raise하는 것이죠.
