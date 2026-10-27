"""
PaperMind AI - Streamlit Web Application.
Interactive dashboard for research paper domain classification,
multi-section summarization, keyword extraction, and side-by-side paper comparison.
"""

import os
import json
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.pdf_extractor import PDFExtractor
from src.classifier import PaperClassifier, RESEARCH_CATEGORIES
from src.summarizer import PaperSummarizer
from src.keyword_extractor import KeywordExtractor
from src.comparator import PaperComparator
from src.utils import generate_markdown_report


# Page configuration
st.set_page_config(
    page_title="PaperMind AI | Research Intelligence",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for academic aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 14px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.15);
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.4rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.05rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: transform 0.15s ease-in-out;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.08);
    }
    .metric-card .val {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e3a8a;
    }
    .metric-card .lbl {
        font-size: 0.85rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.3rem;
    }
    
    .section-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .keyword-pill {
        display: inline-block;
        background-color: #eff6ff;
        color: #1d4ed8;
        border: 1px solid #bfdbfe;
        border-radius: 20px;
        padding: 0.35rem 0.85rem;
        margin: 0.25rem 0.3rem;
        font-size: 0.85rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_pipeline(use_transformers: bool):
    """Cached initialization of PaperMind AI pipeline modules."""
    extractor = PDFExtractor()
    classifier = PaperClassifier(use_transformer=use_transformers)
    summarizer = PaperSummarizer(use_transformer=use_transformers)
    keyword_extractor = KeywordExtractor(top_n=10)
    comparator = PaperComparator()
    return extractor, classifier, summarizer, keyword_extractor, comparator


def main():
    # Header Banner
    st.markdown("""
    <div class="main-header">
        <h1>PaperMind AI</h1>
        <p>Intelligent Research Paper Classification, Multi-Section Summarization & Comparative Analytics</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Pipeline Settings")
        use_transformer_model = st.toggle(
            "Use Deep Transformer Pipelines",
            value=False,
            help="Enables full HuggingFace Transformer inference. When turned off, uses fast local academic supervised models."
        )

        st.markdown("---")
        st.subheader("💡 About PaperMind")
        st.caption(
            "PaperMind AI is an academic deep learning framework designed to accelerate scientific text comprehension. "
            "Upload any 10–30 page PDF to instantly extract structured summaries, research domains, and core terminology."
        )

        st.markdown("---")
        st.subheader("📁 Built-in Test Corpus")
        st.caption("Don't have a PDF handy? Pick one of our pre-bundled papers:")
        sample_choice = st.selectbox(
            "Quick-Load Sample Paper",
            [
                "-- Select a Sample Paper --",
                "Transformer: Attention Is All You Need (NLP)",
                "ResNet: Deep Residual Learning (Computer Vision)",
                "CyberGuard: Phishing Website Detection (Cybersecurity)"
            ]
        )

    # Load components
    extractor, classifier, summarizer, keyword_extractor, comparator = get_pipeline(use_transformer_model)

    # Main Tabs
    tab1, tab2, tab3 = st.tabs([
        "📄 Single Paper Analysis",
        "⚖️ Paper Comparison",
        "📊 Model Benchmarks & Metrics"
    ])

    # -------------------------------------------------------------
    # TAB 1: SINGLE PAPER ANALYSIS
    # -------------------------------------------------------------
    with tab1:
        st.markdown("### 1. Upload or Select a Research Paper")
        uploaded_file = st.file_uploader("Upload scientific paper in PDF format", type=["pdf"])

        # Determine input source
        file_source = None
        doc_label = ""
        sample_map = {
            "Transformer: Attention Is All You Need (NLP)": "sample_attention_transformer.pdf",
            "ResNet: Deep Residual Learning (Computer Vision)": "sample_resnet_computer_vision.pdf",
            "CyberGuard: Phishing Website Detection (Cybersecurity)": "sample_phishing_detection_cybersecurity.pdf"
        }

        if uploaded_file is not None:
            file_source = uploaded_file
            doc_label = uploaded_file.name
        elif sample_choice != "-- Select a Sample Paper --":
            sample_dir = os.path.join(os.path.dirname(__file__), "data", "sample_papers")
            file_source = os.path.join(sample_dir, sample_map[sample_choice])
            doc_label = sample_choice

        if file_source is not None:
            with st.spinner("Extracting text, classifying domain, and generating summaries..."):
                try:
                    # 1. Extraction
                    extracted_data = extractor.extract_from_file(file_source)
                    full_text = extracted_data["full_text"]
                    sections = extracted_data["sections"]
                    metadata = extracted_data["metadata"]
                    title = extracted_data["title"]

                    # 2. Classification
                    classification = classifier.classify(sections.get("abstract", full_text[:1000]), title=title)

                    # 3. Summarization
                    summary = summarizer.summarize_paper(sections, full_text=full_text)

                    # 4. Keywords
                    keywords = keyword_extractor.extract_keywords(full_text, title=title)

                    # Complete paper dictionary
                    paper_data = {
                        "title": title,
                        "metadata": metadata,
                        "sections": sections,
                        "full_text": full_text,
                        "classification": classification,
                        "summary": summary,
                        "keywords": keywords
                    }

                    # Store in session state for cross-tab sharing
                    st.session_state["analyzed_paper_1"] = paper_data

                    st.success(f"Analysis Complete for: **{title}**")

                    # Document Metrics Row
                    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                    with m_col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="val">{metadata['page_count']}</div>
                            <div class="lbl">Total Pages</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with m_col2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="val">{metadata['word_count']:,}</div>
                            <div class="lbl">Word Count</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with m_col3:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="val">~{metadata['estimated_reading_time_mins']} min</div>
                            <div class="lbl">Read Time</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with m_col4:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="val">{round(classification['confidence'] * 100, 1)}%</div>
                            <div class="lbl">Class Confidence</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # Research Classification & Keyword Split View
                    c_col1, c_col2 = st.columns([1.1, 1.0])

                    with c_col1:
                        st.subheader("🎯 Research Domain Classification")
                        st.info(f"**Predicted Domain:** {classification['predicted_category']}")
                        st.caption(f"Inference Engine: *{classification['engine']}*")

                        # Bar chart of top categories
                        all_scores = classification.get("all_scores", {})
                        if all_scores:
                            sorted_scores = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)[:5]
                            score_df = pd.DataFrame(sorted_scores, columns=["Domain", "Probability"])
                            score_df["Percentage"] = score_df["Probability"] * 100

                            fig = px.bar(
                                score_df,
                                x="Percentage",
                                y="Domain",
                                orientation="h",
                                text="Percentage",
                                color="Percentage",
                                color_continuous_scale="Blues"
                            )
                            fig.update_layout(
                                yaxis={"autorange": "reversed"},
                                height=280,
                                margin=dict(l=0, r=20, t=20, b=20),
                                showlegend=False
                            )
                            fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
                            st.plotly_chart(fig, use_container_width=True)

                    with c_col2:
                        st.subheader("🔑 Extracted Key Concepts")
                        if keywords:
                            pills_html = "<div>"
                            for kw in keywords:
                                pills_html += f'<span class="keyword-pill">{kw["phrase"]}</span>'
                            pills_html += "</div>"
                            st.markdown(pills_html, unsafe_allow_html=True)

                            # Table view of top keywords with scores
                            kw_df = pd.DataFrame(keywords)[["phrase", "type", "score"]].rename(
                                columns={"phrase": "Keyphrase", "type": "N-gram Type", "score": "Relevance Score"}
                            )
                            st.dataframe(kw_df.head(6), use_container_width=True, hide_index=True)
                        else:
                            st.write("No distinct keywords identified.")

                    st.markdown("---")

                    # Section Summaries
                    st.subheader("📝 Structured Multi-Section Summaries")

                    # Executive Summary Card
                    st.markdown(f"""
                    <div class="section-box" style="border-left-color: #2563eb; background-color: #f0f7ff;">
                        <div class="section-title">📌 Executive Summary</div>
                        <p style="font-size: 1.02rem; line-height: 1.6; color: #1e293b;">{summary['executive_summary']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # 4-Quadrant Deep Dive
                    s_col1, s_col2 = st.columns(2)

                    with s_col1:
                        st.markdown(f"""
                        <div class="section-box">
                            <div class="section-title">🎯 Problem Statement & Objectives</div>
                            <p style="color: #334155; line-height: 1.55;">{summary['problem_statement']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown(f"""
                        <div class="section-box">
                            <div class="section-title">📊 Key Experimental Findings</div>
                            <p style="color: #334155; line-height: 1.55;">{summary['findings']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with s_col2:
                        st.markdown(f"""
                        <div class="section-box">
                            <div class="section-title">⚙️ Proposed Methodology & Approach</div>
                            <p style="color: #334155; line-height: 1.55;">{summary['methodology']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown(f"""
                        <div class="section-box">
                            <div class="section-title">💡 Conclusion & Future Direction</div>
                            <p style="color: #334155; line-height: 1.55;">{summary['conclusion']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    # Export & Raw Text Accordion
                    exp_col1, exp_col2 = st.columns([1, 1])
                    with exp_col1:
                        report_md = generate_markdown_report(paper_data)
                        st.download_button(
                            label="📥 Download Academic Briefing (Markdown)",
                            data=report_md,
                            file_name=f"PaperMind_Report_{title[:20].strip().replace(' ', '_')}.md",
                            mime="text/markdown"
                        )

                    with st.expander("🔍 Inspect Extracted Raw Text by Section"):
                        for sec_name, sec_text in sections.items():
                            if sec_text:
                                st.markdown(f"**{sec_name.title()}:**")
                                st.text_area(f"{sec_name}_text", sec_text, height=120, disabled=True)

                except Exception as e:
                    st.error(f"Error processing document: {str(e)}")
        else:
            st.info("👆 Please upload a research paper PDF or select a built-in sample paper from the left sidebar to begin.")

    # -------------------------------------------------------------
    # TAB 2: PAPER COMPARISON
    # -------------------------------------------------------------
    with tab2:
        st.markdown("### ⚖️ Side-by-Side Paper Comparison")
        st.caption("Upload or select two scientific papers to contrast their domains, methodologies, findings, and shared technical concepts.")

        cmp_col1, cmp_col2 = st.columns(2)
        with cmp_col1:
            st.markdown("#### Paper A")
            file_a = st.file_uploader("Upload First Paper (PDF)", type=["pdf"], key="cmp_pdf_a")
            sample_a = st.selectbox(
                "Or choose Sample A",
                ["Transformer (NLP)", "ResNet (Computer Vision)", "CyberGuard (Cybersecurity)"],
                index=0,
                key="sample_a"
            )

        with cmp_col2:
            st.markdown("#### Paper B")
            file_b = st.file_uploader("Upload Second Paper (PDF)", type=["pdf"], key="cmp_pdf_b")
            sample_b = st.selectbox(
                "Or choose Sample B",
                ["Transformer (NLP)", "ResNet (Computer Vision)", "CyberGuard (Cybersecurity)"],
                index=1,
                key="sample_b"
            )

        compare_btn = st.button("🚀 Run Comparative Analysis", type="primary")

        if compare_btn:
            sample_dir = os.path.join(os.path.dirname(__file__), "data", "sample_papers")
            sample_file_map = {
                "Transformer (NLP)": "sample_attention_transformer.pdf",
                "ResNet (Computer Vision)": "sample_resnet_computer_vision.pdf",
                "CyberGuard (Cybersecurity)": "sample_phishing_detection_cybersecurity.pdf"
            }

            source_a = file_a if file_a else os.path.join(sample_dir, sample_file_map[sample_a])
            source_b = file_b if file_b else os.path.join(sample_dir, sample_file_map[sample_b])

            with st.spinner("Analyzing and contrasting both papers..."):
                # Process Paper A
                data_a = extractor.extract_from_file(source_a)
                data_a["classification"] = classifier.classify(data_a["sections"]["abstract"], data_a["title"])
                data_a["summary"] = summarizer.summarize_paper(data_a["sections"], data_a["full_text"])
                data_a["keywords"] = keyword_extractor.extract_keywords(data_a["full_text"], data_a["title"])

                # Process Paper B
                data_b = extractor.extract_from_file(source_b)
                data_b["classification"] = classifier.classify(data_b["sections"]["abstract"], data_b["title"])
                data_b["summary"] = summarizer.summarize_paper(data_b["sections"], data_b["full_text"])
                data_b["keywords"] = keyword_extractor.extract_keywords(data_b["full_text"], data_b["title"])

                # Run Comparator
                diff = comparator.compare(data_a, data_b)

                # Similarity Gauge & Verdict
                sim_score = diff["similarity_score"]
                st.markdown("---")

                v_col1, v_col2 = st.columns([1, 2])
                with v_col1:
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=sim_score,
                        title={'text': "Textual & Semantic Similarity (%)"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "#2563eb"},
                            'steps': [
                                {'range': [0, 30], 'color': "#e2e8f0"},
                                {'range': [30, 70], 'color': "#bfdbfe"},
                                {'range': [70, 100], 'color': "#93c5fd"}
                            ]
                        }
                    ))
                    fig_gauge.update_layout(height=240, margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig_gauge, use_container_width=True)

                with v_col2:
                    st.markdown("#### 🔬 Comparative Verdict")
                    st.info(diff["verdict"])

                    st.markdown(f"**Domain Paper A:** `{diff['domain_a']}` | **Domain Paper B:** `{diff['domain_b']}`")
                    st.markdown(f"**Shared Concepts ({len(diff['shared_keywords'])}):** {', '.join(diff['shared_keywords'][:6]) if diff['shared_keywords'] else 'None'}")

                # Metrics Comparison Table
                st.markdown("#### 📊 Quantitative Metrics Comparison")
                metrics_df = pd.DataFrame({
                    "Metric": ["Title", "Domain", "Pages", "Word Count", "Est. Read Time"],
                    "Paper A": [
                        diff["paper_a_metrics"]["title"],
                        diff["domain_a"],
                        diff["paper_a_metrics"]["pages"],
                        f"{diff['paper_a_metrics']['words']:,} words",
                        f"~{diff['paper_a_metrics']['reading_time']} mins"
                    ],
                    "Paper B": [
                        diff["paper_b_metrics"]["title"],
                        diff["domain_b"],
                        diff["paper_b_metrics"]["pages"],
                        f"{diff['paper_b_metrics']['words']:,} words",
                        f"~{diff['paper_b_metrics']['reading_time']} mins"
                    ]
                })
                st.table(metrics_df)

                # Side-by-Side Section Summaries
                st.markdown("#### 📑 Side-by-Side Summary Comparison")

                sections_to_show = [
                    ("Executive Summary", "executive_summary"),
                    ("Problem Statement", "problem_statement"),
                    ("Methodology & Architecture", "methodology"),
                    ("Key Findings & Results", "findings"),
                    ("Conclusion", "conclusion")
                ]

                for label, sec_key in sections_to_show:
                    with st.expander(f"Contrast: {label}", expanded=(sec_key == "executive_summary")):
                        s_a_col, s_b_col = st.columns(2)
                        with s_a_col:
                            st.markdown(f"**{diff['paper_a_metrics']['title'][:35]}...**")
                            st.write(diff["section_comparison"][sec_key]["paper_a"])
                        with s_b_col:
                            st.markdown(f"**{diff['paper_b_metrics']['title'][:35]}...**")
                            st.write(diff["section_comparison"][sec_key]["paper_b"])

    # -------------------------------------------------------------
    # TAB 3: MODEL BENCHMARKS & EVALUATION
    # -------------------------------------------------------------
    with tab3:
        st.markdown("### 📊 Deep Learning Model Benchmarks & Evaluation")
        st.caption(
            "Quantitative evaluation results demonstrating academic rigor for your project report and defense."
        )

        # Classification Metrics
        metrics_file = os.path.join(os.path.dirname(__file__), "data", "classification_metrics.json")
        cm_image_file = os.path.join(os.path.dirname(__file__), "data", "confusion_matrix.png")
        rouge_file = os.path.join(os.path.dirname(__file__), "data", "summarization_metrics.json")

        b_col1, b_col2 = st.columns([1.1, 1.0])

        with b_col1:
            st.subheader("Model 1: Domain Classification Benchmarks")
            if os.path.exists(metrics_file):
                with open(metrics_file, "r") as f:
                    c_metrics = json.load(f)

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Accuracy", f"{c_metrics['accuracy'] * 100:.1f}%")
                c2.metric("Precision", f"{c_metrics['precision'] * 100:.1f}%")
                c3.metric("Recall", f"{c_metrics['recall'] * 100:.1f}%")
                c4.metric("F1-Score", f"{c_metrics['f1_score'] * 100:.1f}%")

                if os.path.exists(cm_image_file):
                    st.image(cm_image_file, caption="Confusion Matrix on Held-Out Academic Test Corpus", use_container_width=True)
            else:
                st.info("Run `python models/train_and_evaluate_classifier.py` to generate metrics.")

        with b_col2:
            st.subheader("Model 2: Summarization Quality (ROUGE)")
            if os.path.exists(rouge_file):
                with open(rouge_file, "r") as f:
                    r_metrics = json.load(f)

                r1, r2, r3 = st.columns(3)
                r1.metric("ROUGE-1 F1", f"{r_metrics['average_rouge1_f1'] * 100:.1f}%", help="Unigram word overlap")
                r2.metric("ROUGE-2 F1", f"{r_metrics['average_rouge2_f1'] * 100:.1f}%", help="Bigram phrasal fluency")
                r3.metric("ROUGE-L F1", f"{r_metrics['average_rougeL_f1'] * 100:.1f}%", help="Longest common sequence")

                st.markdown("#### Per-Paper ROUGE Metrics Breakdown")
                rouge_df = pd.DataFrame(r_metrics["detailed_results"])[["paper", "rouge1_f1", "rouge2_f1", "rougeL_f1"]]
                rouge_df["rouge1_f1"] = (rouge_df["rouge1_f1"] * 100).round(1).astype(str) + "%"
                rouge_df["rouge2_f1"] = (rouge_df["rouge2_f1"] * 100).round(1).astype(str) + "%"
                rouge_df["rougeL_f1"] = (rouge_df["rougeL_f1"] * 100).round(1).astype(str) + "%"
                st.table(rouge_df.rename(columns={
                    "paper": "Paper",
                    "rouge1_f1": "ROUGE-1",
                    "rouge2_f1": "ROUGE-2",
                    "rougeL_f1": "ROUGE-L"
                }))
            else:
                st.info("Run `python models/evaluate_summarizer.py` to generate ROUGE scores.")

            st.markdown("""
            #### 🧠 Deep Learning Architecture Highlights
            - **Text Ingestion:** PyMuPDF (`fitz`) high-fidelity vector parser.
            - **Domain Classifier:** Supervised TF-IDF n-gram feature extractor with softmax calibrated multiclass logistic regression / DistilBERT zero-shot classification across 7 arXiv categories.
            - **Summarizer:** Hierarchical abstractive/salience-graph summarization with section-aware cue-phrase boosting.
            - **Evaluation Protocol:** Multi-class confusion matrix, precision/recall/F1, and standard ROUGE-1/2/L lexical metrics.
            """)


if __name__ == "__main__":
    main()
