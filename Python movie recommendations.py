#API mash-up
#The TasteDive API lets you provide a movie as input and returns a set of related items. (max. 300 requests per hour)
#The OMDB API gives data about the provided movie, including scores from review sites.
#This program puts these two together so that you can get a list of related movies sorted according to their Rotten Tomatoes score.


import json
import requests

#Takes movie name as an input and retuns 5 similar movies (fetched from tastedive API)
def get_movies_from_tastedive(moviename):
    baseurl = "https://tastedive.com/api/similar"
    params_diction = {}
    params_diction["q"] = moviename
    params_diction["type"] = "movies"
    params_diction["limit"] = "5"
    resp = requests.get(baseurl, params=params_diction)
    five_similar = resp.json()
    return five_similar

#Function that extracts just the list of movie titles
def extract_movie_titles(dictionary):
    movietitles = []
    for film in dictionary['Similar']['Results']:
        movietitles.append(film['Name'])
    return movietitles

#Takes a list of movie titles as input. Returns five related movie titles for each movie.
def get_related_titles(list_of_movies):
    list_of_similar_movies = []
    for movie in list_of_movies:
        dictionaryofmovies = get_movies_from_tastedive(movie)
        listofmovietitles = extract_movie_titles(dictionaryofmovies)
        for one_movie in listofmovietitles:
            if one_movie in list_of_similar_movies:
                continue
            else:
                list_of_similar_movies.append(one_movie)
    return list_of_similar_movies


#Fetches data from OMDB. Returns dictionary with information about the movie. 
def get_movie_data(movietitle):
    baseurl = "http://www.omdbapi.com/"
    params_diction = {}
    params_diction['apikey'] = '5081bf1b'
    params_diction["t"] = movietitle
    params_diction["r"] = 'json'
    resp = requests.get(baseurl, params=params_diction)
    movie_data = json.loads(resp.text)
    return movie_data


#Takes OMDB dictionary results and extracts the Rotten Tomatoes rating. If no rotten tomatoes rating, returns 0.
def get_movie_rating(omdb_dictionary):
    rt_rating = 0
    for rate in omdb_dictionary['Ratings']:
        if (rate["Source"]) == "Rotten Tomatoes":
            rt_rating = int(rate['Value'][:-1])
    return rt_rating


#takes a list of movies as input. Returns five related movies per title.
#Movies are sorted in descending order by their Rotten Tomatoes rating.
def get_sorted_recommendations(list_of_movies):
    related_movies = sorted(get_related_titles(list_of_movies), key= lambda m: (get_movie_rating(get_movie_data(m)),m), reverse = True)
    return related_movies


#Test the program here
print(get_sorted_recommendations(["Pulp fiction", "Guardians of the galaxy"]))