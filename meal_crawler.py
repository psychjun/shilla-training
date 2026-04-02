import requests
from bs4 import BeautifulSoup
import urllib3
import os

# SSL 경고 메시지 무시 설정 (8443 포트 접속용)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 식단표 페이지 주소
URL = "https://csmsbiz.airport.kr:8443/cm/main/board/foodMenu.do#"
TARGET_TEXT = "씨제이 [사업지원센터점]"

def crawl_meal():
    # [중요] 브라우저인 척 하기 위한 헤더 설정
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://csmsbiz.airport.kr:8443/'
    }

    try:
        print(f"접속 시도 중: {URL}")
        # verify=False로 인증서 무시, timeout 추가
        res = requests.get(URL, headers=headers, verify=False, timeout=30)
        res.raise_for_status() # 접속 에러 시 바로 예외 발생
        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 모든 링크를 뒤져서 타겟 텍스트 찾기
        links = soup.find_all('a')
        img_url = ""
        
        print(f"찾은 링크 개수: {len(links)}")
        
        for link in links:
            link_text = link.get_text().strip()
            if TARGET_TEXT in link_text:
                print(f"타겟 발견: {link_text}")
                
                # 이미지 경로를 찾는 로직 (사이트 구조가 다를 수 있어 더 넓게 탐색)
                # 1. <a> 태그 안에 <img>가 있는 경우
                img_tag = link.find('img')
                # 2. 부모나 형제 요소에 <img>가 있는 경우
                if not img_tag:
                    parent = link.find_parent('td') or link.find_parent('tr')
                    if parent:
                        img_tag = parent.find('img')
                
                if img_tag and img_tag.get('src'):
                    img_url = img_tag['src']
                    # 상대 경로일 경우 절대 경로로 변환
                    if img_url.startswith('/'):
                        img_url = "https://csmsbiz.airport.kr:8443" + img_url
                    break

        if img_url:
            print(f"이미지 주소 획득: {img_url}")
            img_res = requests.get(img_url, headers=headers, verify=False, timeout=30)
            with open("food_menu.jpg", "wb") as f:
                f.write(img_res.content)
            print("성공: 식단표 이미지가 업데이트 되었습니다.")
        else:
            print(f"실패: '{TARGET_TEXT}' 문구는 찾았으나 이미지 경로를 확보하지 못했습니다.")
            # 디버깅을 위해 페이지 소스 일부 출력
            print("--- HTML 소스 일부 ---")
            print(soup.prettify()[:500])

    except Exception as e:
        print(f"에러 발생: {str(e)}")
        # 에러 발생 시 로그를 남겨 깃허브 메일에서 확인 가능하게 함
        raise e

if __name__ == "__main__":
    crawl_meal()
