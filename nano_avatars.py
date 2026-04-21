"""Génère 6 avatars portrait photo-réels pour les témoignages via Nano Banana."""
from pathlib import Path
from google import genai

client = genai.Client(api_key="AIzaSyDxhc1kS9GHC8fILYnvE_uB2t-5rfp1GB0")
OUT = Path(__file__).parent / "public" / "images" / "temoignages"
OUT.mkdir(parents=True, exist_ok=True)

AVATARS = [
    ("avatar-mehdi.png",
     "Professional headshot portrait of a 28-year-old North African man with short dark hair and trimmed beard, wearing a dark hoodie, neutral grey background, soft natural studio lighting, confident friendly look, modern tech freelancer vibe, square crop centered on face, editorial photography, shot on Sony A7, shallow depth of field, ultra sharp, no text, no watermark"),
    ("avatar-laura.png",
     "Professional headshot portrait of a 26-year-old European woman with long brown wavy hair and light skin, wearing a cream sweater, soft neutral background, natural studio lighting, confident creative content creator vibe, warm welcoming smile, square crop centered on face, editorial photography, ultra sharp, no text"),
    ("avatar-karim.png",
     "Professional headshot portrait of a 32-year-old Mediterranean man with short dark hair, well-groomed beard, wearing a black turtleneck, neutral dark grey background, soft directional lighting, serious entrepreneur agency owner vibe, confident gaze, square crop centered on face, editorial photography, shot on Sony A7, ultra sharp, no text"),
    ("avatar-nora.png",
     "Professional headshot portrait of a 29-year-old woman with short dark curly hair, warm skin tone, wearing a minimalist beige top, neutral light grey background, soft natural light, confident creative studio founder vibe, subtle smile, square crop centered on face, editorial photography, ultra sharp, no text"),
    ("avatar-thomas.png",
     "Professional headshot portrait of a 34-year-old European man with short blond hair, clean shaven, wearing a charcoal zip sweater, neutral grey background, soft directional lighting, thoughtful consultant vibe, confident calm gaze, square crop centered on face, editorial photography, shot on Sony A7, ultra sharp, no text"),
    ("avatar-sarah.png",
     "Professional headshot portrait of a 30-year-old woman with shoulder-length dark blonde hair, light skin, wearing a black blazer over white top, neutral soft beige background, natural studio lighting, confident agency founder vibe, warm professional smile, square crop centered on face, editorial photography, ultra sharp, no text"),
]

for filename, prompt in AVATARS:
    out_path = OUT / filename
    if out_path.exists() and out_path.stat().st_size > 10000:
        print(f"skip {filename}")
        continue
    print(f"gen {filename}")
    try:
        resp = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=prompt,
        )
        saved = False
        for part in resp.candidates[0].content.parts:
            if getattr(part, 'inline_data', None) and part.inline_data.data:
                out_path.write_bytes(part.inline_data.data)
                print(f"  ✓ saved {filename} ({out_path.stat().st_size//1024} KB)")
                saved = True
                break
        if not saved:
            print(f"  ✗ no image for {filename}")
    except Exception as e:
        print(f"  ✗ error: {str(e)[:120]}")

print("done")
