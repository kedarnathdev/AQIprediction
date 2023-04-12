import streamlit as st
import pandas as pd
import pickle


st.set_page_config(
    page_title="Air Pollution Prediction",
    menu_items= {
        "Get Help" : "https://github.com/kedarnathdev/AQIprediction",
        "Report a bug" : "https://github.com/kedarnathdev/AQIprediction/issues",
        "About": None,
       }
)


hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



models = {
    'Random Forest': 'randomforest.pkl',
    'SVM model': 'svm.pkl',
    'Linear Regression': 'linear.pkl',
    'Lasso Regression': 'lasso.pkl'
}
 

def load_model(filename):
    with open(filename, 'rb') as model_file:
        model = pickle.load(model_file)
    return model

st.header('Air Pollution Prediction')
st.subheader('Enter the following values:')
T = st.number_input('Average Temperature (℃)')
TM = st.number_input('Maximum Temperature (℃)')
Tm = st.number_input('Minimum Temperature (℃)')
SLP = st.number_input('Atmospheric pressure at sea level (hPa)')
H = st.number_input('Average Relative Humidity')
VV = st.number_input('Average Visibility (Km/h)')
V = st.number_input('Average Wind Speed (Km/h)')
VM = st.number_input('Maximum Sustained Wind Speed (Km/h)')

selected_model = st.selectbox('Select a model', list(models.keys()))

if st.button('Predict'):
    if not (T and TM and Tm and SLP and H and VV and V and VM):
        st.error('Please fill all the fields.')
    else:
        model_file = models[selected_model]
        model = load_model(model_file)

        input_df = pd.DataFrame({
            'T': T,
            'TM': TM,
            'Tm': Tm,
            'SLP': SLP,
            'H': H,
            'VV': VV,
            'V': V,
            'VM': VM
        }, index=[0])

        prediction = model.predict(input_df)[0]

        if prediction <= 50:
            color = 'green'
            description = 'Good: Air quality is satisfactory, and air pollution poses little or no risk.'
        elif prediction <= 100:
            color = 'yellow'
            description = 'Moderate: Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.'
        elif prediction <= 150:
            color = 'orange'
            description = 'Unhealthy for Sensitive Groups: Members of sensitive groups may experience health effects. The general public is less likely to be affected.'
        elif prediction <= 200:
            color = 'red'
            description = 'Unhealthy: Some members of the general public may experience health effects members of sensitive groups may experience more serious health effects.'
        elif prediction <= 300:
            color = 'purple'
            description = 'Very Unhealthy: Health alert, The risk of health effects is increased for everyone.'
        else:
            color = 'maroon'
            description = 'Hazardous: Health warning of emergency conditions: everyone is more likely to be affected.'

        
        st.markdown(f'<h1 style="color:{color};">Air Quality Index: {prediction}</h1>', unsafe_allow_html=True)
        st.write(description)
