import os
import pickle
from sklearn.metrics import accuracy_score, precision_score, recall_score
from preprocessing import get_dataset, test_pattern

def load_data():
    """
    Load the test dataset.
    """
    dataset = get_dataset(test_pattern)
    features, labels = next(iter(dataset))
    return features, labels

def evaluate_model(X_test, y_test, model):
    """
    Evaluate the machine learning model.
    """
    # Example: Make predictions using the trained model
    y_pred = model.predict(X_test)

    # Example: Calculate evaluation metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)

    return accuracy, precision, recall

def load_model(model_path):
    """
    Load the trained model from the specified file path.
    """
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

def main():
    """
    Main function for model evaluation.
    """
    # Load the data
    features, labels = load_data()

    # Load the trained model
    model_path = 'trained_model.sav'  # Specify the path to the trained model
    model = load_model(model_path)

    # Evaluate the model
    accuracy, precision, recall = evaluate_model(features, labels, model)

    # Print the evaluation metrics
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)

if __name__ == '__main__':
    main()
