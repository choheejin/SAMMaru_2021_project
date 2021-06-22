#cgv 청주성안길점

import requests
from bs4 import BeautifulSoup

url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=205&theatercode=0297&date=20210620'
html = requests.get(url)
soup = BeautifulSoup(html.text, 'html.parser')
movies = soup.select('body > div > div.sect-showtimes > ul > li')

def get_timetable(movie):
    tuples = []
    timetables = movie.select('div > div.type-hall > div.info-timetable > ul > li')
    for timetable in timetables:
        time = timetable.select_one('em').get_text()
        seat = timetable.select_one('span').get_text()
        tuple = (time,seat)
        tuples.append(tuple)
    return tuples


for movie in movies:
    title = movie.select_one('div>div.info-movie>a>strong').get_text().strip()
    timetable = get_timetable(movie)
    print(title, timetable, '\n')
