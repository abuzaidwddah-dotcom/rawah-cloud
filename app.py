import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Set page config for full width
st.set_page_config(page_title="نظام رواح", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS to hide Streamlit header and footer to make the HTML app look native
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 0rem;
                padding-right: 0rem;
            }
            iframe {
                border: none;
                width: 100%;
                height: 100vh;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Load configuration
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize Authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Render Login Widget
try:
    authenticator.login(location='main')
except Exception as e:
    st.error(str(e))

if st.session_state.get('authentication_status'):
    # Sidebar for logout and welcome message
    with st.sidebar:
        st.write(f'مرحباً *{st.session_state.get("name", "")}*')
        authenticator.logout('تسجيل الخروج', 'main')
        
    # Read and render the HTML app
    with open('index.html', 'r', encoding='utf-8') as f:
        html_data = f.read()
        
    st.components.v1.html(html_data, height=1200, scrolling=True)

elif st.session_state.get('authentication_status') is False:
    st.error('اسم المستخدم أو كلمة المرور غير صحيحة')
elif st.session_state.get('authentication_status') is None:
    st.warning('الرجاء إدخال اسم المستخدم وكلمة المرور')
