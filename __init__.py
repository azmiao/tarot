import os
import random
from random import shuffle, randint

from yuiChyan.service import Service
from .util import read_config, meanings, assets_path, chain_reply

sv = Service('tarot', help_cmd='塔罗牌帮助')


@sv.on_match('塔罗牌')
async def send_playerInfo(bot, ev):
    await bot.send(ev, '请稍等，正在洗牌中')
    cards = await read_config()

    indices = random.sample(range(1, 78), 4)
    card_keys = list(cards.keys())
    shuffle(card_keys)
    chain = []
    for count in range(4):
        sv.logger.info(f'第{count}轮')
        index = int(indices[count])
        card_key = card_keys[index - 1]
        meaning_key = list(meanings.keys())[count]
        meaning_value = meanings[meaning_key]
        img_path = os.path.join(assets_path, f'{card_key}.jpg')
        image_file = f'file:///{img_path}'

        # 特殊规则：愚者有两张
        if card_key == '愚者':
            rand = randint(1, 2)
            rand_path = os.path.join(assets_path, f'{card_key}{rand}.jpg')
            image_file = f'file:///{rand_path}'

        # 特殊规则：小阿卡纳分正位逆位
        if isinstance(cards[card_key], dict):
            rand = randint(1, 2)
            if rand == 1:
                card_value = cards[card_key]['正位']
                card_key += '（正位）'
            else:
                card_value = cards[card_key]['逆位']
                card_key += '（逆位）'
        else:
            card_value = cards[card_key]

        msg = []
        msg.extend([meaning_key, '，', meaning_value, '\n', card_key, '，', card_value, '\n'])
        if count <= 3:
            await chain_reply(ev, chain, msg, image_file)
        if count == 3:
            await bot.send_group_forward_msg(group_id=ev['group_id'], messages=chain)
