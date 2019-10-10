from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from PIL import Image
import pyperclip, requests, time, traceback, pyautogui

class Alie:
    def __init__(self):     #chromedriver의 기본 옵션 적용 
        path = "C:\\Users\\sin\\Desktop\\chrome\\chromedriver_win32\\chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.add_argument('disable-infobars')    
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument("no-sandbox")
        options.add_argument("disable-dev-shm-usage")

        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        self.driver = webdriver.Chrome(path, chrome_options=options)

    def url_page(self, url):        #요청받는 urlpage에서의 정보 클릭 및 파싱
        try:
            self.driver.get(url)        #해당 url요청
            myElem = WebDriverWait(self.driver, 8).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))#8초 동안 url load 기다림
            print ("Page is ready!")
            self.driver.find_element_by_xpath("//a[@class='next-dialog-close']").click()    #팝업 close

            right_product = self.driver.find_element_by_xpath("//div[@class='product-info']").find_element_by_xpath("//div[@class='product-sku']").find_element_by_xpath("//div[@class='sku-wrap']")
            product_list = right_product.find_elements_by_class_name("sku-property")

            for x in range(0, len(product_list)):
            
                if product_list[x].text.split(":")[0] == "색깔":
                    color_list = product_list[x].find_element_by_xpath("ul[@class='sku-property-list']").find_elements_by_tag_name("li")
                    sel_num = input("번호를 선택해주세요 1~"+str(len(color_list))+" :")
                    color_list[int(sel_num)-1].click()    
                else:
                    select_list = product_list[x].find_element_by_xpath("ul[@class='sku-property-list']").find_elements_by_tag_name("li")
                    sel_num2 = input("번호를 선택해주세요 1~"+str(len(select_list))+" :")
                    select_list[int(sel_num2)-1].click()
            #select_list = t1[1].find_element_by_xpath("ul[@class='sku-property-list']").find_elements_by_tag_name("li")
            # // 가 있고 없고의 차이 
            
            amount = self.driver.find_element_by_xpath("//div[@class='product-quantity clearfix']").find_element_by_xpath("//div[@class='product-quantity-title']").find_element_by_xpath("//div[@class='product-quantity-info']").find_element_by_xpath("//div[@class='product-quantity-tip']").text
            #수량 경로
            sel_amo = input("수량 "+(amount.split(" ")[0])+"개 입력가능 :") #수량 입력
            amo_click = self.driver.find_element_by_xpath("//div[@class='product-quantity clearfix']").find_element_by_xpath("span[@class='next-number-picker next-number-picker-inline next-medium zoro-ui-number-picker number-picker product-number-picker']").find_element_by_xpath("//span[@class='next-input-group']").find_element_by_xpath("//span[@class='next-input next-medium next-input-group-auto-width']").find_element_by_tag_name("input")
            amo_click.click()
            
            ###################
            #클릭하구 값 넣는거 해야 한다.
            ###################
            #amount = 수량을 확인한다. 사용자에게 제품에대한 이미지를 보여주고 이미지와 같은지 확인 및 다를경우 URL 다시 요청
        
            #### screenshot ####
            name = self.driver.find_element_by_xpath("//div[@class='product-info']").find_element_by_xpath("div[@class='product-title']").text
            #물품 이름
            self.driver.save_screenshot("C:\\Users\\sin\\Desktop\\chrome\\chromedriver_win32\\"+name+".png")
            
        except:
            print("Loading took too much time!")
            traceback.print_exc()

    def login_Alie(self):   #Alie 로그인 함수
        try:
            self.driver.find_element_by_xpath("//button[@class='next-btn next-large next-btn-primary buynow']").click()
            time.sleep(3)   #time.sleep을 안걸시 자동로그인 방지 가 뜬다.
            self.driver.find_element_by_xpath("//ul[@role='tablist']").find_element_by_xpath("//li[@aria-selected='false']").click()
            iframe = self.driver.find_element_by_xpath("//iframe[@id='alibaba-login-box']")
            self.driver.switch_to_frame(iframe)     #iframe으로 감싸져 있어서 변환
            self.driver.find_element_by_xpath("//div[@class='login-content nc-outer-box']")
            login_id = self.driver.find_element_by_xpath("//input[@class='fm-text']")
            login_id.send_keys("gill1994@naver.com")    #ID
            # pyperclip.copy("gill1994@naver.com")
            # ActionChains(self.driver).click(login_id).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform() # Ctrl+V 전달
            login_pw = self.driver.find_element_by_xpath("//input[@type='password']")
            login_pw.send_keys("as14736945025")         #PW
            # pyperclip.copy("as14736945025")
            # ActionChains(self.driver).click(login_pw).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            self.driver.find_element_by_xpath("//button[@type='submit']").click()
            
        except:
            print("No!")
        

    def change_address(self, address):  #사용자에게 입력받은 정보 영문으로 변환 해주는 함수
        url = "https://search.naver.com/search.naver?where=nexearch&ie=utf8&X_CSA=address_search&query=" + address + "영문주소"
        s = requests.session()
        res = s.get(url).content
        change = BeautifulSoup(res, 'html.parser')
        english_language = change.find_all("strong")[2].text    #영문주소
        korean_language = change.find_all("dd")[3].text         #한글주소 
        self.korean_list = korean_language.split(" ")
        self.postal_code = change.find_all("td")[8].text        #우편번호
        self.english_list = english_language.split(",")
        self.english_dict = {}
        self.english_dict[self.english_list[4]] = "".join(self.english_list[0]+self.english_list[1]+self.english_list[2]+self.english_list[3])
        

    def shipping(self, contact, ph_num, clearance):     #영문으로 변환된 정보 입력하는 함수
        self.driver.find_element_by_xpath("//div[@class='main']")
        shipping_info = self.driver.find_element_by_xpath("//div[@class='ship-info']").find_element_by_xpath("//span[@class='next-input next-large']")
        shipping_info_name = shipping_info.find_element_by_xpath("//input[@id='contactPerson']")
        shipping_info_name.send_keys(contact)       #사용자 이름 
        shipping_num = shipping_info.find_element_by_xpath("//input[@id='mobileNo']")
        shipping_num.send_keys(ph_num)              #사용자 핸드폰번호
        shipping_address = shipping_info.find_element_by_xpath("//input[@id='address']")
        shipping_address.send_keys(self.english_list[4])    #사용자 주소(ex 경기도)
        shipping_address2 = shipping_info.find_element_by_xpath("//input[@id='address2']")
        shipping_address2.send_keys(self.english_dict[self.english_list[4]])    #사용자주소(ex 안양시 만안구)
        shipping_region = shipping_info.find_elements_by_xpath("//span[@class='next-select-values next-input-text-field']")
        
        shipping_region[1].click()
        region_list = shipping_region[1].find_element_by_xpath("//div[@class='next-menu zoro-ui-select-dropdown zoro-ui-search-select-dropdown']").find_element_by_xpath("//ul[@class='dropdown-content']").find_elements_by_tag_name("li")
        
        for x in region_list:   #사용자 지역에 맞는 값 클릭(ex 경기도)
            if self.korean_list[0][:2] == x.text:
                x.click()
                break
        
        city_list = shipping_info.find_element_by_xpath("//div[@class='addr-select-container']").find_element_by_xpath("//div[@class='addr-select']").find_elements_by_tag_name("div")[2]
        city_list.click()
        city_list2 = city_list.find_element_by_xpath("//ul[@class='dropdown-content']").find_elements_by_tag_name("li")
            
        for y in city_list2:    #사용자 지역에 맞는 값 클릭(ex 안양시 만안구)
            if self.korean_list[1] == y.text:
                y.click()
                break

        shipping_postal = shipping_info.find_element_by_xpath("//input[@placeholder='Zip Code']")   #우편번호 입력
        shipping_postal.send_keys(self.postal_code)
        
        shipping_ClearanceInformation = shipping_info.find_element_by_xpath("//input[@id='passportNo']")    #통관번호입력
        shipping_ClearanceInformation.send_keys(clearance)
        #"P170003123883"
        self.driver.find_element_by_xpath("//div[@class='save']").find_element_by_xpath("//button[@ae_page_type='Place_Order_Page']").click()
        #확인버튼
    def pay_info(self):     #CARD 입력 함수
        time.sleep(5)
        self.driver.find_element_by_xpath("//div[@class='pay-method']").find_element_by_xpath("//div[@class='pay-detail ']")
        pay_number = self.driver.find_element_by_xpath("//*[@id='cardNo']") #카드 번호
        pay_number.click()
        pay_number.send_keys("4477038008894244")
        pay_name = self.driver.find_element_by_xpath("//*[@id='cardHolder']")   #사용자 영문이름
        pay_name.click()
        pay_name.send_keys("SHIN GYEONG HO")
        pay_period = self.driver.find_element_by_xpath("//*[@id='expire']") #만료기간
        pay_period.click()
        pay_period.send_keys("1221")
        pay_cvc = self.driver.find_element_by_xpath("//*[@id='cvc']")   #카드 cvc번호
        pay_cvc.click()
        pay_cvc.send_keys("403")
        self.driver.find_element_by_xpath("//div[@class='save']").find_element_by_tag_name("button").click()
        time.sleep(100)
        # self.drvier.find_element_by_xpath("//div[@id='side']").find_elements_by_xpath("//div[@id='price-overview']").find_element_by_xpath("//div[@class='next-loading next-loading-inline loading']").find_element_by_xpath("//div[@class='order-btn-holder']").find_element_by_tag_name("button").click()
        # 마지막 결제 버튼
if __name__ == "__main__":
    # addr = input("주소를 입력하세요 : ")
    # ph_num = input("핸드폰 번호를 입력해주세요 : ")
    # name = input("이름을 입력해주세요 : ")
    # clearance = input("통관번호를 입력하세요 : ")
    test = Alie()
    # test.url_page("https://ko.aliexpress.com/item/33055472118.html?spm=a2g0o.productlist.0.0.68635bb7AuBrWZ&algo_pvid=f623c4a4-f07d-4423-b675-f4035a286ef6&algo_expid=f623c4a4-f07d-4423-b675-f4035a286ef6-1&btsid=a42a5534-9e5b-4709-a9bf-2a15decd9c18&ws_ab_test=searchweb0_0,searchweb201602_8,searchweb201603_52")
    test.url_page("https://ko.aliexpress.com/item/4000052480223.html?spm=a2g01.12597576.p99adbb.13.d8923e7dnko4KV&gps-id=7316167&scm=1007.19881.118560.0&scm_id=1007.19881.118560.0&scm-url=1007.19881.118560.0&pvid=48bc1057-80cd-42b3-9a13-ddc87c7b2ab5")
    # test.login_Alie()
    # test.change_address(addr)
    # test.pay_info()
    # test.shipping(name, ph_num, clearance)
