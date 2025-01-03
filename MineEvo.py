# meta developer: @ShabBots
import logging
from .. import loader
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.types import PeerUser

logger = logging.getLogger(__name__)

@loader.tds
class MineEvo(loader.Module):
    """Модуль для бота MineEvo, принимает любые команды которые есть в боте. Выводит сообщения, которые выдает бот."""

    strings = {
        "name": "MineEvo_commands",
        "no_command": "ты не написал команду.",
    }

    @loader.command(
        ru_doc="Отправить команду в @mine_evo_bot",
        eng_doc="Send a command to @mine_evo_bot"
    )
    async def mvcmd(self, message):
        args = self.get_args_raw(message)
        chat_id = "@mine_evo_bot"

        if not args:
          await message.edit(self.strings("no_command"))
          return
      
        await message.delete()

        try:
            async with self.client.conversation(chat_id) as conv:
                chat_msg = await conv.send_message(args)
                response = await conv.get_response()
                if response:
                    await self.client.send_message(message.peer_id, response.text, reply_to=message.id)
                else:
                    await self.client.send_message(message.peer_id, "бот не ответил.", reply_to=message.id)
        except Exception as e:
            logger.error(f"ошибка при отправке боту: {e}")
            await self.client.send_message(message.peer_id, f"произошла ошибка: {e}", reply_to=message.id)

    
    def get_args_raw(self, message):
        args = message.text.split(" ", 1)
        if len(args) > 1:
            return args[1]
        return ""
