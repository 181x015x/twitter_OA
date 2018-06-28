from django.http import HttpResponse
from django.shortcuts import render
from social_django.models import UserSocialAuth
from django.contrib.auth.decorators import login_required
from requests_oauthlib import OAuth1Session
import json
from twitter.models import Userinfo

def index(request):
    #return HttpResponse("Hello, world")
    return render(request,
                  'twitter/index.html')


'''
ログイン後、top_pageが実行される

'''

@login_required
def top_page(request):
    user = UserSocialAuth.objects.get(user_id=request.user.id)

    oa = oauth(user) #OA認証
    status = getUserInfo(oa) #最新のユーザーの情報を取得
    point = calcStatuses(user,status) #前回の情報から最新の情報の引き算

    length = 0
    if (point != -1):  # 前回から変動があれば
        if (point[3] > 0):
            timeline = getUserTimeLine(oa, point[3])  # 変動分のタイムラインの取得
            length = countTxtLength(timeline)  # 変動分のタイムライン上のテキストの数を計算


    createData(user,status,length) #最新の状況をデータベースに登録

    g = Userinfo.objects.get(oauth_token=user.access_token['oauth_token'])


    return render(request,'twitter/top.html',
                  {'user': user,
                   'length':length,
                   'g': g,
                   })




'''
updateStatusを1日1回実行することにより、情報を更新する。
引数userは更新対象のoauth_tokenとoauth_token_secretの入ったリスト
'''

def updateStatus(user):
    oa = OAuth1Session('xaxV7qRjhMtjf8NwFMQ0P8FpP', 'HwFGWy2lft23akAy0QjFqPGQsHJkpFXqrfehC8MtZowND8pG6B', user[0], user[1])  # OA認証
    status = getUserInfo(oa)  # 最新のユーザーの情報を取得
    point = calcStatuses(user, status)  # 前回の情報から最新の情報の引き算

    length = 0
    if (point != -1):  # 前回から変動があれば
        if (point[3] > 0):
            timeline = getUserTimeLine(oa, point[3])  # 変動分のタイムラインの取得
            length = countTxtLength(timeline)  # 変動分のタイムライン上のテキストの数を計算

    createData(user, status, length)  # 最新の状況をデータベースに登録






#OA認証を行う
def oauth(user):
    AT = user.access_token['oauth_token']
    ATS = user.access_token['oauth_token_secret']
    CK = 'xaxV7qRjhMtjf8NwFMQ0P8FpP'
    CS = 'HwFGWy2lft23akAy0QjFqPGQsHJkpFXqrfehC8MtZowND8pG6B'
    twitter = OAuth1Session(CK, CS, AT, ATS)

    return twitter


#最新のユーザのfav数,ツイート数,followe数,followers数を計算する
def getUserInfo(twitter):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"  # タイムライン取得エンドポイント
    params = {'count': 1}  # 取得数
    res = twitter.get(url, params=params)

    followers_count = 0
    friends_count = 0
    favourites_count = 0
    statuses_count = 0

    if res.status_code == 200:  # 正常通信出来た場合
        timelines = json.loads(res.text)

        for line in timelines:

            followers_count = int(line['user']['followers_count'])
            friends_count = int(line['user']['friends_count'])
            favourites_count = int(line['user']['favourites_count'])
            statuses_count = int(line['user']['statuses_count'])

        return followers_count, friends_count, favourites_count, statuses_count

    else:  # 正常通信出来なかった場合
        print("Failed: %d" % res.status_code)
        return -1


#どっかで今日ー昨日のツイート数を計算して下の関数のparamsに入れる

#userのタイムラインを取得する
def getUserTimeLine(twitter,point):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"  # タイムライン取得エンドポイント
    params = {'count': point}  # 取得数
    res = twitter.get(url, params=params)

    if res.status_code == 200:  # 正常通信出来た場合
        timelines = json.loads(res.text)  # レスポンスからタイムラインリストを取得
        return timelines
    else:  # 正常通信出来なかった場合
        print("Failed: %d" % res.status_code)
        return -1


#タイムラインからその日の日付のツイート文字数を計算
def countTxtLength(timeline):

    length = 0

    for line in timeline:
        length = length + len(line['text'])

    return length


#データベースにツイート数などを登録する
def createData(token,val,length):

    try:
        g = Userinfo.objects.get(oauth_token=token.access_token['oauth_token'])
        g.followers_count = val[0]
        g.friends_count = val[1]
        g.favourites_count = val[2]
        g.statuses_count = val[3]
        g.total_point = g.total_point + length
        g.save()

    except:
        Userinfo.objects.create(oauth_token=token.access_token['oauth_token'],
                                oauth_token_secret=token.access_token['oauth_token_secret'],
                                followers_count=val[0],
                                friends_count=val[1],
                                favourites_count=val[2],
                                statuses_count=val[3],
                                total_point=0,
                                )



#前回登録時との差分を計算する.
def calcStatuses(token,status):

    try:
        g = Userinfo.objects.get(oauth_token=token.access_token['oauth_token'])

        #前回のデータベースにあるユーザ情報と最新のユーザ情報の引き算を行う
        a = status[0] - g.followers_count
        b = status[1] - g.friends_count
        c = status[2] - g.favourites_count
        d = status[3] - g.statuses_count

        return a, b, c, d

    except:
        print("A new host")
        return -1