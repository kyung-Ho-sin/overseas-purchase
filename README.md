# overseas-purchase
크롤링을 이용한 해외직구 프로젝트

* Site
 1. Amazon
 2. AliExpress

*method(AliExpress)
1.url_page(요청받은 urlpage에서의 정보 클릭 및 파싱)
2.login_Alie(self):   #Alie 로그인
3.change_address(self, address):  #사용자에게 입력받은 정보 영문으로 변환
4.shipping(self, contact, ph_num, clearance):     #영문으로 변환된 정보 입력
5.pay_info(self):   #CARD 입력

*method(Amazon)
1.url_page(self, url):    #사용자가 입력한 제품 URL,사용자가 선택한 제품옵션을 처리
2.login(self):    #로그인
3.payment(self): #결제방식선택

selenium을 사용해서 프로젝트를 진행했고 모든 제품에 대해서 자동주문되는 상태가 아닌 특정제품에 한에서 자동주문이 가능하다.

