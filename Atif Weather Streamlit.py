import streamlit as st
import requests

# Replace with your OpenWeatherMap API Key
API_KEY = '2261e0068c288fd0a356310770732af0'

st.title("🌤️ Weather App")
st.subheader("Enter a city to get the current weather information")

city = st.text_input("City Name")

if st.button("Get Weather"):
    if not city:
        st.warning("Please enter a city name.")
    else:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        
        try:
            response = requests.get(url)
            data = response.json()

            if data.get("cod") != 200:
                st.error("City not found!")
            else:
                weather = data['weather'][0]['description'].title()
                temp = data['main']['temp']
                humidity = data['main']['humidity']
                wind = data['wind']['speed']

                st.success(f"Weather in **{city.title()}**")
                st.write(f"**Weather:** {weather}")
                st.write(f"**Temperature:** {temp} °C")
                st.write(f"**Humidity:** {humidity} %")
                st.write(f"**Wind Speed:** {wind} m/s")
        except Exception as e:
            st.error("Error retrieving data.")
