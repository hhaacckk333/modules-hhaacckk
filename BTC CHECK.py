from .. import loader, utils
from telethon import types, TelegramClient

import re


@loader.tds
class YourMod(loader.Module):
    """Привет"""

    strings = {"name": "BTC"}
    bot_ids = [159405177]

    async def client_ready(self, client, db):
        self.client: TelegramClient = client
        self.db = db
        self.logs = []

    async def btclogscmd(self, m):
        await utils.answer(m, "/n".join(self.logs or ["логов нет чел"]))

    async def watcher(self, message):
        if not isinstance(message, types.Message):
            return
        
        try:
            user_mess = message.raw_text
            if message.out or message.from_id in self.bot_ids:
                return  # свои сообщения не ловим, это бессмысленно))

            if re.search(r'BTC_CHANGE_BOT\?start=', user_mess):
                m = re.search(r'c_\S+', user_mess)
                await self.client.send_message('BTC_CHANGE_BOT', '/start ' + m.group(0))

                self.logs.append(m.group(0))

        except:
            raise
