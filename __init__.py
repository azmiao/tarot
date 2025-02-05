import os
import random

from yuiChyan import YuiChyan, CQEvent
from yuiChyan.service import Service
from .util import read_config, meanings, assets_path, generate_forward_msg

sv = Service('tarot', help_cmd='塔罗牌帮助')


@sv.on_match('塔罗牌')
async def send_tarot(bot: YuiChyan, ev: CQEvent):
    cards = await read_config()
    msg_list = []
    # 随机选取四张牌
    indices = random.sample(list(cards.keys()), 4)
    for card_key in indices:
        count = indices.index(card_key)
        meaning_key = list(meanings.keys())[count]
        meaning_value = meanings[meaning_key]
        # 特殊规则：愚者有两张
        if card_key == '愚者':
            rand = random.randint(1, 2)
            image_path = os.path.join(assets_path, f'{card_key}{rand}.jpg')
        else:
            image_path = os.path.join(assets_path, f'{card_key}.jpg')
        # 获取含义 | 其中小阿卡纳分正位和逆位
        if isinstance(cards[card_key], dict):
            rand = random.choice(['正位', '逆位'])
            card_key += f'（{rand}）'
            card_value = cards[card_key][rand]
        else:
            card_value = cards[card_key]
        # 生成消息节点内容
        sv.logger.info(f'> 第{count}轮: {card_key}')
        msg_list.append(f'> {meaning_key}，{meaning_value}：\n[{card_key}] {card_value}\n[CQ:image,file=file:///{image_path}]')
    # 准备转发
    data_list = await generate_forward_msg(ev, msg_list)
    await bot.send_group_forward_msg(group_id=ev.group_id, messages=data_list)
