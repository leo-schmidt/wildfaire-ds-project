import pickle
from preprocessing import get_file_paths, get_dataset

def load_model():
    '''
    This function loads the "baseline_model.sav" file and returns the model.
    '''
    return pickle.load(open('baseline_model.sav', 'rb'))

def test_model():
    '''
    This is a test function simply returning the prediction of the very first "test" dataset.
    This function works as a placeholder.
    '''
    model = load_model() # Load model
    test_p = get_file_paths()[1] # Get test file patterns
    test_data = get_dataset(test_p) # Get dataset from test patterns
    test_inputs = next(iter(test_data))[0] # Define features and labels
    return model.predict(test_inputs)

def make_prediction(file_path: str):
    '''
    This model makes a prediction from a given file_path,
    processes the data and returns a prediction of the features in the dataset.

    This function considers that the given file is a tfrecords file.
    '''
    model = load_model() # Load model
    data = get_dataset(file_path) # Transform tfrecord to a dataset
    features = next(iter(data))[0]
    return model.predict(features)

if __name__ == '__main__':
    print(test_model())
