# meta developer: @hhaacckk1

from .. import loader, utils
import requests


class GBSLIVMod(loader.Module):
    """GBSLIV (Р“Р›4Р—РРљ Р‘0Р“4) v1.2"""
    strings = {
        'name': 'GBSLIV',
        'check': '[EYE_API] Р”РµР»Р°РµРј Р·Р°РїСЂРѕСЃ Рє API...',
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
        """ РџСЂРѕРІРµСЂРёС‚СЊ uid РЅР° РЅРѕРјРµСЂ
РћС‚РїСЂР°РІР»СЏРµС‚ РґР°РЅРЅС‹Рµ РІ С‡Р°С‚
Р–СѓС‘С‚ Р»РёР±Рѕ <reply>, Р»РёР±Рѕ <uid>"""
        await check(m, self.strings['check'], self.strings['version'])

    async def pcheckcmd(self, m):
        """ РџСЂРѕРІРµСЂРёС‚СЊ РЅРѕРјРµСЂ РЅР° РЅР°Р»РёС‡РёРµ РІ Р±Рґ
РћС‚РїСЂР°РІР»СЏРµС‚ РґР°РЅРЅС‹Рµ РІ С‡Р°С‚
Р–СѓС‘С‚ Р»РёР±Рѕ <reply>, Р»РёР±Рѕ <phone>"""
        await check(m, self.strings['check'], self.strings['version'], 'p')

    async def scheckcmd(self, m):
        """ РђРЅР°Р»РѕРіРёС‡РЅРѕ check
РћС‚РїСЂР°РІР»СЏРµС‚ РґР°РЅРЅС‹Рµ РІ РёР·Р±СЂР°РЅРЅРѕРµ
Р–СѓС‘С‚ Р»РёР±Рѕ <reply>, Р»РёР±Рѕ <uid>"""
        await check(m, self.strings['check'], self.strings['version'], save=True)

    async def spcheckcmd(self, m):
        """ РђРЅР°Р»РѕРіРёС‡РЅРѕ pcheck
РћС‚РїСЂР°РІР»СЏРµС‚ РґР°РЅРЅС‹Рµ РІ РёР·Р±СЂР°РЅРЅРѕРµ
Р–СѓС‘С‚ Р»РёР±Рѕ <reply>, Р»РёР±Рѕ <phone>"""
        await check(m, self.strings['check'], self.strings['version'], 'p', True)


async def check(m, string, version, arg='u', save=False):
    reply = await m.get_reply_message()
    if utils.get_args_raw(m):
        user = utils.get_args_raw(m)
        if arg == 'u' and not user.isnumeric():
            try:
                user = str((await m.client.get_entity(user)).id)
            except Exception as e:
                return await m.edit(f"]EYE_API[ <b>Err:</b> {e}")
    elif reply:
        try:
            if arg == 'u':
                user = str(reply.sender.id)
            elif arg == 'p':
                user = reply.contact.phone_number[1:]
        except Exception as e:
            return await m.edit(f"]EYE_API[ <b>Err:</b> {e}")
    else:
        return await m.edit("?EYE_API? Рђ РєРѕРіРѕ С‡РµРєР°С‚СЊ?")
    await m.edit(string)
    url_arg = ("uid" if arg == 'u' else "phone")
    resp = await utils.run_sync(
        lambda: requests.get(f'http://api.murix.ru/eye?v={version}&{url_arg}={user}').json()['data']
    )
    if save:
        await m.client.send_message("me", f"[EYE_API] РћС‚РІРµС‚ API: <code>{resp}</code>")
        await m.edit(f"[EYE_API] РћС‚РІРµС‚ API РѕС‚РїСЂР°РІР»РµРЅ РІ РёР·Р±СЂР°РЅРЅРѕРµ!")
    else:
        await m.edit(f"[EYE_API] РћС‚РІРµС‚ API: <code>{resp}</code>")
