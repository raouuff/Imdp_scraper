import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
URL = 'https://m.imdb.com/chart/moviemeter/'
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
page_response = requests.get(URL, headers=headers)
print(page_response)
if page_response.status_code==200:
    #we got the whole content of the page
    soup=BeautifulSoup(page_response.content,'html.parser')
    #to get the moives content to make it more accurmetadataate
    Moives=soup.find('ul',class_='ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 eBRbsI compact-list-view ipc-metadata-list--base')
    ratings=Moives.findAll('div',class_='sc-e2dbc1a3-0 ajrIH sc-b189961a-2 fkPBP cli-ratings-container')
    ratings = [float(r.text.split()[0]) if r.text else 0.0 for r in ratings]
    Moives_Urls=[]
    if Moives:
        for link in Moives.find_all('a', href=True, class_='ipc-lockup-overlay ipc-focusable'):
            Moives_Urls.append('https://m.imdb.com'+link['href'])
        print(len(Moives_Urls))
        data=[]
        for i in range(0,len(Moives_Urls)):
            page = requests.get(Moives_Urls[i], headers=headers)
            page_soup=BeautifulSoup(page.content,'html.parser')
            name=page_soup.find('span',class_='hero__primary-text')
            year=page_soup.find('div',class_='sc-b7c53eda-0 dUpRPQ').find('a',class_='ipc-link ipc-link--baseAlt ipc-link--inherit-color')
            genre = page_soup.find('section', class_='sc-b7c53eda-4 kYwFBt')
            genre= genre.findAll('span',class_='ipc-chip__text') if genre else None
            if genre:genre=[g.text if g else "N/A" for g in genre]
            director=page_soup.find('a',class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')
            image=page_soup.find('img',class_='ipc-image')
            stars=page_soup.findAll('a',class_='sc-bfec09a1-1 gCQkeh')
            starsName=[name.text+' ' for name in stars]
            data.append(
                {
                    'Film title':name.text,
                    'IMDb rating':ratings[i],
                    'Release year':year.text,
                    'Genre':genre,
                    'Director':director.text,
                    'Movie image':image.get('src'),
                    'Star':starsName
                }
            )
            print({
                'Film title': name.text,
                'IMDb rating': ratings[i],
                'Release year': year.text,
                'Genre': genre,
                'Director': director.text,
                'Movie image': image.get('src'),
                'Star': starsName
            })
            time.sleep(3)
        df=pd.DataFrame(data)
        df.to_csv('output.csv',index=False)