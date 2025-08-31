#include <iostream>
#include <vector>
#include <cmath>

using namespace std;

class LinearRegression {
private:
    vector<double> coefficients;
    double bias;
    
public:
    LinearRegression() : bias(0.0) {}
    
    void fit(const vector<vector<double>>& X, const vector<double>& y, double learning_rate = 0.01, int epochs = 1000) {
        int n_features = X[0].size();
        coefficients.resize(n_features, 0.0);
        bias = 0.0;
        
        int n_samples = X.size();
        
        for (int epoch = 0; epoch < epochs; epoch++) {
            vector<double> grad_coefficients(n_features, 0.0);
            double grad_bias = 0.0;
            
            for (int i = 0; i < n_samples; i++) {
                double prediction = predict(X[i]);
                double error = prediction - y[i];
                
                for (int j = 0; j < n_features; j++) {
                    grad_coefficients[j] += error * X[i][j];
                }
                grad_bias += error;
            }
            
            for (int j = 0; j < n_features; j++) {
                coefficients[j] -= learning_rate * grad_coefficients[j] / n_samples;
            }
            bias -= learning_rate * grad_bias / n_samples;
        }
    }
    
    double predict(const vector<double>& x) {
        double result = bias;
        for (size_t i = 0; i < x.size(); i++) {
            result += coefficients[i] * x[i];
        }
        return result;
    }
    
    double evaluate(const vector<vector<double>>& X, const vector<double>& y) {
        double mse = 0.0;
        for (size_t i = 0; i < X.size(); i++) {
            double prediction = predict(X[i]);
            double error = prediction - y[i];
            mse += error * error;
        }
        return mse / X.size();
    }
};

int main() {
    cout << "Machine Learning Model Implementation" << endl;
    cout << "=====================================" << endl;
    
    // Example usage
    vector<vector<double>> X = {
        {1.0, 2.0},
        {2.0, 3.0},
        {3.0, 4.0},
        {4.0, 5.0}
    };
    
    vector<double> y = {3.0, 5.0, 7.0, 9.0};
    
    // Linear Regression
    LinearRegression lr;
    lr.fit(X, y);
    cout << "Linear Regression trained." << endl;
    
    vector<double> test_x = {5.0, 6.0};
    double prediction = lr.predict(test_x);
    cout << "Prediction for [5.0, 6.0]: " << prediction << endl;
    
    double mse = lr.evaluate(X, y);
    cout << "Mean Squared Error: " << mse << endl;
    
    return 0;
}
