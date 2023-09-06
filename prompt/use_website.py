from selenium import webdriver
from selenium.webdriver import Keys #키보드 입력 역할
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager #크롬브라우저
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyperclip
import urllib.request

def using_dalle(prompt):
    #옵션 집어 넣기
    chrome_options=webdriver.ChromeOptions()
    #크롬 브라우저 고정(코드가 끝나도 브라우저 사라지지 않도록)
    chrome_options.add_experimental_option('detach',True)
    #크롬 브라우저 화면에 띄우기
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    #크롬 화면 최대화
    driver.maximize_window()

    #주소로 접근
    driver.get("https://www.bing.com/images/create")
    time.sleep(3)

    #클릭하기
    # 요소 로딩 대기 설정
    wait = WebDriverWait(driver, 10)  # 최대 10초까지 대기

    # 요소가 나타날 때까지 대기 후 요소를 찾음
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.land_login_create.gi_btn_p.gi_ns')))
    element.click()

    #아이디, 비밀번호 입력하기
    bingid= ##bing_id
    bingpw=##bing_password

    #아이디 입력하고 다음버튼 누르기
    pyperclip.copy(bingid)
    driver.find_element(By.ID,'i0116').send_keys(Keys.CONTROL,'v')

    wait = WebDriverWait(driver, 3)
    element = wait.until(EC.presence_of_element_located((By.ID, 'idSIButton9')))
    element.click()
    time.sleep(2)

    #비밀번호 입력하고 다음 누르기
    pyperclip.copy(bingpw)
    driver.find_element(By.ID,'i0118').send_keys(Keys.CONTROL,'v')

    wait = WebDriverWait(driver, 3)
    element = wait.until(EC.presence_of_element_located((By.ID, 'idSIButton9')))
    element.click()

    #다 입력하고 저장하기 버튼 누르기
    wait = WebDriverWait(driver, 3)
    element = wait.until(EC.presence_of_element_located((By.ID, 'idSIButton9')))
    element.click()

    #프롬프트 입력창 클릭
    wait = WebDriverWait(driver, 3)
    element = wait.until(EC.presence_of_element_located((By.ID, 'sb_form_q')))
    element.click()

    #프롬프트 입력
    prompt = prompt
    pyperclip.copy(prompt)
    driver.find_element(By.ID,'sb_form_q').send_keys(Keys.CONTROL,'v')

    wait = WebDriverWait(driver, 3)
    element = wait.until(EC.presence_of_element_located((By.ID, 'create_btn_c')))
    element.click()
    time.sleep(2)

    #생성된 이미지 저장하기

    wait = WebDriverWait(driver, 10)  # 최대 10초까지 대기
    image_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'mimg')))

    image_src = image_element.get_attribute("src")
    #print("Image Source:", image_src)

    #이미지 찾고 다운받기
    wait = WebDriverWait(driver, 10)

    try:
        # 이미지 요소를 찾음
        image_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'mimg')))

        # 이미지의 src 속성과 alt 속성 가져오기
        img_url = image_element.get_attribute("src")
        #img_alt = image_element.get_attribute("alt") #입력된 프롬프트 내용

        # 이미지 다운로드
        #urllib.request.urlretrieve(img_url, 'img/result' + ".jpg")
    except Exception as e:
        print("Error:", e)
    finally:
        # 브라우저 종료
        driver.quit()

    return image_src #이미지 링크 제공
