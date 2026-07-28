"""
Контентные данные проекта: вопросы теста личности, варианты ответов
с привязкой к архетипам, и промпт-блоки для генерации изображений.
"""

# 8 вопросов, каждый вариант ответа (A-H) жёстко привязан к одному архетипу.
QUESTIONS = [
    {
        "number": 1,
        "text": "Тебе предложили проект без чётких правил и границ. Твоя реакция?",
        "options": {
            "A": {"archetype": "rebel", "text": "Наконец-то, делаю по-своему"},
            "B": {"archetype": "hero", "text": "Беру и довожу до конца, чего бы это ни стоило"},
            "C": {"archetype": "jester", "text": "Превращаю хаос в шутку, и всем от этого легче"},
            "D": {"archetype": "ruler", "text": "Сразу выстраиваю структуру и правила сам"},
            "E": {"archetype": "diplomat", "text": "Собираю всех и договариваюсь, как действовать вместе"},
            "F": {"archetype": "creator", "text": "Кайфую — свобода придумать что-то с нуля"},
            "G": {"archetype": "dreamer", "text": "Представляю, каким крутым это может стать в итоге"},
            "H": {"archetype": "explorer", "text": "Берусь, потому что неизвестность — это интересно"},
        },
    },
    {
        "number": 2,
        "text": "В компании начался спор. Что ты делаешь?",
        "options": {
            "A": {"archetype": "rebel", "text": "Подливаю масла в огонь, мне нравится трясти систему"},
            "B": {"archetype": "hero", "text": "Встаю на защиту того, кто прав"},
            "C": {"archetype": "jester", "text": "Шучу, чтобы разрядить обстановку"},
            "D": {"archetype": "ruler", "text": "Беру ситуацию под контроль и решаю, кто прав"},
            "E": {"archetype": "diplomat", "text": "Мирю всех, ищу компромисс"},
            "F": {"archetype": "creator", "text": "Предлагаю неожиданный взгляд на проблему"},
            "G": {"archetype": "dreamer", "text": "Отхожу в сторону, конфликт не по мне"},
            "H": {"archetype": "explorer", "text": "Мне скучно, ухожу искать движуху поинтереснее"},
        },
    },
    {
        "number": 3,
        "text": "У тебя выходной без планов. Чем займёшься?",
        "options": {
            "A": {"archetype": "rebel", "text": "Сделаю что-то, что \"не положено\""},
            "B": {"archetype": "hero", "text": "Найду, кому помочь или что решить"},
            "C": {"archetype": "jester", "text": "Устрою что-то весёлое и спонтанное"},
            "D": {"archetype": "ruler", "text": "Спланирую день по максимуму эффективно"},
            "E": {"archetype": "diplomat", "text": "Проведу время с близкими"},
            "F": {"archetype": "creator", "text": "Займусь любимым творческим хобби"},
            "G": {"archetype": "dreamer", "text": "Просто помечтаю, послушаю музыку, погуляю в своих мыслях"},
            "H": {"archetype": "explorer", "text": "Уеду куда-то, где никогда не был"},
        },
    },
    {
        "number": 4,
        "text": "Тебе сделали серьёзное замечание на людях. Реакция?",
        "options": {
            "A": {"archetype": "rebel", "text": "Отвечаю резко, не люблю, когда меня строят"},
            "B": {"archetype": "hero", "text": "Принимаю и стараюсь исправиться делом"},
            "C": {"archetype": "jester", "text": "Отшучиваюсь, чтобы не выглядело серьёзно"},
            "D": {"archetype": "ruler", "text": "Спокойно объясняю свою правоту"},
            "E": {"archetype": "diplomat", "text": "Извиняюсь, даже если не совсем согласен"},
            "F": {"archetype": "creator", "text": "Слушаю, но всё равно делаю по-своему потом"},
            "G": {"archetype": "dreamer", "text": "Расстраиваюсь внутри, но молчу"},
            "H": {"archetype": "explorer", "text": "Пожимаю плечами, это не так уж важно"},
        },
    },
    {
        "number": 5,
        "text": "О чём ты чаще всего мечтаешь?",
        "options": {
            "A": {"archetype": "rebel", "text": "Сломать систему, которая всех бесит"},
            "B": {"archetype": "hero", "text": "Совершить что-то значимое, что запомнят"},
            "C": {"archetype": "jester", "text": "Просто быть счастливым и смешить людей"},
            "D": {"archetype": "ruler", "text": "Иметь влияние и уважение"},
            "E": {"archetype": "diplomat", "text": "Чтобы всем вокруг было хорошо"},
            "F": {"archetype": "creator", "text": "Создать что-то, чего раньше не было"},
            "G": {"archetype": "dreamer", "text": "Жить в мире, где всё красиво и справедливо"},
            "H": {"archetype": "explorer", "text": "Увидеть весь мир своими глазами"},
        },
    },
    {
        "number": 6,
        "text": "Друг просит у тебя совета в трудной ситуации. Что ты говоришь?",
        "options": {
            "A": {"archetype": "rebel", "text": "\"Забей на правила, делай как чувствуешь\""},
            "B": {"archetype": "hero", "text": "\"Соберись, ты справишься, я помогу\""},
            "C": {"archetype": "jester", "text": "Сначала шучу, чтобы не так страшно было"},
            "D": {"archetype": "ruler", "text": "Даю чёткий пошаговый план"},
            "E": {"archetype": "diplomat", "text": "Внимательно выслушиваю, поддерживаю эмоционально"},
            "F": {"archetype": "creator", "text": "Предлагаю нестандартное решение"},
            "G": {"archetype": "dreamer", "text": "Говорю, что всё образуется, верю в лучшее"},
            "H": {"archetype": "explorer", "text": "\"Брось всё и попробуй что-то новое\""},
        },
    },
    {
        "number": 7,
        "text": "Что тебя больше всего раздражает в людях?",
        "options": {
            "A": {"archetype": "rebel", "text": "Слепое подчинение правилам"},
            "B": {"archetype": "hero", "text": "Трусость и бездействие"},
            "C": {"archetype": "jester", "text": "Излишняя серьёзность"},
            "D": {"archetype": "ruler", "text": "Хаос и безответственность"},
            "E": {"archetype": "diplomat", "text": "Конфликты и агрессия"},
            "F": {"archetype": "creator", "text": "Шаблонность, отсутствие оригинальности"},
            "G": {"archetype": "dreamer", "text": "Цинизм и жестокость"},
            "H": {"archetype": "explorer", "text": "Скука и рутина"},
        },
    },
    {
        "number": 8,
        "text": "Если бы у тебя был девиз по жизни, каким бы он был?",
        "options": {
            "A": {"archetype": "rebel", "text": "\"Правила созданы, чтобы их нарушать\""},
            "B": {"archetype": "hero", "text": "\"Если не я, то кто\""},
            "C": {"archetype": "jester", "text": "\"Жизнь слишком коротка, чтобы быть серьёзным\""},
            "D": {"archetype": "ruler", "text": "\"Порядок начинается с меня\""},
            "E": {"archetype": "diplomat", "text": "\"Вместе мы сильнее\""},
            "F": {"archetype": "creator", "text": "\"Твори или умри\""},
            "G": {"archetype": "dreamer", "text": "\"Верь и мечтай\""},
            "H": {"archetype": "explorer", "text": "\"Мир большой, а жизнь одна\""},
        },
    },
]

# Блок 1 — база кота (константа, не зависит от архетипа)
BLOCK_1 = """A cat character bust portrait — head and upper torso only, cropped at 
chest level, no legs, no lower body visible. Oversized big head relative 
to a moderate, slim torso (not chubby, not overfed, not bloated). The 
cat's fur is a vivid, richly saturated deep violet-purple color with a 
bright electric lime-green belly patch and matching lime ear tips, large 
expressive round eyes with bold dark outlines, small hot-pink nose. Flat 
sticker-pack art style similar to Telegram and LINE messenger stickers — 
highly saturated vivid colors, rounded shapes, simple cel-shading with 
one clear highlight patch on the forehead, cheeks, and nose to suggest 
volume while staying flat and graphic, no soft gradients on the character 
itself, no photorealistic lighting, punchy and characterful, instantly 
recognizable and memorable character design with a bold non-realistic 
color palette."""

# Блок 3 — фон (константа)
BLOCK_3 = """Plain solid white background, no shadows, no vignette, no gradient on
background, no white sticker die-cut outline or border around the
character silhouette, the character should blend directly into the
white background with no visible edge contour, exaggerated comic
expression, sticker-pack energy, funny and a little unhinged, not cute
or wholesome."""

# Блок 2 — по архетипам (динамическая часть)
ARCHETYPE_PROMPTS = {
    "rebel": """The cat has a tall spiked neon mohawk, a studded leather jacket collar,
smudged eyeliner, and a defiant smirk with one raised eyebrow, arms
crossed in classic rebel pose. But pinned to the jacket is a tiny
laminated badge that reads "CERTIFIED REBEL — see rulebook", and one
paw is secretly holding a folded instruction manual titled "How To Be
Punk: 10 Easy Steps" half-hidden behind its back. The safety pin through
one ear is clearly a clip-on, slightly crooked. Despite the tough
expression, there's a flicker of anxious eye-contact-checking, like it's
constantly making sure someone is watching how rebellious it looks.""",

    "hero": """The cat wears a domino mask and a cape that's visibly just a bedsheet
still stapled at the corners, with a lopsided star emblem drawn in
marker on its chest. Pinned proudly across the chest are several
homemade medals made of bottle caps and yarn ribbons, each crudely
labeled "RAT CAUGHT #1", "RAT CAUGHT #2", "MOST RATS CAUGHT 2024" —
clearly self-awarded. One paw is raised in a determined heroic fist —
but the cat's eyes are heavy with exhaustion, dark circles underneath,
a thousand-yard stare of someone who has saved the day one too many
times with zero thanks. A tiny "WORLD'S OKAYEST HERO" trophy sits
crooked on its head like a party hat. The confident jaw is set, but
one back paw is visibly twitching from fatigue.""",

    "jester": """The cat wears a colorful three-pointed jester hat with bells and a
diamond-pattern ruff collar, mouth stretched into an enormous exaggerated
grin showing all teeth. But the eyes are dead flat and unfocused, dark
circles underneath, clearly not matching the smile at all — like the
face is on autopilot while the mind checked out hours ago. One paw
holds a jester scepter with a tiny bell, the other paw is scribbling a
tally mark on a hidden note reading "days since anyone asked if I'm ok"
with a long list of marks already there.""",

    "ruler": """The cat wears a golden jeweled crown that's clearly two sizes too big,
tilting down over one eye, and an ornate red velvet cape with fur trim
that's fraying at the edges. It sits with chin raised in a commanding
regal pose, one paw gripping a small golden scepter — but the "throne" is
obviously a cardboard box with "THRONE" scrawled on it in marker, and the
other paw is white-knuckle gripping the armrest like it's terrified
someone will notice the kingdom is falling apart. Stern authoritative
expression, narrowed eyes, but a single bead of nervous sweat rolling
down its face.""",

    "diplomat": """The cat wears a crisp white collared shirt, a dark tie, and a formal
business suit jacket, paws folded tightly together in a forced composed
manner. Its mouth is stretched into a strained, tight-lipped smile that
doesn't reach the eyes — the corners of the mouth twitching slightly
from the effort of holding it. Eyes are wide open and slightly bloodshot,
one eyebrow twitching, a subtle nervous tension visible around the eyes,
like someone forcing composure while internally screaming. Steam is
visibly puffing out from both ears, and the head glows bright red-orange
like it's about to boil over, with a small thermometer popping out of
the top of its head, needle deep in the red zone. The tie is slightly
crooked and damp with sweat, one paw gripping the other tightly enough
to show tension.""",

    "creator": """The cat wears a simple leaf wreath crown and a single large leaf draped
over one shoulder, one paw dramatically holding a paintbrush aloft in a
pose of divine inspiration, gazing upward with wide soulful eyes. But
the canvas in front of it is completely blank except for one tiny dot
in the corner, and the cat's fur is splattered with paint everywhere
except the canvas itself. A tiny thought bubble above its head shows a
crossed-out lightbulb. The expression is a mix of tortured genius and
mild existential crisis, chewing on the end of the paintbrush anxiously.""",

    "dreamer": """The cat has a soft pastel scarf loosely wrapped around its neck, tiny
stars and a crescent moon floating dreamily around its head, eyes half-
closed and gazing upward with a serene wistful smile, one paw resting
thoughtfully near its chin. Meanwhile, small chaos icons are visible at
the very edge of the frame behind it — a tiny flame, a falling stack of
papers, a "!!!" alert symbol — completely unnoticed and out of focus.
The cat remains blissfully, almost suspiciously unbothered by whatever
is happening just behind it.""",

    "explorer": """The cat wears a worn brown adventurer hat tilted rakishly and a small
compass on a strap, grinning with wild reckless excitement, eyes
squinted toward the horizon, one paw shielding its brow scouting ahead.
But it's covered in small comedic injuries — a crossed bandage over one
eye, a paw in a tiny cast, a visible bruise on one cheek — all clearly
old and re-bandaged many times, yet the grin is even wider than it
should be, like the injuries are trophies rather than warnings.""",
}

ARCHETYPE_NAMES_RU = {
    "rebel": "Бунтарь",
    "hero": "Герой",
    "jester": "Шут",
    "ruler": "Правитель",
    "diplomat": "Дипломат",
    "creator": "Творец",
    "dreamer": "Мечтатель",
    "explorer": "Авантюрист",
}
