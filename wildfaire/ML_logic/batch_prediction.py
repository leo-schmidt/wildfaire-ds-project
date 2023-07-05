import os
import pickle
import glob
from preprocessing import make_prediction

def load_model(model_path):
    """
    Load the trained model from the specified file path.
    """
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

def batch_predict(model, input_dir, output_dir):
    """
    Perform batch prediction on multiple input files and save the predictions.
    """
    # Get a list of input file paths
    input_files = glob.glob(os.path.join(input_dir, '*.tfrecords'))

    # Make predictions for each input file
    for input_file in input_files:
        # Specify the output file name based on the input file name
        output_file = os.path.join(output_dir, os.path.basename(input_file).replace('.tfrecords', '.txt'))

        # Make predictions using the model
        predictions = make_prediction(input_file, model)

        # Save the predictions to the output file
        with open(output_file, 'w') as f:
            for prediction in predictions:
                f.write(str(prediction) + '\n')

def main():
    """
    Main function for batch prediction.
    """
    # Load the trained model
    model_path = 'trained_model.sav'  # Specify the path to the trained model
    model = load_model(model_path)

    # Specify the input directory containing the input data files
    input_dir = 'input_data'  # Specify the path to the input directory

    # Specify the output directory to save the prediction results
    output_dir = 'output_predictions'  # Specify the path to the output directory

    # Perform batch prediction on the input files and save the predictions
    batch_predict(model, input_dir, output_dir)

    print("Batch prediction completed.")

if __name__ == '__main__':
    main()
