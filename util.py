import json
import os

from yuiChyan.config import NICKNAME

config_path = os.path.join(os.path.dirname(__file__), 'config.json')
assets_path = os.path.join(os.path.dirname(__file__), 'assets')
meanings = {
    '第一张牌': '代表过去，即已经发生的事',
    '第二张牌': '代表问题导致的局面',
    '第三张牌': '表示困难可能有的解决方法',
    '切牌': '表示问卜者的主观想法'
}


# 读取配置
async def read_config():
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config


# 生成消息
async def chain_reply(ev, chain, msg, image):
    msg = ''.join(msg)
    data = {
        'type': 'node',
        'data': {
            'name': str(NICKNAME),
            'uin': str(ev.self_id),
            'content': [
                {'type': 'text', 'data': {'text': msg}},
                {'type': 'image', 'data': {'file': image}}
            ]
        }
    }
    chain.append(data)
    return chain
