import bs4, requests
import spotipy
from spotipy.oauth2 import  SpotifyOAuth

#Takes user input for time period and playlist name and returns a list of song names from Bilboard Top 100 songs. 
#If the user input is empty it will return the current Top 100 songs

user_time = input("Please enter your specific date you want in yyy-mm-dd format: ") 
playlist_name=input("Please enter your playlist name: ") #I have not checked if the user input can be empty. 
url = f"https://www.billboard.com/charts/hot-100/{user_time}"


#Scraping proses for the playlist

response = requests.get(url)
songs = []
soup = bs4.BeautifulSoup(response.text, "html.parser")
for list in soup.find_all(class_="o-chart-results-list-row-container"):
    title = list.find("h3", class_="c-title").getText().strip()
    songs.append(title)


#Using your client credentials to login to your spotify account

client_id= "your client id"
client_secret= "your client secret"
redirect_uri = "your redirect uri"
scope = 'playlist-modify-public'  # This scope allows us to create and modify playlists

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

user_id = sp.current_user()['id'] #returns your current user id

#Using your user credentials to create a new playlist

playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True) 
playlist_id = playlist["id"]
external_url = playlist["external_urls"]
playlist_url = external_url["spotify"]


#Using your bilboard top 100 list to search and add songs into your playlist

for song_name in songs:
    results = sp.search(q=song_name, type='track')
    track_uri = results['tracks']['items'][0]['uri']
    sp.playlist_add_items(playlist_id=playlist_id, items=[track_uri])


#prints your playlist URL
print(playlist_url)


