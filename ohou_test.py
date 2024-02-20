import random
import re
import time

from Test_func import test_func
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
test_func = test_func(driver)
test_func.create_folder('C:/test')
f = open("C:/test/ohou_test_result.txt", 'w')
f.close()
folder = 'C:/test/'
result = []


def test_1():
    # 랜덤 상품 장바구니 담기 확인
    f = open("C:/test/ohou_test_result.txt", 'a')
    f.write('OHO-1:랜덤 상품 장바구니 담기 확인\n')

    # 1.오늘의집 홈페이지 이동
    url = 'https://ohou.se/'
    driver.get(url)

    # 2.GNB의 쇼핑 클릭
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[text()='쇼핑']"))).click()

    # 3.임의의 상품 장바구니에 담기
    try:
        count = random.randrange(2, 7)  # 장바구니에 담을 상품 수 선택
        for number in range(1, count + 1):

            xpath = '//*[@id="store-index"]/section[3]/div[2]/div[' + str(number) + ']/article/a'
            element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).get_attribute('href')
            item = re.findall(r'\d+', element)
            driver.get(element)                 #상품 페이지 이동
            itemname = test_func.item_name()    #상품 이름 추출
            test_func.item_option()             #상품 장바구니에 담기

            # 4.장바구니 아이콘 클릭
            xpath_s = '/html/body/div[1]/div/div/header/div[1]/div/div/div[4]/div/a'
            driver.find_element(By.XPATH, xpath_s).click()

            # 5.상품명 확인
            driver.implicitly_wait(3)
            xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div/ul/li[1]/article/ul/li/article/ul/li/article/a/div[2]/h1'
            element = driver.find_element(By.XPATH, xpath).text

            if element == itemname:         #실제 상품 명칭과 장바구니내 노출되는 상품 명칭 비교
                result = ' / ' + str(number) + '번 상품' + '[상품번호' + str(item) + ' Pass]'
            else:
                result = ' / ' + str(number) + '번 상품' + '[상품번호' + str(item) + ' Fail]'
            f.write(result)
            if element != itemname:
                return False

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[text()='쇼핑']"))).click()       #쇼핑탭 이동

        f.close()
    finally: test_func.cart_screenshot(folder+'OHO-1')          #장바구니 내부 이미지 저장
    print('\ntest1 pass')


def test_2():
    # 장바구니 아이콘에 노출된 상품 수 확인
    driver.delete_all_cookies()  # 쿠키 삭제
    f = open("C:/test/ohou_test_result.txt", 'a')
    f.write('\n\nOHO-2:장바구니 아이콘에 노출된 상품 수 확인\n')

    # 1.오늘의집 홈페이지 이동
    url = 'https://ohou.se/'
    driver.get(url)

    # 2.GNB의 쇼핑 클릭
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[text()='쇼핑']"))).click()

    # 3.임의의 상품 장바구니에 담기
    count = random.randrange(2, 7)      #장바구니에 담을 상품 수 선택
    for number in range(1, count + 1):
        xpath = '//*[@id="store-index"]/section[3]/div[2]/div[' + str(number) + ']/article/a'       #상품링크 추출
        element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).get_attribute('href')
        driver.get(element)         #상품 페이지 이동
        test_func.item_option()     #상품 장바구니에 담기
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[text()='쇼핑']"))).click() #쇼핑탭 이동

    # 4.장바구니 아이콘 클릭
    xpath = '/html/body/div[1]/div/div/header/div[1]/div/div/div[4]/div/a'
    driver.find_element(By.XPATH, xpath).click()

    # 5.장바구니 아이콘에 표시된 상품 수 확인
    driver.refresh()
    xpath_s = '/html/body/div[1]/div/div/header/div/div/div/div[4]/div/a/span[2]'
    element_s = driver.find_element(By.XPATH, xpath_s).text         #상단 장바구니 아이콘에 담긴 상품 노출 개수 확인
    count_s = str(count)
    if count_s == element_s:                                        #실제 담은 상품 수 와 장바구니 아이콘에 노출된 상품 개수 비교
        f.write('장바구니에 담은 상품 수: ' + count_s + '\n')
        f.write('장바구니 아이콘에 노출된 상품 수: ' + element_s + '\n')
        f.write('Pass')
    else:
        f.write('실제 담긴 상품 수: ' + count_s + ' / 장바구니 표시 수: ' + element_s + '\n')
        f.write('Faill - 장바구니에 담긴 상품 수 확인\n')

    f.close()
    test_func.cart_screenshot(folder + 'OHO-2')          #장바구니 내부 이미지 저장

    if count_s != element_s:
        return False
    print('test2 pass')

def test_3():
    # 장바구니 상품 삭제 기능 확인
    driver.delete_all_cookies()  # 쿠키 삭제
    f = open("C:/test/ohou_test_result.txt", 'a')
    f.write('\n\nOHO-3:장바구니 상품 삭제 기능 확인\n')
    itemname=[]

    # 1.오늘의집 홈페이지 이동
    url = 'https://ohou.se/'
    driver.get(url)

    # 2.GNB의 쇼핑 클릭
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[text()='쇼핑']"))).click()

    # 3.임의의 상품 장바구니에 담기
    count = random.randrange(2, 7)      #장바구니에 담을 상품 수 선택
    for number in range(1, count + 1):
        xpath = '//*[@id="store-index"]/section[3]/div[2]/div[' + str(number) + ']/article/a'       #상품링크 추출
        element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).get_attribute('href')
        driver.get(element)         #상품 페이지 이동
        itemname.append(test_func.item_name())
        test_func.item_option()     #상품 장바구니에 담기
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[text()='쇼핑']"))).click() #쇼핑탭 이동


    # 4.장바구니 아이콘 클릭
    xpath = '/html/body/div[1]/div/div/header/div[1]/div/div/div[4]/div/a'
    driver.find_element(By.XPATH, xpath).click()

    # 5.상품 확인
    count_s = count
    a = 0
    f.write('장바구니에 담김 상품 수: ' + str(count) + '\n')
    test_func.cart_screenshot(folder + 'OHO-3_before')  # 장바구니 내부 이미지 저장
    while count_s >= 1:                                 #장바구니내 상품 이름 추출
        driver.implicitly_wait(3)
        name_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div/ul/li['+ str(count_s) +']/article/ul/li/article/ul/li/article/a/div[2]/h1'
        element = driver.find_element(By.XPATH, name_xpath).text

        if itemname[a] == element:      #담은 상품명과 장바구니내 노출 상품명 확인
            pass
        else:
            f.write('Fail - 장바구니에 담긴 상품 확인(상품명 불일치)\n')
            f.write('담은 상품: '+itemname+' / 노출 상품: '+ element)
        if itemname[a] != element:
            return False
        count_s -=1
        a +=1


    # 6.임의의 상품 삭제
    if count < 3:                                               #삭제할 상품 개수 설정
        number_del = 1
    else:
        number_del = random.randrange(1, count - 1)

    itemname = ["default_value"] * number_del                   #리스트 초기화
    for count_s in range(1, number_del+1):                      #삭제할 상품의 상품명 확인
        name_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div/ul/li['+str(count_s)+']/article/ul/li/article/ul/li/article/a/div[2]/h1'
        itemname[(count_s-1)] = driver.find_element(By.XPATH, name_xpath).text

    element = driver.find_elements(By.CLASS_NAME, '_3UImz')
    for a in range(number_del + 1):                             #삭제 할 상품 수만큼 상품 선택
        item_index = element[a]
        item_index.click()
    element = driver.find_element(By.XPATH, '//button[contains(text(),"삭제")]')          #선택삭제 버튼 클릭
    driver.execute_script("arguments[0].click();", element)
    element = driver.find_element(By.CLASS_NAME,'css-97tdd8')
    element.screenshot(folder+'OHO-3_before/del.png')                                   #팝업 이미지 저장
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'css-6ums0u')))
    element.click()                                                                     #팝업의 삭제 버튼 클릭
    f.write('삭제한 상품 수: ' + str(number_del) + '\n')

    # 7.장바구니 페이지에 노출되는 상품 확인
    try:                                                        #팝업 닫침 확인
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-97tdd8')))
        element.click()
        f.write('삭제 버튼 클릭 확인 필요\n')
    except TimeoutException:
        pass
    driver.refresh()

    count_s = (count - number_del)
    while count_s >=1:
        name_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div/ul/li[' + str(count_s) + ']/article/ul/li/article/ul/li/article/a/div[2]/h1'
        element = driver.find_element(By.XPATH, name_xpath).text  # 장바구니내 남은 상품 상품명 확인
        for a in itemname :
            if a == element:  # 남은 상품의 상품명과 삭제한 상품의 상품명 비교
                f.write('Fail - 삭제 실패 상품 확인\n')
            else:pass
        count_s -=1

    f.write('남은 상품 수: ' + str(count - number_del)+'\n')
    f.write('Pass')
    f.close()
    test_func.cart_screenshot(folder + 'OHO-3_after')           #장바구니 내부 이미지 저장

    if a == element: return False
    else: print('test3 pass')

def test_4():
    # 장바구니 총 결제 금액 확인
    driver.delete_all_cookies()  # 쿠키 삭제
    f = open("C:/test/ohou_test_result.txt", 'a')
    f.write('\n\nOHO-4:장바구니 총 결제 금액 확인\n')

    # 1.오늘의집 홈페이지 이동
    url = 'https://ohou.se/'
    driver.get(url)

    # 2.GNB의 쇼핑 클릭
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[text()='쇼핑']"))).click()

    # 3.임의의 상품 장바구니에 담기
    count = random.randrange(2, 7)          # 장바구니에 담을 상품 수 선택
    item_costs = 0
    for number in range(1, count + 1):
        xpath = '//*[@id="store-index"]/section[3]/div[2]/div[' + str(number) + ']/article/a'
        element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).get_attribute('href')
        driver.get(element)                           #상품 페이지 이동
        item_cost = test_func.item_option_price()     #상품 장바구니에 담기 & 상품 금액 확인
        item_costs += int(re.sub(r'[^0-9]', '', item_cost))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[text()='쇼핑']"))).click()      #쇼핑탭 이동

    # 4.장바구니 아이콘 클릭
    xpath = '/html/body/div[1]/div/div/header/div[1]/div/div/div[4]/div/a'
    driver.find_element(By.XPATH, xpath).click()

    # 5.총 결제 금액 확인
    time.sleep(2)
    element = driver.find_elements(By.CLASS_NAME, 'commerce-cart__summary__row.commerce-cart__summary__row--total')[0]
    element = element.find_element(By.XPATH, './dd/span').get_attribute('innerText')            #장바구니에서 총 결제 금액 확인
    total_cost = int(re.sub(r'[^0-9]', '', element))
    element = driver.find_elements(By.XPATH, '//*[contains(text(),"총 배송비")]/../dd/span')[0].get_attribute('innerText')
    ship_cost = int(re.sub(r'[^0-9]', '', element))
    if (item_costs + ship_cost) == total_cost:                                                  #상품별 합산 금액과 장바구니에 노출되는 총 결제 금액 확인
        f.write('노출금액:' + str(total_cost) + '\n')
        f.write('실제금액:(상품금액:' + str(item_costs) + ' / 총 배송비:' + str(ship_cost) + ')'+'\n')
        f.write('Pass')
    else:
        f.write('노출금액:' + str(total_cost) + '\n')
        f.write('실제금액:(상품금액:' + str(item_costs) + ' / 총 배송비:' + str(ship_cost) + ')')
        f.write('False\n')

    f.close()
    test_func.cart_screenshot(folder+'OHO-4')                                                   #장바구니 이미지 저장
    if (item_costs + ship_cost) != total_cost:
        return False

    print('test4 pass')

def test_5():
    # 로그인 팝업 노출 확인
    driver.delete_all_cookies()  # 쿠키 삭제
    f = open("C:/test/ohou_test_result.txt", 'a')
    f.write('\n\nOHO-5:로그인 팝업 노출 확인\n')

    # 1.오늘의집 홈페이지 이동
    url = 'https://ohou.se/'
    driver.get(url)

    # 2.GNB의 쇼핑 클릭
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[text()='쇼핑']"))).click()

    # 3.임의의 상품 장바구니에 담기
    count = random.randrange(2, 7)  # 장바구니에 담을 상품 수 선택
    for number in range(1, count + 1):
        xpath = '//*[@id="store-index"]/section[3]/div[2]/div[' + str(number) + ']/article/a'  # 상품링크 추출
        element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).get_attribute(
            'href')
        driver.get(element)  # 상품 페이지 이동
        test_func.item_option()  # 상품 장바구니에 담기
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[text()='쇼핑']"))).click()  # 쇼핑탭 이동

    # 4.장바구니 아이콘 클릭
    xpath = '/html/body/div[1]/div/div/header/div[1]/div/div/div[4]/div/a'
    driver.find_element(By.XPATH, xpath).click()

    # 5.상품 구매하기 버튼 클릭
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'commerce-cart__side-bar__order')))
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div/div/div/button').click()
    time.sleep(10)

    # 6.로그인 팝업 확인
    driver.to_switch(driver.window_handles[1])
    time.sleep(10)
    element = driver.find_element(By.CLASS_NAME,'css-fwddxj.ebon26m7')
    element.screenshot(folder+'OHO-5/pop.png')
    if element :
        f.write('로그인 팝업 노출\n')
        f.write('Pass')
    else:
        f.write('로그인 팝업 미노출\n')
        f.write('False')

    f.close()
    if element: pass
    else: return False
    print('test5 pass')





