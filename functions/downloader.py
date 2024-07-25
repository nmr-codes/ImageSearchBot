from pytube import YouTube

class Downloader:
    def __init__(self, link):
      self.link = link
    
    def download(self):
      youtubeObject = YouTube(self.link)
      title = youtubeObject.title
      youtubeObject = youtubeObject.streams.get_highest_resolution()
      try:
          youtubeObject.download()
      except:
          print("An error has occurred")
      print("Download is completed successfully")
    