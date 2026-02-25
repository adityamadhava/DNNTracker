"""
Pre-filled DNN topics and subtopics for seeding Firestore.
"""
DNN_TOPICS = [
    {
        "topic_name": "Foundations",
        "subtopics": [
            "Linear Algebra basics",
            "Calculus",
            "Probability & Statistics",
        ],
    },
    {
        "topic_name": "Perceptron & MLP",
        "subtopics": [
            "Single neuron",
            "Activation functions (ReLU, Sigmoid, Tanh, Softmax)",
        ],
    },
    {
        "topic_name": "Forward Propagation",
        "subtopics": [
            "Matrix operations",
            "Layer computations",
            "Output generation",
        ],
    },
    {
        "topic_name": "Loss Functions",
        "subtopics": [
            "MSE",
            "Cross-entropy",
            "Hinge loss",
            "Custom losses",
        ],
    },
    {
        "topic_name": "Backpropagation",
        "subtopics": [
            "Chain rule",
            "Gradient computation",
            "Vanishing/Exploding gradients",
        ],
    },
    {
        "topic_name": "Optimization",
        "subtopics": [
            "SGD",
            "Momentum",
            "RMSProp",
            "Adam",
            "Learning rate schedules",
        ],
    },
    {
        "topic_name": "Regularization",
        "subtopics": [
            "Dropout",
            "L1/L2",
            "Batch Normalization",
            "Early stopping",
        ],
    },
    {
        "topic_name": "CNNs",
        "subtopics": [
            "Convolution",
            "Pooling",
            "Filters",
            "Architectures (VGG, ResNet, InceptionNet)",
        ],
    },
    {
        "topic_name": "RNNs & LSTMs",
        "subtopics": [
            "Vanishing gradient in RNN",
            "LSTM gates",
            "GRU",
            "Bidirectional RNN",
        ],
    },
    {
        "topic_name": "Attention & Transformers",
        "subtopics": [
            "Self-attention",
            "Multi-head attention",
            "Positional encoding",
            "BERT",
            "GPT",
        ],
    },
    {
        "topic_name": "Training Techniques",
        "subtopics": [
            "Data augmentation",
            "Transfer learning",
            "Fine-tuning",
            "Mixed precision",
        ],
    },
    {
        "topic_name": "Evaluation & Metrics",
        "subtopics": [
            "Accuracy",
            "Precision",
            "Recall",
            "F1",
            "ROC-AUC",
            "Confusion matrix",
        ],
    },
    {
        "topic_name": "Advanced Topics",
        "subtopics": [
            "GANs",
            "VAEs",
            "Diffusion models",
            "Graph Neural Networks",
        ],
    },
]

DIFFICULTY_CHOICES = ["Easy", "Medium", "Hard"]
