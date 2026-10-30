"""
Dataset Loader and Curated arXiv Academic Corpus for PaperMind AI.
Provides 112 landmark real-world research paper abstracts with ground-truth
category labels across 7 core computer science and engineering disciplines.
"""

from typing import List, Dict
import pandas as pd


ARXIV_SAMPLE_PAPERS: List[Dict[str, str]] = [
    # =========================================================================
    # 1. Artificial Intelligence & Machine Learning (16 Papers)
    # =========================================================================
    {
        "title": "Mastering the Game of Go with Deep Neural Networks and Tree Search",
        "abstract": "The game of Go has long been viewed as the most challenging of classic games for artificial intelligence. We introduce AlphaGo, which combines deep neural networks with Monte Carlo tree search, trained on human expert games and reinforcement learning from self-play to achieve superhuman performance.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Proximal Policy Optimization Algorithms",
        "abstract": "We propose a new family of policy gradient methods for reinforcement learning, which alternate between sampling data through interaction with the environment, and optimizing a 'surrogate' objective function using stochastic gradient ascent.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Adam: A Method for Stochastic Optimization",
        "abstract": "We introduce Adam, an algorithm for first-order gradient-based optimization of stochastic objective functions, based on adaptive estimates of lower-order moments. The method is computationally efficient and well suited for large deep neural network training.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Deep Double Q-Learning in Atari Environments",
        "abstract": "The popular Q-learning algorithm is known to overestimate action values under certain conditions. We show that the idea behind Double Q-learning can be generalized to deep neural networks for reinforcement learning and value function estimation.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Dropout: A Simple Way to Prevent Neural Networks from Overfitting",
        "abstract": "Deep neural networks with a large number of parameters are very powerful machine learning systems. However, overfitting is a serious problem. We introduce dropout which randomly drops units and their connections during training to prevent complex co-adaptations.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift",
        "abstract": "Training Deep Neural Networks is complicated by the fact that the distribution of each layer's inputs changes during training. We address this by incorporating Batch Normalization into the network architecture to stabilize activation distributions.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Generative Adversarial Networks",
        "abstract": "We propose a framework for estimating generative models via an adversarial process, in which we simultaneously train two models: a generative model that captures data distribution, and a discriminative model that estimates the probability of sample authenticity.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Auto-Encoding Variational Bayes",
        "abstract": "We introduce a stochastic variational inference and learning algorithm for directed probabilistic latent variable models. The reparameterization of the variational lower bound yields a simple differentiable estimator optimized via standard gradient ascent.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Decoupled Neural Interfaces using Synthetic Gradients",
        "abstract": "Training neural networks requires feedforward and error backpropagation across layers. We introduce synthetic gradients where layers communicate asynchronously using learned gradient estimators, breaking forward and backward locking in deep networks.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Deep Reinforcement Learning with Double Q-learning",
        "abstract": "The goal of reinforcement learning is to learn policies that maximize cumulative expected discounted reward. We prove that standard Q-learning suffers from overestimation bias and derive an improved double Bellman operator formulation.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks",
        "abstract": "We propose an algorithm for meta-learning that is compatible with any model trained with gradient descent. The goal of few-shot meta-learning is to train a model on a variety of tasks such that it can solve new learning tasks using only a few training samples.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Layer Normalization for Deep Recurrent and Feedforward Neural Networks",
        "abstract": "Training state-of-the-art deep neural networks is computationally expensive. We propose layer normalization which estimates the normalization statistics directly from the summed inputs to the neurons within the same hidden layer, speeding up training.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Mixup: Beyond Empirical Risk Minimization",
        "abstract": "Large deep neural networks are prone to memorization and sensitivity to adversarial examples. We propose mixup, a simple learning principle that trains neural networks on convex linear combinations of pairs of examples and their training targets.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Representation Learning with Contrastive Predictive Coding",
        "abstract": "While supervised learning has driven massive progress, unsupervised representation learning remains a core challenge in machine learning. We propose contrastive predictive coding (CPC) using powerful autoregressive models to extract representations.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Graph Attention Networks: Scalable Graph Representation Learning",
        "abstract": "We present graph attention networks (GAT), novel neural network architectures that operate on graph-structured data, leveraging masked self-attentional layers to address the shortcomings of prior methods based on graph convolutions.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Denoising Diffusion Probabilistic Models",
        "abstract": "We present high quality image synthesis results using diffusion probabilistic models. Our models are trained using a weighted variational bound designed according to a novel connection between diffusion probabilistic models and denoising score matching.",
        "category": "Artificial Intelligence & Machine Learning"
    },

    # =========================================================================
    # 2. Computer Vision & Pattern Recognition (16 Papers)
    # =========================================================================
    {
        "title": "Deep Residual Learning for Image Recognition",
        "abstract": "Deeper convolutional neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper. On ImageNet we evaluate residual nets with a depth of up to 152 layers.",
        "category": "Computer Vision & Pattern Recognition"
    },
    {
        "title": "Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks",
        "abstract": "State-of-the-art object detection networks depend on region proposal algorithms to hypothesize object locations. We introduce a Region Proposal Network (RPN) that shares full-image convolutional features with the detection network for real-time inference.",
        "category": "Computer Vision & Pattern Recognition"
    },
    {
        "title": "U-Net: Convolutional Networks for Biomedical Image Segmentation",
        "abstract": "There is large consent that successful training of deep networks requires many thousand annotated training samples. We present a network and training strategy that relies on the strong use of data augmentation for segmentation of neuronal structures.",
        "category": "Computer Vision & Pattern Recognition"
    },
    {
        "title": "YOLO: You Only Look Once: Unified, Real-Time Object Detection",
        "abstract": "We present YOLO, a new approach to object detection. Prior work repurposes classifiers to perform detection. Instead, we frame object detection as a regression problem to spatially separated bounding boxes and associated class probabilities.",
        "category": "Computer Vision & Pattern Recognition"
    },
    {
        "title": "Vision Transformer: An Image is Worth 16x16 Words",
        "abstract": "While the Transformer architecture has become the de-facto standard for natural language processing tasks, its applications to computer vision remain limited. We show that a pure transformer applied directly to sequences of image patches can perform very well on image classification.",
        "category": "Computer Vision & Pattern Recognition"
    },
    {
        "title": "Mask R-CNN for Instance Segmentation",
        "abstract": "We present a conceptually simple, flexible, and general framework for object instance segmentation. Our approach efficiently detects objects in an image while simultaneously generating a high-quality segmentation mask for each instance.",
        "category": "Computer Vision & Pattern Recognition"
    },
    {
        "title": "Feature Pyramid Networks for Object Detection",
        "abstract": "Feature pyramids are a basic component in recognition systems for detecting objects at different scales. We develop a top-down architecture with lateral connections for building high-level semantic feature maps at all scales in convolutional networks.",
        "category": "Computer Vision & Pattern Recognition"
    },
    {
        "title": "NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis",
        "abstract": "We present a method that achieves state-of-the-art results for synthesizing novel views of complex 3D scenes by optimizing an underlying continuous volumetric scene function using a sparse set of input views and volume rendering techniques.",
        "category": "Computer Vision & Pattern Recognition"
    },
    {
        "title": "PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation",
        "abstract": "Point cloud is an important type of geometric data structure. We design a novel type of deep neural network that directly consumes point clouds, which well respects the permutation invariance of points in the input 3D coordinate space.",
        "category": "Computer Vision & Pattern Recognition"
    },
    {
        "title": "Segment Anything: Foundation Models for Image Segmentation",
        "abstract": "We introduce the Segment Anything (SAM) project: a new task, model, and dataset for image segmentation. Using an efficient model in a data collection loop, we built the largest segmentation dataset to date, with over 1 billion masks on 11 million licensed images.",
        "category": "Computer Vision & Pattern Recognition"
    },
    {
        "title": "FlowNet: Learning Optical Flow with Convolutional Networks",
        "abstract": "Optical flow estimation is a core problem in computer vision. We propose and train end-to-end convolutional neural networks capable of predicting optical flow fields directly from pairs of consecutive video frames at high frame rates.",
        "category": "Computer Vision & Pattern Recognition"
    },
    {
        "title": "High-Resolution Image Synthesis with Latent Diffusion Models",
        "abstract": "By decomposing the image formation process into a sequential application of denoising autoencoders, diffusion models achieve state-of-the-art visual synthesis. We apply latent diffusion models to high-resolution image rendering and inpainting.",
        "category": "Computer Vision & Pattern Recognition"
    },
    {
        "title": "Real-Time Panoramic Video Stitching with Deep Warping and Feature Matching",
        "abstract": "Panoramic multi-camera video stitching requires accurate spatial alignment and photometric blending. We develop deep homography estimation and mesh deformation networks to eliminate parallax artifacts across multi-view visual sensors.",
        "category": "Computer Vision & Pattern Recognition"
    },
    {
        "title": "Image Super-Resolution Using Deep Convolutional Networks",
        "abstract": "We propose a deep learning method for single image super-resolution (SRCNN). Our method directly learns an end-to-end mapping between the low-resolution and high-resolution images, with lightweight network layers achieving high PSNR.",
        "category": "Computer Vision & Pattern Recognition"
    },
    {
        "title": "Deep High-Resolution Representation Learning for Human Pose Estimation",
        "abstract": "In this paper, we are interested in the human pose estimation problem with a focus on learning high-resolution representations. High-resolution representations are maintained throughout the whole process, generating precise keypoint heatmaps.",
        "category": "Computer Vision & Pattern Recognition"
    },
    {
        "title": "End-to-End Object Detection with Transformers (DETR)",
        "abstract": "We present a new method that views object detection as a direct set prediction problem. Our approach streamlines the detection pipeline, dropping many hand-designed components like non-maximum suppression or anchor generation using transformer encoder-decoders.",
        "category": "Computer Vision & Pattern Recognition"
    },

    # =========================================================================
    # 3. Natural Language Processing (NLP) (16 Papers)
    # =========================================================================
    {
        "title": "Attention Is All You Need",
        "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks. We propose the Transformer, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism.",
        "category": "Natural Language Processing (NLP)"
    },
    {
        "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        "abstract": "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. BERT is designed to pre-train deep bidirectional representations from unlabeled text.",
        "category": "Natural Language Processing (NLP)"
    },
    {
        "title": "Language Models are Few-Shot Learners",
        "abstract": "Recent work has demonstrated substantial gains on many NLP tasks and benchmarks through pre-training on a large corpus of text followed by fine-tuning. We demonstrate that scaling up language models greatly improves task-agnostic, few-shot performance.",
        "category": "Natural Language Processing (NLP)"
    },
    {
        "title": "RoBERTa: A Robustly Optimized BERT Pretraining Approach",
        "abstract": "Language model pretraining has led to significant performance gains, but careful comparisons between approaches are challenging. We find that BERT was significantly undertrained, and propose RoBERTa which improves downstream NLP benchmark results.",
        "category": "Natural Language Processing (NLP)"
    },
    {
        "title": "Speech and Language Processing: Neural Machine Translation by Jointly Learning to Align and Translate",
        "abstract": "Neural machine translation is a recently proposed approach to machine translation. We hypothesize that the use of a fixed-length vector is a bottleneck in improving the performance of this basic encoder-decoder architecture and introduce attention.",
        "category": "Natural Language Processing (NLP)"
    },
    {
        "title": "GPT-4 Technical Report: Advanced Reasoning and Text Generation",
        "abstract": "We report the development of GPT-4, a large-scale, multimodal model which can accept image and text inputs and produce text outputs. GPT-4 exhibits human-level performance on various professional and academic benchmarks.",
        "category": "Natural Language Processing (NLP)"
    },
    {
        "title": "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer (T5)",
        "abstract": "Transfer learning has emerged as a powerful technique in natural language processing (NLP). We introduce a unified framework that treats every text processing problem as a text-to-text task, achieving state-of-the-art results across summarization and translation.",
        "category": "Natural Language Processing (NLP)"
    },
    {
        "title": "XLNet: Generalized Autoregressive Pretraining for Language Understanding",
        "abstract": "With the capability of modeling bidirectional contexts, denoising autoencoding based pretraining like BERT achieves better performance than autoregressive language modeling. We propose XLNet, a generalized autoregressive pretraining method that enables learning bidirectional contexts.",
        "category": "Natural Language Processing (NLP)"
    },
    {
        "title": "LLaMA: Open and Efficient Foundation Language Models",
        "abstract": "We introduce LLaMA, a collection of foundation language models ranging from 7B to 65B parameters. We train our models on trillions of tokens, showing that it is possible to train state-of-the-art models using publicly available datasets without proprietary data.",
        "category": "Natural Language Processing (NLP)"
    },
    {
        "title": "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
        "abstract": "BERT and RoBERTa have set a new state-of-the-art performance on sentence-pair regression tasks like semantic textual similarity. However, it requires that both sentences are fed into the network, which is computationally expensive. We present Sentence-BERT.",
        "category": "Natural Language Processing (NLP)"
    },
    {
        "title": "Direct Preference Optimization: Your Language Model is Secretly a Reward Model",
        "abstract": "While reinforcement learning from human feedback (RLHF) is effective in steering large language models, it requires training complex reward models. We introduce Direct Preference Optimization (DPO), which stably aligns language models directly on preference pairs.",
        "category": "Natural Language Processing (NLP)"
    },
    {
        "title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
        "abstract": "Large pre-trained language models store factual knowledge in their parameters, but struggle with precise knowledge retrieval and hallucinations. We propose Retrieval-Augmented Generation (RAG) models combining pre-trained parametric and non-parametric memory.",
        "category": "Natural Language Processing (NLP)"
    },
    {
        "title": "LoRA: Low-Rank Adaptation of Large Language Models",
        "abstract": "An important paradigm of natural language processing consists of large-scale pre-training on general domain data and adaptation to specific tasks. We propose Low-Rank Adaptation (LoRA), which freezes the pre-trained model weights and injects trainable rank decomposition matrices.",
        "category": "Natural Language Processing (NLP)"
    },
    {
        "title": "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness",
        "abstract": "Transformers are slow and memory-hungry on long sequences, as the time and memory complexity of self-attention are quadratic in sequence length. We propose FlashAttention, an IO-aware exact attention algorithm that uses tiling to reduce memory reads and writes.",
        "category": "Natural Language Processing (NLP)"
    },
    {
        "title": "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models",
        "abstract": "We explore how generating a chain of thought—a series of intermediate reasoning steps—significantly improves the ability of large language models to perform complex arithmetic, commonsense, and symbolic reasoning tasks without fine-tuning.",
        "category": "Natural Language Processing (NLP)"
    },
    {
        "title": "BLEU: A Method for Automatic Evaluation of Machine Translation",
        "abstract": "Human evaluations of machine translation are extensive but expensive. We propose BLEU, an automated evaluation metric that measures the n-gram concordance between machine translation candidates and reference texts, establishing the standard benchmark for translation quality.",
        "category": "Natural Language Processing (NLP)"
    },

    # =========================================================================
    # 4. Cybersecurity & Cryptography (16 Papers)
    # =========================================================================
    {
        "title": "Deep Neural Network Architectures for Phishing Website Detection and URL Threat Classification",
        "abstract": "Phishing attacks remain one of the most prominent cybersecurity threats facing internet users. We propose CyberGuard-Net, a deep learning pipeline integrating convolutional neural networks and character embeddings for real-time malicious URL detection.",
        "category": "Cybersecurity & Cryptography"
    },
    {
        "title": "DeepLog: Anomaly Detection and Diagnosis from System Logs through Deep Learning",
        "abstract": "Automated log analysis and intrusion detection is critical for large-scale software systems. We propose DeepLog, a deep neural network utilizing Long Short-Term Memory (LSTM) to model system log sequences and flag cyber anomalies.",
        "category": "Cybersecurity & Cryptography"
    },
    {
        "title": "End-to-End Deep Learning for Android Malware Detection and Classification",
        "abstract": "The exponential growth of malicious Android applications threatens mobile security. We present a deep learning malware analysis framework that inspects bytecode instructions, permissions, and API call graphs without manual feature engineering.",
        "category": "Cybersecurity & Cryptography"
    },
    {
        "title": "Adversarial Attacks on Deep Learning Systems for Network Intrusion Detection",
        "abstract": "Deep learning models are increasingly deployed in network intrusion detection systems (NIDS). We explore how adversarial evasion perturbations craft malicious packet traffic that evades deep neural classifiers while maintaining payload execution.",
        "category": "Cybersecurity & Cryptography"
    },
    {
        "title": "Post-Quantum Cryptography: Lattice-Based Key Encapsulation and Digital Signatures",
        "abstract": "With quantum computers threatening public-key cryptography (RSA and ECC), lattice-based cryptosystems have emerged as leading post-quantum cryptography candidates against Shor's algorithm.",
        "category": "Cybersecurity & Cryptography"
    },
    {
        "title": "Zero-Day Vulnerability Discovery via Automated Smart Contract Fuzzing",
        "abstract": "Smart contract vulnerabilities cause massive financial exploits in decentralized finance. We introduce hybrid symbolic execution and greybox fuzzing to uncover reentrancy bugs and authorization bypasses.",
        "category": "Cybersecurity & Cryptography"
    },
    {
        "title": "Advanced Persistent Threat Detection via Provenance Graph Neural Networks",
        "abstract": "Detecting Advanced Persistent Threats (APTs) requires correlating system-level audit events over long temporal windows. We model kernel audit logs as provenance graphs and apply graph neural networks to reconstruct attack kill chains and lateral movement.",
        "category": "Cybersecurity & Cryptography"
    },
    {
        "title": "Homomorphic Encryption for Privacy-Preserving Machine Learning Inference",
        "abstract": "Outsourcing machine learning inference to untrusted cloud environments raises severe privacy concerns. We construct secure evaluation protocols using leveled homomorphic encryption (CKKS) enabling encrypted inference without plaintext exposure.",
        "category": "Cybersecurity & Cryptography"
    },
    {
        "title": "Ransomware Early Warning System via File System Telemetry and Entropy Analysis",
        "abstract": "Crypto-ransomware attacks devastate enterprise operations by encrypting critical user files. We present an early warning detection system that analyzes real-time I/O request packets, file entropy spikes, and canary file tampering to halt encryption processes.",
        "category": "Cybersecurity & Cryptography"
    },
    {
        "title": "Automated Firmware Vulnerability Analysis via Emulation and Directed Fuzzing",
        "abstract": "Internet of Things (IoT) devices frequently harbor unpatched security vulnerabilities. We develop a full-system firmware emulation harness combined with directed greybox fuzzing to discover memory corruption and buffer overflow exploits in embedded binaries.",
        "category": "Cybersecurity & Cryptography"
    },
    {
        "title": "Zero Trust Architecture: Microsegmentation and Dynamic Access Control Policies",
        "abstract": "Traditional perimeter-based network defenses fail against insider threats and credential compromise. We formulate a Zero Trust Architecture integrating continuous device authentication, microsegmentation, and dynamic risk-based access control.",
        "category": "Cybersecurity & Cryptography"
    },
    {
        "title": "Deep Learning for Side-Channel Attack Resistance in Hardware Cryptography",
        "abstract": "Physical cryptographic implementations leak sensitive key material through power consumption and electromagnetic radiation. We evaluate convolutional deep learning classifiers against protected AES implementations to assess side-channel resistance.",
        "category": "Cybersecurity & Cryptography"
    },
    {
        "title": "Darknet Threat Intelligence Mining using NLP and Entity Resolution",
        "abstract": "Underground darknet marketplaces and hacker forums serve as hubs for trading zero-day exploits and stolen credentials. We implement natural language processing pipelines and named entity recognition to track threat actors and illicit cyber activity.",
        "category": "Cybersecurity & Cryptography"
    },
    {
        "title": "Differential Privacy for Federated Learning Against Model Inversion Attacks",
        "abstract": "Distributed federated learning models are vulnerable to gradient leakage and reconstruction attacks. We apply Renyi differential privacy with adaptive noise injection to protect user gradients against malicious central aggregators.",
        "category": "Cybersecurity & Cryptography"
    },
    {
        "title": "DNS Tunneling and Domain Generation Algorithm Detection at Scale",
        "abstract": "Malware command-and-control (C2) servers utilize domain generation algorithms (DGAs) and DNS tunneling to bypass perimeter firewalls. We train recurrent neural network classifiers on passive DNS queries to intercept covert data exfiltration.",
        "category": "Cybersecurity & Cryptography"
    },
    {
        "title": "Defending Against Software Supply Chain Attacks: Continuous Provenance and Dependency Auditing",
        "abstract": "Modern software ecosystems heavily rely on third-party dependencies, opening attack vectors for malicious package injection. We propose automated software bill of materials (SBOM) auditing and cryptographic package provenance verification.",
        "category": "Cybersecurity & Cryptography"
    },

    # =========================================================================
    # 5. Data Science & Big Data Analytics (16 Papers)
    # =========================================================================
    {
        "title": "XGBoost: A Scalable Tree Boosting System",
        "abstract": "Tree boosting is a highly effective and widely used machine learning method. We describe a scalable end-to-end tree boosting system called XGBoost, used widely by data scientists to achieve state-of-the-art results on tabular machine learning challenges.",
        "category": "Data Science & Big Data Analytics"
    },
    {
        "title": "T-SNE: Visualizing Data using t-SNE Dimensionality Reduction",
        "abstract": "We present a new technique called t-SNE that visualizes high-dimensional data by giving each datapoint a location in a two or three-dimensional map, revealing clusters, local structure, and multi-scale manifold relationships.",
        "category": "Data Science & Big Data Analytics"
    },
    {
        "title": "Feature Engineering and Imbalanced Learning in High-Dimensional Clinical Datasets",
        "abstract": "High-dimensional healthcare records present severe class imbalance and missing value challenges. We introduce statistical imputation, SMOTE sampling, and mutual information feature selection protocols for predictive patient analytics.",
        "category": "Data Science & Big Data Analytics"
    },
    {
        "title": "Time Series Anomaly Detection for Cloud Datacenters using Matrix Profiles",
        "abstract": "Monitoring millions of telemetry metrics in cloud server clusters requires scalable data mining algorithms. We apply fast matrix profile algorithms for streaming time series anomaly detection and motif discovery across distributed server logs.",
        "category": "Data Science & Big Data Analytics"
    },
    {
        "title": "Apache Spark: Cluster Computing with Working Sets",
        "abstract": "MapReduce and its variants have been highly successful in implementing large-scale data-intensive applications. We introduce Spark, a specialized framework for iterative machine learning and interactive data analytics queries.",
        "category": "Data Science & Big Data Analytics"
    },
    {
        "title": "Principal Component Analysis and Sparse Dictionary Learning for High-Dimensional Data",
        "abstract": "High-dimensional data analytics often suffers from the curse of dimensionality. We develop convex sparse coding and PCA formulations for unsupervised feature reduction and latent factor modeling.",
        "category": "Data Science & Big Data Analytics"
    },
    {
        "title": "LightGBM: A Highly Efficient Gradient Boosting Decision Tree",
        "abstract": "Gradient Boosting Decision Tree is a popular machine learning algorithm. We propose LightGBM with Gradient-based One-Side Sampling and Exclusive Feature Bundling, dramatically speeding up training on massive tabular big data datasets.",
        "category": "Data Science & Big Data Analytics"
    },
    {
        "title": "Forecasting at Scale using Decomposable Additive Time Series Models",
        "abstract": "Forecasting is a common data science task that helps with resource allocation and goal setting. We introduce Prophet, a decomposable time series model combining trend, seasonality, and holiday components for automated business forecasting.",
        "category": "Data Science & Big Data Analytics"
    },
    {
        "title": "Isolation Forest for Fast Anomaly Detection in Streaming Data",
        "abstract": "Most existing anomaly detection approaches construct a profile of normal instances and identify anomalies as instances that do not conform. We propose Isolation Forest, which detects anomalies purely by isolating mechanisms without distance metrics.",
        "category": "Data Science & Big Data Analytics"
    },
    {
        "title": "Dremel: Interactive Analysis of Web-Scale Datasets in Cloud Warehouses",
        "abstract": "Dremel is an interactive query system for analyzing read-only nested data. By combining multi-level execution trees and columnar data representations, it can run aggregation queries over petabyte datasets in seconds, powering Google BigQuery.",
        "category": "Data Science & Big Data Analytics"
    },
    {
        "title": "UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction",
        "abstract": "UMAP is a novel manifold learning technique for dimension reduction. UMAP is constructed from a theoretical framework based in Riemannian geometry and algebraic topology, outperforming t-SNE in preservation of global dataset structure.",
        "category": "Data Science & Big Data Analytics"
    },
    {
        "title": "Causal Inference in Observational Studies using Propensity Score Matching",
        "abstract": "Estimating causal effects in observational data is hindered by confounding variables. We review non-parametric propensity score matching and double machine learning to estimate unbiased average treatment effects across economic datasets.",
        "category": "Data Science & Big Data Analytics"
    },
    {
        "title": "Automated Machine Learning: Hyperparameter Optimization and Pipeline Synthesis",
        "abstract": "Data scientists spend extensive manual effort designing preprocessing pipelines and tuning model hyperparameters. We develop Bayesian optimization and genetic algorithms to automate model selection and ensemble pipeline synthesis.",
        "category": "Data Science & Big Data Analytics"
    },
    {
        "title": "Scalable Graph Mining and Community Detection in Complex Social Networks",
        "abstract": "Social networks and citation graphs contain millions of vertices and billions of edges. We design parallel Louvain modularity algorithms and random-walk graph embeddings to partition large-scale relational graphs into cohesive community structures.",
        "category": "Data Science & Big Data Analytics"
    },
    {
        "title": "Data Quality Validation and Schema Drift Detection in Modern Data Lakehouses",
        "abstract": "Production machine learning pipelines frequently fail due to silent data corruption and unexpected schema drift. We propose automated data contracts, statistical constraint verification, and drift monitors for streaming data lakehouses.",
        "category": "Data Science & Big Data Analytics"
    },
    {
        "title": "Spatial-Temporal Modeling of Urban Sensor Data for Traffic and Pollution Forecasting",
        "abstract": "Smart city sensor networks generate high-frequency multivariate spatial-temporal data streams. We formulate spatial autoregression and graph convolutional recurrent models to predict urban traffic congestion and particulate emissions.",
        "category": "Data Science & Big Data Analytics"
    },

    # =========================================================================
    # 6. Robotics & Autonomous Systems (16 Papers)
    # =========================================================================
    {
        "title": "ORB-SLAM2: An Open-Source SLAM System for Monocular, Stereo, and RGB-D Cameras",
        "abstract": "We present ORB-SLAM2, a complete SLAM system for monocular, stereo, and RGB-D cameras, including map reuse, loop closing, and relocalization capabilities for autonomous mobile robots operating in real-time indoor and outdoor environments.",
        "category": "Robotics & Autonomous Systems"
    },
    {
        "title": "End-to-End Training of Deep Visuomotor Policies for Robotic Manipulation",
        "abstract": "Policy search methods enable robots to acquire complex motor skills from trial-and-error experience. We introduce a method for training deep visuomotor policies that map camera images directly to robot joint torque commands.",
        "category": "Robotics & Autonomous Systems"
    },
    {
        "title": "Trajectory Optimization and Motion Planning for Quadruped Locomotion on Uneven Terrain",
        "abstract": "Agile legged locomotion requires dynamic balance and robust foothold selection. We formulate non-linear model predictive control and whole-body trajectory optimization for quadrupedal robots navigating obstacle-laden terrains.",
        "category": "Robotics & Autonomous Systems"
    },
    {
        "title": "Autonomous Drone Navigation in GPS-Denied Environments using Visual Inertial Odometry",
        "abstract": "Unmanned aerial vehicles (UAVs) operating indoors cannot rely on global positioning satellites. We propose multi-sensor fusion combining IMU, optical flow, and stereo vision for drift-free autonomous flight.",
        "category": "Robotics & Autonomous Systems"
    },
    {
        "title": "Soft Robotics Actuation and Tactile Sensing for Compliant Grasping",
        "abstract": "Rigid robotic grippers struggle with delicate object manipulation. We design pneumatically actuated elastomeric soft fingers equipped with embedded piezoresistive sensor arrays for adaptive grasping.",
        "category": "Robotics & Autonomous Systems"
    },
    {
        "title": "RRT*: Sampling-Based Algorithms for Optimal Motion Planning in Complex Environments",
        "abstract": "Sampling-based motion planning algorithms like Rapidly-exploring Random Trees (RRT) are widely used for robotic arm manipulation. We introduce RRT*, proving asymptotic optimality for collision-free trajectory generation in high-dimensional configuration spaces.",
        "category": "Robotics & Autonomous Systems"
    },
    {
        "title": "Learning Agile Bipedal Locomotion via Sim-to-Real Reinforcement Learning",
        "abstract": "Humanoid and bipedal robots demand robust stabilization against uneven ground disturbances. We train deep neural locomotion policies in physics simulators with domain randomization, transferring dynamic walking controllers directly to physical hardware.",
        "category": "Robotics & Autonomous Systems"
    },
    {
        "title": "3D LiDAR Point Cloud Perception and Bounding Box Tracking for Autonomous Vehicles",
        "abstract": "Self-driving vehicles require accurate 3D scene understanding. We implement point cloud voxelization and PointPillars neural architectures coupled with multi-hypothesis Kalman filter tracking for real-time pedestrian and vehicle obstacle detection.",
        "category": "Robotics & Autonomous Systems"
    },
    {
        "title": "Bilateral Force-Feedback Teleoperation for Robotic Minimally Invasive Surgery",
        "abstract": "Surgical telemanipulation systems enhance precision in endoscopic procedures. We develop passivity-based bilateral controllers providing high-fidelity force reflection to the surgeon's master console while guaranteeing absolute control loop stability.",
        "category": "Robotics & Autonomous Systems"
    },
    {
        "title": "Autonomous Underwater Vehicle (AUV) Navigation using Acoustic SLAM and Bathymetry",
        "abstract": "Underwater environments severely attenuate electromagnetic waves, precluding GPS and visual tracking. We implement acoustic multibeam sonar SLAM and bathymetric terrain matching for long-range autonomous submarine navigation.",
        "category": "Robotics & Autonomous Systems"
    },
    {
        "title": "Multi-Agent Pathfinding (MAPF) and Coordination for Autonomous Warehouse Robot Fleets",
        "abstract": "Logistics fulfillment centers deploy hundreds of mobile robots to retrieve shelving pods. We formulate conflict-based search algorithms to compute collision-free, time-minimal trajectories for dense multi-robot fleets.",
        "category": "Robotics & Autonomous Systems"
    },
    {
        "title": "Tactile-Driven In-Hand Manipulation with Dense Visuotactile Sensing",
        "abstract": "Dexterous robotic hands need rich tactile feedback to adjust grip and reorient objects. We incorporate GelSight elastomeric sensors to track contact geometry and shear traction fields for closed-loop in-hand robotic repositioning.",
        "category": "Robotics & Autonomous Systems"
    },
    {
        "title": "Deep Inverse Reinforcement Learning for Human-Robot Cooperative Manipulation",
        "abstract": "Collaborative robots (cobots) working alongside human operators must infer intent and adjust compliance. We formulate maximum entropy inverse reinforcement learning to extract human task preferences from kinesthetic demonstrations.",
        "category": "Robotics & Autonomous Systems"
    },
    {
        "title": "String-Stable Cooperative Adaptive Cruise Control for Heavy-Duty Autonomous Vehicle Platooning",
        "abstract": "Vehicle platooning reduces aerodynamic drag and fuel consumption on highways. We design vehicle-to-vehicle (V2V) cooperative adaptive cruise control laws ensuring string stability and safe trailing distances under emergency braking.",
        "category": "Robotics & Autonomous Systems"
    },
    {
        "title": "Cartesian Impedance Control and Compliant Peg-in-Hole Assembly for Industrial Robots",
        "abstract": "High-precision mechanical insertion tasks cannot rely on rigid position control due to part manufacturing tolerances. We formulate Cartesian impedance control with vision-guided search trajectories for contact-rich robotic assembly.",
        "category": "Robotics & Autonomous Systems"
    },
    {
        "title": "Semantic Topological Mapping for Autonomous Service Robots in Domestic Environments",
        "abstract": "Service robots must interpret natural language instructions and navigate complex homes. We build 3D semantic scene graphs linking metric metric point clouds to room entities, enabling semantic goal-directed robotic navigation.",
        "category": "Robotics & Autonomous Systems"
    },

    # =========================================================================
    # 7. Networks & Distributed Computing (16 Papers)
    # =========================================================================
    {
        "title": "Spanner: Google's Globally-Distributed Database",
        "abstract": "Spanner is Google's scalable, multi-version, globally-distributed, and synchronously-replicated database. It is the first system to distribute data globally and support externally-consistent distributed transactions using TrueTime GPS hardware clocks.",
        "category": "Networks & Distributed Computing"
    },
    {
        "title": "Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing",
        "abstract": "We present Resilient Distributed Datasets (RDDs), a distributed memory abstraction that lets programmers perform in-memory computations on large clusters in a fault-tolerant manner, forming the foundational architecture of Apache Spark.",
        "category": "Networks & Distributed Computing"
    },
    {
        "title": "BBR: Congestion-Based Congestion Control for High-Throughput Network Protocols",
        "abstract": "Traditional loss-based congestion control protocols degrade network throughput and cause bufferbloat. We introduce BBR, a model-based congestion control algorithm that continuously measures bottleneck bandwidth and round-trip propagation time.",
        "category": "Networks & Distributed Computing"
    },
    {
        "title": "Raft: In Search of an Understandable Consensus Algorithm",
        "abstract": "Raft is a consensus algorithm for managing a replicated log. It produces a result equivalent to (multi-)Paxos, and it is as efficient as Paxos, but its structure is different, making Raft more understandable than Paxos.",
        "category": "Networks & Distributed Computing"
    },
    {
        "title": "Software-Defined Networking: A Comprehensive Survey of OpenFlow Controllers and Edge Routing",
        "abstract": "Decoupling the control plane from the data plane enables programmable network management. We review OpenFlow protocols, SDN controller architectures, and low-latency packet switching across WAN backbones.",
        "category": "Networks & Distributed Computing"
    },
    {
        "title": "Paxos Made Live: An Engineering Perspective on Replicated State Machines",
        "abstract": "Building a production fault-tolerant distributed system based on Paxos presents significant engineering challenges. We describe our experiences building a distributed lock service and master coordinator, covering disk corruption and quorum leases.",
        "category": "Networks & Distributed Computing"
    },
    {
        "title": "Edge Computing and Multi-Access Edge Cloud Architecture for Low-Latency Industrial Services",
        "abstract": "Industrial automation requires sub-millisecond network latency that centralized cloud datacenters cannot provide. We design an edge computing framework that dynamically offloads computation to 5G Multi-Access Edge Computing (MEC) nodes.",
        "category": "Networks & Distributed Computing"
    },
    {
        "title": "QUIC: A UDP-Based Multiplexed and Secure Transport Protocol for the Modern Internet",
        "abstract": "TCP and TLS impose multiple round trips during connection establishment and suffer from head-of-line blocking. We present QUIC, a transport protocol deployed over UDP that supports zero-round-trip handshakes and multiplexed independent streams.",
        "category": "Networks & Distributed Computing"
    },
    {
        "title": "Kubernetes: Production-Grade Container Scheduling and Cluster Orchestration at Scale",
        "abstract": "Managing thousands of microservice containers across heterogeneous compute clusters requires automated deployment and failure recovery. We analyze the architectural design of Kubernetes, pod scheduling controllers, and service meshes.",
        "category": "Networks & Distributed Computing"
    },
    {
        "title": "Consistent Hashing and Distributed Caching Protocols for High-Availability Storage",
        "abstract": "Web cache servers and distributed key-value stores face severe load imbalances when servers join or leave. We formulate consistent hashing algorithms with virtual replication rings, ensuring minimal key migration and hot spot avoidance.",
        "category": "Networks & Distributed Computing"
    },
    {
        "title": "Network Function Virtualization (NFV) and Service Function Chaining in 5G Core Networks",
        "abstract": "Carrier-grade telecommunications networks are transitioning from dedicated hardware middleboxes to software appliances. We evaluate high-speed packet processing frameworks (DPDK) and dynamic service function chaining for 5G core slicing.",
        "category": "Networks & Distributed Computing"
    },
    {
        "title": "Multipath TCP: Protocol Design and Performance in Heterogeneous Wireless Networks",
        "abstract": "Mobile devices typically possess multiple network interfaces such as Wi-Fi and Cellular LTE. Multipath TCP allows simultaneous transmission across multiple paths, increasing connection resilience and aggregate data throughput.",
        "category": "Networks & Distributed Computing"
    },
    {
        "title": "Serverless Computing Architectures: Cold Start Latency and Lightweight Sandboxing",
        "abstract": "Function-as-a-Service (FaaS) platforms execute ephemeral user code in response to events. We investigate container warm-up caching and microVM sandboxing (Firecracker) to reduce invocation cold starts in distributed serverless clouds.",
        "category": "Networks & Distributed Computing"
    },
    {
        "title": "Secure Multi-Party Computation over Peer-to-Peer Networks without Centralized Coordinators",
        "abstract": "Executing joint privacy-preserving computations among mistrusting entities requires robust distributed protocols. We implement Shamir secret sharing and asynchronous gossip networks for fault-tolerant decentralized multi-party computation.",
        "category": "Networks & Distributed Computing"
    },
    {
        "title": "Peer-to-Peer Content Delivery Networks using Distributed Hash Tables and Swarm Bandwidth",
        "abstract": "Centralized video streaming distribution suffers from severe bandwidth bottlenecks and single-point-of-failure vulnerabilities. We evaluate Kademlia distributed hash tables and BitTorrent tit-for-tat choker algorithms for P2P video delivery.",
        "category": "Networks & Distributed Computing"
    },
    {
        "title": "Low-Latency Remote Direct Memory Access (RDMA) for Datacenter Distributed Memory Systems",
        "abstract": "Operating system TCP/IP stack overhead limits throughput in high-performance cloud clusters. We implement Remote Direct Memory Access (RDMA over Converged Ethernet) allowing direct user-space memory access with sub-microsecond round-trip latency.",
        "category": "Networks & Distributed Computing"
    }
]


def load_academic_dataset() -> pd.DataFrame:
    """Returns the full academic papers dataset as a pandas DataFrame."""
    return pd.DataFrame(ARXIV_SAMPLE_PAPERS)
