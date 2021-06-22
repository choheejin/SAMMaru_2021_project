import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import csv
import requests

URL = "https://movie.naver.com/movie/running/current.nhn"
response = requests.get(URL)

soup = BeautifulSoup(response.text, "html.parser")

movie_data = []

movies = soup.select('dt.tit a')
for a_tag in movies:
    title = a_tag.text

    link_split = a_tag['href'].split('=')
    code = link_split[1]
    movie_tile_code = {
        'title' : title,
        'code' : code
    }
    movie_data.append(movie_tile_code)

subBreak = True
for movie in movie_data:
    if subBreak == False:
        break
    print()
    movie_code = movie['code']

    headers = {
        'authority': 'movie.naver.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'iframe',
        'referer': 'https://movie.naver.com/movie/bi/mi/point.nhn?code=189069',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'NRTK=ag#20s_gr#0_ma#-2_si#0_en#-1_sp#-1; ASID=731711cf0000017332744bcd0000005c; NM_THUMB_PROMOTION_BLOCK=Y; MM_NEW=1; NFS=2; MM_NOW_COACH=1; nx_ssl=2; NNB=HJOWCJ4MSYVF6; nid_inf=-1587872843; NID_AUT=ms/s8984xk6pp5LiYixmlL0IJ19FuO2FOm8M63dpFdlRQIer+58aNToXqSlELYWA; NID_JKL=9Vo5Vegco/eLv1m+6P1Kbt0bWcBm1Axn+OghbQooVbw=; BMR=s=1596694645166&r=https%3A%2F%2Fm.post.naver.com%2Fviewer%2FpostView.nhn%3FvolumeNo%3D29000825%26memberNo%3D15470144%26vType%3DVERTICAL&r2=https%3A%2F%2Fsearch.naver.com%2Fsearch.naver%3Fwhere%3Dnexearch%26sm%3Dtab_htk.nws%26ie%3Dutf8%26query%3D%25EB%25A5%2598%25ED%2598%25B8%25EC%25A0%2595%2B%25EC%259B%2590%25ED%2594%25BC%25EC%258A%25A4%2B%25EB%2585%25BC%25EB%259E%2580%25EC%2597%2590; page_uid=UyXlAlp0JywssPTkfEossssssYG-206097; NID_SES=AAABkPEddfvEDn4INl9+yjFY54DF1EAo9SXIt1ebEH/9DgMDSQwfatPgMGF/9beXBPUF1sun8XY4+EejzCKKpp+Mh2mooDsva1lg/m5Pg+4wpvJGDl9YwEPWuKCKOHqGaQK+mu0DSfA7rJvq6+tGjsNh52KPiszv8gxs2n4hX336qyFY+5LE0zkEjmVkbvJFfqCuX1sRpHCKSx5r7ql+/hwJUR1ckIVya6/XEheUE+fJcNeGFjaGR+FfCUVEQxRk8cRXkQ1NyCi1Hs487Eth02WVgXDYSBkJdL5DoYQMypX2NyxTbJoQqXX+SowjraC1GV+vw3j47tjiuvYK/IFUidW0Z4nF/wZCRq4J9ryiDvznMOfy0NO48fl5Vsw+P9FB3WIfOaXbjMDplKEcMTL4DpNxm3j+POHamQZ1qGRYhf8zYSu6aIWOrO8TnQ/KO9vrDhxJIVIYsFfZ96cq3qjwQ9WrcNRd1rLqZMNggXG5tImNVxn1m73Z2aJM/qqCu04G58ORcUW1u2TjjQ4ksyXzeOKo5IA=; REFERER_DOMAIN="d3d3Lmdvb2dsZS5jb20="; NM_VIEWMODE_AUTO=basic; csrf_token=5c41a00a-906f-450f-8594-970720a6feba',
    }

    params = (
        ('code', movie_code),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )

    response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', headers=headers,
                            params=params)

    soup = BeautifulSoup(response.text, "html.parser")
    lis = soup.select('body > div > div > div.score_result > ul > li')
    # 우선 li 들을 리스트 형태로 받아오고 이를 반복문으로 돌린다.
    num = 1
    lists = []
    for li in lis :
        if num >= 10:
            subBreak = False
            break
        # li에서 별점정보를 찾는다.
        # 다만 성분이 단 하나임에도 이 역시 리스트형태로 반환됨이 확인되어
        # [0]로 값에 접근한 뒤 텍스트(별점)을 받아왔다
        star = li.select('div.star_score > em')[0].getText()
        # 이것도 리스트로 반환되서 [0] 처리
        p = li.select('div.score_reple > p > span')
        if len(p) == 2:
            p = p[1]
        else:
            p = p[0]
        # 내용이 길면 p안에 a태그가 존재한다
        # a가 존재할 경우 하나의 성분을, 없으면 [] 반환
        if movie['title'] == "루카":
            num += 1
            strTitle = movie['title']
            strStar = star + "점"
            strRe = p.text.strip()
            list = [strTitle, strStar, strRe]
            lists.append(list)
            print(strTitle, strStar, strRe)
            print("===========================================================")

answer = sum(lists, [])
StrA = " ".join(answer)
print(StrA)



