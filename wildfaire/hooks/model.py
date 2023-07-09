
from preprocessing import get_file_paths, get_dataset
from tensorflow.keras import models, layers

def initialize_model() -> models.Sequential:
    '''
    Instantiates a base model for now.

    model = models.Sequential([
        layers.Dense(10, activation='relu', input_shape=(100, 32, 32, 12)),
        layers.Dense(12, activation='relu'),
        layers.Dense(7, activation='relu'),
        layers.Dense(100 * 32 * 32 * 1, activation='linear'),
        layers.Reshape((-1, 100, 32, 32, 1))
    ])
    '''
    model = models.Sequential([
        layers.Dense(10, activation='relu', input_shape=(32, 32, 12)),
        layers.Dense(12, activation='relu'),
        layers.Dense(7, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    return model


def compile_model(model: models.Sequential, optimizer_name: str) -> models.Sequential:
    """
    Compiles the base model with loss as 'mse' (L2), and 'mae' (L1) for metrics.

    model.compile(
        loss = 'mse',
        optimizer = optimizer_name,
        metrics = ['mae']
    )
    """
    model.compile(
        loss = 'mse',
        optimizer = optimizer_name,
        metrics = ['mae']
    )

    return model

def train_model():
    """
    This function trains initializes the model and trains it on the train dataset.

    model = compile_model(initialize_model(), 'adam')

    train_p = get_file_paths()[0]

    train_data = get_dataset(train_p)

    model.fit(train_data, epochs=10)

    return model
    """
    model = compile_model(initialize_model(), 'adam')
    train_p = get_file_paths()[0]
    train_data = get_dataset(train_p)
    model.fit(train_data, epochs=20)
    return model

def save_model(model, model_name: str):
    """
    This function saves the given model with a chosen name for the models file.
    Do not add any file extensions!

    The model will be saved automatically as .h5
    """
    model.save(f"{model_name}.h5")
    print(f'Model was saved succesfully! as "{model_name}.h5"')


def load_model():
    '''
    This function loads the "baseline_model.sav" file and returns the model.
    '''
    return models.load_model('baseline_model.h5')


def test_model():
    '''
    This is a test function simply returning the prediction of the very first "test" dataset.
    This function works as a placeholder.
    '''
    try:
        model = load_model() # Load model
    except AttributeError:
        print(
            f"[{'='*50}]\n",
            'There was an error loading the model.\n',
            'It seems there was an issue loading the model.',
            '\n\nInitializing a new one.',
            '\nSaving it as "baseline_model.h5"'
            f"[{'='*50}]\n"
            )
        model = compile_model(initialize_model(), 'adam')
        print('Training the model')
        model = train_model()
        print('saving the model')
        save_model(model, 'baseline_model')
    except OSError:
        print(
            f"[{'='*50}]\n",
            'There was an error loading the model.\n',
            'It seems the model does not exist on your computer.',
            '\n\nInitializing a new one.',
            '\nSaving it as "baseline_model.h5"'
            f"[{'='*50}]\n"
            )
        model = compile_model(initialize_model(), 'adam')
        print('Training the model')
        model = train_model()
        print('saving the model')
        save_model(model, 'baseline_model')
    test_p = get_file_paths()[1] # Get test file patterns
    test_data = get_dataset(test_p) # Get dataset from test patterns
    test_inputs = next(iter(test_data))[0] # Define features and labels
    return model.predict(test_inputs)

def test_init_model():
    model = compile_model(initialize_model(), 'adam')
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
    print(f"[{'='*50}]\n", 'Loading Model', f"[{'='*50}]\n")
    try:
        model = load_model() # Load model
    except AttributeError:
        print(
            f"[{'='*50}]\n",
            'There was an error loading the model.\n',
            'It seems there was an issue loading the model.',
            '\n\nInitializing a new one.',
            '\nSaving it as "baseline_model.h5"'
            f"[{'='*50}]\n"
            )
        model = compile_model(initialize_model(), 'adam')
        print('Training the model')
        model = train_model()
        print('saving the model')
        save_model(model, 'baseline_model')
    except OSError:
        print(
            f"[{'='*50}]\n",
            'There was an error loading the model.\n',
            'It seems the model does not exist on your computer.',
            '\n\nInitializing a new one.',
            '\nSaving it as "baseline_model.h5"'
            f"[{'='*50}]\n"
            )
        model = compile_model(initialize_model(), 'adam')
        print('Training the model')
        model = train_model()
        print('saving the model')
        save_model(model, 'baseline_model')
    data = get_dataset(file_path) # Transform tfrecord to a dataset
    features = next(iter(data))[0]
    return model.predict(features)

if __name__ == '__main__':
    print(test_model())
