#!/usr/bin/env python
# coding: utf-8

# In[3]:


""" 동아일보 특정 키워드를 포함하는, 특정 날짜 이전 기사 내용 크롤러(정확도순 검색)
    python [모듈 이름] [키워드] [가져올 페이지 숫자] [결과 파일명]
    한 페이지에 기사 15개
"""

#먼저 필요한 라이브러리를 불러옵니다.
import sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote

#이 부분은 'urlopen'으로 요청을 보낼 타겟 주소를 세 부분으로 나누어 상수에 할당한 부분입니다.

TARGET_URL_BEFORE_PAGE_NUM = "http://news.donga.com/search?p="
TARGET_URL_BEFORE_KEWORD = '&query='
TARGET_URL_REST = '&check_news=1&more=1&sorting=3&search_date=1&v1=&v2=&range=3'

#세 가지로 나눈 이유는 검색 페이지의 URL 패턴에 있습니다.
#http://news.donga.com/search?check_news=1&more=1&sorting=3&range=3&search_date=&query=그랜드캐니언
#위링크는 검색 설정을 모두 맞추고, 키워드인 "그랜드캐니언"을 검색한 결과입니다.
#우리는 이 화면의 15개의 검색 결과 뿐만 아니라, 기사 목록 페이지에 있는
#각각의 기사에 접근해 본문 내용까지 수집해야합니다.
#위 URL을 보면, 'check_news=1'은 뉴스로 한정지은 것, 'more=1'은 더보기를 누른 상태,
#'sorting=3'과 'range=3'은 각각 정확도순 정렬이며, 전체기간 검색,
#마지막으로 'query=그랜드캐니언'은 우리가 검색한 키워드라고 짐작할 수 있습니다.
#눈치채셨을 수 있지만, 이 주소에는 페이지에 해당하는 내용이 없습니다.
#페이지에 관한 내용은 숨겨져 있는 것이지요, 두번째 페이지의 URL을 보겠습니다.
#http://news.donga.com/search?p=16&query=그랜드캐니언&check_news=1&more=1&sorting=3&search_date=1&v1=&v2=&range=3
#좀 달라졌지요? 'query' 부분은 앞으로, 그리고 페이지 숫자로 보이는 'p=16'이 나왔습니다.
#이 숫자는 페이지를 넘어갈 때마다 15씩 더해지는 것을 알 수 있습니다.
#다시 세가지로 상수화 한 부분을 봅시다.

#TARGET_URL_BEFORE_PAGE_NUM = "http://news.donga.com/search?p="
#TARGET_URL_BEFORE_KEWORD = '&query='
#TARGET_URL_REST = '&check_news=1&more=1&sorting=3&search_date=1&v1=&v2=&range=3'

#'그랜드캐니언'을 통해 검색된 기사 목록 전체를 둘러보기 위해선 'query=사드'로 설정되어야 하며
#페이지 번호를 'p=1', 'p=16', 'p=31'... 처럼 원하는 페이지를 나타내는 수 만큼 변경시켜가며
#전부 둘러봐야 하는 것을 알 수 있습니다. 
#따라서 위 처럼 페이지수를 나타내는 'p='부분과 검색 키워드를 나타내는 '&query='부분의 정보를
#사용자로부터 입력받아 하나의 타겟 주소로 결합하기 위해서 타겟 주소를 세 부분으로 나눈 것입니다.
#그럼 타겟 주소가 어떻게 결합되어 사용되는지 알아보기 위해 크롤러 모듈에서 메인함수를 먼저 살펴보겠습니다.


# 기사 검색 페이지에서 기사 제목에 링크된 기사 본문 주소 받아오기
def get_link_from_news_title(page_num, URL, output_file):
    for i in range(page_num):
        current_page_num = 1 + i*15
        position = URL.index('=')
        URL_with_page_num = URL[: position+1] + str(current_page_num)                             + URL[position+1 :]
        source_code_from_URL = urllib.request.urlopen(URL_with_page_num)
        soup = BeautifulSoup(source_code_from_URL, 'lxml',
                             from_encoding='utf-8')
        for title in soup.find_all('p', 'tit'):
            title_link = title.select('a')
            article_URL = title_link[0]['href']
            get_text(article_URL, output_file)
 
 
# 기사 본문 내용 긁어오기 (위 함수 내부에서 기사 본문 주소 받아 사용되는 함수)
def get_text(URL, output_file):
    source_code_from_url = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_url, 'lxml', from_encoding='utf-8')
    content_of_article = soup.select('div.article_txt')
    for item in content_of_article:
        string_item = str(item.find_all(text=True))
        output_file.write(string_item)
 
 
# 메인함수
def main(argv):
    if len(argv) != 4:
        print("python [모듈이름] [키워드] [가져올 페이지 숫자] [결과 파일명]")
        return
    keyword = argv[1]
    page_num = int(argv[2])
    output_file_name = argv[3]
    target_URL = TARGET_URL_BEFORE_PAGE_NUM + TARGET_URL_BEFORE_KEWORD                  + quote(keyword) + TARGET_URL_REST
    output_file = open(output_file_name, 'w')
    get_link_from_news_title(page_num, target_URL, output_file)
    output_file.close()
 
 
if __name__ == '__main__':
    main(sys.argv)


# In[ ]:



