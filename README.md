# Weather Forecasting App

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Streamlit](https://img.shields.io/badge/streamlit-v1.10.0-brightgreen)

## Introduction

**Weather Forecasting App** is a web application that predicts the next day's temperature for any location entered by the user. The application uses a Long Short-Term Memory (LSTM) model trained on temperature data fetched through an API. The app fetches the latest 30 days of temperature data and provides a temperature forecast for the following day. The frontend is built using Streamlit.

## Features

- **Temperature Prediction:** Predicts the next day's temperature for any given location using an LSTM model.
- **Data Visualization:** Visualizes the actual and predicted temperatures using matplotlib.
- **Historical Data Display:** Shows the weather data for the previous five days.

## Installation

To run the Weather Forecasting App locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hiroshi990/Weather-Time-Series-Forecasting.git
   cd Weather-Time-Series-Forecasting

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv

3. **Activate the Virtual environment:**
   ```bash
   venv\Scripts\activate

4. **Install the required deoendencies:**
   ```bash
   pip install -r requirements.txt

5. **Set Up Your API Key:**
   - Create a `.env` file in the project root directory.
   - Add your Weather API key to the `.env` file as follows:
   ```bash
   weather_api=your_api_key

6. **Run the Streamlit App:**
   ```bash
   streamlit run app.py

7. **Usage:**
     1. Open the app in your web browser after running the Streamlit command.
     2. Enter the location for which you want the temperature forecast (e.g., "Delhi").
     3. The app will display:
        - The weather data for the past five days.
        - A graph showing actual and predicted temperatures.
        - The forecasted temperature for the next day.






