import re
from mcdreforged.api.all import *

version = '1.1.0'

def on_load(server, params):
    server.logger.info('正在注册指令')
    server.register_help_message('!!skull <player>', '获取指定玩家的头颅')
    server.register_help_message('!!show', '展示自己手上的物品')

def on_info(server: ServerInterface, info: Info):
	if info.is_player and info.content.find('!!skull ') > -1:
		give_skull(server, info)
	if info.is_player and info.content == '!!show':
		player = info.player
		if server.is_rcon_running():
			data = server.rcon_query('data get entity {} SelectedItem'.format(player))
			nbt = data.lstrip(re.search(r'\w+ has the following entity data: ', data).group()).replace('"',r'\"')
			json = '[{"text":"[ShowShowWay] "},{"text":"' + player + '","color":"yellow"},{"text":" 正在展示一个物品！ "},{"text":"[点我查看]","color":"aqua","bold":"true","underlined":"true","hoverEvent":{"action":"show_item","value":"' + nbt + '"}}]'
			show_item(server, json)
		else:
			server.execute('data get entity {} SelectedItem'.format(player))
	if not info.is_player and re.match(r'\w+ has the following entity data: ', info.content) is not None:
		nbt = info.content.lstrip(re.search(r'\w+ has the following entity data: ', info.content).group()).replace('"',r'\"')
		player = re.search(r'^\w+', info.content).group()
		json = '[{"text":"[ShowShowWay] "},{"text":"' + player + '","color":"yellow"},{"text":" 正在展示一个物品！ "},{"text":"[点我查看]","color":"aqua","bold":"true","underlined":"true","hoverEvent":{"action":"show_item","value":"' + nbt + '"}}]'
		show_item(server, json)


def give_skull(server, info):
	info.cancel_send_to_server()
	owner = '{SkullOwner:"' + info.content[8:] + '"}'
	player = info.player
	message = '[ShowShowWay] 已给予你 {} 的头颅'.format(info.content[8:])
	server.logger.info('{} 请求获取 {} 的头颅'.format(player,info.content[8:]))
	server.execute('execute at {0} run give {0} minecraft:player_head{1}'.format(player,owner))
	server.reply(info, message)

def show_item(server, json):
	server.execute('tellraw @a {}'.format(json))
    server.execute('execute run playsound minecraft:entity.arrow.hit_player player @a')
