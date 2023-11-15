#########################################
##### Name:     Meng Wang           #####
##### Uniqname:     meeewang        #####
#########################################

import json
import webbrowser
import requests
class Media:
    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", json=None):
        if json is None:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url
        else:
            try:
                self.title = json["trackName"]
            except KeyError:
                self.title = json["collectionName"]
            try:
                self.author = json["artistName"]
            except KeyError:
                self.title = json["collectionName"]
            try:
                self.release_year = json["releaseDate"][0:4]
            except KeyError:
                pass
            try:
                self.url = json["trackViewUrl"]
            except KeyError:
                self.url = json["collectionViewUrl"]    

    def info(self):
        return "{} by {} ({})".format(self.title, self.author, self.release_year)
        
    def length(self):
        return 0

# Other classes, functions, etc. should go here

class Song(Media):

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", album="No Album", genre="No Genre", track_length=0, json=None):
        super().__init__(title, author, release_year, url, json)
        if json is None: 
            self.album = album
            self.genre = genre
            self.track_length = track_length
        else:
            self.author = json ['artistName']
            self.album = json['collectionName']
            self.genre = json['primaryGenreName']
            self.track_lenght = json['trackTimeMillis']
 
    def info(self):
        return "{} by {} ({}) [{}]".format(self.title, self.author, self.release_year, self.genre)
        
    def length(self):
        return round(self.track_length)
    
class Movie(Media):

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", rating="No Rating", movie_length=0, json=None):
        super().__init__(title, author, release_year, url, json)
        if json is None:
            self.rating = rating
            self.movie_length = movie_length
        else:
            self.rating = json['contentAdvisoryRating']
            self.movie_length = json['trackName']
            try:
                self.movie_length = json["trackTimeMillis"]
            except KeyError:
                pass

    def info(self):
        return "{} by {} ({}) [{}]".format(self.title, self.author, self.release_year, self.rating)
        
    def length(self):
        return round(self.movie_length)
def data_from_itunes_api(query, params=None, limit=10):
    baseurl = "https://itunes.apple.com/search"
    params = {
        "term": query,
        "limit": limit
    }
    try:
        response = requests.get(baseurl, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from iTunes API: {e}")
        return []
    
def user_entry():

    item = ""
    user_entry = input("Enter a search term, or 'exit' to quit: ")

    if user_entry == 'exit':
        print('Bye!')
    else:
        item = user_entry

    return item

songs = []
movies = []
media = []
all_media_list = [] 

def media_list_parser(media_dict_lst):
    counter = 1

    for media_dict in media_dict_lst:
        print(f"MEDIA_DICT: {media_dict}")
        if "kind" in media_dict:
            if media_dict['kind'] == 'song':
                songs.append(media_dict)
            elif media_dict['kind'] == 'feature-movie':
                movies.append(media_dict)
            else:
                media.append(media_dict)
        else:
            media.append(media_dict)
    print(f"\nSONGS")
    if len(songs) == 0:
        print(f"None")
    else:
        for song in songs:
            song_results = Song(json=song)
            print(f"{counter} {song_results.info()}")
            counter += 1  

    print(f"\nMOVIES")
    if len(movies) == 0:
        print(f"None")
    else:
        for movie in movies:
            movie_results = Movie(json=movie)
            print(f"{counter} {movie_results.info()}")
            counter += 1

    print(f"\nOTHER MEDIA")
    if len(media) == 0:
        print(f"None\n")
    else:
        for m in media:
            media_results = Media(json=m)
            print(f"{counter} {media_results.info()}")
            counter += 1

    if len(songs) == 0 and len(movies) == 0 and len(media) == 0:
        print("Looks like nothing's here. Check your spelling?\n")

if __name__ == "__main__":
    media_dict_result = data_from_itunes_api(user_entry())

    i = 0
    while i == 0:
        media_list_parser(media_dict_result)
        break
    
    i = 1
    while i != 0:
        more_info = input(f"Enter a number for more info, or a search term, or exit: ")
        if more_info == "exit":
            print("Bye!")

        elif more_info.isnumeric():         
            more_info = int(more_info)
            all_media_list.extend(songs)
            all_media_list.extend(movies)
            all_media_list.extend(media)
            for i in range(len(all_media_list)):
                if i == (more_info - 1):
                    search_query = Media(json=all_media_list[i])
                    print(f"\nLaunching\n{search_query.url}\nin web browser...\n")
                    webbrowser.open(search_query.url)

        else:
            songs = []
            movies = []
            media = []
            all_media_list = []
            json_to_parse = data_from_itunes_api(more_info)
            media_list_parser(json_to_parse)

