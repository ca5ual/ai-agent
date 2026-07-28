from google import genai
from google.genai import types

PROJECT_ID = "ai-cats-502309"  # твой project ID
LOCATION = "global"  # gemini-3-pro-image доступна только на global endpoint

client = genai.Client(enterprise=True, project=PROJECT_ID, location=LOCATION)

# Наша финальная формула: Блок 1 (база кота) + Блок 2 (архетип: Дипломат) + Блок 3 (фон)
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

BLOCK_2_DIPLOMAT = """The cat wears a crisp white collared shirt, a dark tie, and a formal
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
to show tension."""

BLOCK_3 = """Plain solid white background, no shadows, no vignette, no gradient on
background, no white sticker die-cut outline or border around the
character silhouette, the character should blend directly into the
white background with no visible edge contour, exaggerated comic
expression, sticker-pack energy, funny and a little unhinged, not cute
or wholesome."""

final_prompt = f"{BLOCK_1}\n\n{BLOCK_2_DIPLOMAT}\n\n{BLOCK_3}"

print("Отправляю запрос к Nano Banana Pro...")

response = client.models.generate_content(
    model="gemini-3-pro-image",
    contents=final_prompt,
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
    ),
)

# Достаём картинку из ответа и сохраняем на диск
saved = False
for part in response.candidates[0].content.parts:
    if part.inline_data is not None:
        with open("test_cat.png", "wb") as f:
            f.write(part.inline_data.data)
        print("Готово! Картинка сохранена как test_cat.png")
        saved = True

if not saved:
    print("Картинка не найдена в ответе. Полный ответ модели:")
    print(response)