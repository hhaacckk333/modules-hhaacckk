# by hhaacckk 2021

from .. import loader, utils
import requests
import re
def getcontent(query):
		link = f"https://www.kinopoisk.ru/s/type/film/find/{query.replace(' ','+')}"
		return str(requests.get(link).content)

def getkinopoiskid(message, query):
	#try:
		#await message.reply(getcontent(f"{query} кинопоиск"))
	print(query)
	cont = getcontent(query)
	try:
		return re.findall(r'/film/([0-9]+?)/sr/1/',cont)[0]
	except:
		return None	
	#except Exception as:
		#print(
def getlink(message, query=None, id=None):
	if query == None:
		return f"Ваша ссылка на фильм, приятного просмотра: http://sergatv.github.io/Kinopoisk-Watch/?id={int(id)}\nhttps://ww1.flink.su/film/{result}/ (если верхняя не работает)\n"
	elif id == None:
		result = getkinopoiskid(message, query)
		
		if result != None:
			return f"Ваша ссылка на фильм, приятного просмотра: http://sergatv.github.io/Kinopoisk-Watch/?id={int(result)}\nhttps://ww1.flink.su/film/{result}/ (если верхняя не работает)\nЕсли это не то, что вы искали, попробуйте указать год выпуска фильма."
		else:
			return "Не найдено! Попробуйте вставить сразу айди!"

class kinopososososMod(loader.Module):
	"""Ссылка на просмотр фильма из кинопоиска"""

	strings = {'name': 'VIP Кинопоиск'}
	
	def __init__(self):
		self.name = self.strings['name']

	async def client_ready(self, client, db):
		self.db = db
		self.client = client
	


	async def kinoidcmd(self, message):
		""""Ищет фильм по айди и возвращает ссылку. Использование пример: .kinoid 260991"""
		args = utils.get_args_raw(message)
		try:
			int(args)
		except:
			await message.edit("Неправильный id!")
			return
		answer = getlink(message, id=args)
		await message.edit(answer, parse_mode="HTML")
	async def kinosearcmd(self, message):
		"""Ищет фильм по аргументу в гугле и если нашел то возвращает ссылку. Использование пример: .kinosear @hhaacckk1 :D"""
		args = utils.get_args_raw(message)
		answer = getlink(message, query=args)
		await message.edit(answer, parse_mode="HTML")