"""
app.py - Calorie Lens Interactive Web Application
FastAPI Server for Indian Food Calorie & Nutrient Estimation
"""

import io
import json
import base64
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from calorie_lens_engine import engine, OUTPUTS_DIR, RESULTS_DIR, BASE_DIR

app = FastAPI(
    title="Calorie Lens API",
    description="Indian Food Calorie and Nutrient Estimator with Portion Segmentation",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Frontend index.html not found.")
    return HTMLResponse(content=index_file.read_text(encoding="utf-8"))


@app.get("/api/foods")
async def get_all_foods():
    """Return all 51 Indian food classes with nutrient summaries."""
    return {"status": "success", "foods": engine.get_food_names()}


@app.get("/api/samples")
async def get_sample_images():
    """Return list of preloaded sample images from the repository."""
    samples = []
    
    # Check test images/ and images/
    sample_paths = [
        ("images/laddu.png", "Bandar Laddu", "dessert"),
        ("images/aloo methi.png", "Aloo Methi", "vegetable_curry"),
        ("test images/000004.jpg", "Mysore Pak", "dessert"),
        ("test images/53223.jpg", "Bandar Laddu", "dessert"),
        ("test images/0b12f2389d.jpg", "Aloo Methi", "vegetable_curry"),
        ("test images/0f964b310f.jpg", "Chana Masala", "legume_curry"),
        ("test images/463454.jpg", "Dal Makhani", "legume_curry"),
        ("test images/4b37a397df.jpg", "Aloo Tikki", "snack"),
        ("test images/8d15768f3d.jpg", "Biryani", "rice_dish"),
        ("images/masking.png", "Chapati", "bread"),
    ]

    for rel_path, title, category in sample_paths:
        full_path = BASE_DIR / rel_path
        if full_path.exists():
            try:
                # generate small base64 thumbnail
                with Image.open(full_path) as im:
                    thumb = im.copy()
                    thumb.thumbnail((160, 160))
                    buf = io.BytesIO()
                    thumb.convert("RGB").save(buf, format="JPEG", quality=75)
                    thumb_b64 = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
                
                samples.append({
                    "id": rel_path.replace("\\", "/"),
                    "title": title,
                    "category": category,
                    "thumbnail": thumb_b64,
                })
            except Exception:
                continue

    return {"status": "success", "samples": samples}


@app.post("/api/analyze")
async def analyze_food(
    file: Optional[UploadFile] = File(None),
    sample_path: Optional[str] = Form(None),
    food_id: Optional[str] = Form(None),
    vessel_type: Optional[str] = Form(None),
):
    """
    Analyzes an uploaded image or preloaded sample image.
    Executes vessel classification, portion segmentation, food recognition,
    and returns calorie/macronutrient breakdown with mask overlays.
    """
    try:
        if file and file.filename:
            content = await file.read()
            img = Image.open(io.BytesIO(content)).convert("RGB")
            filename = file.filename
        elif sample_path:
            full_path = BASE_DIR / sample_path
            if not full_path.exists():
                raise HTTPException(status_code=400, detail=f"Sample '{sample_path}' not found.")
            img = Image.open(full_path).convert("RGB")
            filename = full_path.name
        else:
            raise HTTPException(status_code=400, detail="No image provided. Upload a file or select a sample.")

        vessel_override = vessel_type if vessel_type in ("plate", "bowl") else None
        food_override = food_id if food_id and food_id in engine.df.index else None

        result = engine.estimate(
            img,
            chosen_food_id=food_override,
            vessel_type_override=vessel_override
        )
        result["filename"] = filename

        # Save JSON output in results directory
        clean_json = {k: v for k, v in result.items() if k != "images"}
        json_path = RESULTS_DIR / f"{Path(filename).stem}_result.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(clean_json, f, indent=2)

        # Generate report image in outputs directory
        fig_path = OUTPUTS_DIR / f"{Path(filename).stem}_analysis.png"
        engine.generate_report_figure(result, fig_path)

        return {
            "status": "success",
            "result": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/figure/{stem}")
async def download_figure(stem: str):
    """Download generated 3-panel visualization PNG."""
    fig_path = OUTPUTS_DIR / f"{stem}_analysis.png"
    if not fig_path.exists():
        raise HTTPException(status_code=404, detail="Figure not found.")
    return FileResponse(
        fig_path,
        media_type="image/png",
        filename=f"calorie_lens_{stem}_analysis.png"
    )


@app.get("/api/download/json/{stem}")
async def download_json(stem: str):
    """Download analysis JSON result."""
    json_path = RESULTS_DIR / f"{stem}_result.json"
    if not json_path.exists():
        raise HTTPException(status_code=404, detail="Result JSON not found.")
    return FileResponse(
        json_path,
        media_type="application/json",
        filename=f"calorie_lens_{stem}_result.json"
    )
