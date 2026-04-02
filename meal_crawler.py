import requests
from bs4 import BeautifulSoup
import os

# 식단표 페이지 주소
URL = "https://csmsbiz.airport.kr:8443/cm/main/board/foodMenu.do#"
TARGET_TEXT = "씨제이 [사업지원센터점]"

def crawl_meal():
    res = requests.get(URL, verify=False) # 보안 인증서 무시
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # "씨제이 [사업지원센터점]" 문구가 포함된 링크 찾기
    links = soup.find_all('a')
    img_url = ""
    
    for link in links:
        if TARGET_TEXT in link.get_text():
            # 실제 이미지가 있는 경로 추출 로직 (해당 사이트 구조에 맞춰 수정 필요)
            # 여기서는 예시로 첫 번째 이미지를 가져오는 흐름
            parent = link.find_parent('tr')
            img_tag = parent.find('img') if parent else None
            if img_tag:
                img_url = img_tag['src']
                break

    if img_url:
        # 이미지 다운로드 및 food_menu.jpg로 저장
        img_data = requests.get(img_url).content
        with open("food_menu.jpg", "wb") as f:
            f.write(img_data)
        print("Success: Food menu updated!")
    else:
        print("Fail: Menu not found.")

if __name__ == "__main__":
    crawl_meal()
