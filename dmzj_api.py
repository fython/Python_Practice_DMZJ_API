#!/usr/bin/env python3
# encoding: UTF8

import urllib.request
import json

'''测试常量'''
TEST_MANGA_OBJ_ID = 21202 # FGO
TEST_MANGA_CHAPTER_ID = 62777 # FGO
TEST_UID = 103487651 # 这是我的自用 uid，请务必改为自己的 uid 进行测试！谢谢
TEST_AUTHOR_ID = 10401 # FGO Author
TEST_OTHER_USER_UID = 102258057 # 老司机的 uid
TEST_AVATAR_URL = 'http%3A%2F%2Fimages.dmzj.com%2Fuser%2F44%2F45%2F44456c28bcb8dc69810cf92dc4af1839.png' # 我的测试头像

'''通用函数'''
def url_readstr(url):
    return urllib.request.urlopen(url).read().decode()

def url_postdata(requrl, data_unencoded):
    req = urllib.request.Request(url = requrl, data = urllib.parse.urlencode(data_unencoded).encode(encoding='UTF8'))
    return urllib.request.urlopen(req).read().decode()

def api_request(params, data = None):
    return url_readstr(API_HOST + params + ('' if (data == None) else ('?' + urllib.parse.urlencode(data))))

def api_post(params, data):
    return url_postdata(API_HOST + params, data)


'''接口常量'''
API_HOST = 'http://v2.api.dmzj.com' # 动漫之家 API 主机
GET_LATEST = '/latest/{type}/{page}.json' # 获取最新漫画 type: 100=全部, 0=译制漫画, 1=原创漫画
GET_RECOMMEND = '/recommend.json' # 获取首页推荐
GET_RECOMMEND_BATCH_UPDATE = '/recommend/batchUpdate' # 根据用户获取首页推荐 uid: 用户id, category_id: 分类id，详情请看调用函数
GET_TYPE_FILTER = '/rank/type_filter.json' # 获取分区列表
GET_CLASSIFY_FILTER = '/classify/filter.json' # 获取作品分类
GET_LIST_BY_CLASSIFY_FILTER = '/classify/{filter}/{sort}/{page}.json' # 获取分类下的列表 (多分类使用'-'作分隔符相连，例如'1-2-3-4') sort: 0 人气；1 更新
SUBJECT = {
    'list' : '/subject/{subject}/{page}.json', # 获取专题列表
    'info' : '/subject/{id}.json', # 获取专题信息
    'comment' : {
        'total' : '/comment/total/2/{id}.json', # 获取专题评论总数
        'list' : '/comment/2/{sort}/{id}/{page}.json', # 获取专题评论 sort: 0 人气；1 更新
        'add' : '/comment/add', # 添加专题评论 (POST)
        'agree' : '/comment/agree' # 点赞专题评论
    }
}
SUBSCRIBE = {
    'read' : '/subscribe/read', # 阅读
    'add' : '/subscribe/add', # 订阅 (POST)
    'cancel' : '/subscribe/cancel' # 退订
}
SEARCH = {
    'hot' : '/search/hot/{page}.json', # 热门搜索
    'show' : '/search/show/0/{keyword}/{page}.json' # 搜索漫画
}
GET_COMIC = '/comic/{obj_id}.json' # 获取漫画详情
GET_COMIC_RELATED = '/comic/related/{obj_id}.json' # 获取相关漫画
GET_CHAPTER = '/chapter/{obj_id}/{chapter_id}.json' # 获取章节详情
GET_CHAPTER_VIEWPOINT = '/viewPoint/{page}/{obj_id}/{chapter_id}.json' # 获取章节观点
AUTHOR = {
    'get' : '/UCenter/author/{author_id}.json' # 获取作者信息
}
USER = {
    'get' : '/UCenter/comics/{uid}.json', # 获取用户信息
    'subscribe' : '/subscribe/0/{uid}/{page}.json' # 获取用户订阅
}
COMMENT = {
    'total' : '/old/comment/total/0/{obj_id}.json', # 获取漫画评论总数
    'list' : '/old/comment/0/{sort}/{obj_id}/{page}.json', # 获取漫画评论 sort: 0 人气；1 更新
    'add' : '/old/comment/add', # 添加漫画评论 (POST)
    'agree' : '/old/comment/agree' # 点赞漫画评论
}

'''接口'''
def latest_get(page, type = 100):
    return api_request(GET_LATEST.format(type = type, page = page))

def recommend_get():
    return api_request(GET_RECOMMEND)

def recommend_get_by_uid(uid, category_id):
    #category_id: 46 大图推荐(Banner); 47 近期必看; 48 火热专题; 49 我的订阅; 50 猜你喜欢; 51 大师级作者怎能不看; 52 国漫也精彩; 53 美漫大事件; 54 热门连载; 55 条漫专区
    return api_request(GET_RECOMMEND_BATCH_UPDATE, {'uid':uid, 'category_id':category_id})

def type_filter_get():
    return api_request(GET_TYPE_FILTER)

def classify_filter_get():
    return api_request(GET_CLASSIFY_FILTER)

def list_get_by_classify_filter(filter, sort, page = 0):
    return api_request(GET_LIST_BY_CLASSIFY_FILTER.format(filter = filter, sort = sort, page = page))

def subject_get(page, subject = 0):
    return api_request(SUBJECT['list'].format(subject = subject, page = page))

def subject_info_get(id):
    return api_request(SUBJECT['info'].format(id = id))

def subject_comment_total(id):
    return api_request(SUBJECT['comment']['total'].format(id = id))

def subject_comment_list(id, sort, page = 0):
    return api_request(SUBJECT['comment']['list'].format(id = id, sort = sort, page = page))

def subject_comment_add(id, sender_uid, content, to_comment_id = 0, to_uid = 0, origin_comment_id = 0, type = 2):
    return api_post(SUBJECT['comment']['add'], {
        'obj_id':id, 'to_comment_id':to_comment_id, 'to_uid':to_uid, 'origin_comment_id': origin_comment_id,
        'sender_uid':sender_uid, 'type':type, 'content':content
    })

def subject_comment_agree(id, comment_id, type = 2):
    return api_request(SUBJECT['comment']['agree'], {'obj_id':id, 'comment_id':comment_id, 'type':type})

def subscribe_read(obj_id, uid):
    return api_request(SUBSCRIBE['read'], {'obj_id':obj_id, 'uid':uid, 'type':'mh'})

def subscribe_add(obj_id, uid):
    return api_post(SUBSCRIBE['add'], {'obj_ids':obj_id, 'uid':uid, 'type':'mh'})

def subscribe_cancel(obj_id, uid):
    return api_request(SUBSCRIBE['cancel'], {'obj_ids':obj_id, 'uid':uid, 'type':'mh'})

def search_hot(page = 0):
    return api_request(SEARCH['hot'].format(page = page))

def search_show(keyword, page = 0):
    return api_request(SEARCH['show'].format(keyword = keyword, page = page))

def comic_get(obj_id):
    return api_request(GET_COMIC.format(obj_id = obj_id))

def comic_related(obj_id):
    return api_request(GET_COMIC_RELATED.format(obj_id = obj_id))

def comic_total_comments(obj_id):
    return api_request(COMMENT['total'].format(obj_id = obj_id))

def comic_comments_get(obj_id, sort, page = 0):
    return api_request(COMMENT['list'].format(sort = sort, obj_id = obj_id, page = page))

def comic_comments_add(uid, avatar_url, nickname, obj_id, content, to_comment_id = 0, author = '', to_uid = 0, pid = 0, author_id = '', type = 0):
    return api_post(COMMENT['add'], {
        'uid':uid, 'obj_id':obj_id, 'avatar_url':avatar_url, 'to_comment_id':to_comment_id,
        'author':author, 'to_uid':to_uid, 'nickname':nickname, 'pid':pid,
        'author_id':author_id, 'type':type, 'content':content
        })

def comic_comments_agree(obj_id, comment_id, type = 0):
    return api_request(COMMENT['agree'], {'obj_id':obj_id, 'comment_id':comment_id, 'type':type})

def chapter_get(obj_id, chapter_id):
    return api_request(GET_CHAPTER.format(obj_id = obj_id, chapter_id = chapter_id))

def chapter_view_point_get(obj_id, chapter_id, page = 0):
    return api_request(GET_CHAPTER_VIEWPOINT.format(page = page, obj_id = obj_id, chapter_id = chapter_id))

def ucenter_author_get(author_id):
    return api_request(AUTHOR['get'].format(author_id = author_id))

def ucenter_user_get(uid):
    return api_request(USER['get'].format(uid = uid))

def ucenter_user_subscribe_list(uid, page = 0):
    return api_request(USER['subscribe'].format(uid = uid, page = page))

'''Main'''
def main():
    choice = input('选择你想要测试的接口，参数请看源码:')

    if choice == '0':
        print(latest_get(input('【查看最新漫画】输入页码：'), input('输入类型（100=全部, 0=译制漫画, 1=原创漫画）：')))
    if choice == '1':
        print('【获取推荐】' + recommend_get())
    if choice == '2':
        print('【查看热门搜索】' + search_hot())
    if choice == '3':
        print(search_show(input('【搜索漫画】关键词：')))
    if choice == '4':
        print(comic_get(input('【获取漫画详情】漫画编号：')))
    if choice == '5':
        print(chapter_get(input('【获取漫画章节】漫画编号：'), input('章节编号：')))
    if choice == '6':
        print(chapter_view_point_get(input('【获取章节观点】漫画编号：'), input('章节编号：')))
    if choice == '7':
        print(comic_related(input('【获取相关漫画】原漫画编号：')))
    if choice == '8':
        print('【获取分区列表】' + type_filter_get())
    if choice == '9':
        print('【获取作品分类】' + classify_filter_get())
    if choice == '10':
        print(list_get_by_classify_filter(input('【获取分类下的作品列表】分类：'), input('0、人气，1、更新：'), input('页码：')))
    if choice == '11':
        print(comic_total_comments(input('【获取漫画评论总数】漫画编号：')))
    if choice == '12':
        print(comic_comments_get(input('【获取漫画评论】漫画编号：'), input('0、人气，1、更新：'), input('页码：')))
    if choice == '13':
        print(comic_comments_add(uid = input('【添加漫画评论】请输入你的用户id：'), nickname = input('请输入你的用户昵称：'), obj_id = input('请输入要评论的漫画编号：'),
        avatar_url = input('请输入你的头像地址：'), content = input('请输入评论内容：')))
    if choice == '14':
        print(comic_comments_agree(input('【点赞漫画评论】请输入漫画编号：'), input('请输入评论编号：')))
    if choice == '15':
        print(recommend_get_by_uid(input('【根据用户获取推荐】用户id：'), input('分类id：')))
    if choice == '16':
        print(subject_get(input('【获取专题】页码：'), input('专题类型：')))
    if choice == '17':
        print(subject_info_get(input('【获取专题信息】专题编号：')))
    if choice == '18':
        print(subject_comment_total(input('【获取专题评论总数】专题编号：')))
    if choice == '19':
        print(subject_comment_list(input('【获取专题评论列表】专题编号'), input('0、人气，1、更新：'), input('页码：')))
    if choice == '20':
        print(subject_comment_add(sender_uid = input('【添加专题评论】请输入你的用户id：'), id = input('请输入要评论的专题编号：'), content = input('请输入评论内容：')))
    if choice == '21':
        print(subject_comment_agree(input('【点赞专题评论】请输入专题编号：'), input('请输入评论编号：')))
    if choice == '100':
        print(ucenter_author_get(input('【获取作者】作者编号：')))
    if choice == '101':
        print(ucenter_user_get(input('【获取用户】用户编号：')))
    if choice == '102':
        print(ucenter_user_subscribe_list(input('【获取用户的订阅】用户编号：'), input('页码：')))
    if choice == '1000':
        print('【模拟点击漫画】' + subscribe_read(TEST_MANGA_OBJ_ID, TEST_UID))
    if choice == '1001':
        print('【订阅漫画】' + subscribe_add(TEST_MANGA_OBJ_ID, TEST_UID))
    if choice == '1002':
        print('【退订漫画】' + subscribe_cancel(TEST_MANGA_OBJ_ID, TEST_UID))

if __name__ == '__main__':
    main()
