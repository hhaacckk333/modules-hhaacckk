__version__ = (2, 0, 0)

#
#              © Copyright 2022
#
#          https://t.me/hhaacckk1
#
# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta pic: https://img.icons8.com/external-icongeek26-flat-icongeek26/512/000000/external-tic-tac-toe-playground-icongeek26-flat-icongeek26.png
# meta developer: @hhaacckk1
# scope: inline
# scope: hikka_only
# scope: hikka_min 1.0.25

import copy
import enum
from random import choice
from typing import List

from telethon.tl.types import Message
from telethon.utils import get_display_name

from .. import loader, utils
from ..inline.types import InlineCall

phrases = [
    "Your brain is just a joke... Use it!",
    "What a nice move...",
    "Try to overcome me!",
    "I'm irresistible, you have no chances!",
    "The clock is ticking... Hurry up.",
    "Don't act, stop to think!",
    "It was your choice, not mine...",
]

# AI from https://github.com/morgankenyon/RandomML/tree/master/src/tictactoe


class Player(enum.Enum):
    x = 1
    o = 2

    @property
    def other(self):
        return Player.x if self == Player.o else Player.o


class Choice:
    def __init__(self, move, value, depth):
        self.move = move
        self.value = value
        self.depth = depth

    def __str__(self):
        return f"{str(self.move)}: {str(self.value)}"


class AbBot:
    def __init__(self, player):
        self.player = player

    def alpha_beta_search(self, board, is_max, current_player, depth, alpha, beta):
        # if board has a winner or is a tie
        # return with appropriate values
        winner = board.has_winner()
        if winner == self.player:
            return Choice(board.last_move(), 10 - depth, depth)
        elif winner == self.player.other:
            return Choice(board.last_move(), -10 + depth, depth)
        elif len(board.moves) == 9:
            return Choice(board.last_move(), 0, depth)

        candidates = board.get_legal_moves()
        max_choice = None
        min_choice = None
        for i in range(len(candidates)):
            row = candidates[i][0]
            col = candidates[i][1]
            newboard = copy.deepcopy(board)
            newboard.make_move(row, col, current_player)
            result = self.alpha_beta_search(
                newboard, not is_max, current_player.other, depth + 1, alpha, beta
            )
            result.move = newboard.last_move()

            if is_max:
                alpha = max(result.value, alpha)
                if alpha >= beta:
                    return result

                if max_choice is None or result.value > max_choice.value:
                    max_choice = result
            else:
                beta = min(result.value, beta)
                if alpha >= beta:
                    return result

                if min_choice is None or result.value < min_choice.value:
                    min_choice = result

        return max_choice if is_max else min_choice

    def select_move(self, board):
        choice = self.alpha_beta_search(board, True, self.player, 0, -100, 100)
        return choice.move


MARKER_TO_CHAR = {
    None: " . ",
    Player.x: " x ",
    Player.o: " o ",
}


class Board:
    def __init__(self):
        self.dimension = 3
        self.grid = [
            [None for _ in range(self.dimension)] for _ in range(self.dimension)
        ]

        self.moves = []

    def print(self):
        print()
        for row in range(self.dimension):
            line = [
                MARKER_TO_CHAR[self.grid[row][col]] for col in range(self.dimension)
            ]
            print("%s" % ("".join(line)))

    def has_winner(self):
        # need at least 5 moves before x hits three in a row
        if len(self.moves) < 5:
            return None

        # check rows for win
        for row in range(self.dimension):
            unique_rows = set(self.grid[row])
            if len(unique_rows) == 1:
                value = unique_rows.pop()
                if value is not None:
                    return value

        # check columns for win
        for col in range(self.dimension):
            unique_cols = {self.grid[row][col] for row in range(self.dimension)}
            if len(unique_cols) == 1:
                value = unique_cols.pop()
                if value is not None:
                    return value

        # check backwards diagonal (top left to bottom right) for win
        backwards_diag = {self.grid[0][0], self.grid[1][1], self.grid[2][2]}
        if len(backwards_diag) == 1:
            value = backwards_diag.pop()
            if value is not None:
                return value

        # check forwards diagonal (bottom left to top right) for win
        forwards_diag = {self.grid[2][0], self.grid[1][1], self.grid[0][2]}
        if len(forwards_diag) == 1:
            value = forwards_diag.pop()
            if value is not None:
                return value

        # found no winner, return None
        return None

    def make_move(self, row, col, player):
        if self.is_space_empty(row, col):
            self.grid[row][col] = player
            self.moves.append([row, col])
        else:
            raise Exception("Attempting to move onto already occupied space")

    def last_move(self):
        return self.moves[-1]

    def is_space_empty(self, row, col):
        return self.grid[row][col] is None

    def get_legal_moves(self):
        choices = []
        for row in range(self.dimension):
            choices.extend(
                [row, col]
                for col in range(self.dimension)
                if (self.is_space_empty(row, col))
            )

        return choices

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        dp = Board()
        dp.grid = copy.deepcopy(self.grid)
        dp.moves = copy.deepcopy(self.moves)
        return dp


# /AI


@loader.tds
class TicTacToeMod(loader.Module):
    """Play your favorite game in Telegram"""

    strings = {
        "name": "TicTacToe",
        "gamestart": "🧠 <b>You want to play, let's play!</b>\n<i>Waiting for second player...</i>",
        "gamestart_ai": "💀 <b>Χάρων is ready to compete! Are you?</b>",
        "game_discarded": "Game is discarded",
        "wait_for_your_turn": "Wait for your turn",
        "no_move": "This cell is not empty",
        "not_your_game": "It is not your game, don't interrupt it",
        "draw": "🧠 <b>The game is over! What a pity...</b>\n<i>🐉 The game ended with <b>draw</b>. No winner, no argument...</i>",
        "normal_game": "🧠 <b>{}</b>\n<i>Playing with <b>{}</b></i>\n\n<i>Now is the turn of <b>{}</b></i>",
        "win": "🧠 <b>The game is over! What a pity...</b>\n\n<i>🏆 Winner: <b>{} ({})</b></i>\n<code>{}</code>",
        "ai_game": "🧠 <b>{}</b>\n<i><b>{}</b> is playing with <b>💀 Χάρων</b></i>\n\n<i>You are {}</i>",
        "not_with_yourself": "You can't play with yourself!",
    }

    strings_ru = {
        "gamestart": "🧠 <b>Поиграть захотелось? Поиграем!</b>\n<i>Ожидание второго игрока...</i>",
        "gamestart_ai": "💀 <b>Харон готов сражаться! А что насчет тебя?</b>",
        "game_discarded": "Игра отменена",
        "wait_for_your_turn": "Ожидание хода",
        "no_move": "Эта клетка уже заполнена",
        "not_your_game": "Это не твоя игра, не мешай",
        "draw": "🧠 <b>Игра окончена! Какая жалость...</b>\n<i>🐉 Игра закончилась <b>ничьей</b>. Нет победителя, нет спора...</i>",
        "normal_game": "🧠 <b>{}</b>\n<i>Игра с <b>{}</b></i>\n\n<i>Сейчас ходит <b>{}</b></i>",
        "win": "🧠 <b>Игра окончена! Какая жалость...</b>\n\n<i>🏆 Победитель: <b>{} ({})</b></i>\n<code>{}</code>",
        "ai_game": "🧠 <b>{}</b>\n<i><b>{}</b> играет с <b>💀 Хароном</b></i>\n\n<i>Ты {}</i>",
        "not_with_yourself": "Ты не можешь играть сам с собой!",
        "_cmd_doc_tictactoe": "Начать новую игру в крестики-нолики",
        "_cmd_doc_tictacai": "Сыграть с 💀 Хароном (У тебя нет шансов)",
        "_cls_doc": "Сыграй в крестики-нолики прямо в Телеграм",
    }

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self._games = {}
        self._me = await client.get_me()

    async def inline__close(self, call: InlineCall):
        await call.delete()

    async def _process_click(
        self,
        call: InlineCall,
        i: int,
        j: int,
        line: str,
    ):
        if call.from_user.id not in [
            self._me.id,
            self._games[call.form["uid"]]["2_player"],
        ]:
            await call.answer(self.strings("not_your_game"))
            return

        if call.from_user.id != self._games[call.form["uid"]]["turn"]:
            await call.answer(self.strings("wait_for_your_turn"))
            return

        if line != ".":
            await call.answer(self.strings("no_move"))
            return

        self._games[call.form["uid"]]["score"] = (
            self._games[call.form["uid"]]["score"][: j + i * 4]
            + self._games[call.form["uid"]]["mapping"][call.from_user.id]
            + self._games[call.form["uid"]]["score"][j + i * 4 + 1 :]
        )

        self._games[call.form["uid"]]["turn"] = (
            self._me.id
            if call.from_user.id != self._me.id
            else self._games[call.form["uid"]]["2_player"]
        )

        await call.edit(**self._render(call.form["uid"]))

    async def _process_click_ai(self, call: InlineCall, i: int, j: int, line: str):
        if call.form["uid"] not in self._games:
            await call.answer(self.strings("game_discarded"))
            await call.delete()

        if call.from_user.id != self._games[call.form["uid"]]["user"].id:
            await call.answer(self.strings("not_your_game"))
            return

        if line != ".":
            await call.answer(self.strings("no_move"))
            return

        self._games[call.form["uid"]]["board"].make_move(
            i, j, self._games[call.form["uid"]]["human_player"]
        )

        try:
            self._games[call.form["uid"]]["board"].make_move(
                *self._games[call.form["uid"]]["bot"].select_move(
                    self._games[call.form["uid"]]["board"]
                ),
                self._games[call.form["uid"]]["ai_player"],
            )
        except Exception:
            pass

        await call.edit(**self._render_ai(call.form["uid"]))

    def win_indexes(self, n):
        return (
            [[(r, c) for r in range(n)] for c in range(n)]
            + [[(r, c) for c in range(n)] for r in range(n)]
            + [[(i, i) for i in range(n)]]
            + [[(i, n - 1 - i) for i in range(n)]]
        )

    def is_winner(self, board, decorator):
        n = len(board)

        return any(
            all(board[r][c] == decorator for r, c in indexes)
            for indexes in self.win_indexes(n)
        )

    def _render_text(self, board_raw: List[List[str]]) -> str:
        board = [[char.replace(".", " ") for char in line] for line in board_raw]
        return f"""
{board[0][0]} | {board[0][1]} | {board[0][2]}
----------
{board[1][0]} | {board[1][1]} | {board[1][2]}
----------
{board[2][0]} | {board[2][1]} | {board[2][2]}"""

    def _render(self, uid: str) -> dict:
        if uid not in self._games or uid not in self.inline._units:
            return

        game = self._games[uid]
        text = self.strings("normal_game").format(
            choice(phrases),
            game["name"],
            utils.escape_html(get_display_name(self._me))
            if game["turn"] == self._me.id
            else game["name"],
        )
        score = game["score"].split("|")
        kb = []
        rmap = {v: k for k, v in game["mapping"].items()}

        win_x, win_o = self.is_winner(score, "x"), self.is_winner(score, "o")

        if win_o or win_x:
            try:
                del self._games[uid]
            except KeyError:
                pass

            winner = rmap["x" if win_x else "o"]

            return {
                "text": self.strings("win").format(
                    game["name"]
                    if winner != self._me.id
                    else utils.escape_html(get_display_name(self._me)),
                    "❌" if win_x else "⭕️",
                    self._render_text(score),
                )
            }

        if game["score"].count("."):
            for i, row in enumerate(score):
                kb_row = [
                    {
                        "text": line.replace(".", " ")
                        .replace("x", "❌")
                        .replace("o", "⭕️"),
                        "callback": self._process_click,
                        "args": (
                            i,
                            j,
                            line,
                        ),
                    }
                    for j, line in enumerate(row)
                ]
                kb += [kb_row]
        else:
            try:
                del self._games[uid]
            except KeyError:
                pass

            return {"text": self.strings("draw")}

        return {"text": text, "reply_markup": kb}

    async def inline__start_game(self, call: InlineCall):
        if call.from_user.id == self._me.id:
            await call.answer(self.strings("not_with_yourself"))
            return

        uid = call.form["uid"]
        first = choice([call.from_user.id, self._me.id])
        self._games[uid] = {
            "2_player": call.from_user.id,
            "turn": first,
            "mapping": {
                first: "x",
                (call.from_user.id if call.from_user.id != first else self._me.id): "o",
            },
            "name": utils.escape_html(
                get_display_name(await self._client.get_entity(call.from_user.id))
            ),
            "score": "...|...|...",
        }

        await call.edit(**self._render(uid))

    async def inline__start_game_ai(self, call: InlineCall):
        uid = call.form["uid"]

        user = await self._client.get_entity(call.from_user.id)

        first = choice(["Χάρων", user.id])
        self._games[uid] = {
            "2_player": "Χάρων",
            "turn": user.id,
            "mapping": {first: "x", "Χάρων" if first != "Χάρων" else user.id: "o"},
            "amifirst": first == user.id,
            "user": user,
            "ai_player": Player.x if first == "Χάρων" else Player.o,
            "human_player": Player.o if first == "Χάρων" else Player.x,
            "bot": AbBot(Player.x if first == "Χάρων" else Player.o),
            "board": Board(),
        }

        if first == "Χάρων":
            self._games[uid]["board"].make_move(
                *self._games[uid]["bot"].select_move(self._games[uid]["board"]),
                self._games[uid]["ai_player"],
            )

        await call.edit(**self._render_ai(uid))

    async def tictactoecmd(self, message: Message):
        """Start new tictactoe game"""
        await self.inline.form(
            self.strings("gamestart"),
            message=message,
            reply_markup={"text": "💪 Play", "callback": self.inline__start_game},
            ttl=15 * 60,
            disable_security=True,
        )

    def _render_ai(self, uid: str) -> dict:
        if uid not in self._games or uid not in self.inline._units:
            return

        game = self._games[uid]
        text = self.strings("ai_game").format(
            choice(phrases),
            utils.escape_html(get_display_name(game["user"])),
            "❌" if game["amifirst"] else "⭕️",
        )
        score = [
            [MARKER_TO_CHAR[char].strip() for char in line]
            for line in game["board"].grid
        ]
        kb = []
        rmap = {v: k for k, v in game["mapping"].items()}

        win_x, win_o = self.is_winner(score, "x"), self.is_winner(score, "o")

        if win_o or win_x:
            try:
                del self._games[uid]
            except KeyError:
                pass

            winner = rmap["x" if win_x else "o"]

            return {
                "text": self.strings("win").format(
                    "💀 Χάρων"
                    if winner != game["user"]
                    else utils.escape_html(get_display_name(game["user"])),
                    "❌" if win_x else "⭕️",
                    self._render_text(score),
                )
            }

        if "".join(["".join(line) for line in score]).count("."):
            for i, row in enumerate(score):
                kb_row = [
                    {
                        "text": line.replace(".", " ")
                        .replace("x", "❌")
                        .replace("o", "⭕️"),
                        "callback": self._process_click_ai,
                        "args": (
                            i,
                            j,
                            line,
                        ),
                    }
                    for j, line in enumerate(row)
                ]
                kb += [kb_row]
        else:
            try:
                del self._games[uid]
            except KeyError:
                pass

            return {"text": self.strings("draw")}

        return {"text": text, "reply_markup": kb}

    async def tictacaicmd(self, message: Message):
        """Play with 💀 Χάρων (You have no chances to win)"""
        await self.inline.form(
            self.strings("gamestart_ai"),
            message=message,
            reply_markup={
                "text": "🧠 Let's go!",
                "callback": self.inline__start_game_ai,
            },
            ttl=15 * 60,
            disable_security=True,
        )
