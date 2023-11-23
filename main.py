import requests
from bs4 import BeautifulSoup
#get the user input for a particular date
date=input("which year do you want to travel and it must be on the format YYYY-MM-DD")

#get the data from the music site
response=requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")

#web scrape the web page to get a particular component( song name)from page
scrape=BeautifulSoup(response.text,"html.parser")

song_name_element=scrape.select("li ul li h3")

#store the respective data which is song names into a list
song_name=[ title.get_text().strip()for title in song_name_element]
print(song_name)
print(response.status_code)

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
#with the help spotify dash board for developers we can create the spotify app
# coz we cant make changes in the general applications

#the client id and secret key is used to get the authentication
#the Redirect URI is a critical mechanism that ensures secure and smooth communication
# between the OAuth 2.0 authorization server (e.g., Spotify) and the client application.
# It plays a significant role in the authentication process, allowing the client to obtain
# the necessary tokens to access resources on behalf of the user while maintaining security and user privacy.
CLIENT_ID_SPOTIFY = "e6a9dee4691743f1bc17a543020ebb5e"
CLIENT_SECRET_SPOTIFY = "9c04b7e237ee432ab491cddf7e25bc97"
URL_REDIRECT = "http://example.com"
USER_NAME="Sanjaikumar"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID_SPOTIFY ,
        client_secret=CLIENT_SECRET_SPOTIFY,
        show_dialog=True,
        cache_path="token.txt",
        username=USER_NAME,
    )
)
user_id = sp.current_user()["id"]
song_uris=[]
c=0
year=date.split("-")[0]
print(year)
for song in song_name:
    result = sp.search(q=f"track:{song} year:2003", type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
        c+=1
print(c)
print(len(song_uris))

playlist=sp.user_playlist_create(user=user_id,name=f"billboard{year}",public="false")
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print(playlist['external_urls']['spotify'])
#When authenticating with the Spotify API, the general process is as follows:

#The client application (developer) registers their application on the Spotify Developer
# Dashboard to obtain a Client ID and Client Secret.

#The client initiates the authentication process by redirecting the user to Spotify's authorization endpoint,
# passing along their Client ID and the desired scopes (permissions). This is typically done through a user login page hosted by Spotify.

#The user logs in to their Spotify account (if not already logged in) and
# grants permission to the client application to access the requested scopes.

#After successful user consent, Spotify redirects the user back to the client application's Redirect URI,
# appending an authorization code as a query parameter.

#The client application securely exchanges the received authorization code with Spotify's token endpoint,
# along with its Client ID and Client Secret.

#In response, Spotify's token endpoint returns an access token, which the client can use to make authorized API requests on behalf of the user.
# Optionally, it may also receive a refresh token, which allows the client to obtain a new access token when the current one expires.

#There is no requirement for the client application to create a "token file" during this process.
# Instead, the client application typically stores the access token and refresh token securely in memory or in a database on the server-side.
# The tokens are used for subsequent API requests until they expire or are revoked.