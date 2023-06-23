from matplotlib import pyplot as plt, colors
from tensorflow import data
from preprocessing import train_pattern, get_dataset, INPUT_FEATURES

def load_data_for_visualization() -> data.Dataset:
    '''
    Loads the training dataset for visualization.

    This function is not meant to be used, it is used internally for the "print_data" function.
    '''
    # Load the dataset
    file_pattern = train_pattern
    data_size = 64
    sample_size = 32
    batch_size = 100
    num_in_channels = 12
    compression_type = None
    clip_and_normalize = False
    clip_and_rescale = False
    random_crop = True
    center_crop = False

    dataset = get_dataset(
        file_pattern,
        data_size,
        sample_size,
        batch_size,
        num_in_channels,
        compression_type,
        clip_and_normalize,
        clip_and_rescale,
        random_crop,
        center_crop
        )

    return dataset

def show_data():
    '''
    This function simply prints out the data from 5 samples in the dataset.

    No arguments needed.

    P.S: It is the train data which is used.
    '''
    dataset = load_data_for_visualization()
    inputs, labels = next(iter(dataset))
    # Titles for the different features & the label
    TITLES = [
    'Elevation',
    'Wind\ndirection',
    'Wind\nvelocity',
    'Min\ntemp',
    'Max\ntemp',
    'Humidity',
    'Precip',
    'Drought',
    'Vegetation',
    'Population\ndensity',
    'Energy\nrelease\ncomponent',
    'Previous\nfire\nmask',
    'Fire\nmask'
    ]

    # Number of rows of data samples to plot
    n_rows = 5
    # Number of data variables
    n_features = inputs.shape[3]
    # Variables for controllong the color map for the fire masks
    CMAP = colors.ListedColormap(['black', 'silver', 'orangered'])
    BOUNDS = [-1, -0.1, 0.001, 1]
    NORM = colors.BoundaryNorm(BOUNDS, CMAP.N)

    # The plot itself
    fig = plt.figure(figsize=(15,6.5))

    for i in range(n_rows):
        for j in range(n_features + 1):
            plt.subplot(n_rows, n_features + 1, i * (n_features + 1) + j + 1)
            if i == 0:
                if j < 11:
                    plt.title(f'{TITLES[j]}\n({INPUT_FEATURES[j]})', fontsize=13)
                else:
                    plt.title(TITLES[j], fontsize=13)
            if j < n_features - 1:
                plt.imshow(inputs[i, :, :, j], cmap='viridis')
            if j == n_features - 1:
                plt.imshow(inputs[i, :, :, -1], cmap=CMAP, norm=NORM)
            if j == n_features:
                plt.imshow(labels[i, :, :, 0], cmap=CMAP, norm=NORM)
            plt.axis('off')
    fig.suptitle('next day wildfire spread (Training data)', fontsize=16)
    plt.tight_layout()
    plt.show()
