# WildfAIre

Welcome to the WildfAIre project repository, a collaborative effort initiated during the final weeks of the LeWagon Data Science Bootcamp Batch #1175. This project aims to demonstrate a proof-of-concept that utilises openly available satellite data to predict the spread of wildfires in the United States, presenting the results in an interactive map.

## Project Components

### 1. Machine Learning Model
The heart of WildfAIre is an ML model that predicts the next day's wildfire spread. The model is trained on data sourced from [Kaggle](https://www.kaggle.com/datasets/fantineh/next-day-wildfire-spread).

### 2. Backend
The backend component is responsible for loading recent wildfire information and remote sensing/satellite data, ensuring the model has access to the most up-to-date information.

### 3. API
An API has been developed to facilitate seamless communication between the frontend and the model. It takes input data, passes it to the ML model, and returns the prediction.

### 4. Streamlit Frontend
The interface is powered by Streamlit, providing an intuitive display of wildfire predictions on an interactive map.

## Technologies Used

The project is built using the following technologies:

- **TensorFlow**: Used for developing and training the machine learning model.
- **FastAPI**: Powers the backend and facilitates efficient API development.
- **Google Earth Engine**: Utilised for accessing and processing satellite data throught its Python API.
- **Streamlit**: Empowers the frontend with a dynamic display.
- **Docker**: The entire application is containerized for easy deployment and scalability.
- **Google Cloud Platform**: Hosted on GCP to ensure reliable and scalable access.
