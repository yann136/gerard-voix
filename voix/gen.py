import asyncio, json, os, edge_tts
V = {  # voix Microsoft neuronales (edge-tts)
  "narr":    [("fr-FR-VivienneMultilingualNeural", "+0%", "+0Hz"), ("fr-FR-DeniseNeural", "+0%", "+0Hz")],
  "gerard":  [("fr-FR-RemyMultilingualNeural", "+8%", "+18Hz"), ("fr-FR-HenriNeural", "+10%", "+25Hz"), ("fr-BE-GerardNeural", "+8%", "+20Hz")],
  "gardien": [("fr-FR-HenriNeural", "+6%", "-6Hz"), ("fr-CA-AntoineNeural", "+6%", "-4Hz")],
  "roi":     [("fr-BE-GerardNeural", "-8%", "-14Hz"), ("fr-CH-FabriceNeural", "-8%", "-12Hz")],
}
async def main():
    os.makedirs("voix/out", exist_ok=True)
    for l in json.load(open("voix/lignes.json", encoding="utf-8")):
        for k, (voice, rate, pitch) in enumerate(V[l["spk"]]):
            out = f"voix/out/l{l['i']:02d}_{k}.mp3"
            for tries in range(4):
                try:
                    await edge_tts.Communicate(l["text"], voice, rate=rate, pitch=pitch).save(out); break
                except Exception as e:
                    print("retry", out, e); await asyncio.sleep(3)
            print(out, voice)
asyncio.run(main())
