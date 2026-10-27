"""
Dataset Loader and Curated arXiv Academic Corpus for PaperMind AI.
Provides real-world research paper abstracts with ground-truth category labels.
"""

from typing import List, Dict
import pandas as pd


ARXIV_SAMPLE_PAPERS = [
    # --- Artificial Intelligence & Machine Learning ---
    {
        "title": "Mastering the Game of Go with Deep Neural Networks and Tree Search",
        "abstract": "The game of Go has long been viewed as the most challenging of classic games for artificial intelligence. We introduce AlphaGo, which combines deep neural networks with Monte Carlo tree search, trained on human expert games and reinforcement learning from self-play.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Proximal Policy Optimization Algorithms",
        "abstract": "We propose a new family of policy gradient methods for reinforcement learning, which alternate between sampling data through interaction with the environment, and optimizing a 'surrogate' objective function using stochastic gradient ascent.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Adam: A Method for Stochastic Optimization",
        "abstract": "We introduce Adam, an algorithm for first-order gradient-based optimization of stochastic objective functions, based on adaptive estimates of lower-order moments. The method is straightforward to implement and computationally efficient.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Deep Double Q-Learning in Atari Environments",
        "abstract": "The popular Q-learning algorithm is known to overestimate action values under certain conditions. We show that the idea behind Double Q-learning can be generalized to deep neural networks for reinforcement learning.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Dropout: A Simple Way to Prevent Neural Networks from Overfitting",
        "abstract": "Deep neural networks with a large number of parameters are very powerful machine learning systems. However, overfitting is a serious problem. We introduce dropout which randomly drops units and their connections during training.",
        "category": "Artificial Intelligence & Machine Learning"
    },
    {
        "title": "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift",
        "abstract": "Training Deep Neural Networks is complicated by the fact that the distribution of each layer's inputs changes during training. We address this by incorporating Batch Normalization into the network architecture.",
        "category": "Artificial Intelligence & Machine Learning"
    },

    # --- Computer Vision & Pattern Recognition ---
    {
        "title": "Deep Residual Learning for Image Recognition",
        "abstract": "Deeper convolutional neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper. On ImageNet we evaluate residual nets with a depth of up to 152 layers.",
        "category": "Computer Vision & Pattern Recognition"
    },
    {
        "title": "Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks",
        "abstract": "State-of-the-art object detection networks depend on region proposal algorithms to hypothesize object locations. We introduce a Region Proposal Network (RPN) that shares full-image convolutional features with the detection network.",
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

    # --- Natural Language Processing (NLP) ---
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

    # --- Cybersecurity & Cryptography ---
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

    # --- Data Science & Big Data Analytics ---
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

    # --- Robotics & Autonomous Systems ---
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

    # --- Networks & Distributed Computing ---
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
    }
]


def load_academic_dataset() -> pd.DataFrame:
    """Returns academic papers dataset as a pandas DataFrame."""
    return pd.DataFrame(ARXIV_SAMPLE_PAPERS)
