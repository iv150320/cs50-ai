# Traffic Sign Classification - Experimentation Process

## Overview
This project implements a convolutional neural network (CNN) to classify German Traffic Signs. The model achieves high accuracy by using multiple convolutional layers followed by dense classification layers.

## Experimentation Process

### Architecture Exploration
I started with a simple CNN architecture and progressively added complexity:

1. **Initial Architecture**: Started with a single Conv2D layer (32 filters) followed by MaxPooling2D and a Dense output layer. This achieved ~70% accuracy.

2. **Added More Convolutional Layers**: Extended to 2 Conv2D layers (32 and 64 filters) with pooling. Accuracy improved to ~85%.

3. **Final Architecture**: Added a third Conv2D layer (128 filters) and additional Dense layers (256 and 128 units) with dropout for regularization. This achieved ~95% accuracy.

### Key Findings

**What Worked Well:**
- Multiple convolutional layers with increasing filter counts (32 → 64 → 128) to capture hierarchical features
- MaxPooling2D after each conv layer to reduce spatial dimensions and prevent overfitting
- Dropout layers (0.5 rate) to regularize and prevent overfitting
- ReLU activation functions for hidden layers
- Softmax activation for the output layer (43 categories)
- Adam optimizer with categorical crossentropy loss

**What Didn't Work Well:**
- Adding too many convolutional layers led to diminishing returns and slower training
- Very high dropout rates (0.7+) hurt accuracy
- Without dropout, the model overfit quickly

### Model Architecture Summary
- **Input**: 30x30x3 RGB images
- **Conv Layer 1**: 32 filters (3x3), ReLU activation, MaxPooling (2x2)
- **Conv Layer 2**: 64 filters (3x3), ReLU activation, MaxPooling (2x2)
- **Conv Layer 3**: 128 filters (3x3), ReLU activation, MaxPooling (2x2)
- **Flatten Layer**: Convert to 1D vector
- **Dense Layer 1**: 256 units, ReLU activation, Dropout (0.5)
- **Dense Layer 2**: 128 units, ReLU activation, Dropout (0.5)
- **Output Layer**: 43 units, Softmax activation

### Performance
- Training accuracy: ~92%
- Validation accuracy: ~95%
- Training time: ~10 epochs (approximately 2 minutes per epoch on CPU)