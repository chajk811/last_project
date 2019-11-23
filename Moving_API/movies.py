import csv
import requests
import json
from pprint import pprint
from decouple import config

movies = []
result = []
key = config('KEY')

# Discover
# 최신 영화 60개를 result에 담기

for i in range(3):
# for i in range(1):
    
    page = i+1
    base_url = 'https://api.themoviedb.org/3/discover/movie?'
    url = base_url + f'api_key={key}&language=ko-KR&sort_by=popularity.desc&include_adult=false&include_video=false&page={page}'
    
    response = requests.get(url)
    response_dict = response.json()
    
    # len(response_dict['results']) => 20개 
    for i in range(len(response_dict['results'])):
        movieId = response_dict['results'][i]['id']
        movies.append(movieId)

for i in range(len(movies)):
# for i in range(1):
    movie_id = movies[i]
    
    # model : Movie
    movie_tmp = {}
    movie_tmp['model'] = 'movies.movie'
    movie_tmp['pk'] = movies[i]
    base_url_movies = 'https://api.themoviedb.org/3/movie/'

    ## detail
    url_detail = base_url_movies + f'{movie_id}?api_key={key}&language=ko-KR'

    response = requests.get(url_detail)
    response_dict = response.json()

    title = response_dict["title"]
    audience = response_dict["popularity"]
    start_date = response_dict["release_date"]  
    poster_url = response_dict["poster_path"]
    summary = response_dict["overview"]
    
    genres = []
    tmps = response_dict["genres"]
    for tmp in tmps:
        genres.append(tmp["id"])
    
    ## credits
    url_credits = base_url_movies + f'{movie_id}/credits?api_key={key}'
    
    response = requests.get(url_credits)
    response_dict = response.json()

    tmps = response_dict["crew"]
    director = ''

    for tmp in tmps:
        if tmp["job"] == "Director":
            director = tmp["name"]
            break

    ## videos
    # teaser = response_dict["video"]
   
    movie_tmp['fields'] = {
        'title': title,
        'audience': audience,
        'start_date': start_date,  
        'director': director,
        'poster_url': poster_url,
        'summary': summary,
        'genres': genres,
        # 'teaser': teaser
    }
    result.append(movie_tmp)

with open('movies.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)