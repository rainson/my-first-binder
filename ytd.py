#
from pytube import YouTube, Playlist
from youtube_transcript_api import YouTubeTranscriptApi

#
yturl = "https://www.youtube.com/watch?v=nhUKHf-GN_Y"
yt = YouTube(yturl)

yt.streams.filter(file_extension="mp4")

title = yt.title.replace(" ","")
out_dir = "/home/jovyan/ytd"
yt.streams.get_by_itag(22).download(output_path=out_dir,filename=title)


transcript_list = YouTubeTranscriptApi.list_transcripts(yt.video_id)
transcript_list

transcript = transcript_list.find_transcript(['en'])
translated_transcript = transcript.translate('zh-Hans')
zh_trans = translated_transcript.fetch()
en_trans = transcript.fetch()

#
import json


fname = "en_{}.json".format(yt.title.replace(" ",""))
with open(fname, "w") as fh:
    json.dump(en_trans, fh)
fname = "zh_{}.json".format(yt.title.replace(" ",""))
with open(fname, "w") as fh:
    json.dump(zh_trans, fh)
    
fname = "en_zh_{}.json".format(yt.title.replace(" ",""))
with open(fname, "w") as fh:
    json.dump(zh_trans+en_trans, fh)
    
#!tar -czvf ytd.tar.gz /home/jovyan/ytd
    
import seafileapi

client = seafileapi.connect('https://box.nju.edu.cn', 'KY2005901', '%1@WyEiiwtl')
repo_list = client.repos.list_repos()
for repo in repo_list:
    print(repo.name, repo.id)

repo = client.repos.get_repo('d2d11acc-32fb-43f5-b1aa-f893e9d3c719')
seafdir = repo.get_dir('/youtube_videos/others')
file = seafdir.upload_local_file('/home/jovyan/ytd.tar.gz')