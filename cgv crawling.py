import requests
from bs4 import BeautifulSoup


# 필요한 기능 : 영화관을 사용자가 입력할 수 있게 하기.
#               날짜를 받아올 수 있게 하기.

url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0013&date=20210619'
html = requests.get(url)
soup = BeautifulSoup(html.text, 'html.parser')
movies = soup.select('body > div > div.sect-showtimes > ul > li')

def get_timetable(movie):
    lists = []
    timetables = movie.select('div > div.type-hall > div.info-timetable > ul > li')
    num = 1
    for timetable in timetables:
        if num % 4 == 0:
            break
        time = timetable.select_one('em').get_text()
        seat = timetable.select_one('span').get_text()
        list = [time, seat]
        lists.append(list)
        num = num + 1
    answer = sum(lists, [])
    StrA = " ".join(answer)
    return StrA


for movie in movies:
    title = movie.select_one('div>div.info-movie>a>strong').get_text().strip()
    timetable = get_timetable(movie)
    print(timetable)