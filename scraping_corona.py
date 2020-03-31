import requests
from bs4 import BeautifulSoup

#探すサイト(　--https://www.mhlw.go.jp/stf/houdou/houdou_list_202003.html--　)

# 新型コロナウイルス感染症の現在の状況と厚生労働省の対応について（令和2年3月26日版）
url = 'https://www.mhlw.go.jp/stf/newpage_10465.html'

#都道府県のナンバリング
prefectures_directory = {
    '北海道':1,
    '青森県':2,
    '岩手県':3,
    '宮城県':4,
    '秋田県':5,
    '山形県':6,
    '福島県':7,
    '茨城県':8,
    '栃木県':9,
    '群馬県':10,
    '埼玉県':11,
    '千葉県':12,
    '東京都':13,
    '神奈川県':14,
    '新潟県':15,
    '富山県':16,
    '石川県':17,
    '福井県':18,
    '山梨県':19,
    '長野県':20,
    '岐阜県':21,
    '静岡県':22,
    '愛知県':23,
    '三重県':24,
    '滋賀県':25,
    '京都府':26,
    '大阪府':27,
    '兵庫県':28,
    '奈良県':29,
    '和歌山県':30,
    '鳥取県':31,
    '島根県':32,
    '岡山県':33,
    '広島県':34,
    '山口県':35,
    '徳島県':36,
    '香川県':37,
    '愛媛県':38,
    '高知県':39,
    '福岡県':40,
    '佐賀県':41,
    '長崎県':42,
    '熊本県':43,
    '大分県':44,
    '宮崎県':45,
    '鹿児島県':46,
    '沖縄県':47
}

def get_colona_data():
    r = requests.get(url)#指定したURLの情報を入手
    if r.status_code == requests.codes.ok:#正しくアクセスができたかチェック
        soup = BeautifulSoup(r.content, 'html.parser')#HTML情報を解析する
        #取得したHTML情報のtableのth td情報を取得する。
        data = [[[td.get_text(strip=True) for td in trs.select('th, td')]
                 for trs in tables.select('tr')]
                for tables in soup.select('table')]

        #１行目がアナウンス・対策情報
        announce_data = data[0]

        #2行目が国別の感染者数のデータ
        country_corona_data = data[1]

        #3行目が国内の感染者数データ　['都道府県名', '患者数', '現在は入院等', '退院者', '死亡者']
        japan_corona_data = data[2]

        print(announce_data)
        print(country_corona_data)
        print(japan_corona_data)

        japan_corona_data_true = []#都道府県のみのデータ
        max_patient_num = max([int(japan_data[1]) for japan_data in japan_corona_data[1:-1]])

        def hex_color_change(patient_num):#患者数から色を情報を取得する
            ratio = patient_num / max_patient_num * 255
            hex_data = hex(int(ratio))[2:]
            if len(hex_data) == 1:
                str_hex_data = "#0"+str(hex_data) + "0000"
            else:
                str_hex_data = "#" + str(hex_data) + "0000"
            return str_hex_data

        for japan_data in japan_corona_data[1:-1]:
            prefectures = japan_data[0]#都道府県名
            code_num = prefectures_directory[prefectures]#都道県から都道府県番号を取得
            code_id = "pref_"+str(code_num)#都道府県番号から指定するIDを記述
            patient_num = int(japan_data[1])#患者数
            hospitalized_num = int(japan_data[2])#入院数
            end_hospitalized_num = int(japan_data[3])#退院数
            dead_num = int(japan_data[4])#死者数
            hex_data = hex_color_change(patient_num)#患者数から色を変更
            jd = {
                "prefectures": prefectures,
                "code_num:": code_num,
                "code_id": code_id,
                "patient_num": patient_num,
                "hospitalized_num": hospitalized_num,
                "end_hospitalized_num": end_hospitalized_num,
                "dead_num": dead_num,
                "hex_data": hex_data
            }
            japan_corona_data_true.append(jd)

        return japan_corona_data_true

#確認用
#jcd = get_colona_data()
#print(jcd)