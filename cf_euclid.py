#! /usr/bin/env python
# -*- coding:utf-8 -*-\
from math import sqrt


#それぞれの人が見た映画とその評価点
dataset={
 'teppei': {
 'ジュラシックパーク': 3.0, 'ロストワールド': 3.5, 'ジュラシックパーク３':4.0
  },
 'suzuki': {
 'ジュラシックパーク': 3.0, 'ジュラシックワールド炎の王国':3.5, 'ジュラシックワールド': 3.5,'バックトゥザフューチャー':3.5
 },
 'seita': {
 'バックトゥザフューチャー': 1.5, 'ジュラシックパーク': 3.0
 },
 'satou': {
 'バックトゥザフューチャー': 4.0, 'ET': 5.0,'メリーポピンズ':4.0
 }
}


#二人の間の類似度をとる
def get_sim(person1, person2):
    set_person1 = set(dataset[person1].keys())
    set_person2 = set(dataset[person2].keys())
    both = set_person1.intersection(set_person2)

    if len(both)==0:
        return 0

    #ユークリッド距離
    list_des = [pow(dataset[person1][item]-dataset[person2][item], 2) for item in both]
    return 1/(1+sqrt(sum(list_des)))


def recommend(person, top_n):

    totals = {}
    sim_sum = {}
    # 自分以外のユーザのリストを取得してループ
    list_others = list(dataset.keys())
    list_others.remove(person)

    for other in list_others:

        #他の人が見てる映画取得
        set_other = set(dataset[other])
        #自分が見ている映画
        set_person = set(dataset[person])
        #set_otherにしか含まれないものを取得
        set_new_movie = set_other.difference(set_person)
        # あるユーザと本人の類似度を計算(simは0~1の数字)
        sim = get_sim(person, other)

        for item in set_new_movie:

            # "類似度 x レビュー点数" を推薦度のスコアにする
            totals.setdefault(item,0)
            totals[item] += dataset[other][item]*sim

            # またユーザの類似度の積算値をとっておき、これで上記のスコアを除する
            sim_sum.setdefault(item,0)
            sim_sum[item] += sim

    #0になってしまうものを除去
    last_total = {}
    for k,v in totals.items():
        if v != 0.0:
            last_total[k] = v

    #重みの合計/類似性の合計で正規化するらしい
    rankings = [(total/sim_sum[item],item) for item,total in last_total.items()]
    rankings.sort()
    rankings.reverse()

    return [i[1] for i in rankings][:top_n]


print("哲平さんへのおすすめ")
rec1 = recommend("teppei",5)
print(rec1)

print("鈴木さんへのおすすめ")
rec2 = recommend("suzuki",5)
print(rec2)

print("清田さんへのおすすめ")
rec3 = recommend("seita",5)
print(rec3
)
print("佐藤さんへのおすすめ")
rec4 = recommend("satou",5)
print(rec4)
