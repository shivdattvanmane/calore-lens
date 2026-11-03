"""
build_presentation.py
Generates the complete 12-slide academic presentation for Calorie Lens
with embedded speaker notes, exact 16:9 widescreen layout, custom visual hierarchy,
and genuine project screenshots.
"""

import os
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── COLOR PALETTE DEFINITION ──────────────────────────────────────────
# Academic Minimal Theme: Crisp white/light grey, Deep Navy, Muted Teal, Slate
COLOR_BG_LIGHT     = RGBColor(248, 250, 252) # #F8FAFC (Slate-50)
COLOR_WHITE        = RGBColor(255, 255, 255) # #FFFFFF
COLOR_NAVY         = RGBColor(15, 23, 42)    # #0F172A (Slate-900 / Deep Navy)
COLOR_TEXT_BODY    = RGBColor(51, 65, 85)    # #334155 (Slate-700 / Charcoal)
COLOR_TEXT_MUTED   = RGBColor(100, 116, 139) # #64748B (Slate-500)
COLOR_TEAL_ACCENT  = RGBColor(13, 148, 136)  # #0D9488 (Teal-600)
COLOR_TEAL_LIGHT   = RGBColor(240, 253, 250) # #F0FDFA (Teal-50)
COLOR_BLUE_ACCENT  = RGBColor(2, 132, 199)   # #0284C7 (Sky-600)
COLOR_BLUE_LIGHT   = RGBColor(240, 249, 255) # #F0F9FF (Sky-50)
COLOR_CARD_BORDER  = RGBColor(226, 232, 240) # #E2E8F0 (Slate-200)
COLOR_CARD_BG      = RGBColor(255, 255, 255)
COLOR_ALERT_BG     = RGBColor(254, 242, 242) # #FEF2F2 (Rose-50)
COLOR_ALERT_BORDER = RGBColor(254, 205, 205) # #FECACA
COLOR_ALERT_TEXT   = RGBColor(153, 27, 27)   # #991B1B

FONT_HEADING = "Arial"
FONT_BODY    = "Calibri"

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # completely blank layout

    def add_background(slide):
        # Full slide subtle background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG_LIGHT
        bg.line.fill.background() # no border
        return bg

    def add_header(slide, section_tag: str, title: str, subtitle: str = ""):
        # Subtle accent pill for section
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(2.8), Inches(0.32))
        pill.fill.solid()
        pill.fill.fore_color.rgb = COLOR_TEAL_LIGHT
        pill.line.color.rgb = COLOR_TEAL_ACCENT
        pill.line.width = Pt(1)
        tf_pill = pill.text_frame
        tf_pill.word_wrap = True
        tf_pill.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_pill = tf_pill.paragraphs[0]
        p_pill.text = section_tag.upper()
        p_pill.font.name = FONT_HEADING
        p_pill.font.size = Pt(8.5)
        p_pill.font.bold = True
        p_pill.font.color.rgb = COLOR_TEAL_ACCENT
        p_pill.alignment = PP_ALIGN.CENTER

        # Main Slide Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.55))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.name = FONT_HEADING
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_NAVY

        # Subtitle if present
        if subtitle:
            tb_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.24), Inches(11.7), Inches(0.35))
            tf_sub = tb_sub.text_frame
            tf_sub.word_wrap = True
            tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle
            p_sub.font.name = FONT_BODY
            p_sub.font.size = Pt(11.5)
            p_sub.font.color.rgb = COLOR_TEXT_MUTED

    def add_footer(slide, slide_num: int, total_slides: int = 12):
        # Subtle divider line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_CARD_BORDER
        line.line.fill.background()

        # Footer Left text
        tb_l = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(7.0), Inches(0.3))
        tf_l = tb_l.text_frame
        tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
        p_l = tf_l.paragraphs[0]
        p_l.text = "Calorie Lens: AI-Based Food Recognition & Calorie Estimation | Department Project Review"
        p_l.font.name = FONT_BODY
        p_l.font.size = Pt(8.5)
        p_l.font.color.rgb = COLOR_TEXT_MUTED

        # Footer Right text
        tb_r = slide.shapes.add_textbox(Inches(8.5), Inches(7.05), Inches(4.033), Inches(0.3))
        tf_r = tb_r.text_frame
        tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
        p_r = tf_r.paragraphs[0]
        p_r.text = f"Slide {slide_num} of {total_slides}"
        p_r.font.name = FONT_BODY
        p_r.font.size = Pt(8.5)
        p_r.font.color.rgb = COLOR_TEXT_MUTED
        p_r.alignment = PP_ALIGN.RIGHT

    def add_card(slide, left, top, width, height, title="", title_color=COLOR_NAVY, bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)

        if title:
            tb = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.15), Inches(width - 0.4), Inches(0.35))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = FONT_HEADING
            p.font.size = Pt(12.5)
            p.font.bold = True
            p.font.color.rgb = title_color
        return card

    def set_speaker_notes(slide, notes_text: str):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_background(s1)

    # Left Container: Project Title & Details
    left_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(7.2), Inches(5.9))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = COLOR_WHITE
    left_card.line.color.rgb = COLOR_CARD_BORDER
    left_card.line.width = Pt(1)

    # Category Pill
    pill1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.2), Inches(3.2), Inches(0.35))
    pill1.fill.solid()
    pill1.fill.fore_color.rgb = COLOR_TEAL_LIGHT
    pill1.line.color.rgb = COLOR_TEAL_ACCENT
    pill1.line.width = Pt(1)
    tf1 = pill1.text_frame
    tf1.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf1.paragraphs[0]
    p.text = "MAJOR ENGINEERING PROJECT REVIEW"
    p.font.name = FONT_HEADING
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL_ACCENT
    p.alignment = PP_ALIGN.CENTER

    # Title Textbox
    tb_t1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.7), Inches(6.4), Inches(1.8))
    tf_t1 = tb_t1.text_frame
    tf_t1.word_wrap = True
    p = tf_t1.paragraphs[0]
    p.text = "CALORIE LENS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    p2 = tf_t1.add_paragraph()
    p2.text = "AI-Based Food Recognition and Calorie Estimation Using Computer Vision"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(15)
    p2.font.color.rgb = COLOR_BLUE_ACCENT
    p2.space_before = Pt(8)

    # Metadata Placeholders
    tb_meta = s1.shapes.add_textbox(Inches(1.2), Inches(3.6), Inches(6.4), Inches(2.8))
    tf_meta = tb_meta.text_frame
    tf_meta.word_wrap = True

    meta_items = [
        ("Presented by", "[Student Name] (Roll No: [XXXXXX])"),
        ("Department", "Department of Computer Science & Engineering"),
        ("College", "[College / Institute Name]"),
        ("Guided by", "[Guide / Faculty Supervisor Name]"),
        ("Academic Year", "2025 – 2026"),
        ("Repository", "https://github.com/SHIVANSH-BHARTI2002/Calorie-Lens")
    ]
    for i, (label, val) in enumerate(meta_items):
        p = tf_meta.paragraphs[0] if i == 0 else tf_meta.add_paragraph()
        run1 = p.add_run()
        run1.text = f"{label:16}:  "
        run1.font.bold = True
        run1.font.name = FONT_HEADING
        run1.font.size = Pt(11)
        run1.font.color.rgb = COLOR_NAVY
        run2 = p.add_run()
        run2.text = val
        run2.font.name = FONT_BODY
        run2.font.size = Pt(11)
        run2.font.color.rgb = COLOR_TEXT_BODY
        p.space_after = Pt(4)

    # Right Image Frame: Authentic Food Plate
    img_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(0.8), Inches(4.2), Inches(5.9))
    img_card.fill.solid()
    img_card.fill.fore_color.rgb = COLOR_WHITE
    img_card.line.color.rgb = COLOR_CARD_BORDER
    img_card.line.width = Pt(1)

    food_img_path = IMAGES_DIR / "aloo methi.png"
    if food_img_path.exists():
        s1.shapes.add_picture(str(food_img_path), Inches(8.5), Inches(1.1), width=Inches(3.8))

    # Caption beneath image
    tb_cap = s1.shapes.add_textbox(Inches(8.5), Inches(4.8), Inches(3.8), Inches(1.7))
    tf_cap = tb_cap.text_frame
    tf_cap.word_wrap = True
    p = tf_cap.paragraphs[0]
    p.text = "Target Domain: Indian Regional Cuisine"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p_cap2 = tf_cap.add_paragraph()
    p_cap2.text = "Automated dietary assessment through deep learning classification, tableware identification, instance segmentation, and calibrated nutrient lookup."
    p_cap2.font.name = FONT_BODY
    p_cap2.font.size = Pt(9.5)
    p_cap2.font.color.rgb = COLOR_TEXT_MUTED
    p_cap2.space_before = Pt(3)

    set_speaker_notes(s1, """[SLIDE 1 — TITLE SLIDE]
Speaking Time: ~45 seconds

Good morning respected Head of Department, Course Coordinator, faculty members, and fellow students.
I am pleased to present our major engineering project titled "CALORIE LENS: AI-Based Food Recognition and Calorie Estimation Using Computer Vision."

The primary goal of this project is to address a significant challenge in personal health informatics: automatically identifying Indian cuisine from a single photograph, estimating the serving portion weight using instance segmentation, and calculating calories and macronutrients scaled to the actual meal size.

Transition to next slide:
Before looking at our technical implementation, let us look at why manual dietary tracking fails and why Indian cuisine is uniquely challenging for computer vision.""")

    # =========================================================================
    # SLIDE 2: INTRODUCTION & BACKGROUND
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_background(s2)
    add_header(s2, "Project Context & Motivation", "Introduction: The Dietary Tracking Bottleneck", "Why computer vision is necessary for automated, friction-free nutrition monitoring")
    add_footer(s2, 2)

    # 3 Column Layout
    col_w = Inches(3.64)
    # Column 1: Traditional Logging Friction
    add_card(s2, 0.8, 1.7, 3.64, 5.0, "The Nutrition Tracking Gap", COLOR_NAVY)
    tb_c1 = s2.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(3.24), Inches(4.3))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    bullets_c1 = [
        ("Rising Lifestyle Diseases", "Conditions like Type-2 diabetes, hypertension, and obesity demand consistent, long-term calorie and macronutrient monitoring."),
        ("High Manual Friction", "Current apps require manual searching, barcode scanning (which fails for unpackaged home meals), and physical weighing scales."),
        ("High Abandonment Rate", "Over 70% of users abandon dietary tracking apps within 30 days due to the daily cognitive load of logging ingredients manually."),
        ("2D Image Ambiguity", "Photographs capture flat 2D projections. Translating visual appearance into 3D portion volume is fundamentally ill-posed.")
    ]
    for i, (b_title, b_desc) in enumerate(bullets_c1):
        p = tf_c1.paragraphs[0] if i == 0 else tf_c1.add_paragraph()
        r1 = p.add_run()
        r1.text = f"•  {b_title}: "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.name = FONT_HEADING
        r1.font.color.rgb = COLOR_NAVY
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10)
        r2.font.name = FONT_BODY
        r2.font.color.rgb = COLOR_TEXT_BODY
        p.space_after = Pt(8)

    # Column 2: The Indian Cuisine Challenge
    add_card(s2, 4.84, 1.7, 3.64, 5.0, "Why Indian Food is Challenging", COLOR_NAVY)
    tb_c2 = s2.shapes.add_textbox(Inches(5.04), Inches(2.2), Inches(3.24), Inches(4.3))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    bullets_c2 = [
        ("Complex Gravies & Mixtures", "Dishes like Dal Makhani, Dal Tadka, and Curries lack rigid geometric boundaries, appearing as amorphous fluid mixtures."),
        ("High Intra-Class Variance", "The same dish (e.g., Paneer Butter Masala) varies dramatically in color, texture, and oil sheen across regions and restaurants."),
        ("Inter-Class Visual Similarity", "Dishes with identical yellow/red gravy bases (Aloo Gobi vs. Aloo Matar) look almost indistinguishable to standard classifiers."),
        ("Hidden Caloric Density", "High-calorie components (ghee, butter, hidden sugar syrups) alter calories drastically without changing visible plate area.")
    ]
    for i, (b_title, b_desc) in enumerate(bullets_c2):
        p = tf_c2.paragraphs[0] if i == 0 else tf_c2.add_paragraph()
        r1 = p.add_run()
        r1.text = f"•  {b_title}: "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.name = FONT_HEADING
        r1.font.color.rgb = COLOR_NAVY
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10)
        r2.font.name = FONT_BODY
        r2.font.color.rgb = COLOR_TEXT_BODY
        p.space_after = Pt(8)

    # Column 3: The AI & CV Solution
    add_card(s2, 8.88, 1.7, 3.64, 5.0, "The Calorie Lens Approach", COLOR_NAVY)
    # Image in Col 3
    sample_grid_path = IMAGES_DIR / "dataset sample images.png"
    if sample_grid_path.exists():
        s2.shapes.add_picture(str(sample_grid_path), Inches(9.08), Inches(2.2), width=Inches(3.24))

    tb_c3 = s2.shapes.add_textbox(Inches(9.08), Inches(4.8), Inches(3.24), Inches(1.8))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True
    p = tf_c3.paragraphs[0]
    p.text = "Automating the Analysis Pipeline:"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p_steps = tf_c3.add_paragraph()
    p_steps.text = "1. Food ID: ResNet50 transfer learning (51 classes)\n2. Vessel Context: EfficientNet plate vs. bowl\n3. Segmentation: Mask R-CNN pixel coverage\n4. Nutrient Lookup: Calibrated Indian Food CSV"
    p_steps.font.name = FONT_BODY
    p_steps.font.size = Pt(9.5)
    p_steps.font.color.rgb = COLOR_TEXT_BODY
    p_steps.space_before = Pt(4)

    set_speaker_notes(s2, """[SLIDE 2 — INTRODUCTION & BACKGROUND]
Speaking Time: ~50 seconds

Managing one's diet is fundamental to preventing and managing lifestyle diseases such as diabetes and hypertension. However, most people abandon manual dietary logging apps within a month because typing every ingredient and weighing food is tedious.

Furthermore, Western dietary apps like MyFitnessPal rely heavily on barcode scanning, which completely fails for Indian home-cooked meals and street food.

Indian food presents three unique computer vision challenges:
First, amorphous geometry—curries and dals do not have rigid shapes like an apple or a sandwich.
Second, visual similarity—a bowl of Dal Tadka and Dal Makhani can look almost identical in low lighting.
Third, hidden calories—ghee and oil contribute significant calories without dramatically altering the 2D surface area.

Calorie Lens solves this by utilizing deep transfer learning for dish identification, tableware context detection, and instance segmentation to estimate portion coverage.

Transition to next slide:
Let us now clearly define our problem statement, formal objectives, and project boundaries.""")

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT, OBJECTIVES & SCOPE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_background(s3)
    add_header(s3, "Problem Definition & Engineering Scope", "Problem Statement, Objectives, and Scope", "Formal definition of the research problem, six engineering goals, and technical boundaries")
    add_footer(s3, 3)

    # 2 Column Split (5.7 inches each)
    # Column 1: Problem Statement
    add_card(s3, 0.8, 1.7, 5.7, 3.8, "Problem Statement", COLOR_NAVY)
    tb_prob = s3.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.3), Inches(3.1))
    tf_prob = tb_prob.text_frame
    tf_prob.word_wrap = True

    p = tf_prob.paragraphs[0]
    p.text = "Core Engineering Problem:"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_ACCENT

    p_ptext = tf_prob.add_paragraph()
    p_ptext.text = '"Manual calorie tracking depends on knowing both the exact food item and its consumed quantity. Accurately estimating both from a single 2D photograph is challenging due to perspective distortion, absence of depth information, and the amorphous nature of regional Indian dishes."'
    p_ptext.font.name = FONT_BODY
    p_ptext.font.size = Pt(10.5)
    p_ptext.font.italic = True
    p_ptext.font.color.rgb = COLOR_TEXT_BODY
    p_ptext.space_before = Pt(4)
    p_ptext.space_after = Pt(8)

    p_keys = tf_prob.add_paragraph()
    p_keys.text = "Key Technical Bottlenecks:"
    p_keys.font.name = FONT_HEADING
    p_keys.font.size = Pt(10.5)
    p_keys.font.bold = True
    p_keys.font.color.rgb = COLOR_NAVY

    prob_bullets = [
        "Scale Ambiguity: A 2D pixel count has no physical meaning without a reference object or known vessel size.",
        "Visual Homogeneity: Regional Indian gravies share similar color distributions despite having distinct nutritional profiles.",
        "Segmentation Overlap: Differentiating where the food boundary ends and the plate boundary begins."
    ]
    for pb in prob_bullets:
        p_b = tf_prob.add_paragraph()
        p_b.text = f"•  {pb}"
        p_b.font.name = FONT_BODY
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = COLOR_TEXT_BODY
        p_b.space_before = Pt(2)

    # Column 2: Six Structured Objectives
    add_card(s3, 6.8, 1.7, 5.7, 3.8, "Project Objectives", COLOR_NAVY)
    tb_obj = s3.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(3.1))
    tf_obj = tb_obj.text_frame
    tf_obj.word_wrap = True

    objectives = [
        ("1. Food Classification", "Fine-tune ResNet50 to accurately identify 51 distinct classes of Indian cuisine from a single image."),
        ("2. Tableware Identification", "Classify container geometry (Plate vs. Bowl) using EfficientNet to establish baseline physical dimensions."),
        ("3. Instance Segmentation", "Segment food and container boundaries using Mask R-CNN to extract relative surface area coverage."),
        ("4. Calibrated Portion Estimation", "Derive estimated weight (grams) using food-to-vessel area fractions and expected fill ratios."),
        ("5. Curated Nutritional Scaling", "Map predicted weight to verified per-100g nutritional dataset, computing calories, protein, carbs, fat, and fiber."),
        ("6. Confidence & Range Reporting", "Output a confidence-bounded calorie range (±10% to ±18%) acknowledging natural preparation variance.")
    ]
    for i, (o_title, o_desc) in enumerate(objectives):
        p = tf_obj.paragraphs[0] if i == 0 else tf_obj.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{o_title}: "
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.name = FONT_HEADING
        r1.font.color.rgb = COLOR_NAVY
        r2 = p.add_run()
        r2.text = o_desc
        r2.font.size = Pt(9)
        r2.font.name = FONT_BODY
        r2.font.color.rgb = COLOR_TEXT_BODY
        p.space_after = Pt(2)

    # Bottom Full-Width Scope Card
    add_card(s3, 0.8, 5.65, 11.7, 1.25, "System Scope & Boundaries", COLOR_NAVY)
    tb_sc = s3.shapes.add_textbox(Inches(1.0), Inches(5.95), Inches(11.3), Inches(0.85))
    tf_sc = tb_sc.text_frame
    tf_sc.word_wrap = True

    p = tf_sc.paragraphs[0]
    r_in = p.add_run()
    r_in.text = "IN SCOPE: "
    r_in.font.bold = True
    r_in.font.name = FONT_HEADING
    r_in.font.size = Pt(9.5)
    r_in.font.color.rgb = COLOR_TEAL_ACCENT
    r_in_text = p.add_run()
    r_in_text.text = "Single-dish overhead/angled images; standard round plates (~25cm) and bowls (~15cm); 51 popular Indian dishes; relative surface area heuristic portion calculation; REST API and web UI.\n"
    r_in_text.font.name = FONT_BODY
    r_in_text.font.size = Pt(9.5)
    r_in_text.font.color.rgb = COLOR_TEXT_BODY

    p2 = tf_sc.add_paragraph()
    r_out = p2.add_run()
    r_out.text = "OUT OF SCOPE: "
    r_out.font.bold = True
    r_out.font.name = FONT_HEADING
    r_out.font.size = Pt(9.5)
    r_out.font.color.rgb = COLOR_ALERT_TEXT
    r_out_text = p2.add_run()
    r_out_text.text = "Multi-dish thali decomposition in a single pass; irregular/novel tableware; 3D volume reconstruction via LiDAR; clinical or laboratory-grade calorific verification."
    r_out_text.font.name = FONT_BODY
    r_out_text.font.size = Pt(9.5)
    r_out_text.font.color.rgb = COLOR_TEXT_BODY

    set_speaker_notes(s3, """[SLIDE 3 — PROBLEM STATEMENT, OBJECTIVES & SCOPE]
Speaking Time: ~50 seconds

Here is our formal problem statement:
Manual calorie tracking requires the user to know both what they are eating and how much it weighs. Estimating both from a flat photograph is an ill-posed mathematical problem because depth is lost.

To tackle this systematically, we formulated six concrete technical objectives:
First: Classify the food across 51 Indian dish categories using ResNet50.
Second: Identify whether the food is served on a plate or in a bowl using EfficientNet.
Third: Segment the food object and container using Mask R-CNN.
Fourth: Calculate the food-to-vessel pixel ratio to estimate portion mass in grams.
Fifth: Scale per-100g nutritional facts from our curated CSV database.
Sixth: Provide a realistic uncertainty range rather than an overconfident single number.

Equally important is our scope:
We explicitly scope this project to single-dish meals served in standard dining plates or bowls. We do not claim 3D point cloud volume reconstruction or multi-item thali separation in this first release.

Transition to next slide:
Let us now examine the verified technology stack and deep learning frameworks powering this architecture.""")

    # =========================================================================
    # SLIDE 4: TECHNOLOGY STACK
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_background(s4)
    add_header(s4, "System Implementation & Tooling", "Verified Technology Stack & Library Roles", "Hardware, frameworks, and models verified directly against repository codebase")
    add_footer(s4, 4)

    # 3-Column Structured Table
    rows = 11
    cols = 3
    left = Inches(0.8)
    top = Inches(1.7)
    width = Inches(11.733)
    height = Inches(5.1)

    table_shape = s4.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(3.4)
    table.columns[2].width = Inches(5.733)

    tech_data = [
        ("Technology / Tool", "Technical Role in Project", "Implementation Detail & Ground Truth Verification"),
        ("Python 3.9+", "Primary Programming Language", "Core pipeline scripting, async server execution, and numerical data processing."),
        ("TensorFlow / Keras", "Deep Learning Framework", "Training & inference execution for ResNet50 (food) and EfficientNet (vessel)."),
        ("PyTorch & Torchvision", "Segmentation Framework", "Executes Mask R-CNN with ResNet50-FPN backbone and default COCO weights."),
        ("ResNet50 (Fine-tuned)", "Food Image Classifier", "51 Indian food classes; 224x224 input; trained with categorical cross-entropy (~72% val acc)."),
        ("EfficientNetB4", "Vessel Binary Classifier", "Classifies tableware as plate vs. bowl (224x224 input, ~92% val accuracy)."),
        ("Mask R-CNN (COCO)", "Instance Segmentation Model", "Segments tableware (COCO labels 47/51) and food foreground mask (score threshold 0.50)."),
        ("OpenCV & Pillow", "Image Processing Libraries", "Image decoding, resizing, color space conversions (RGB/BGR/HSV), and mask visualization."),
        ("NumPy & Pandas", "Numerical & Data Handling", "Vectorized pixel mask operations, ratio computations, and CSV nutrition database indexing."),
        ("FastAPI & Uvicorn", "Interactive Web Application", "REST API backend providing asynchronous single-image analysis and interactive browser UI."),
        ("Curated Nutrition CSV", "Nutritional Reference Database", "54-row verified reference dataset mapping food items to calories, protein, carbs, fat, fiber.")
    ]

    for r_idx, row in enumerate(tech_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_HEADING if r_idx == 0 else FONT_BODY
            p.font.size = Pt(10 if r_idx == 0 else 9)
            p.alignment = PP_ALIGN.CENTER if (c_idx == 0 and r_idx == 0) else PP_ALIGN.LEFT

            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_NAVY
                p.font.bold = True
                p.font.color.rgb = COLOR_WHITE
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_WHITE if r_idx % 2 == 1 else RGBColor(241, 245, 249)
                p.font.color.rgb = COLOR_NAVY if c_idx == 0 else COLOR_TEXT_BODY
                if c_idx == 0:
                    p.font.bold = True

    set_speaker_notes(s4, """[SLIDE 4 — TECHNOLOGY STACK]
Speaking Time: ~50 seconds

This slide outlines our verified technology stack. Every library and model listed here has been confirmed directly in our repository source code.

For our core programming environment, we use Python 3.9.
In terms of deep learning frameworks, we use a hybrid design:
TensorFlow and Keras are used for our classification models:
1. ResNet50, fine-tuned on 51 Indian food classes.
2. EfficientNetB4, trained as a binary classifier to distinguish plates from bowls.

For instance segmentation, we use PyTorch and Torchvision running Mask R-CNN with a ResNet50 Feature Pyramid Network backbone. This model is pre-trained on COCO and identifies vessels and foreground food regions.

For image manipulation and data operations, we utilize OpenCV, Pillow, NumPy, and Pandas.
For deployment, we built a modern FastAPI web server that accepts image uploads and serves dynamic nutrition breakdowns.

Notice an important engineering consideration: loading both TensorFlow and PyTorch onto GPU memory simultaneously can cause out-of-memory errors on modest GPUs like an RTX 3050 with 4GB VRAM. In our implementation, we enable TensorFlow memory growth and load Mask R-CNN lazily only after classification predictions finish.

Transition to next slide:
Now, let us examine how these components connect in our end-to-end System Architecture.""")

    # =========================================================================
    # SLIDE 5: SYSTEM ARCHITECTURE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_background(s5)
    add_header(s5, "End-to-End Engineering Pipeline", "System Architecture & Execution Pipeline", "Multi-stage pipeline connecting image preprocessing, dual classifiers, segmentation, and nutrient lookup")
    add_footer(s5, 5)

    # 6 Step Flow Cards Horizontally / Grid
    # Row 1: 3 Cards (Step 1, Step 2, Step 3)
    card_w = Inches(3.64)
    card_h = Inches(2.35)

    # Stage 1: Input & Preprocessing
    add_card(s5, 0.8, 1.7, 3.64, 2.35, "Stage 1: Preprocessing", COLOR_NAVY)
    tb = s5.shapes.add_textbox(Inches(0.95), Inches(2.1), Inches(3.34), Inches(1.85))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Input: Raw RGB photograph (any aspect ratio)\n• Food Branch: Resize 224x224, BGR conversion, zero-center with ImageNet mean\n• Vessel Branch: Resize 224x224, normalize [0, 1]\n• Output: Normalized 4D tensors for Keras"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_BODY

    # Stage 2: Dual Model Classification
    add_card(s5, 4.84, 1.7, 3.64, 2.35, "Stage 2: Dual Classification", COLOR_NAVY)
    tb = s5.shapes.add_textbox(Inches(4.99), Inches(2.1), Inches(3.34), Inches(1.85))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Food Classifier (ResNet50): Predicts food class across 51 categories (threshold: 0.40)\n• Vessel Classifier (EfficientNetB4): Predicts container type (Plate vs. Bowl, threshold: 0.50)\n• Output: (food_name, confidence) and (vessel_type)"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_BODY

    # Stage 3: Mask R-CNN Segmentation
    add_card(s5, 8.88, 1.7, 3.64, 2.35, "Stage 3: Instance Segmentation", COLOR_NAVY)
    tb = s5.shapes.add_textbox(Inches(9.03), Inches(2.1), Inches(3.34), Inches(1.85))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Model: Mask R-CNN (ResNet50-FPN, COCO)\n• Vessel Mask: Matches COCO labels 47 (cup) / 51 (bowl); fallback to 84% centered ellipse\n• Food Mask: Best foreground mask overlapping vessel > 20% and area > 500 px\n• Output: Binary food & vessel masks"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_BODY

    # Row 2: 3 Cards (Step 4, Step 5, Step 6)
    # Stage 4: Geometric Area Ratio
    add_card(s5, 0.8, 4.3, 3.64, 2.5, "Stage 4: Area Fraction", COLOR_NAVY)
    tb = s5.shapes.add_textbox(Inches(0.95), Inches(4.7), Inches(3.34), Inches(2.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Food Pixels (f_pix) & Vessel Pixels (v_pix)\n• Area Fraction = f_pix / v_pix (clamped [0.05, 1.0])\n• Reference Geometry:\n   - Plate: 25 cm diameter, expected fill = 0.65\n   - Bowl: 15 cm diameter, expected fill = 0.80\n• Fill Ratio = Area Fraction / Expected Fill"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_BODY

    # Stage 5: Weight Estimation
    add_card(s5, 4.84, 4.3, 3.64, 2.5, "Stage 5: Weight Estimation", COLOR_NAVY)
    tb = s5.shapes.add_textbox(Inches(4.99), Inches(4.7), Inches(3.34), Inches(2.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Lookup avg_serving_g from dataset for predicted food\n• Clamp Fill Ratio to [0.15, 2.0] to prevent outlier spikes\n• Formula: Est. Weight (g) = avg_serving_g * Fill Ratio\n• Output: Portion weight in grams"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_BODY

    # Stage 6: Nutrient Scaling & Output
    add_card(s5, 8.88, 4.3, 3.64, 2.5, "Stage 6: Calorie Output", COLOR_NAVY)
    tb = s5.shapes.add_textbox(Inches(9.03), Inches(4.7), Inches(3.34), Inches(2.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Scale per-100g database values by (Weight / 100)\n• Calculate Calories, Protein, Carbs, Fat, Fiber\n• Calorie Uncertainty Range: ±10% to ±18% based on food density profile\n• Output: Structured JSON + Web / Console Report"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_BODY

    set_speaker_notes(s5, """[SLIDE 5 — SYSTEM ARCHITECTURE]
Speaking Time: ~60 seconds

This diagram represents the core architecture of Calorie Lens. Let us trace a food photo as it flows through the six stages of our pipeline:

Stage 1: Preprocessing. The input image is converted into two distinct input streams. For food classification, it is resized to 224x224 and preprocessed using ResNet zero-centering. For vessel classification, it is normalized to values between 0 and 1.

Stage 2: Dual Classification. In parallel, ResNet50 determines the food identity across 51 Indian food classes, while EfficientNetB4 predicts whether the container is a plate or a bowl.

Stage 3: Instance Segmentation. PyTorch loads Mask R-CNN. It segments the container and the food. If tableware is obscured, our elliptical fallback algorithm creates a virtual container region covering 84% of the frame.

Stage 4: Geometric Area Ratio. We calculate the food pixels divided by vessel pixels. This gives us the surface coverage fraction. Because a plate is typically filled to 65% capacity and a bowl to 80% capacity, we compute the relative fill ratio.

Stage 5: Weight Estimation. We multiply the fill ratio by the baseline standard serving weight from our nutrition dataset. To prevent extreme errors, the fill ratio is constrained between 0.15 and 2.0.

Stage 6: Nutrient Scaling. Finally, per-100g nutrients from our curated database are scaled to this estimated weight, producing calories, macronutrients, and a confidence range.

Transition to next slide:
Let us examine Stage 2 in detail: Image Preprocessing and our ResNet50 classification model.""")

    # =========================================================================
    # SLIDE 6: IMAGE PREPROCESSING & FOOD CLASSIFICATION
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_background(s6)
    add_header(s6, "Machine Learning Methodology — Part 1", "Image Preprocessing & ResNet50 Food Classification", "Deep transfer learning with residual connections for 51 Indian food classes")
    add_footer(s6, 6)

    # Left: Explanation (5.7 in)
    add_card(s6, 0.8, 1.7, 5.7, 5.0, "Classification Pipeline & ResNet50 Architecture", COLOR_NAVY)
    tb_c6 = s6.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3))
    tf_c6 = tb_c6.text_frame
    tf_c6.word_wrap = True

    sections_c6 = [
        ("Preprocessing Pipeline", "Images are loaded via Pillow/Keras, bilinearly resized to 224x224x3. Preprocessing converts RGB to BGR and subtracts ImageNet channel means: [103.939, 116.779, 123.68]."),
        ("Why ResNet50 Architecture?", "Standard deep CNNs suffer from the vanishing gradient problem. ResNet introduces residual skip connections where the layer learns F(x) = H(x) - x. If performance degrades, identity mapping bypasses the layer, enabling effective training of 50 layers."),
        ("Transfer Learning Strategy", "Backbone initialized with ImageNet-1K pre-trained weights. Custom head added: GlobalAveragePooling2D -> Dense(256, relu) -> Dropout(0.4) -> Dense(51, softmax)."),
        ("Training Execution", "Trained on Kaggle GPU across 15 epochs. Base layers frozen during Phase 1, followed by progressive unfreezing of upper residual blocks with low learning rate (1e-4) to prevent catastrophic forgetting.")
    ]
    for i, (st, sd) in enumerate(sections_c6):
        p = tf_c6.paragraphs[0] if i == 0 else tf_c6.add_paragraph()
        r1 = p.add_run()
        r1.text = f"•  {st}: "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.name = FONT_HEADING
        r1.font.color.rgb = COLOR_NAVY
        r2 = p.add_run()
        r2.text = sd
        r2.font.size = Pt(9.5)
        r2.font.name = FONT_BODY
        r2.font.color.rgb = COLOR_TEXT_BODY
        p.space_after = Pt(8)

    # Right: Genuine Training Result Image
    add_card(s6, 6.8, 1.7, 5.7, 5.0, "Experimental Validation & Training Curves", COLOR_NAVY)
    food_curve_path = IMAGES_DIR / "food classification model result.png"
    if food_curve_path.exists():
        s6.shapes.add_picture(str(food_curve_path), Inches(7.0), Inches(2.2), width=Inches(5.3))

    tb_curve_desc = s6.shapes.add_textbox(Inches(7.0), Inches(4.5), Inches(5.3), Inches(2.0))
    tf_cd = tb_curve_desc.text_frame
    tf_cd.word_wrap = True
    p = tf_cd.paragraphs[0]
    p.text = "Verified Model Performance Metrics:"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    perf_points = [
        "Final Validation Accuracy: ~72% across 51 classes after 15 epochs.",
        "High-Performing Classes (>90% accuracy): Distinctive geometry & color like Jalebi, Biryani, Palak Paneer, and Bandar Laddu.",
        "Challenging Classes (<55% accuracy): Visual twins with similar curry bases such as Dal Makhani vs. Dal Tadka and Aloo Gobi vs. Aloo Matar.",
        "Confidence Gate: Predictions with confidence < 0.40 are flagged to avoid propagating incorrect nutritional estimates."
    ]
    for pp in perf_points:
        p_p = tf_cd.add_paragraph()
        p_p.text = f"•  {pp}"
        p_p.font.name = FONT_BODY
        p_p.font.size = Pt(9)
        p_p.font.color.rgb = COLOR_TEXT_BODY
        p_p.space_before = Pt(2)

    set_speaker_notes(s6, """[SLIDE 6 — IMAGE PREPROCESSING & FOOD CLASSIFICATION]
Speaking Time: ~55 seconds

Let us examine the classification engine.
For preprocessing, every image is resized to 224x224 pixels and processed using ResNet's standard zero-centering normalization, which converts RGB to BGR and subtracts ImageNet channel means.

Why did we select ResNet50?
In traditional deep convolutional networks, as depth increases, gradients diminish during backpropagation—known as the vanishing gradient problem. ResNet solves this through residual skip connections, allowing gradients to flow directly through the identity shortcut. This allows the network to learn rich, hierarchical visual features without degradation.

We used transfer learning: starting with ImageNet pre-trained weights, we attached a custom classification head featuring Global Average Pooling, a 256-unit dense layer, 40% dropout for regularization, and a 51-way softmax output.

Looking at the authentic training curves on the right, you can see steady convergence over 15 epochs, reaching approximately 72% validation accuracy.
Dishes with distinctive shapes or colors—like Jalebi, Palak Paneer, and Biryani—achieve over 90% accuracy. The primary errors occur between visually similar gravies, such as Dal Tadka versus Dal Makhani. We apply a confidence threshold of 0.40 to prevent propagating low-confidence errors.

Transition to next slide:
Knowing the food name alone is insufficient; we must also determine how much food is present. Let us look at Tableware Classification and Mask R-CNN Segmentation.""")

    # =========================================================================
    # SLIDE 7: VESSEL CLASSIFICATION & IMAGE SEGMENTATION
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_background(s7)
    add_header(s7, "Machine Learning Methodology — Part 2", "Tableware Classification & Mask R-CNN Instance Segmentation", "Contextual vessel classification and pixel-accurate instance mask generation")
    add_footer(s7, 7)

    # Left: Vessel Classification (5.7 in)
    add_card(s7, 0.8, 1.7, 5.7, 5.0, "Vessel Classification (EfficientNetB4)", COLOR_NAVY)
    tb_v = s7.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3))
    tf_v = tb_v.text_frame
    tf_v.word_wrap = True

    vessel_pts = [
        ("Role in the System", "To calibrate portion weight from a 2D image without an external reference coin or checkerboard, the system needs to know the physical container geometry."),
        ("Architecture & Training", "EfficientNetB4 utilizes compound scaling (balancing depth, width, and resolution). Binary classifier: 'food_in_plate' vs. 'food_in_bowl'. Trained on Kaggle dual T4 GPUs with MirroredStrategy."),
        ("Validation Accuracy: ~92%", "Achieved robust ~92% validation accuracy. Gradient clipping (clipnorm=1.0) was essential to prevent NaN loss during training."),
        ("Calibrated Tableware Dimensions", "• Standard Plate: 25.0 cm diameter, 490.9 cm² area, 75% usable surface, 0.65 expected fill ratio.\n• Standard Bowl: 15.0 cm diameter, 176.7 cm² area, 85% usable surface, 0.80 expected fill ratio.")
    ]
    for i, (vt, vd) in enumerate(vessel_pts):
        p = tf_v.paragraphs[0] if i == 0 else tf_v.add_paragraph()
        r1 = p.add_run()
        r1.text = f"•  {vt}: "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.name = FONT_HEADING
        r1.font.color.rgb = COLOR_NAVY
        r2 = p.add_run()
        r2.text = vd
        r2.font.size = Pt(9.5)
        r2.font.name = FONT_BODY
        r2.font.color.rgb = COLOR_TEXT_BODY
        p.space_after = Pt(6)

    # Right: Mask R-CNN Segmentation (5.7 in)
    add_card(s7, 6.8, 1.7, 5.7, 5.0, "Instance Segmentation (Mask R-CNN)", COLOR_NAVY)
    masking_img_path = IMAGES_DIR / "masking.png"
    if masking_img_path.exists():
        s7.shapes.add_picture(str(masking_img_path), Inches(7.0), Inches(2.15), width=Inches(5.3))

    tb_m = s7.shapes.add_textbox(Inches(7.0), Inches(4.1), Inches(5.3), Inches(2.4))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    p = tf_m.paragraphs[0]
    p.text = "How Mask R-CNN Segments Food:"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    m_pts = [
        "Architecture: ResNet50-FPN backbone with Region Proposal Network (RPN). Outputs bounding boxes, class labels, and binary pixel masks.",
        "COCO Pre-trained Weights: Identifies vessels using COCO labels 47 (cup) and 51 (bowl) at confidence >= 0.50.",
        "Food Mask Selection: Selects highest-scoring non-vessel mask covering > 500 pixels with >= 20% vessel overlap.",
        "Robust Elliptical Fallback: If no vessel is detected, a centered ellipse (covering 84% of frame) acts as the baseline container, ensuring zero runtime crashes."
    ]
    for mp in m_pts:
        p_m = tf_m.add_paragraph()
        p_m.text = f"•  {mp}"
        p_m.font.name = FONT_BODY
        p_m.font.size = Pt(9)
        p_m.font.color.rgb = COLOR_TEXT_BODY
        p_m.space_before = Pt(2)

    set_speaker_notes(s7, """[SLIDE 7 — VESSEL CLASSIFICATION & IMAGE SEGMENTATION]
Speaking Time: ~55 seconds

A major challenge in mobile calorie estimation is that we cannot assume the user carries a calibration card or reference coin. Instead, we use the dining tableware as our natural reference object.

To do this, we built a vessel classifier using EfficientNetB4, which achieves approximately 92% validation accuracy distinguishing plates from bowls. EfficientNet uses compound scaling, which balances network depth, width, and image resolution efficiently.

Knowing whether the vessel is a plate or bowl gives us calibrated physical dimensions:
A standard plate has a 25 cm diameter, while a standard bowl has a 15 cm diameter.

Next, on the right, you see our instance segmentation pipeline powered by Mask R-CNN with a ResNet50 Feature Pyramid Network.
Classification only tells us *what* is in the image; Mask R-CNN predicts *which specific pixels* belong to the food versus the container.

In the authentic project screenshot shown:
The left panel is the raw input.
The center panel shows the segmented food mask overlay (covering 63.9% of the plate).
The right panel displays the scaled nutritional bars.

If lighting or camera angle causes vessel detection to fail, our system automatically falls back to an elliptical region covering 84% of the frame. This guarantees the pipeline never crashes in production.

Transition to next slide:
Now, let us examine the exact mathematical formulation used to turn these segmented pixels into grams and calories.""")

    # =========================================================================
    # SLIDE 8: PORTION WEIGHT AND CALORIE ESTIMATION
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_background(s8)
    add_header(s8, "Mathematical Methodology & Formulation", "Portion Weight & Nutritional Scaling Formulation", "Converting 2D segmented pixel coverage into physical mass and scaled nutrients")
    add_footer(s8, 8)

    # 3 Structured Columns/Cards
    # Card 1: Mathematical Formulas (3.64 in)
    add_card(s8, 0.8, 1.7, 3.64, 5.0, "1. Mathematical Formulas", COLOR_NAVY)
    tb_f = s8.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(3.24), Inches(4.3))
    tf_f = tb_f.text_frame
    tf_f.word_wrap = True

    formulas = [
        ("Area Fraction (Af)", "Af = clamp(Food_Pixels / Vessel_Pixels, 0.05, 1.0)\nRepresents the 2D surface coverage of the food within the tableware boundary."),
        ("Fill Ratio (R_fill)", "R_fill = clamp(Af / Expected_Fill, 0.15, 2.0)\nExpected fill is 0.65 for plates and 0.80 for bowls. Clamped between 0.15x and 2.0x standard serving."),
        ("Estimated Weight (W)", "Weight (g) = avg_serving_g * R_fill\nScaled directly from the reference standard serving in the verified CSV dataset."),
        ("Calorie Calculation", "Calories = (Weight / 100) * Cal_per_100g\nMacronutrients (Protein, Carbs, Fat, Fiber) are scaled identically.")
    ]
    for i, (ft, fd) in enumerate(formulas):
        p = tf_f.paragraphs[0] if i == 0 else tf_f.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{ft}:\n"
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.name = FONT_HEADING
        r1.font.color.rgb = COLOR_BLUE_ACCENT
        r2 = p.add_run()
        r2.text = f"{fd}\n"
        r2.font.size = Pt(9)
        r2.font.name = FONT_BODY
        r2.font.color.rgb = COLOR_TEXT_BODY
        p.space_after = Pt(4)

    # Card 2: Concrete Step-by-Step Example (4.0 in)
    add_card(s8, 4.64, 1.7, 4.2, 5.0, "2. Step-by-Step Numerical Example", COLOR_NAVY)
    tb_ex = s8.shapes.add_textbox(Inches(4.84), Inches(2.2), Inches(3.8), Inches(4.3))
    tf_ex = tb_ex.text_frame
    tf_ex.word_wrap = True

    p = tf_ex.paragraphs[0]
    p.text = "Concrete Run: Aloo Methi in a Plate"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL_ACCENT

    steps = [
        "1. Classification Result: Dish = Aloo Methi (105 kcal/100g, avg serving = 140g). Vessel = Plate.",
        "2. Segmentation: Food pixels = 288,720; Vessel pixels = 400,000.",
        "3. Area Fraction: Af = 288,720 / 400,000 = 0.7218 (72.2% coverage).",
        "4. Fill Ratio: R_fill = 0.7218 / 0.65 = 1.111 (Serving is 11.1% larger than average).",
        "5. Estimated Portion Weight:\nW = 140g * 1.111 = 155.5 grams.",
        "6. Scaled Nutrients (Base per 100g -> Scaled to 155.5g):\n• Calories: (155.5 / 100) * 105 = 163.3 kcal\n• Protein: (155.5 / 100) * 3.0g = 4.7g\n• Carbs: (155.5 / 100) * 13.0g = 20.2g\n• Fat: (155.5 / 100) * 4.5g = 7.0g\n• Fiber: (155.5 / 100) * 4.0g = 6.2g",
        "7. Confidence Range: Uncertainty ±12% -> [143.7 kcal – 182.9 kcal]."
    ]
    for s in steps:
        p_s = tf_ex.add_paragraph()
        p_s.text = s
        p_s.font.name = FONT_BODY
        p_s.font.size = Pt(8.8)
        p_s.font.color.rgb = COLOR_TEXT_BODY
        p_s.space_before = Pt(3)

    # Card 3: Sources of Physical Uncertainty (3.49 in)
    add_card(s8, 9.04, 1.7, 3.49, 5.0, "3. Physical Uncertainty & Limits", COLOR_NAVY)
    tb_u = s8.shapes.add_textbox(Inches(9.24), Inches(2.2), Inches(3.09), Inches(4.3))
    tf_u = tb_u.text_frame
    tf_u.word_wrap = True

    unc_factors = [
        ("Loss of 3D Depth", "A single overhead photograph measures surface area, not depth. A shallow 1 cm spread and a deep 5 cm mound can yield identical 2D pixel areas."),
        ("Density Variations", "Solid sweets (e.g., Bandar Laddu, density ~0.74 g/cm³) vs. semi-liquids (Basundi, density ~1.03 g/cm³) possess differing mass-to-volume ratios."),
        ("Cooking Method Variance", "The quantity of cooking oil or clarified butter (ghee) used drastically shifts caloric density without visibly altering plate coverage."),
        ("Why Uncertainty Bounds Matter", "We explicitly present a bounded interval (e.g., 144–183 kcal) rather than an artificial single number.")
    ]
    for i, (ut, ud) in enumerate(unc_factors):
        p = tf_u.paragraphs[0] if i == 0 else tf_u.add_paragraph()
        r1 = p.add_run()
        r1.text = f"•  {ut}:\n"
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.name = FONT_HEADING
        r1.font.color.rgb = COLOR_ALERT_TEXT
        r2 = p.add_run()
        r2.text = f"{ud}\n"
        r2.font.size = Pt(8.8)
        r2.font.name = FONT_BODY
        r2.font.color.rgb = COLOR_TEXT_BODY
        p.space_after = Pt(4)

    set_speaker_notes(s8, """[SLIDE 8 — PORTION WEIGHT AND CALORIE ESTIMATION]
Speaking Time: ~60 seconds

This slide explains the exact mathematical bridge between raw segmented pixels and physical nutritional values.

In Box 1, you see our governing formulas:
1. The Area Fraction, A_f, is the ratio of segmented food pixels to vessel pixels, bounded between 0.05 and 1.0.
2. The Fill Ratio, R_fill, divides the area fraction by the expected fill baseline—which is 0.65 for plates and 0.80 for bowls. This fill ratio is clamped between 0.15 and 2.0 to eliminate unrealistic outliers.
3. Estimated Weight in grams is simply the baseline average serving weight multiplied by this fill ratio.
4. Nutritional scaling follows the standard formula: Estimated Weight divided by 100, multiplied by the nutrient value per 100 grams.

In Box 2, we show a concrete numerical run directly from our test results for Aloo Methi:
The model detects Aloo Methi in a plate.
The food covers 72.2% of the plate.
Since a standard serving corresponds to 65% coverage, this serving has a fill ratio of 1.111—meaning 11% larger than average.
Multiplying 140 grams baseline by 1.111 yields an estimated portion weight of 155.5 grams.
Scaling the CSV nutrients gives 163.3 calories, with a ±12% confidence interval of 144 to 183 kcal.

In Box 3, we emphasize honesty regarding physical limitations:
Single-camera 2D images cannot capture depth or density, and hidden cooking oils add calorie variance. That is precisely why Calorie Lens reports confidence ranges rather than misleading point estimates.

Transition to next slide:
Let us now examine genuine output reports and experimental results from our repository.""")

    # =========================================================================
    # SLIDE 9: OUTPUT AND RESULTS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_background(s9)
    add_header(s9, "Experimental Results & Verification", "System Outputs, Verified Metrics & Demonstration", "Genuine pipeline outputs, verified model metrics, and live demo procedure")
    add_footer(s9, 9)

    # Left: Genuine Output Screenshots (5.7 in)
    add_card(s9, 0.8, 1.7, 5.7, 5.0, "Genuine Pipeline Outputs (From Repository)", COLOR_NAVY)
    out1_path = IMAGES_DIR / "aloo methi output.png"
    out2_path = IMAGES_DIR / "laddu output.png"

    if out1_path.exists():
        s9.shapes.add_picture(str(out1_path), Inches(1.0), Inches(2.2), width=Inches(2.6))
    if out2_path.exists():
        s9.shapes.add_picture(str(out2_path), Inches(3.8), Inches(2.2), width=Inches(2.55))

    tb_out_desc = s9.shapes.add_textbox(Inches(1.0), Inches(4.3), Inches(5.3), Inches(2.2))
    tf_od = tb_out_desc.text_frame
    tf_od.word_wrap = True
    p = tf_od.paragraphs[0]
    p.text = "Analysis of Genuine Pipeline Outputs:"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    out_points = [
        "Aloo Methi Run: Plate detection -> 72.2% coverage -> 155.5g weight -> 163.3 kcal [143.7 - 182.9 kcal range].",
        "Bandar Laddu Run: Dessert classification -> 64.8% coverage -> 77.8g weight -> 350.1 kcal [287.1 - 413.1 kcal range].",
        "Consistent Structured Reporting: Outputs include macronutrient breakdown (Protein, Carbs, Fat, Fiber) and caloric density (kcal/g)."
    ]
    for op in out_points:
        p_op = tf_od.add_paragraph()
        p_op.text = f"•  {op}"
        p_op.font.name = FONT_BODY
        p_op.font.size = Pt(9)
        p_op.font.color.rgb = COLOR_TEXT_BODY
        p_op.space_before = Pt(2)

    # Right: Verified Metrics & Context (5.7 in)
    add_card(s9, 6.8, 1.7, 5.7, 5.0, "Verified Performance Metrics & Validation Context", COLOR_NAVY)
    tb_mctx = s9.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3))
    tf_mc = tb_mctx.text_frame
    tf_mc.word_wrap = True

    p = tf_mc.paragraphs[0]
    p.text = "Verified Model Performance Figures:"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_ACCENT

    perf_context = [
        ("ResNet50 Food Classification", "~72% Validation Accuracy across 51 Indian food classes on Kaggle validation split (15 epochs)."),
        ("EfficientNetB4 Vessel Classification", "~92% Validation Accuracy on binary classification ('food_in_plate' vs. 'food_in_bowl')."),
        ("CRITICAL DISTINCTION — What These Numbers Mean", "72% and 92% are CLASSIFICATION accuracies. They do NOT represent calorie estimation accuracy. Calorie estimation is an automated heuristic approximation with reported confidence bounds."),
        ("Multi-Modal Output Formats", "• Structured JSON (saved to results/ folder)\n• Terminal Console Report (with formatted tables)\n• Interactive Web UI (FastAPI + HTML5/CSS3 frontend)"),
        ("Standard Demonstration Procedure", "1. Execute run_web.bat or 'python app.py'\n2. Navigate to localhost:8000\n3. Upload photo or choose sample -> View live segmentation & nutrition card")
    ]
    for i, (pct, pcd) in enumerate(perf_context):
        p_c = tf_mc.add_paragraph()
        r1 = p_c.add_run()
        r1.text = f"•  {pct}: "
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.name = FONT_HEADING
        r1.font.color.rgb = COLOR_NAVY if "CRITICAL" not in pct else COLOR_ALERT_TEXT
        r2 = p_c.add_run()
        r2.text = pcd
        r2.font.size = Pt(9)
        r2.font.name = FONT_BODY
        r2.font.color.rgb = COLOR_TEXT_BODY
        p_c.space_before = Pt(3)

    set_speaker_notes(s9, """[SLIDE 9 — OUTPUT AND RESULTS]
Speaking Time: ~55 seconds

On this slide, we present the actual outputs generated by Calorie Lens, directly extracted from the project repository.

On the left, you see two authentic output cards:
The first is Aloo Methi, classified as a vegetable curry, estimated at 155.5 grams and 163.3 kcal.
The second is Bandar Laddu, classified as a dessert, estimated at 77.8 grams and 350.1 kcal.
Each output provides calories, a bounded confidence range, caloric density in kcal/gram, and individual macronutrient amounts.

Now, look at the right card, where we address our performance metrics with rigorous academic honesty:
Our ResNet50 food classifier achieved ~72% validation accuracy on the 51-class dataset.
Our EfficientNet vessel classifier achieved ~92% validation accuracy.

I want to emphasize a critical technical distinction that the HOD and Coordinator will appreciate:
These figures—72% and 92%—measure image classification accuracy on validation test splits. They are NOT calorie estimation accuracy.
Calorie estimation is a multi-step heuristic that depends on classification accuracy, segmentation quality, and standard vessel assumptions.

For demonstration, the user can either run inference from the command line using `python inference.py` or launch our interactive FastAPI web interface via `run_web.bat`.

Transition to next slide:
Let us now evaluate the practical applications, key advantages, and real-world engineering limitations of our approach.""")

    # =========================================================================
    # SLIDE 10: APPLICATIONS, ADVANTAGES & LIMITATIONS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_background(s10)
    add_header(s10, "Critical Engineering Evaluation", "Applications, Advantages, and Technical Limitations", "Balanced assessment of practical utility, competitive benefits, and operational boundaries")
    add_footer(s10, 10)

    # 2 Column Split (5.7 in each)
    # Column 1: Applications & Advantages
    add_card(s10, 0.8, 1.7, 5.7, 5.0, "Practical Applications & Advantages", COLOR_NAVY)
    tb_adv = s10.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3))
    tf_a = tb_adv.text_frame
    tf_a.word_wrap = True

    p = tf_a.paragraphs[0]
    p.text = "Target Applications:"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL_ACCENT

    apps = [
        ("Personal Health & Fitness", "Zero-friction photo logging for individuals tracking daily caloric deficits or surpluses."),
        ("Clinical Dietary Assistance", "Enables healthcare providers and dietitians to monitor carbohydrate and sodium intake trends for diabetic patients."),
        ("Institutional Food Analytics", "Automated portion checks and nutritional auditing in college cafeterias and hospital meal services.")
    ]
    for at, ad in apps:
        p_app = tf_a.add_paragraph()
        r1 = p_app.add_run()
        r1.text = f"•  {at}: "
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.name = FONT_HEADING
        r1.font.color.rgb = COLOR_NAVY
        r2 = p_app.add_run()
        r2.text = ad
        r2.font.size = Pt(9)
        r2.font.name = FONT_BODY
        r2.font.color.rgb = COLOR_TEXT_BODY
        p_app.space_before = Pt(2)

    p_adv_head = tf_a.add_paragraph()
    p_adv_head.text = "Key Engineering Advantages:"
    p_adv_head.font.name = FONT_HEADING
    p_adv_head.font.size = Pt(11)
    p_adv_head.font.bold = True
    p_adv_head.font.color.rgb = COLOR_TEAL_ACCENT
    p_adv_head.space_before = Pt(8)

    advs = [
        ("Tailored to Indian Cuisine", "Addresses the severe gap in commercial dietary applications, which lack coverage for regional Indian dishes."),
        ("Reference-Free Operation", "Utilizes natural tableware geometry rather than forcing users to place coins or calibration markers."),
        ("Transparent Uncertainty", "Provides realistic ±10-18% bounds instead of misleading single-point precision.")
    ]
    for at, ad in advs:
        p_adv = tf_a.add_paragraph()
        r1 = p_adv.add_run()
        r1.text = f"•  {at}: "
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.name = FONT_HEADING
        r1.font.color.rgb = COLOR_NAVY
        r2 = p_adv.add_run()
        r2.text = ad
        r2.font.size = Pt(9)
        r2.font.name = FONT_BODY
        r2.font.color.rgb = COLOR_TEXT_BODY
        p_adv.space_before = Pt(2)

    # Column 2: Limitations
    add_card(s10, 6.8, 1.7, 5.7, 5.0, "Technical Limitations & Failure Modes", COLOR_NAVY)
    tb_lim = s10.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3))
    tf_l = tb_lim.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "Operational Limitations:"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_ALERT_TEXT

    limits = [
        ("Depth & 3D Loss", "A single 2D camera cannot measure mound height or bottom hollows; a flat spread and deep pile can share identical area."),
        ("Hidden Cooking Oils & Ghee", "Invisible fats drastically alter caloric density without altering visible surface pixels."),
        ("Non-Standard Tableware", "Unusual bowl diameters or non-circular artisan plates skew weight scaling."),
        ("Single-Dish Constraint", "The current pipeline does not separate composite thali plates containing multiple curries and flatbreads simultaneously."),
        ("Classification Error Propagation", "If the food classifier misidentifies Dal Makhani as Dal Tadka, the nutrient database lookup propagates the wrong base values.")
    ]
    for lt, ld in limits:
        p_lim = tf_l.add_paragraph()
        r1 = p_lim.add_run()
        r1.text = f"•  {lt}: "
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.name = FONT_HEADING
        r1.font.color.rgb = COLOR_ALERT_TEXT
        r2 = p_lim.add_run()
        r2.text = ld
        r2.font.size = Pt(9)
        r2.font.name = FONT_BODY
        r2.font.color.rgb = COLOR_TEXT_BODY
        p_lim.space_before = Pt(3)

    p_box = tf_l.add_paragraph()
    p_box.text = "Estimated vs. Laboratory Measurement: Calorie Lens provides an estimation tool for behavioral awareness, not a substitute for bomb-calorimetry or clinical dietary prescription."
    p_box.font.name = FONT_BODY
    p_box.font.size = Pt(8.8)
    p_box.font.italic = True
    p_box.font.color.rgb = COLOR_TEXT_MUTED
    p_box.space_before = Pt(8)

    set_speaker_notes(s10, """[SLIDE 10 — APPLICATIONS, ADVANTAGES & LIMITATIONS]
Speaking Time: ~50 seconds

Every engineering project must be evaluated on both its practical utility and its inherent technical limitations.

On the left, we highlight the applications and advantages:
Calorie Lens is well suited for personal fitness tracking, clinical dietary adherence monitoring, and institutional cafeteria auditing.
Its main advantages are twofold:
First, it focuses specifically on Indian cuisine—a domain where commercial applications like MyFitnessPal perform poorly.
Second, it requires no artificial calibration tokens—using the dining plate or bowl itself as the scaling reference.

On the right, we present an honest analysis of our limitations:
1. 2D depth loss: An overhead image cannot distinguish a shallow spread of rice from a deep mound.
2. Hidden ingredients: Ghee and cooking oils are chemically dense in calories but invisible in surface area.
3. Tableware variance: Non-standard plates disrupt our diameter assumptions.
4. Single-dish limitation: A composite Indian thali containing multiple bowls currently requires multi-pass analysis.
5. Error propagation: If the classifier misclassifies a dish, the nutrient lookup will scale the wrong nutritional baseline.

Calorie Lens is an awareness and estimation tool—not a replacement for laboratory bomb calorimetry or clinical nutrition measurement.

Transition to next slide:
Let us look at how future work can overcome these challenges, followed by our project conclusion.""")

    # =========================================================================
    # SLIDE 11: FUTURE ENHANCEMENTS & CONCLUSION
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_background(s11)
    add_header(s11, "Future Roadmap & Summary", "Future Enhancements & Project Conclusion", "Key technical roadmap pillars and project summary takeaways")
    add_footer(s11, 11)

    # Top Half: 3 Roadmap Cards (3.64 in each)
    # Roadmap Card 1: 3D Depth Sensing
    add_card(s11, 0.8, 1.7, 3.64, 2.9, "1. 3D Depth & LiDAR", COLOR_NAVY)
    tb = s11.shapes.add_textbox(Inches(0.95), Inches(2.1), Inches(3.34), Inches(2.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Mobile LiDAR & RGB-D: Capture genuine 3D point clouds on modern smartphones (e.g., iPhone LiDAR, ToF sensors).\n• Monocular Depth Networks: Integrate models like Depth Anything or MiDaS to predict relative surface depth.\n• Volume Calculation: Volume = Integral of depth over segmented mask; Weight = Volume * Density."
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_BODY

    # Roadmap Card 2: Multi-Dish Thali Parsing
    add_card(s11, 4.84, 1.7, 3.64, 2.9, "2. Multi-Dish Thali Parsing", COLOR_NAVY)
    tb = s11.shapes.add_textbox(Inches(4.99), Inches(2.1), Inches(3.34), Inches(2.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Fine-Tuned Instance Segmentation: Train Mask R-CNN specifically on Indian tableware (katoris, rotis, rice portions).\n• Multi-Class Mask Extraction: Segment each dish simultaneously on a composite thali plate.\n• Aggregate Nutritional Summary: Sum macronutrients across all segmented components on the plate."
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_BODY

    # Roadmap Card 3: User-in-the-Loop Active Learning
    add_card(s11, 8.88, 1.7, 3.64, 2.9, "3. Active User Feedback", COLOR_NAVY)
    tb = s11.shapes.add_textbox(Inches(9.03), Inches(2.1), Inches(3.34), Inches(2.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• User Correction Interface: If Top-1 prediction is incorrect, user can pick from Top-5 predictions with one tap.\n• Interactive Serving Adjustment: User can fine-tune portion slider (e.g., half-plate vs. full-plate).\n• Continuous Fine-Tuning: User-corrected images populate an active-learning retraining queue."
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_BODY

    # Bottom Half: Project Conclusion & 3 Key Takeaways
    add_card(s11, 0.8, 4.85, 11.7, 1.95, "Project Conclusion & Key Takeaways", COLOR_NAVY)
    tb_c = s11.shapes.add_textbox(Inches(1.0), Inches(5.2), Inches(11.3), Inches(1.5))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    takeaways = [
        ("Takeaway 1 — Automated Pipeline Viability", "Calorie Lens demonstrates that combining deep transfer learning (ResNet50) with instance segmentation (Mask R-CNN) provides an effective, non-intrusive approach to dietary tracking for complex Indian cuisines."),
        ("Takeaway 2 — Contextual Tableware Reference", "Utilizing tableware context (plates vs. bowls) via EfficientNet enables reference-free portion estimation from standard dining photos without external calibration markers."),
        ("Takeaway 3 — Honest Caloric Uncertainty", "Reporting confidence-bounded nutritional intervals rather than false single-point precision ensures scientific rigor and realistic expectations in mobile dietary health informatics.")
    ]
    for i, (tt, td) in enumerate(takeaways):
        p = tf_c.paragraphs[0] if i == 0 else tf_c.add_paragraph()
        r1 = p.add_run()
        r1.text = f"•  {tt}: "
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.name = FONT_HEADING
        r1.font.color.rgb = COLOR_NAVY
        r2 = p.add_run()
        r2.text = td
        r2.font.size = Pt(9)
        r2.font.name = FONT_BODY
        r2.font.color.rgb = COLOR_TEXT_BODY
        p.space_after = Pt(2)

    set_speaker_notes(s11, """[SLIDE 11 — FUTURE ENHANCEMENTS & CONCLUSION]
Speaking Time: ~50 seconds

Looking ahead, we have identified three high-impact engineering directions:
1. 3D Depth Integration: Utilizing smartphone LiDAR or monocular depth estimation networks like Depth Anything to calculate true physical volume (Volume = Integral of depth over mask area), then multiplying by density to eliminate portion height assumptions.
2. Multi-Dish Thali Parsing: Training custom segmentation models on Indian thalis to simultaneously segment multiple katoris, rotis, and rice mounds in a single shot.
3. User-in-the-Loop Learning: Allowing users to quickly confirm or correct Top-5 predictions, creating an active-learning pipeline for ongoing model improvements.

In conclusion, our project delivers three core takeaways:
First: Combining transfer-learned classification with instance segmentation provides a feasible, automated pipeline for Indian dietary assessment.
Second: Classifying tableware context eliminates the need for awkward calibration tokens.
Third: Providing confidence-bounded calorie ranges reflects true scientific rigor rather than artificial precision.

Transition to final slide:
Thank you for your time. Let us look at our references and open the floor for questions.""")

    # =========================================================================
    # SLIDE 12: REFERENCES AND THANK YOU
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_background(s12)
    add_header(s12, "Academic References & Open Floor", "References, Repository & Acknowledgments", "Citations of foundational literature, open-source repositories, and Q&A session")
    add_footer(s12, 12)

    # Left: References (5.7 in)
    add_card(s12, 0.8, 1.7, 5.7, 5.0, "Key Literature & Technical References", COLOR_NAVY)
    tb_ref = s12.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3))
    tf_r = tb_ref.text_frame
    tf_r.word_wrap = True

    references = [
        "1. He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep Residual Learning for Image Recognition. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pp. 770-778.",
        "2. He, K., Gkioxari, G., Dollár, P., & Girshick, R. (2017). Mask R-CNN. In Proceedings of the IEEE International Conference on Computer Vision (ICCV), pp. 2961-2969.",
        "3. Tan, M., & Le, Q. V. (2019). EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks. In International Conference on Machine Learning (ICML), pp. 6105-6114.",
        "4. Long, J., Shelhamer, E., & Darrell, T. (2015). Fully Convolutional Networks for Semantic Segmentation. IEEE CVPR, pp. 3431-3440.",
        "5. National Institute of Nutrition (NIN) / ICMR. Indian Food Composition Tables (IFCT). Curated reference database for regional nutritional densities.",
        "6. Official Framework Documentation: PyTorch (torchvision.models), TensorFlow / Keras Applications, OpenCV-Python, and FastAPI."
    ]
    for i, ref in enumerate(references):
        p = tf_r.paragraphs[0] if i == 0 else tf_r.add_paragraph()
        p.text = ref
        p.font.name = FONT_BODY
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_TEXT_BODY
        p.space_after = Pt(4)

    # Right: Thank You & Repository Details (5.7 in)
    add_card(s12, 6.8, 1.7, 5.7, 5.0, "Questions & Project Repository", COLOR_NAVY)
    tb_ty = s12.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3))
    tf_ty = tb_ty.text_frame
    tf_ty.word_wrap = True

    p = tf_ty.paragraphs[0]
    p.text = "THANK YOU!"
    p.font.name = FONT_HEADING
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    p_sub = tf_ty.add_paragraph()
    p_sub.text = "Questions, Feedback & Discussion"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = COLOR_TEAL_ACCENT
    p_sub.space_after = Pt(12)

    details = [
        ("Project Title", "Calorie Lens: AI-Based Food Recognition & Calorie Estimation"),
        ("GitHub Repository", "https://github.com/SHIVANSH-BHARTI2002/Calorie-Lens"),
        ("Primary Models", "ResNet50 (Food) | EfficientNetB4 (Vessel) | Mask R-CNN (Segmentation)"),
        ("Supported Dishes", "51 Curated Regional Indian Cuisines"),
        ("Deployment", "FastAPI REST API Server + Web Application")
    ]
    for label, val in details:
        p_d = tf_ty.add_paragraph()
        r1 = p_d.add_run()
        r1.text = f"{label}: "
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.name = FONT_HEADING
        r1.font.color.rgb = COLOR_NAVY
        r2 = p_d.add_run()
        r2.text = val
        r2.font.size = Pt(9)
        r2.font.name = FONT_BODY
        r2.font.color.rgb = COLOR_TEXT_BODY
        p_d.space_before = Pt(3)

    set_speaker_notes(s12, """[SLIDE 12 — REFERENCES AND THANK YOU]
Speaking Time: ~30 seconds

Here are the key academic references supporting our work, including foundational papers on ResNet, Mask R-CNN, and EfficientNet, along with reference data from the Indian Council of Medical Research.

Our complete codebase, models, dataset scripts, and web server are openly accessible on GitHub at:
https://github.com/SHIVANSH-BHARTI2002/Calorie-Lens.

Thank you very much, respected HOD, Coordinator, and committee members.
I now welcome your questions, feedback, and technical discussion.""")

    output_pptx_path = BASE_DIR / "Calorie_Lens_Academic_Presentation.pptx"
    prs.save(str(output_pptx_path))
    print(f"Presentation saved successfully to: {output_pptx_path}")

if __name__ == "__main__":
    create_presentation()
