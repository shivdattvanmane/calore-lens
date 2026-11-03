"""
run_calorie_lens.py - CLI Runner for Calorie Lens
=================================================
Usage:
    python run_calorie_lens.py
    python run_calorie_lens.py --image "test images/000004.jpg"
    python run_calorie_lens.py --image "images/aloo methi.png" --food aloo_methi --vessel plate
"""

import os
import sys
import json
import argparse
from pathlib import Path
from calorie_lens_engine import engine, OUTPUTS_DIR, RESULTS_DIR


def format_console_report(result: dict) -> str:
    n = result["nutrients"]
    p = result["portion"]
    v = result["vessel"]
    food_name = result["food_name"]
    weight = p["weight_g"]
    cal_lo, cal_hi = n["calories_range"]

    lines = []
    lines.append("=" * 54)
    lines.append(f"  CALORIE LENS: {result['filename']}")
    lines.append("=" * 54)
    lines.append(f"  Food Item   : {food_name}  (conf: {result['food_conf']:.1%})")
    lines.append(f"  Category    : {result['category']}")
    lines.append(f"  Vessel      : {v['name']} ({v['diameter_cm']}cm, fill: {p['area_percent']:.1f}%)")
    lines.append(f"  Est. Weight : {weight} g  (x{p['fill_ratio']:.2f} standard serving)")
    lines.append("-" * 54)
    lines.append(f"  {'Nutrient':<22} {'Portion Amount':>14}  {'Per 100g':>12}")
    lines.append("  " + "-" * 50)

    p100 = n["per_100g"]
    rows = [
        ("Calories (kcal)", f"{n['calories_kcal']} kcal", f"{p100['calories']} kcal"),
        ("Protein (g)", f"{n['protein_g']} g", f"{p100['protein']} g"),
        ("Carbohydrates (g)", f"{n['carbohydrates_g']} g", f"{p100['carbs']} g"),
        ("Fat (g)", f"{n['fat_g']} g", f"{p100['fat']} g"),
        ("Dietary Fiber (g)", f"{n['fiber_g']} g", f"{p100['fiber']} g"),
    ]
    for label, amount, per100 in rows:
        lines.append(f"  {label:<22} {amount:>14}  {per100:>12}")

    lines.append("-" * 54)
    lines.append(f"  Caloric Density: {n['cal_per_g']} kcal/g  ({n['food_type']})")
    lines.append(f"  Calorie Range  : {cal_lo} - {cal_hi} kcal  (+-{n['uncertainty_pct']}%)")
    lines.append(f"  Energy Split   : {n['energy_breakdown']['protein_pct']}% Protein | {n['energy_breakdown']['carbs_pct']}% Carbs | {n['energy_breakdown']['fat_pct']}% Fat")
    lines.append("=" * 54)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Calorie Lens - Indian Food Calorie & Nutrient Estimator")
    parser.add_argument("--image", default=None, help="Path to input food image")
    parser.add_argument("--food", default=None, help="Override food item id (e.g. aloo_methi, biryani)")
    parser.add_argument("--vessel", choices=["plate", "bowl", "auto"], default=None, help="Vessel type override")
    parser.add_argument("--no-fig", action="store_true", help="Skip saving 3-panel figure")
    parser.add_argument("--json", action="store_true", help="Print raw JSON output")
    args = parser.parse_args()

    image_path = args.image
    if not image_path:
        default_samples = [
            "test images/000004.jpg",
            "images/aloo methi.png",
            "images/laddu.png",
            "test images/53223.jpg",
            "test images/0b12f2389d.jpg"
        ]
        existing = [p for p in default_samples if Path(p).exists()]
        default_choice = existing[0] if existing else "test images/000004.jpg"

        print("\n=== CALORIE LENS: INDIAN FOOD NUTRIENT ESTIMATOR ===")
        print(f"Sample images found: {len(existing)}")
        user_input = input(f"Enter image path (or press Enter for default '{default_choice}'): ").strip()
        image_path = user_input if user_input else default_choice

    img_file = Path(image_path)
    if not img_file.exists():
        print(f"Error: Image '{image_path}' not found.", file=sys.stderr)
        sys.exit(1)

    vessel_override = None if args.vessel in (None, "auto") else args.vessel
    result = engine.estimate(
        img_file,
        chosen_food_id=args.food,
        vessel_type_override=vessel_override
    )

    # Print formatted report
    report_text = format_console_report(result)
    print("\n" + report_text)

    # Save JSON result (excluding base64 image blobs to keep it clean)
    clean_json = {k: v for k, v in result.items() if k != "images"}
    json_path = RESULTS_DIR / f"{img_file.stem}_result.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(clean_json, f, indent=2)
    print(f"\n[+] Results JSON saved to -> {json_path}")

    # Generate visualization figure
    if not args.no_fig:
        fig_path = OUTPUTS_DIR / f"{img_file.stem}_analysis.png"
        engine.generate_report_figure(result, fig_path)
        print(f"[+] Visualization figure saved to -> {fig_path}")

    if args.json:
        print("\n--- JSON OUTPUT ---")
        print(json.dumps(clean_json, indent=2))


if __name__ == "__main__":
    main()
