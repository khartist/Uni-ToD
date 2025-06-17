import json, chardet, pathlib, io

src = pathlib.Path("output_json_incar_vi.json")
dst = pathlib.Path("output_utf8.json")

# 1️⃣  Read raw bytes
raw = src.read_bytes()

# 2️⃣  Guess encoding (chardet is “good enough” for Vietnamese)
enc_guess = chardet.detect(raw)["encoding"] or "utf-8"

# 3️⃣  Decode using that guess (replace impossible bytes, just in case)
text = raw.decode(enc_guess, errors="replace")

# 4️⃣  Parse JSON
data = json.loads(text)

# 5️⃣  Write back in *real* UTF-8 with Vietnamese characters intact
with io.open(dst, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Clean file saved to → {dst}")
