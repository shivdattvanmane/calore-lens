import os
from PIL import Image
from calorie_lens_engine import CalorieLensEngine

engine = CalorieLensEngine()

print("=== IMAGES DIRECTORY ===")
for f in os.listdir("images"):
    if f.endswith((".png", ".jpg", ".jpeg")) and not f.endswith("output.png") and not f.endswith("result.png") and not "sample" in f:
        p = os.path.join("images", f)
        im = Image.open(p)
        preds = engine.classify_food(im, top_k=2)
        top = preds[0]
        print(f"[{f:20s}] -> {top['name']:20s} ({top['confidence']*100:5.1f}%) | category: {top['category']}")

print("\n=== TEST IMAGES DIRECTORY ===")
for f in os.listdir("test images"):
    if f.endswith((".png", ".jpg", ".jpeg")):
        p = os.path.join("test images", f)
        im = Image.open(p)
        preds = engine.classify_food(im, top_k=2)
        top = preds[0]
        print(f"[{f:20s}] -> {top['name']:20s} ({top['confidence']*100:5.1f}% | 2nd: {preds[1]['name']} {preds[1]['confidence']*100:4.1f}%) | category: {top['category']}")
