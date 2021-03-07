from ipywebrtc import VideoStream
from pytube import YouTube

video = YouTube('https://www.youtube.com/watch?v=NqC_1GuY3dw')

video.streams.all()

video.streams.get_by_itag(18).download()
# video2 = VideoStream.from_url("./Game Boy Longplay [009] Mega Man Dr Wilys Revenge.mp4")
# video2
