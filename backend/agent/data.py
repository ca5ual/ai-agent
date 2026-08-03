"""
Контентные данные проекта: вопросы теста личности, варианты ответов
с привязкой к архетипам, и промпт-блоки для генерации изображений.
"""

# 8 вопросов, каждый вариант ответа (A-H) жёстко привязан к одному архетипу.
QUESTIONS = [
    {
        "number": 1,
        "text": "You get a project with no clear rules or limits. What's your reaction?",
        "options": {
            "A": {"archetype": "rebel", "text": "Finally! I do it my way"},
            "B": {"archetype": "hero", "text": "I take it and finish it no matter what"},
            "C": {"archetype": "jester", "text": "I turn the chaos into a joke and make everyone feel better"},
            "D": {"archetype": "ruler", "text": "I create rules and organize everything myself"},
            "E": {"archetype": "diplomat", "text": "I gather everyone and figure out a plan together"},
            "F": {"archetype": "creator", "text": "Awesome — I get to invent something from zero"},
            "G": {"archetype": "dreamer", "text": "I imagine how amazing this could become"},
            "H": {"archetype": "explorer", "text": "I jump in because unknown things are exciting"},
        },
    },
    {
        "number": 2,
        "text": "People around you start arguing. What do you do?",
        "options": {
            "A": {"archetype": "rebel", "text": "I add some chaos. I like shaking things up"},
            "B": {"archetype": "hero", "text": "I defend the person who is right"},
            "C": {"archetype": "jester", "text": "I make jokes to calm everyone down"},
            "D": {"archetype": "ruler", "text": "I take control and decide what should happen"},
            "E": {"archetype": "diplomat", "text": "I make peace and find a compromise"},
            "F": {"archetype": "creator", "text": "I suggest a completely different way to see the problem"},
            "G": {"archetype": "dreamer", "text": "I step away. Drama is not my thing"},
            "H": {"archetype": "explorer", "text": "This is boring. I go find something more interesting"},
        },
    },
    {
        "number": 3,
        "text": "You have a free day with no plans. What do you do?",
        "options": {
            "A": {"archetype": "rebel", "text": "I do something I'm probably not supposed to do"},
            "B": {"archetype": "hero", "text": "I find someone to help or a problem to solve"},
            "C": {"archetype": "jester", "text": "I create something fun and totally random"},
            "D": {"archetype": "ruler", "text": "I plan the perfect productive day"},
            "E": {"archetype": "diplomat", "text": "I spend time with people I care about"},
            "F": {"archetype": "creator", "text": "I work on my favorite creative hobby"},
            "G": {"archetype": "dreamer", "text": "I listen to music, daydream, and wander in my thoughts"},
            "H": {"archetype": "explorer", "text": "I go somewhere I've never been before"},
        },
    },
    {
        "number": 4,
        "text": "Someone seriously criticizes you in front of others. Your reaction?",
        "options": {
            "A": {"archetype": "rebel", "text": "I answer back. I hate people telling me what to do"},
            "B": {"archetype": "hero", "text": "I accept it and prove myself with actions"},
            "C": {"archetype": "jester", "text": "I joke about it so it doesn't feel so serious"},
            "D": {"archetype": "ruler", "text": "I calmly explain why I am right"},
            "E": {"archetype": "diplomat", "text": "I apologize, even if I don't fully agree"},
            "F": {"archetype": "creator", "text": "I listen, but I'll probably do it my own way later"},
            "G": {"archetype": "dreamer", "text": "I feel bad inside but don't say much"},
            "H": {"archetype": "explorer", "text": "I shrug. It's not a big deal"},
        },
    },
 {
        "number": 5,
        "text": "What do you dream about most often?",
        "options": {
            "A": {"archetype": "rebel", "text": "Breaking a system that annoys everyone"},
            "B": {"archetype": "hero", "text": "Doing something important that people remember"},
            "C": {"archetype": "jester", "text": "Being happy and making people laugh"},
            "D": {"archetype": "ruler", "text": "Having power, influence, and respect"},
            "E": {"archetype": "diplomat", "text": "Making sure everyone around me is happy"},
            "F": {"archetype": "creator", "text": "Creating something that never existed before"},
            "G": {"archetype": "dreamer", "text": "Living in a world that is beautiful and fair"},
            "H": {"archetype": "explorer", "text": "Seeing the whole world with my own eyes"},
        },
    },
    {
        "number": 6,
        "text": "A friend asks for advice during a difficult situation. What do you say?",
        "options": {
            "A": {"archetype": "rebel", "text": "\"Forget the rules. Do what feels right\""},
            "B": {"archetype": "hero", "text": "\"Stay strong. You can do this. I'll help you\""},
            "C": {"archetype": "jester", "text": "I make a joke first so it feels less scary"},
            "D": {"archetype": "ruler", "text": "I give a clear step-by-step plan"},
            "E": {"archetype": "diplomat", "text": "I listen carefully and give emotional support"},
            "F": {"archetype": "creator", "text": "I suggest an unusual solution"},
            "G": {"archetype": "dreamer", "text": "I say everything will be okay and believe in the best"},
            "H": {"archetype": "explorer", "text": "\"Drop everything and try something new\""},
        },
    },
    {
        "number": 7,
        "text": "What annoys you the most about people?",
        "options": {
            "A": {"archetype": "rebel", "text": "Following rules without thinking"},
            "B": {"archetype": "hero", "text": "Fear and doing nothing"},
            "C": {"archetype": "jester", "text": "Taking everything too seriously"},
            "D": {"archetype": "ruler", "text": "Chaos and irresponsibility"},
            "E": {"archetype": "diplomat", "text": "Fighting and aggression"},
            "F": {"archetype": "creator", "text": "Being boring and having no original ideas"},
            "G": {"archetype": "dreamer", "text": "Cynicism and cruelty"},
            "H": {"archetype": "explorer", "text": "Boredom and boring routines"},
        },
    },
    {
        "number": 8,
        "text": "If you had a life motto, what would it be?",
        "options": {
            "A": {"archetype": "rebel", "text": "\"Rules exist to be broken\""},
            "B": {"archetype": "hero", "text": "\"If not me, then who?\""},
            "C": {"archetype": "jester", "text": "\"Life is too short to be serious\""},
            "D": {"archetype": "ruler", "text": "\"Order starts with me\""},
            "E": {"archetype": "diplomat", "text": "\"Together we are stronger\""},
            "F": {"archetype": "creator", "text": "\"Create or disappear\""},
            "G": {"archetype": "dreamer", "text": "\"Believe and dream\""},
            "H": {"archetype": "explorer", "text": "\"The world is huge and life happens once\""},
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