import enum

EMOJIS = {
    "yes": 1029915446029336696,
    "no": 1029915423694651552,
    "warning": 1029916562955702292,
    "unoreverse": 1029989262311034941,
}

CLEAR_FORMATTING = "\u001b[0;0m"


class Emoji:
    def __init__(self):
        self.yes = "<:yes:1029915446029336696>"
        self.no = "<:no:1029915423694651552>"
        self.warning = "<:warning:1029916562955702292>"
        self.unoreverse = "<:unoreverse:1029989262311034941>"


class format(enum.Enum):
    normal = 0
    bold = 1
    underline = 4
    reverse_text = 7


class text_color(enum.Enum):
    normal = 0
    gray = 30
    red = 31
    green = 32
    yellow = 33
    blue = 34
    pink = 35
    cyan = 36
    white = 37
    dark_grey = 90
    bright_red = 91
    bright_green = 92
    bright_yellow = 93
    bright_blue = 94
    bright_magenta = 95
    bright_cyan = 96
    bright_white = 97


class background_color(enum.Enum):
    normal = 0
    dark_blue = 40
    orange = 41
    light_blue = 42
    turquoise = 43
    gray = 44
    indigo = 45
    light_gray = 46
    white = 47
