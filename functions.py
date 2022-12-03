import re
from googleapiclient.discovery import build
from yt_dlp import YoutubeDL
import datetime
import random, string
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

#download関数を定義
def download(searchword,downloadDir,isSilence):
    #動画情報を取得する関数
    def get_videos_search(keyword):
        api_key = 'AIzaSyAwbUJ2BqmHmDPLal0M6VfVRLL0xARtsNs'
        youtube = build('youtube', 'v3', developerKey=api_key)
        youtube_query = youtube.search().list(q=keyword, part='id,snippet', maxResults=1)
        youtube_res = youtube_query.execute()
        return youtube_res.get('items', [])

    #動画情報を取得し、urlへ格納
    result = get_videos_search(searchword)
    for item in result:
        if item['id']['kind'] == 'youtube#video':
            url = ('https://www.youtube.com/watch?v=' + item['id']['videoId'])
            title = (item['snippet']['title'])

    #ファッキン記号
    manukekigou = re.compile('[!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]')
    cleanedTitle = manukekigou.sub('', title)

    #動画をダウンロード
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl':  (downloadDir + cleanedTitle + '.%(ext)s'),
        'postprocessors': [
            {'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'},
            {'key': 'FFmpegMetadata'},
        ],
    }
    ydl = YoutubeDL(ydl_opts)
    ydl.extract_info(url, download=True)
    path = downloadDir + cleanedTitle + '.mp3'
    if(isSilence == 'true'):
        print('[delSilence:Start]\u0020' + searchword)
        sound = AudioSegment.from_mp3(path)
        chunks = split_on_silence(sound, min_silence_len=3000, silence_thresh=-40, keep_silence=600)
        chunksLen = len(chunks)
        musicLens = []
        for i in range(chunksLen):
            musicLens.append([i,chunks[i].duration_seconds])
        bestItem = max(musicLens)
        addSilent = AudioSegment.silent(duration=3000)
        exMusic = chunks[bestItem[0]] + addSilent
        exMusic.export(path + '_cut.mp3', format="mp3", bitrate="192k", parameters=["-vbr", "2","-ac","1"])
        os.remove(path)
        os.rename(path + '_cut.mp3', path)
        print('[delSilence:End]\u0020' + searchword)
        print('[System:End]\u0020'+searchword)
    else:
        print('[System:notice]\u0020'+searchword+' のダウンロードが完了しました')

#delSilence関数を定義

#makeDirName関数を定義
def makeDirName():
    date = datetime.datetime.now()
    def randomname(n):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=n))
    uniqueNumber = randomname(date.second)
    unique = str(date.year) + str(date.month) + str(date.day) + '_' + str(uniqueNumber)
    return unique