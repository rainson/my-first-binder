def getVideo(url):
    print 'Downloading. video..%s'%url
    key = hashlib.sha1(os.urandom(24)).hexdigest() + ".mp4"
    try:
        yt=YouTube(url)
        video = yt.filter('mp4')[-1]
        video.download(base_url)
        qiniu_video(key,video.filename+'.mp4')
    except:
        print('Downloading. video. error.%s' % url)
