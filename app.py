import requests
import numpy as np 
import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import streamlit as st
from src.exception import CustomException
from src.logger import logging
import sys
import os
import tensorflow as tf 
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
plt.style.use("ggplot")
from dotenv import load_dotenv
load_dotenv() 
# loading variables from .env file


# importing the model
model=load_model("notebook/LSTM model.keras")
scaler=MinMaxScaler(feature_range=(0,1))
#accesing the api key
API_key=os.environ["weather_api"]


start_date = pd.to_datetime("2024-04-01").strftime('%Y-%m-%d')
today = datetime.now().strftime('%Y-%m-%d')
st.title("Future Weather Forecasting")
location_input = st.text_input("Enter Place", "delhi")
@st.cache_data(persist=True)
def data_extraction(api, begin, end, location):
    base_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{begin}/{end}?unitGroup=metric&include=days&key={api}&contentType=json"
    
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            data = response.json()
            fetched_data = []
            
            if "days" in data:
                for day in data["days"]:
                    weather_info = {
                        "date": day["datetime"],
                        "tempmax": day["tempmax"],
                        "tempmin": day["tempmin"],
                        "temp": day["temp"],
                        "feelslike": day["feelslike"],
                        "humidity": day["humidity"],
                        "windspeed": day["windspeed"],
                        "pressure": day["pressure"],
                        "precipitation": day["precip"],
                        "conditions": day["conditions"]
                    }
                    
                    fetched_data.append(weather_info)
                    
            return pd.DataFrame(fetched_data)
        
        elif response.status_code==400:
            st.error("No data available for the input location")
        else:
            st.error(f"Error: Received status code {response.status_code}")
            st.error(response.text)
            return pd.DataFrame()  # Return empty DataFrame on error
            
    except Exception as e:
        raise CustomException(e,sys)

df = data_extraction(API_key, start_date, today, location_input)
df["date"]=pd.to_datetime(df["date"])
df["day"]=df["date"].dt.day
df["month"]=df["date"].dt.month
df["year"]=df["date"].dt.year
df_datetime=df.set_index("date")

if not df.empty:
    st.subheader(f" Weather data of previous 5 days",divider="rainbow")
    st.write(df.tail().reset_index().drop("index",axis=1))
    mean_temp=df.describe()["temp"]["mean"]
    st.text(f"The mean temperature of {location_input} is : {mean_temp:.2f}°C")
else:
    st.error("No data available to display.")
    
###making the prediction system
def feature_extraction():
    try:
        
        #creating the list for each feature
        X4=[] #temperature
        y=[] #temperature
        for i in range(0,df.shape[0]-30):
            X4.append(df.iloc[i:i+30,3])
            y.append(df.iloc[i+30,3])
            
        X4,y=np.array(X4),np.array(y)
        y=np.reshape(y,(len(y),1))
        
        scldX4=scaler.fit_transform(X4)
        scldy=scaler.fit_transform(y)
        
        X=np.stack([scldX4],axis=2)
        
        #Predictions
        predictions=model.predict(X)
        predictions=scaler.inverse_transform(predictions)
        inv_y=scaler.inverse_transform(scldy)
        
        #Visualisation
        plotting_data=pd.DataFrame({
            "Actual Temperature":inv_y.reshape(-1),
            "Predicted Temperature ":predictions.reshape(-1)
        },
            index=df_datetime.index[30:]
        )
        

        whole_df=pd.concat([df_datetime["temp"][:30],plotting_data],axis=0)
        
        
        latest_data = df.tail(30)
        latest_X4 = scaler.transform(latest_data[["temp"]])
        latest_X4=np.array(latest_X4)

        latest_X = np.stack([latest_X4], axis=2)

        # Predict the next day's temperature
        next_day_prediction = model.predict(latest_X)
        next_day_prediction = scaler.inverse_transform(next_day_prediction)
        next_day_prediction=next_day_prediction[0][0]

        fig=plt.figure(figsize=(25,10))
        plt.title("Complete temperature Data")
        plt.plot(whole_df,lw=2)
        plt.legend(["temp","Actual Temperature","Predicted temperature"],loc="best")
        st.subheader("Graphical Visualization",divider="rainbow")
        st.pyplot(fig)
        
        
        return whole_df,next_day_prediction
    
    except Exception as e:
        raise CustomException(e,sys)
whole_df,next_day_temp=feature_extraction()
st.text(f"Tomorrow's forcasted temperature : {next_day_temp:.2f}°C")
