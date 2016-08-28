# from collections import OrderedDict
import json

'''
需要读取 crawler_movie.py 爬取得到的 movie_mine_seen.txt 片名及类型数据.

读取统计的电影数据，使用字典static_movie统计类型数量，得到数据格式如下：
    {'惊悚': 107, '悬疑': 60, '西部': 6, '恐怖': 8, '冒险': 85, '战争': 23, '爱情': 159, '奇幻': 66, '运动': 5,
    '传记': 32, '鬼怪': 1, '音乐': 13, '犯罪': 129, '喜剧': 161, '动作': 164, '家庭': 46, '同性': 11, '历史': 30,
    '武侠': 23, '歌舞': 8, '科幻': 43, '儿童': 6, '短片': 2, '灾难': 6, '剧情': 374, '动画': 41, '古装': 40, '情色': 6}
'''


def readData():
    data_list = []
    with open('movie_mine_seen.txt', 'r', encoding='utf-8') as f:
        for a_line in f:
            a_line = a_line.rstrip() # 去掉最右的回车键
            # 问题：诸如"权力的游戏 第六季         剧情 战争 奇幻 冒险"数据，'第六季'被当成类型字段了。
            a_list = a_line.split(' ') # 以空格分隔字符串，得到list数据
            b_list = a_list.copy()  # 直接赋值其实指向的是同一list
            for a_str in b_list: # 去除list中的''元素
                if a_str == '':
                    a_list.remove('')
            data_list.append(a_list)
            # print(a_list)

    return data_list


def coutTypes(all_movie_list):
    static_type = dict()
    for a_list in all_movie_list:
        for type_word in a_list[1::]:
            if type_word not in static_type.keys() and len(type_word)==2: # len(type_word)==2排除'第六季'等字段被当成类型。
                static_type[type_word] = 1
            elif len(type_word)==2:
                static_type[type_word] += 1
    return static_type


if __name__ == '__main__':

    movie_list = readData()
    # print(movie_list)

    static_movie = coutTypes(movie_list)
    print(static_movie)

    with open('static_movie.json', 'w') as f:
        json.dump(static_movie, f)

    # with open('static_movie.json', 'r') as f:
    #     a_dict = json.load(f)

    # print(a_dict)





