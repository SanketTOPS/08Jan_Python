from pytubefix import YouTube

url="https://www.youtube.com/watch?v=ATyjL5M4ljo"

YouTube(url).streams.first().download()