import urllib.request
import json

boundary = "----WebKitFormBoundaryTest123"
with open("images/laddu.png", "rb") as f:
    img_data = f.read()

body = (
    f"--{boundary}\r\n"
    f'Content-Disposition: form-data; name="file"; filename="laddu.png"\r\n'
    f"Content-Type: image/png\r\n\r\n"
).encode("utf-8") + img_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

req = urllib.request.Request(
    "http://127.0.0.1:8000/api/analyze",
    data=body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
)

with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode())
    result = res.get("result", {})
    food = result.get("food_item", {})
    vessel = result.get("vessel", {})
    portion = result.get("portion", {})
    nutrients = result.get("nutrients", {})
    
    print("API STATUS:", res.get("status"))
    print(f"FOOD ITEM:  {food.get('name')} (id: {food.get('id')})")
    print(f"CONFIDENCE: {food.get('confidence') * 100:.1f}%")
    print(f"CATEGORY:   {food.get('category')}")
    print(f"VESSEL:     {vessel.get('type')} ({vessel.get('estimated_diameter_cm')}cm)")
    print(f"WEIGHT:     {portion.get('estimated_weight_g')} g")
    print(f"CALORIES:   {nutrients.get('portion_nutrients', {}).get('calories_kcal')} kcal")
    print("\nTOP CANDIDATES:")
    for c in food.get("top_candidates", [])[:3]:
        print(f"  {c['name']:20s} ({c['confidence']*100:5.1f}%)")
