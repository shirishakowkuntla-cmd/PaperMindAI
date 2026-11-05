"""
Script to generate the official presentation for PaperMind AI.
Course: DS306 - Deep Learning
Instructor: Dr. Kongara Srinivasa Rao
Submitted by:
  - Kowkuntla Shirisha (23STUCHH010987)
  - E M Dimple Reddy (23STUCHH010967)
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE


def build_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presentation_assets")
    output_pptx = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PaperMind_AI_Presentation.pptx")

    BG_DARK = RGBColor(15, 23, 42)        # #0F172A
    CARD_BG = RGBColor(30, 41, 59)        # #1E293B
    CARD_BORDER = RGBColor(51, 65, 85)    # #334155
    ACCENT_BLUE = RGBColor(37, 99, 235)   # #2563EB
    ACCENT_CYAN = RGBColor(56, 189, 248)  # #38BDF8
    TEXT_LIGHT = RGBColor(248, 250, 252)  # #F8FAFC
    TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8
    CARD_SUCCESS = RGBColor(16, 185, 129) # #10B981

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text, slide_num):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_CYAN

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(10.5), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT

        num_box = slide.shapes.add_textbox(Inches(11.8), Inches(0.4), Inches(1.0), Inches(0.4))
        tf_num = num_box.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = f"{slide_num} / 9"
        p_num.font.size = Pt(11)
        p_num.font.color.rgb = TEXT_MUTED

    # SLIDE 1: TITLE SLIDE
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    accent_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = ACCENT_CYAN
    accent_bar.line.fill.background()

    badge = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.1), Inches(3.2), Inches(0.45))
    badge.fill.solid()
    badge.fill.fore_color.rgb = CARD_BG
    badge.line.color.rgb = ACCENT_CYAN
    badge.line.width = Pt(1)
    badge.text_frame.paragraphs[0].text = "DEEP LEARNING PROJECT"
    badge.text_frame.paragraphs[0].font.size = Pt(11)
    badge.text_frame.paragraphs[0].font.bold = True
    badge.text_frame.paragraphs[0].font.color.rgb = ACCENT_CYAN
    badge.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    t_box = slide1.shapes.add_textbox(Inches(0.9), Inches(1.7), Inches(11.5), Inches(1.4))
    tf1 = t_box.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "PaperMind AI"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT

    p2 = tf1.add_paragraph()
    p2.text = "Intelligent Research Paper Classification & Structured Summarization System"
    p2.font.size = Pt(18)
    p2.font.color.rgb = ACCENT_CYAN
    p2.space_before = Pt(8)

    c_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(3.4), Inches(5.5), Inches(3.2))
    c_card.fill.solid()
    c_card.fill.fore_color.rgb = CARD_BG
    c_card.line.color.rgb = CARD_BORDER
    c_card.line.width = Pt(1)

    tf_c = c_card.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = Inches(0.35)
    tf_c.margin_right = Inches(0.35)
    tf_c.margin_top = Inches(0.3)

    p_c1 = tf_c.paragraphs[0]
    p_c1.text = "ACADEMIC DETAILS"
    p_c1.font.size = Pt(11)
    p_c1.font.bold = True
    p_c1.font.color.rgb = ACCENT_CYAN

    p_c2 = tf_c.add_paragraph()
    p_c2.text = "Subject:"
    p_c2.font.size = Pt(13)
    p_c2.font.bold = True
    p_c2.font.color.rgb = TEXT_LIGHT
    p_c2.space_before = Pt(12)

    p_c3 = tf_c.add_paragraph()
    p_c3.text = "Deep Learning (Course Code: DS306)"
    p_c3.font.size = Pt(13)
    p_c3.font.color.rgb = TEXT_MUTED

    p_c4 = tf_c.add_paragraph()
    p_c4.text = "Course Instructor:"
    p_c4.font.size = Pt(13)
    p_c4.font.bold = True
    p_c4.font.color.rgb = TEXT_LIGHT
    p_c4.space_before = Pt(12)

    p_c5 = tf_c.add_paragraph()
    p_c5.text = "Dr. Kongara Srinivasa Rao"
    p_c5.font.size = Pt(13)
    p_c5.font.color.rgb = ACCENT_CYAN

    s_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.4), Inches(5.6), Inches(3.2))
    s_card.fill.solid()
    s_card.fill.fore_color.rgb = CARD_BG
    s_card.line.color.rgb = CARD_BORDER
    s_card.line.width = Pt(1)

    tf_s = s_card.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = Inches(0.35)
    tf_s.margin_right = Inches(0.35)
    tf_s.margin_top = Inches(0.3)

    p_s1 = tf_s.paragraphs[0]
    p_s1.text = "SUBMITTED BY"
    p_s1.font.size = Pt(11)
    p_s1.font.bold = True
    p_s1.font.color.rgb = ACCENT_CYAN

    p_s2 = tf_s.add_paragraph()
    p_s2.text = "1. Kowkuntla Shirisha"
    p_s2.font.size = Pt(14)
    p_s2.font.bold = True
    p_s2.font.color.rgb = TEXT_LIGHT
    p_s2.space_before = Pt(12)

    p_s3 = tf_s.add_paragraph()
    p_s3.text = "    Roll No: 23STUCHH010987"
    p_s3.font.size = Pt(13)
    p_s3.font.color.rgb = TEXT_MUTED

    p_s4 = tf_s.add_paragraph()
    p_s4.text = "2. E M Dimple Reddy"
    p_s4.font.size = Pt(14)
    p_s4.font.bold = True
    p_s4.font.color.rgb = TEXT_LIGHT
    p_s4.space_before = Pt(14)

    p_s5 = tf_s.add_paragraph()
    p_s5.text = "    Roll No: 23STUCHH010967"
    p_s5.font.size = Pt(13)
    p_s5.font.color.rgb = TEXT_MUTED

    # SLIDE 2: PROBLEM STATEMENT
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "The Core Problem in Academic Literature Research", "Problem Statement", 2)

    col_w = Inches(3.75)
    gap = Inches(0.3)
    top_pos = Inches(1.6)
    card_h = Inches(5.1)

    cards_data = [
        ("THE CHALLENGE", "Massive Volume & High Complexity", [
            "Research papers are typically 10 to 30 pages long.",
            "Written in highly specialized, mathematically dense language.",
            "Reading an entire paper just to check its relevance takes 45–60 minutes per document."
        ], ACCENT_CYAN),
        ("THE RESEARCH BOTTLENECK", "Cognitive Overload for Students", [
            "Literature review takes weeks of manual scanning.",
            "Hard to quickly extract key problem statements, architectures, and quantitative results.",
            "Comparing two related papers across methods requires manual note-taking and tabulation."
        ], RGBColor(239, 68, 68)),
        ("THE SOLUTION", "PaperMind AI Automated Intelligence", [
            "Instant PDF vector text extraction & section segmentation.",
            "Automatic domain classification into 7 arXiv computer science categories.",
            "Multi-quadrant structured summaries (Problem, Methods, Findings, Conclusions).",
            "Side-by-side contrastive paper comparison in seconds."
        ], CARD_SUCCESS)
    ]

    for i, (tag, title, points, color) in enumerate(cards_data):
        x = Inches(0.8) + i * (col_w + gap)
        box = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, top_pos, col_w, card_h)
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = color
        box.line.width = Pt(1.5)

        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_right = Inches(0.3)
        tf.margin_top = Inches(0.3)

        p_tag = tf.paragraphs[0]
        p_tag.text = tag
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = color

        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_LIGHT
        p_t.space_before = Pt(6)

        for pt in points:
            p = tf.add_paragraph()
            p.text = f"•  {pt}"
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_MUTED
            p.space_before = Pt(12)

    # SLIDE 3: INTRODUCTION & WORKFLOW
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "What is PaperMind AI & How It Operates", "Introduction & Workflow", 3)

    left_w = Inches(5.8)
    left_box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), left_w, Inches(5.1))
    left_box.fill.solid()
    left_box.fill.fore_color.rgb = CARD_BG
    left_box.line.color.rgb = CARD_BORDER

    tf_l = left_box.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = Inches(0.35)
    tf_l.margin_right = Inches(0.35)
    tf_l.margin_top = Inches(0.3)

    tf_l.paragraphs[0].text = "END-TO-END EXECUTION WORKFLOW"
    tf_l.paragraphs[0].font.size = Pt(11)
    tf_l.paragraphs[0].font.bold = True
    tf_l.paragraphs[0].font.color.rgb = ACCENT_CYAN

    steps = [
        ("Step 1: Document Upload", "User uploads any PDF research paper (or selects from built-in arXiv samples)."),
        ("Step 2: Vector Parsing & Ingestion", "PyMuPDF extracts clean text, normalizes font ligatures, and parses Title, Abstract, Methods, Results, and Conclusions."),
        ("Step 3: Deep Learning Inference", "Transformer/Classifier predicts academic discipline, while the Summarization pipeline generates structured multi-part briefs."),
        ("Step 4: Interactive Visualization", "Outputs metrics, probability distribution bars, keyword tags, and side-by-side comparative analytics.")
    ]

    for title, desc in steps:
        p_st = tf_l.add_paragraph()
        p_st.text = title
        p_st.font.size = Pt(13)
        p_st.font.bold = True
        p_st.font.color.rgb = TEXT_LIGHT
        p_st.space_before = Pt(10)

        p_sd = tf_l.add_paragraph()
        p_sd.text = desc
        p_sd.font.size = Pt(11)
        p_sd.font.color.rgb = TEXT_MUTED

    img_path = os.path.join(assets_dir, "dashboard_single_analysis.png")
    if os.path.exists(img_path):
        slide3.shapes.add_picture(img_path, Inches(6.9), Inches(1.6), width=Inches(5.6))

    # SLIDE 4: WHAT DL & NLP TECHNOLOGIES USED
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "Deep Learning & NLP Technology Stack", "Technologies Used", 4)

    tech_cards = [
        ("PyTorch & Transformers", "Hugging Face Ecosystem", [
            "Pretrained DistilBERT and BERT for semantic domain classification.",
            "BART (distilbart-cnn-12-6) / T5 sequence-to-sequence transformers for abstractive summarization."
        ], ACCENT_CYAN),
        ("Sublinear N-Gram Modeling", "Fast Calibrated Classification", [
            "Sublinear term frequency TF-IDF (1-2 n-grams) over 12,000 features.",
            "Multinomial Softmax Logistic Regression delivering 91.3% accuracy across 7 arXiv disciplines."
        ], ACCENT_BLUE),
        ("PyMuPDF (fitz)", "High-Fidelity Document Parser", [
            "Direct vector stream extraction with layout-aware column sorting.",
            "Unicode normalization (NFKD) resolving typographic ligatures (fi, fl) and soft hyphens."
        ], CARD_SUCCESS),
        ("Streamlit & Plotly", "Reactive Dashboard UI", [
            "In-memory stream processing with zero temporary disk clutter.",
            "@st.cache_resource for instant deep learning model caching and sub-second inference."
        ], RGBColor(245, 158, 11))
    ]

    for i, (title, subtitle, points, color) in enumerate(tech_cards):
        col = i % 2
        row = i // 2
        x = Inches(0.8) + col * Inches(5.95)
        y = Inches(1.6) + row * Inches(2.6)

        c = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.65), Inches(2.35))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = color
        c.line.width = Pt(1.2)

        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_right = Inches(0.3)
        tf.margin_top = Inches(0.2)

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED

        for pt in points:
            p = tf.add_paragraph()
            p.text = f"•  {pt}"
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_LIGHT
            p.space_before = Pt(4)

    # SLIDE 5: DL MODEL ARCHITECTURE & HOW IT WORKS
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "Deep Learning Pipeline Architecture & Mechanism", "Architecture & Workflow", 5)

    arch_steps = [
        ("1. Input & Parsing", "PyMuPDF Vector Engine", [
            "PDF Stream Ingestion",
            "Reading Order Sorting",
            "Unicode Normalization",
            "Title & Section Extraction"
        ]),
        ("2. Model 1: Classifier", "Academic Domain Predictor", [
            "DistilBERT / Sublinear TF-IDF",
            "Title-Weighted Context",
            "Multi-class Softmax Scoring",
            "7 arXiv Domain Classes"
        ]),
        ("3. Model 2: Summarizer", "Hierarchical Summarizer", [
            "Section-Aware Map-Reduce",
            "BART / Salience Graph",
            "Abbreviation Masking",
            "5-Part Structured Summary"
        ]),
        ("4. Analytics Engine", "Comparative Engine", [
            "Semantic Cosine Similarity",
            "N-Gram Keyword Extraction",
            "Concept Venn Comparison",
            "Downloadable Markdown"
        ])
    ]

    card_w = Inches(2.75)
    card_gap = Inches(0.25)
    for i, (title, subtitle, bullets) in enumerate(arch_steps):
        x = Inches(0.8) + i * (card_w + card_gap)
        y = Inches(1.6)

        c = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_w, Inches(3.2))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = ACCENT_CYAN if i % 2 == 0 else ACCENT_BLUE
        c.line.width = Pt(1.5)

        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.2)

        tf.paragraphs[0].text = title
        tf.paragraphs[0].font.size = Pt(13)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = ACCENT_CYAN if i % 2 == 0 else ACCENT_BLUE

        p_sub = tf.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.size = Pt(10)
        p_sub.font.color.rgb = TEXT_MUTED

        for b in bullets:
            p = tf.add_paragraph()
            p.text = f"→  {b}"
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_LIGHT
            p.space_before = Pt(8)

    sol_banner = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.1), Inches(11.75), Inches(1.7))
    sol_banner.fill.solid()
    sol_banner.fill.fore_color.rgb = CARD_BG
    sol_banner.line.color.rgb = CARD_BORDER

    tf_b = sol_banner.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = Inches(0.3)
    tf_b.margin_right = Inches(0.3)
    tf_b.margin_top = Inches(0.2)

    tf_b.paragraphs[0].text = "💡 KEY INNOVATION: SOLVING THE 512-TOKEN TRANSFORMER BOTTLENECK"
    tf_b.paragraphs[0].font.size = Pt(11)
    tf_b.paragraphs[0].font.bold = True
    tf_b.paragraphs[0].font.color.rgb = CARD_SUCCESS

    p_sol = tf_b.add_paragraph()
    p_sol.text = (
        "Standard pretrained transformers (DistilBERT, BART) fail on 20-page papers due to strict token length limits. "
        "PaperMind AI solves this using Hierarchical Section Segmentation: instead of truncating 90% of the paper, it extracts "
        "individual sections (Abstract, Intro, Methods, Results, Conclusion), summarizes each with domain cue-phrase salience scoring, "
        "and aggregates them into a comprehensive structured briefing."
    )
    p_sol.font.size = Pt(11.5)
    p_sol.font.color.rgb = TEXT_LIGHT
    p_sol.space_before = Pt(4)

    # SLIDE 6: MODEL 1 - RESEARCH PAPER DOMAIN CLASSIFICATION
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "Model 1: Research Paper Domain Classification", "Deep Learning Classification", 6)

    m1_box = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.5), Inches(5.1))
    m1_box.fill.solid()
    m1_box.fill.fore_color.rgb = CARD_BG
    m1_box.line.color.rgb = CARD_BORDER

    tf_m1 = m1_box.text_frame
    tf_m1.word_wrap = True
    tf_m1.margin_left = Inches(0.3)
    tf_m1.margin_right = Inches(0.3)
    tf_m1.margin_top = Inches(0.25)

    tf_m1.paragraphs[0].text = "CLASSIFICATION ARCHITECTURE & RESULTS"
    tf_m1.paragraphs[0].font.size = Pt(11)
    tf_m1.paragraphs[0].font.bold = True
    tf_m1.paragraphs[0].font.color.rgb = ACCENT_CYAN

    m1_points = [
        ("Trained Corpus", "112 landmark arXiv research papers across 7 computer science disciplines."),
        ("Title Weighting", "Title tokens are emphasized to boost domain centroid alignment."),
        ("7 Supported Domains", "AI/ML, Computer Vision, NLP, Cybersecurity, Data Science, Robotics, Networks.")
    ]

    for t, d in m1_points:
        p_t = tf_m1.add_paragraph()
        p_t.text = t
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_LIGHT
        p_t.space_before = Pt(8)

        p_d = tf_m1.add_paragraph()
        p_d.text = d
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_MUTED

    p_met_title = tf_m1.add_paragraph()
    p_met_title.text = "Held-Out Test Set Performance:"
    p_met_title.font.size = Pt(12)
    p_met_title.font.bold = True
    p_met_title.font.color.rgb = CARD_SUCCESS
    p_met_title.space_before = Pt(12)

    p_met_scores = tf_m1.add_paragraph()
    p_met_scores.text = "• Accuracy: 91.30%  |  Precision: 92.39%\n• Recall: 91.30%    |  F1-Score: 91.30%"
    p_met_scores.font.size = Pt(12)
    p_met_scores.font.bold = True
    p_met_scores.font.color.rgb = TEXT_LIGHT

    bm_img = os.path.join(assets_dir, "model_benchmarks.png")
    if os.path.exists(bm_img):
        slide6.shapes.add_picture(bm_img, Inches(6.6), Inches(1.6), width=Inches(5.95))

    # SLIDE 7: MODEL 2 - STRUCTURED SUMMARIZATION & KEYWORD EXTRACTION
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "Model 2: Multi-Section Summarization & Concept Mining", "Summarization & Keywords", 7)

    m2_box = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.5), Inches(5.1))
    m2_box.fill.solid()
    m2_box.fill.fore_color.rgb = CARD_BG
    m2_box.line.color.rgb = CARD_BORDER

    tf_m2 = m2_box.text_frame
    tf_m2.word_wrap = True
    tf_m2.margin_left = Inches(0.3)
    tf_m2.margin_right = Inches(0.3)
    tf_m2.margin_top = Inches(0.25)

    tf_m2.paragraphs[0].text = "STRUCTURED MULTI-SECTION SUMMARIZATION"
    tf_m2.paragraphs[0].font.size = Pt(11)
    tf_m2.paragraphs[0].font.bold = True
    tf_m2.paragraphs[0].font.color.rgb = ACCENT_CYAN

    sum_secs = [
        ("📌 Executive Summary", "High-level overview of the document's central contribution."),
        ("🎯 Problem & Objectives", "Specific scientific challenge addressed by the researchers."),
        ("⚙️ Methodology & Architecture", "Algorithms, model designs, datasets, and pipelines."),
        ("📊 Key Findings & Results", "Quantitative benchmarks, error rates, and metric gains."),
        ("💡 Conclusion & Impact", "Final takeaways and outlined future directions.")
    ]

    for title, desc in sum_secs:
        p_st = tf_m2.add_paragraph()
        p_st.text = title
        p_st.font.size = Pt(11.5)
        p_st.font.bold = True
        p_st.font.color.rgb = TEXT_LIGHT
        p_st.space_before = Pt(6)

        p_sd = tf_m2.add_paragraph()
        p_sd.text = desc
        p_sd.font.size = Pt(10)
        p_sd.font.color.rgb = TEXT_MUTED

    p_r = tf_m2.add_paragraph()
    p_r.text = "ROUGE Quality Scores: ROUGE-1: 83.2% | ROUGE-2: 81.8% | ROUGE-L: 83.2%"
    p_r.font.size = Pt(11)
    p_r.font.bold = True
    p_r.font.color.rgb = CARD_SUCCESS
    p_r.space_before = Pt(8)

    sum_img = os.path.join(assets_dir, "structured_summary.png")
    if os.path.exists(sum_img):
        slide7.shapes.add_picture(sum_img, Inches(6.6), Inches(1.6), width=Inches(5.95))

    # SLIDE 8: PAPER COMPARISON FEATURE
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, "Contrastive Side-by-Side Paper Comparison", "Comparative Intelligence", 8)

    cmp_box = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.3), Inches(5.1))
    cmp_box.fill.solid()
    cmp_box.fill.fore_color.rgb = CARD_BG
    cmp_box.line.color.rgb = CARD_BORDER

    tf_cmp = cmp_box.text_frame
    tf_cmp.word_wrap = True
    tf_cmp.margin_left = Inches(0.3)
    tf_cmp.margin_right = Inches(0.3)
    tf_cmp.margin_top = Inches(0.25)

    tf_cmp.paragraphs[0].text = "CROSS-DOCUMENT ANALYSIS CAPABILITIES"
    tf_cmp.paragraphs[0].font.size = Pt(11)
    tf_cmp.paragraphs[0].font.bold = True
    tf_cmp.paragraphs[0].font.color.rgb = ACCENT_CYAN

    cmp_features = [
        ("Semantic Cosine Similarity Gauge", "Calculates document-level textual and structural similarity percentage (0% to 100%)."),
        ("Concept Venn Analysis", "Automatically separates overlapping shared technical keyphrases from unique terms exclusive to each paper."),
        ("Side-by-Side Section Contrasting", "Aligns Problem vs. Problem, Method vs. Method, and Results vs. Results for direct comparison."),
        ("Automated Comparative Verdict", "Generates natural language synthesis explaining domain divergence or convergence.")
    ]

    for title, desc in cmp_features:
        p_t = tf_cmp.add_paragraph()
        p_t.text = f"•  {title}"
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_LIGHT
        p_t.space_before = Pt(10)

        p_d = tf_cmp.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_MUTED

    cmp_img = os.path.join(assets_dir, "paper_comparison.png")
    if os.path.exists(cmp_img):
        slide8.shapes.add_picture(cmp_img, Inches(6.4), Inches(1.6), width=Inches(6.1))

    # SLIDE 9: CONCLUSION & FUTURE SCOPE
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_header(slide9, "Project Conclusion & Future Enhancements", "Conclusion", 9)

    card_w2 = Inches(5.7)
    left_x = Inches(0.8)
    right_x = Inches(6.8)

    c1 = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, Inches(1.6), card_w2, Inches(5.1))
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = CARD_SUCCESS
    c1.line.width = Pt(1.5)

    tf_c1 = c1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = Inches(0.35)
    tf_c1.margin_right = Inches(0.35)
    tf_c1.margin_top = Inches(0.3)

    tf_c1.paragraphs[0].text = "PROJECT ACHIEVEMENTS"
    tf_c1.paragraphs[0].font.size = Pt(11)
    tf_c1.paragraphs[0].font.bold = True
    tf_c1.paragraphs[0].font.color.rgb = CARD_SUCCESS

    achievements = [
        "End-to-End Pipeline: Complete working system from raw PDF bytes to Deep Learning classification, summarization, and interactive UI.",
        "High Empirical Accuracy: 91.3% Domain Classification Accuracy and 83.2% ROUGE-1 summarization quality.",
        "Zero-Friction Ingestion: Handles 10–30 page complex multi-column academic PDFs with PyMuPDF vector extraction.",
        "Practical Academic Utility: Reduces paper evaluation time from 45 minutes to under 5 seconds with 1-click Markdown briefing export."
    ]

    for a in achievements:
        p = tf_c1.add_paragraph()
        parts = a.split(":")
        p.text = f"✔  {parts[0]}:"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(10)

        p2 = tf_c1.add_paragraph()
        p2.text = f"    {parts[1].strip()}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED

    c2 = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, Inches(1.6), card_w2, Inches(5.1))
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG
    c2.line.color.rgb = ACCENT_CYAN
    c2.line.width = Pt(1.5)

    tf_c2 = c2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = Inches(0.35)
    tf_c2.margin_right = Inches(0.35)
    tf_c2.margin_top = Inches(0.3)

    tf_c2.paragraphs[0].text = "FUTURE RESEARCH DIRECTIONS"
    tf_c2.paragraphs[0].font.size = Pt(11)
    tf_c2.paragraphs[0].font.bold = True
    tf_c2.paragraphs[0].font.color.rgb = ACCENT_CYAN

    future_points = [
        "Citation Graph Mining: Integrating CrossRef and Semantic Scholar APIs to map citation influence networks.",
        "Multimodal Equation & Table Parsing: Vision-language models (e.g. Nougat / Donut) for extracting LaTeX mathematical proofs directly from figures.",
        "Cross-Lingual Support: Extending summarization to international conference proceedings in German, French, and Japanese.",
        "Conversational Paper Q&A: Localized RAG chat allowing students to ask specific follow-up questions on uploaded PDFs."
    ]

    for f in future_points:
        p = tf_c2.add_paragraph()
        parts = f.split(":")
        p.text = f"🚀  {parts[0]}:"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(10)

        p2 = tf_c2.add_paragraph()
        p2.text = f"    {parts[1].strip()}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED

    prs.save(output_pptx)
    print(f"Presentation saved successfully to: {output_pptx}")


if __name__ == "__main__":
    build_presentation()
