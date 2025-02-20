import time
import os
import qbittorrentapi

# pip3 install qbittorrent-api
# 连接到qBittorrent客户端的登录功能


# 从环境变量中读取配置
host = os.getenv('QBITTORRENT_HOST', 'http://192.168.1.121:3000')  # 默认值可以根据需要修改
username = os.getenv('QBITTORRENT_USERNAME', 'user')  # 默认用户名
password = os.getenv('QBITTORRENT_PASSWORD', 'XXXXXX')  # 默认密码


def login_qbittorrent(host, username, password):
    print("==========================================================")
    print(f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    qb = qbittorrentapi.Client(host=host, username=username, password=password)
    try:
        qb.auth_log_in()
        print("Login successful!")
        return qb
    except qbittorrentapi.exceptions.LoginFailed as e:
        print(f"Login failed: {e}")
        exit(1)

def deleteTorrent(qb, torrent_hash):
    # 尝试删除种子及其相关文件
    qb.torrents_delete(
        torrent_hashes=[torrent_hash],  # 传递哈希值列表
        delete_files=True  # 设置为 True 删除文件
    )



def willDelete(torrent):
    # 打印 torrent 的所有属性（调试时查看）
    # for key, value in torrent.items():
    #     print(f"{key}: {value}")
    
    # 从字典中提取必要的字段
    name = torrent.get('name', 0)
    category = torrent.get('category', '')
    seeding_time = torrent.get('seeding_time', 0)
    status = torrent.get('state', '')  # 状态
    added_on = torrent.get('added_on', 0)
    progress = torrent.get('progress', 0)
    ratio = torrent.get('ratio', 0)
    uploaded = torrent.get('uploaded', 0)
    upspeed = torrent.get('upspeed', 0)
    
    
    # print('种子名称 name:', name)
    # print('自定义分类 category:', category)
    # print('做种时间 seeding_time:', seeding_time)
    # print('状态 status:', status)
    # print('加入时间 added_on:', added_on)
    # print('进度 progress:', progress)
    # print('上传比例 ratio:', ratio)
    # print('已上传 uploaded:', uploaded)
    # print('上传速度 upspeed:', upspeed)



    # 判断删除条件：
    # 1. 删除条件1: 种子在 'DelAfterDownload' 类别中,并且做种时间大于 1小时
    if category == 'DelAfterDownload' and seeding_time > 3600:  # 3600秒 = 1小时
        return True
    
    # 2. 删除条件2: 如果上传速度>50k，或者种子处于停止状态，或者种子在 'NoDel' 类别中
    if upspeed > 50 * 1024 or status == 'stoppedUP' or category == 'NoDel':  # 假设 stalledUP 表示暂停
        return False
    
    # 3. 删除条件3: 如果做种时间大于 30分钟（1800秒）
    elif seeding_time > 1800:  # 0.5h
        return True
    
    # 4. 删除条件4: 如果种子添加超过 4 小时
    elif time.time() - added_on > 3600 * 4:  # 4h
        return True
    
    else:
        return False



def main():
    # 使用提取的登录函数
    qb = login_qbittorrent(host, username, password)

    # 获取所有种子
    try:
        torrents = qb.torrents_info()
    except Exception as e:
        print(f"Error retrieving torrents: {e}")
        return

    for torrent in torrents:
        if willDelete(torrent):
            print(f"删除 | {torrent.get('name', 'Unknown')}")
            deleteTorrent(qb, torrent.get('hash', 'Unknown')) 
        else:
            print(f"保留 | {torrent.get('name', 'Unknown')}")

if __name__ == '__main__':
    main()
