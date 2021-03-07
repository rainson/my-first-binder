# encoding=utf-8
import json
import re
from urlparse import urljoin
from pytube import YouTube
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from videos2.items import VideoItem
from videos2.util import getImage,getVideo
class VideoSiper(scrapy.Spider):
    name = 'video-youtube'
 
    def parse(self, response):
        sel = response.selector
        self.parse_video_list(response)
        for href in sel.xpath('//div[contains(@class,"branded-page-box")]/a/@href').extract():
            yield Request(url=urljoin(response.url, href), callback=self.parse_video_list)
    def start_requests(self):
        url ='https://www.youtube.com/results?search_query=%E6%97%85%E8%A1%8C'
        yield Request(url=url)
    ##列表页
    def parse_video_list(self,response):
        sel=response.selector
        #sel2=response.selector
        tmp1=sel.xpath('//ol[contains(@class,"item-section")]/li//a[contains(@class,"yt-uix-tile-link")]/@href').extract()
        tmp2=sel.xpath('//ol[contains(@class,"item-section")]/li//div[contains(@class,"yt-thumb")]//span[contains(@class,"video-time")]/text()').extract()
        for (href,length) in zip(tmp1,tmp2):
            yield  Request(url=urljoin(response.url,href),callback=self.parse_video_url,meta={"length":length})
    ##详情页
    def parse_video_url(self,response):
        sel =response.selector
        meta = response.meta
        url =response.url
        try :
            #yt
            tmp=sel.xpath('//div[contains(@id,"watch7-content")]')
        except:
            self.logger.warning('Invalid response: %s' % response.url)
            self.logger.warning(response.body)
 
        content=tmp.xpath('//meta[contains(@itemprop,"name")]/@content').extract()[0]
        videoPlayTimes=meta['length']
 
        user=sel.xpath('//div[contains(@id,"watch7-user-header")]//span[contains(@class,"yt-thumb-clip")]//img/@alt').extract()[0]
        time=sel.xpath('//meta[contains(@itemprop,"datePublished")]/@content').extract()[0]
        ShowImg=sel.xpath('//link[contains(@itemprop,"thumbnailUrl")]/@href').extract()
        realvideo1=getVideo(url)
        ###装配数据
        videoItem=VideoItem()
        videoItem['content']=content
        videoItem['user']=user
        videoItem['source']='youtube'
        videoItem['types']='video'
        videoItem['time']=time
        videoItem['ShowImg']=ShowImg
        videoItem['realvideo1']=realvideo1
        videoItem['videoPlayTimes']=videoPlayTimes
        videoItem['url']=response.url
        tmpUrl=url.replace('wacth','get_endscreen')
        yield Request(url=tmpUrl,callback=self.parse_avatar,meta={'item':videoItem})
        ##搜索相关详情视频
        for href in sel.xpath('//li[contains(@class,"video-list-item")]//a/@href').extract():
            yield Request(url=urljoin(response.url,href),callback=self.parse_video_url)
 
    def parse_avatar(self,response):
        html_text = json.loads(response.body[4:])['payload']['list_html']
        meta = response.meta
        videoItem = response.meta.get('item', VideoItem())
        user_avatar_old=html_text['elements'][0]['endscreenElementRenderer']['image']['thumbnails'][0]['url']
        user_avatar= getImage(user_avatar_old)
        videoItem['user_avatar']=user_avatar
        videoItem['user_avatar_old']=user_avatar_old
        yield videoItem
