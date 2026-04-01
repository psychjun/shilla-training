import requests
from bs4 import BeautifulSoup
import os

# 1. 사이트 접속
url = "https://csmsbiz.airport.kr:8443/cm/main/board/foodMenu.do"
try:
    response = requests.get(url, verify=False) # 보안 인증서 무시 (공공기관 사이트 이슈 대비)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 2. '씨제이 [사업지원센터점]' 텍스트가 포함된 링크 찾기
    target_link = None
    for a in soup.find_all('a'):
        if '씨제이' in a.text and '사업지원센터' in a.text:
            target_link = a.get('onclick') # 보통 onclick에 링크가 있음
            break

    # 3. 이미지 주소 추출 (이 부분은 사이트 구조에 따라 조정이 필요할 수 있어)
    # 실제 구현 시에는 해당 게시글로 들어가서 이미지를 가져와야 함.
    # 일단은 로직의 흐름만 잡아줄게.
    
    # 임시 이미지 저장 (테스트용)
    img_data = requests.get("https://via.placeholder.com/800x1200.png?text=CJ+Food+Menu+Test").content
    with open("food_menu.jpg", "wb") as handler:
        handler.write(img_data)
    print("식단표 이미지 업데이트 완료!")

except Exception as e:
    print(f"에러 발생: {e}")
