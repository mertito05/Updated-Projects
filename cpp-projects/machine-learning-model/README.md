# Machine Learning Model Implementation

A C++ implementation of basic machine learning algorithms from scratch.

## Features

- Linear Regression
- Logistic Regression
- K-Nearest Neighbors (KNN)
- Decision Tree Classifier
- Neural Network (Basic MLP)
- Data preprocessing and normalization
- Model evaluation metrics

## Algorithms Implemented

### Linear Regression
- Ordinary Least Squares
- Gradient Descent optimization
- Regularization (L1/L2)

### Logistic Regression
- Binary classification
- Sigmoid activation
- Cross-entropy loss

### K-Nearest Neighbors
- Euclidean distance metric
- K-value optimization
- Classification and regression

### Decision Tree
- Information gain splitting
- Gini impurity
- Pre-pruning and post-pruning

### Neural Network
- Multi-layer perceptron
- Backpropagation
- Activation functions (Sigmoid, ReLU, Tanh)

## Requirements

- C++11 or later
- Standard Template Library (STL)
- Basic linear algebra operations

## Usage

```bash
# Compile the project
g++ main.cpp -o ml_model -std=c++11

# Run with sample data
./ml_model
```

## Example Code Structure

```cpp
// Create and train a linear regression model
LinearRegression model;
model.fit(X_train, y_train);
vector<double> predictions = model.predict(X_test);
double mse = model.evaluate(X_test, y_test);
```

## Data Format

Input data should be in CSV format with the first row as headers:
```
feature1,feature2,feature3,target
1.2,3.4,5.6,7.8
2.3,4.5,6.7,8.9
```

## Future Enhancements

- Support for more algorithms (SVM, Random Forest, etc.)
- GPU acceleration
- Model serialization/deserialization
- Hyperparameter tuning
- Cross-validation
- Integration with popular ML frameworks
