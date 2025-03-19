import requests
import csv

def GetResponse(url, data):
    # 模拟浏览器
    headers = {
        "Cookie": "buvid3=3371E7F1-C48F-8D12-AEA2-250552CC34AD86923infoc; buvid_fp=a250987cbdd4a883921635bec53d4a61; PVID=1; b_nut=100; _uuid=C75A74910-A339-168F-9B7D-D5CF1111010B8704810infoc; header_theme_version=CLOSE; enable_web_push=DISABLE; enable_feed_channel=ENABLE; home_feed_column=5; browser_resolution=1659-808; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDI1Njg2MDYsImlhdCI6MTc0MjMwOTM0NiwicGx0IjotMX0.C08zR5Mf8XgxKVzEe4EFR9_z-EQ-oQWSkH1XhJjdD3k; bili_ticket_expires=1742568546; rpdid=|(um~JRll~um0J'u~RkJ|mRuY; buvid4=409E1824-0073-291B-7BC1-EB30CB0C9CEF87857-022101111-e9zSllVrEGxzXMYqGnp%2BpQ%3D%3D; SESSDATA=7ae1a362%2C1757861476%2Cf2819%2A31CjCyul_UiGAJVrEnTrl6UhwgxIZDp36vu0hl_7qFi_TY06bV-j1JyhU5k_YWLOPP0lYSVnJqT19SdVJpZE92eGlXT2pLV0ZjWkhMMWZ3S2xFWGZobDdKQzNhZjk5ck41OU1rdjR5dEw3YjBGRzc4dlkyRVNDZuEU; bili_jct=fb212dc42e7314aa89f6bd4f45fb8511; DedeUserID=1854538731; DedeUserID__ckMd5=8e6255c34dacdaac; sid=4n88xzr3; bp_t_offset_1854538731=1045739659432296448; b_lsid=94FDED1C_195AC27797A; bsource=search_baidu; CURRENT_FNVAL=4048",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 SLBrowser/9.0.6.2081 SLBChan/105 SLBVPV/64-bit",
        "Referer": "https://www.bilibili.com/bangumi/play/ss12548?from_spmid=666.23.0.0"
    }
    # 发送请求
    response = requests.get(url=url, params=data, headers=headers)
    # 返回响应对象
    return response

# 获取评论数据内容
def GetContent():
    link = 'https://api.bilibili.com/x/v2/reply/wbi/main'
    params = {
        'oid': '21071819',
        'type': '1',
        'mode': '2',
        'pagination_str': '{"offset":""}',
        'plat': '1',
        'seek_rpid': '',
        'web_location': '1315875',
        'w_rid': '1b121e8c81cf00b43a891e28c5bcd789',
        'wts': '1742350180'
    }
    # 调用发送请求的函数
    response = GetResponse(url=link, data=params)

    # 获取响应json数据内容
    JsonData = response.json()
    # 解析数据
    # 根据字典取值，提取评论数据所在列表
    replies = JsonData.get('data', {}).get('replies', [])
    info_list = []
    for index in replies:
        # 提取数据
        dit = {
            '昵称': index['member']['uname'],
            '性别': index['member']['sex'],
            '地区': index.get('reply_control', {}).get('location', '').replace('IP属地：', ''),
            '评论': index['content']['message'],
        }
        info_list.append(dit)
    return info_list

if __name__ == '__main__':
    f = open('让子弹飞-评论2.csv', mode='w', encoding='utf-8-sig', newline='')
    csv_writer = csv.DictWriter(f, fieldnames=['昵称', '性别', '地区', '评论'])
    csv_writer.writeheader()
    info_list = GetContent()
    csv_writer.writerows(info_list)
    f.close()