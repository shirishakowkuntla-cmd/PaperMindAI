"""
Sample Academic Paper Generator.
Generates genuine academic PDF samples for immediate testing in PaperMind AI.
"""

import os
try:
    import pymupdf as fitz
except ImportError:
    import fitz

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sample_papers")
os.makedirs(OUTPUT_DIR, exist_ok=True)

SAMPLE_PAPERS = [
    {
        "filename": "sample_attention_transformer.pdf",
        "title": "Attention Is All You Need: Scalable Sequence Transduction Models",
        "authors": "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones",
        "category": "Natural Language Processing (NLP)",
        "abstract": (
            "The dominant sequence transduction models are based on complex recurrent or convolutional "
            "neural networks in an encoder-decoder configuration. In this work, we propose the Transformer, "
            "a model architecture eschewing recurrence and instead relying entirely on an attention mechanism "
            "to draw global dependencies between input and output. The Transformer allows for significantly more "
            "parallelization and can reach a new state of the art in translation quality after being trained for "
            "as little as twelve hours on eight P100 GPUs. Experiments on two machine translation tasks show "
            "these models to be superior in quality while being more parallelizable and requiring significantly "
            "less time to train."
        ),
        "introduction": (
            "Recurrent neural networks, especially long short-term memory (LSTM) and gated recurrent units (GRU), "
            "have been firmly established as state-of-the-art approaches in sequence modeling and transduction problems "
            "such as language modeling and machine translation. Numerous efforts have since continued to push the boundaries "
            "of recurrent language models and encoder-decoder architectures. Recurrent models typically factor computation "
            "along the symbol positions of the input and output sequences. Aligning the positions to steps in computation time, "
            "they generate a sequence of hidden states h_t, as a function of the previous hidden state h_{t-1} and the input for position t. "
            "This inherently sequential nature precludes parallelization within training examples, which becomes critical at longer "
            "sequence lengths, as memory constraints limit batching across examples."
        ),
        "methodology": (
            "The Transformer follows this overall architecture using stacked self-attention and point-wise, fully connected layers "
            "for both the encoder and decoder. The encoder is composed of a stack of N = 6 identical layers. Each layer has two sub-layers: "
            "a multi-head self-attention mechanism, and a simple, position-wise fully connected feed-forward network. We employ a residual "
            "connection around each of the two sub-layers, followed by layer normalization. To compute attention, we map a query and a set of "
            "key-value pairs to an output. Scaled Dot-Product Attention computes the dot products of the query with all keys, divides each by "
            "the square root of the key dimension d_k, and applies a softmax function to obtain weights on the values."
        ),
        "results": (
            "On the WMT 2014 English-to-German translation task, the big transformer model achieves a state-of-the-art BLEU score of 28.4, "
            "improving over the existing best results, including ensembles by more than 2.0 BLEU. On the WMT 2014 English-to-French translation task, "
            "our big model achieves a BLEU score of 41.0, outperforming all of the previously published single models, at 1/4 the training cost of "
            "the previous state-of-the-art model. Model training was exceptionally fast, establishing new records on both benchmark suites."
        ),
        "conclusion": (
            "In this work, we presented the Transformer, the first sequence transduction model based entirely on attention, replacing the "
            "recurrent layers most commonly used in encoder-decoder architectures with multi-headed self-attention. For translation tasks, the "
            "Transformer can be trained significantly faster than architectures based on recurrent or convolutional layers. On both WMT 2014 "
            "English-to-German and WMT 2014 English-to-French translation tasks, we achieve a new state of the art."
        )
    },
    {
        "filename": "sample_resnet_computer_vision.pdf",
        "title": "Deep Residual Learning for Image Recognition and Visual Classification",
        "authors": "Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun",
        "category": "Computer Vision & Pattern Recognition",
        "abstract": (
            "Deeper convolutional neural networks are more difficult to train. We present a residual learning framework to ease "
            "the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers "
            "as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. We provide "
            "comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from "
            "considerably increased depth. On the ImageNet dataset we evaluate residual nets with a depth of up to 152 layers—8× deeper "
            "than VGG nets but still having lower complexity."
        ),
        "introduction": (
            "Deep convolutional neural networks have led to a series of breakthroughs for image classification. Driven by the significance "
            "of depth, recent leading results on the challenging ImageNet dataset all exploit 'very deep' models with a depth of 16 to 30. "
            "Many other visual recognition tasks have also greatly benefited from deep models. But when deeper networks are able to start "
            "converging, a degradation problem has been exposed: with network depth increasing, accuracy gets saturated and then degrades rapidly. "
            "Unexpectedly, such degradation is not caused by overfitting, and adding more layers to a suitably deep model leads to higher training error."
        ),
        "methodology": (
            "Instead of hoping every few stacked layers directly fit a desired underlying mapping H(x), we explicitly let these layers fit a "
            "residual mapping F(x) := H(x) - x. The original mapping is recast into F(x) + x. We hypothesize that it is easier to optimize the "
            "residual mapping than to optimize the original, unreferenced mapping. The formulation of F(x) + x can be realized by feedforward "
            "neural networks with 'shortcut connections'. In our architecture, shortcut connections simply perform identity mapping, and their "
            "outputs are added to the outputs of the stacked layers. Identity shortcut connections introduce neither extra parameter nor "
            "computation complexity."
        ),
        "results": (
            "We evaluate our methods on the ImageNet 2012 classification dataset that consists of 1000 classes. An ensemble of these residual "
            "nets achieves 3.57% top-5 error on the ImageNet test set. This result won first place in the ILSVRC 2015 classification competition. "
            "Our 152-layer ResNet achieves significantly higher accuracy than 34-layer plain networks while demonstrating smooth convergence "
            "throughout standard stochastic gradient descent training."
        ),
        "conclusion": (
            "Residual learning effectively addresses the degradation problem that plagues extremely deep neural networks. By enabling depth "
            "up to 152 layers, ResNet establishes new state-of-the-art benchmarks in image recognition, object detection, and semantic segmentation."
        )
    },
    {
        "filename": "sample_phishing_detection_cybersecurity.pdf",
        "title": "Deep Neural Network Architectures for Phishing Website Detection and URL Threat Classification",
        "authors": "Elena Vance, Marcus Thorne, David S. Mitchell",
        "category": "Cybersecurity & Cryptography",
        "abstract": (
            "Phishing attacks remain one of the most prominent cybersecurity threats facing modern internet users, causing billions in financial "
            "damages through credential theft and identity compromise. Traditional blacklist and heuristic-based defense systems struggle to identify "
            "zero-hour phishing domains that dynamically alter their URL structure and host infrastructure. In this paper, we propose CyberGuard-Net, "
            "a deep learning pipeline integrating convolutional neural networks and character-level embeddings for real-time phishing detection. "
            "Evaluated on a benchmark of 120,000 legitimate and malicious URLs, our model achieves a 99.1% detection accuracy with a 0.2% false "
            "positive rate, outperforming commercial intrusion detection systems."
        ),
        "introduction": (
            "The rapid proliferation of digital services and online banking has amplified the threat landscape of social engineering and cybercrime. "
            "Among varied attack vectors, phishing continues to be the dominant gateway for enterprise intrusions, ransomware deployment, and credential "
            "harvesting. Conventional defense mechanisms rely heavily on static blacklists maintained by security vendors. However, modern adversaries "
            "employ automated domain generation algorithms (DGAs), fast-flux DNS configurations, and obfuscated subdomains to circumvent static rules. "
            "There is an urgent demand for automated, deep learning-based security systems capable of analyzing structural lexical properties in real-time."
        ),
        "methodology": (
            "We propose CyberGuard-Net, a multi-stage deep neural network architecture. First, raw URL strings are parsed without relying on third-party "
            "DNS lookups. Characters are tokenized into 128-dimensional dense vector embeddings. Next, parallel 1D convolutional layers with multiple "
            "filter kernel sizes (3, 5, 7) extract localized n-gram syntax features. A bidirectional LSTM layer models long-range semantic dependencies "
            "across query strings, path segments, and top-level domain anomalies. Finally, a fully connected dense layer with dropout regularization (0.4) "
            "and sigmoid activation outputs the binary threat probability."
        ),
        "results": (
            "We conducted extensive experiments on a corpus of 120,000 URLs collected from PhishTank, OpenPhish, and the Alexa Top 1M domains. "
            "CyberGuard-Net achieved an overall accuracy of 99.12%, precision of 98.84%, recall of 99.41%, and an F1-score of 99.12%. "
            "Comparative baselines, including Random Forest (94.2%) and Support Vector Machines (92.8%), were substantially outperformed. "
            "Inference latency averaged 4.2 milliseconds per URL, making it suitable for live browser-level blocking and firewall deployment."
        ),
        "conclusion": (
            "We demonstrated that character-level deep neural networks can accurately distinguish malicious phishing domains from legitimate web resources "
            "without manual feature engineering or network query overhead. Future work will extend the framework to adversarial evasion detection and "
            "cross-lingual phishing detection across internationalized domain names."
        )
    }
]


def create_sample_pdf(paper: dict, filepath: str):
    """Creates a multi-page academic PDF document."""
    doc = fitz.open()

    # --- Page 1: Title, Abstract, Introduction ---
    page1 = doc.new_page(width=595, height=842)  # A4 size in points
    y = 50

    # Header / Journal info
    page1.insert_text((50, y), "INTERNATIONAL CONFERENCE ON LEARNING & COMPUTING (ICLC)", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    y += 40

    # Title
    page1.insert_text((50, y), paper["title"][:50], fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.1))
    y += 22
    if len(paper["title"]) > 50:
        page1.insert_text((50, y), paper["title"][50:], fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.1))
        y += 25

    # Authors
    page1.insert_text((50, y), paper["authors"], fontsize=10, fontname="helv", color=(0.2, 0.3, 0.6))
    y += 35

    # Abstract Section
    page1.insert_text((50, y), "ABSTRACT", fontsize=11, fontname="hebo", color=(0.1, 0.1, 0.1))
    y += 18
    # Wrap abstract text
    rect_abstract = fitz.Rect(50, y, 545, y + 140)
    page1.insert_textbox(rect_abstract, paper["abstract"], fontsize=9.5, fontname="heit")
    y += 150

    # Introduction Section
    page1.insert_text((50, y), "1. INTRODUCTION", fontsize=11, fontname="hebo", color=(0.1, 0.1, 0.1))
    y += 18
    rect_intro = fitz.Rect(50, y, 545, y + 250)
    page1.insert_textbox(rect_intro, paper["introduction"], fontsize=9.5, fontname="helv")

    # --- Page 2: Methodology, Results, Conclusion ---
    page2 = doc.new_page(width=595, height=842)
    y2 = 50

    page2.insert_text((50, y2), "2. PROPOSED METHODOLOGY & SYSTEM ARCHITECTURE", fontsize=11, fontname="hebo", color=(0.1, 0.1, 0.1))
    y2 += 20
    rect_method = fitz.Rect(50, y2, 545, y2 + 230)
    page2.insert_textbox(rect_method, paper["methodology"], fontsize=9.5, fontname="helv")
    y2 += 245

    page2.insert_text((50, y2), "3. EXPERIMENTAL EVALUATION & RESULTS", fontsize=11, fontname="hebo", color=(0.1, 0.1, 0.1))
    y2 += 20
    rect_results = fitz.Rect(50, y2, 545, y2 + 200)
    page2.insert_textbox(rect_results, paper["results"], fontsize=9.5, fontname="helv")
    y2 += 215

    page2.insert_text((50, y2), "4. CONCLUSION AND FUTURE WORK", fontsize=11, fontname="hebo", color=(0.1, 0.1, 0.1))
    y2 += 20
    rect_conclusion = fitz.Rect(50, y2, 545, y2 + 150)
    page2.insert_textbox(rect_conclusion, paper["conclusion"], fontsize=9.5, fontname="helv")

    doc.save(filepath)
    doc.close()


def main():
    print(f"Generating sample academic PDFs in {OUTPUT_DIR}...")
    for paper in SAMPLE_PAPERS:
        path = os.path.join(OUTPUT_DIR, paper["filename"])
        create_sample_pdf(paper, path)
        print(f"Generated: {path}")
    print("All sample PDFs successfully generated!")


if __name__ == "__main__":
    main()
