from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

#Check Readme file for moe details 
SPOTIPY_CLIENT_ID = "your spotify client id"
SPOTIPY_CLIENT_SECRET = "your spotify client secret"
SPOTIPY_REDIRECT_URL = "your spotify redirect url"
USERNAME = "your username"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                                               redirect_uri=SPOTIPY_REDIRECT_URL,
                                               client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               cache_path="token.txt",
                                               username=USERNAME,
                                               )
                     )

# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track=item["track"]
#     print(idx, track['artists'][0]['name'], "-", track['name'])

user_id = sp.current_user()["id"]
user_display_name = sp.current_user()["display_name"]
print(user_id)
print(user_display_name)

which_date = input("Which year would you want to travel to? Type the date in format YYYY-MM-DD:")

URL = f"https://www.billboard.com/charts/hot-100/{which_date}"
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

response = requests.get(url=URL, headers=header)
billboard_webpage = response.text

soup = BeautifulSoup(billboard_webpage, "html.parser")

Song_titles = soup.find_all(name="h3", id="title-of-a-story", class_="a-no-trucate")
Song_singers = soup.find_all(name="span", class_="a-no-trucate")
songs_list = [song.getText().strip() for song in Song_titles]
singers_list = [singer.getText().strip() for singer in Song_singers]

# print(songs_list)
# print(singers_list)

song_uris = []

year = which_date.split("-")[0]

for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")

    # print(result)
    try:
        uri = result["tracks"]['items'][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        # print(f"{song} doesn't exist in Spotify.. Skipped")
        pass

playlist = sp.user_playlist_create(user=user_id,
                                   name=f"{which_date} Billboard 100",
                                   public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print(playlist["external_urls"]["spotify"])