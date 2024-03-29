# Based on 404 source code
# 404
# 404

# for more info: 404
# by 404, 2023

# meta developer: @hhaacckk1

from .. import loader, utils
import requests


class EyeCheckerTGMod(loader.Module):
    """GBSLIV v1.2"""
    strings = {
        'name': 'GBSLIV',
        'check': '[EZHG] Делаем запрос к API...',
        'version': '1.2.1'
    }

    def __init__(self):
        self.name = self.strings['name']
        self._me = None
        self._ratelimit = []

    async def client_ready(self, client, db):
        self._db = db
        self._client = client

    async def checkcmd(self, m):
        """ Проверить uid на номер
Отправляет данные в чат
Жуёт либо <reply>, либо <uid>"""
        await check(m, self.strings['check'], self.strings['version'])

    async def pcheckcmd(self, m):
        """ Проверить номер на наличие в бд
Отправляет данные в чат
Жуёт либо <reply>, либо <phone>"""
        await check(m, self.strings['check'], self.strings['version'], 'p')

    async def scheckcmd(self, m):
        """ Аналогично check
Отправляет данные в избранное
Жуёт либо <reply>, либо <uid>"""
        await check(m, self.strings['check'], self.strings['version'], save=True)

    async def spcheckcmd(self, m):
        """ Аналогично pcheck
Отправляет данные в избранное
Жуёт либо <reply>, либо <phone>"""
        await check(m, self.strings['check'], self.strings['version'], 'p', True)


async def check(m, string, version, arg='u', save=False):
    reply = await m.get_reply_message()
    if utils.get_args_raw(m):
        user = utils.get_args_raw(m)
        if arg == 'u' and not user.isnumeric():
            try:
                user = str((await m.client.get_entity(user)).id)
            except Exception as e:
                return await m.edit(f"]EZHG[ <b>Err:</b> {e}")
    elif reply:
        try:
            if arg == 'u':
                user = str(reply.sender.id)
            elif arg == 'p':
                user = reply.contact.phone_number[1:]
        except Exception as e:
            return await m.edit(f"]EZHG[ <b>Err:</b> {e}")
    else:
        return await m.edit("?EZHG? А кого чекать?")
    await m.edit(string)
    url_arg = ("uid" if arg == 'u' else "phone")
    resp = await utils.run_sync(
        lambda: requests.get(f'http://api.murix.ru/eye?v={version}&{url_arg}={user}').json()['data']
    )
    if save:
        await m.client.send_message("me", f"[EZHG] Ответ API: <code>{resp}</code>")
        await m.edit(f"[EZHG] Ответ API отправлен в избранное!")
    else:
        await m.edit(f"[EZHG] Ответ API: <code>{resp}</code>")
