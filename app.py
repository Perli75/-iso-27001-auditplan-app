1  from PIL import Image
2  import streamlit as st
3  
4  # Load and display logo
5  logo = Image.open("Logo.png")
6  st.image(logo, width=200)  # Adjust width as needed
7  
8  from utils import calculate_audit_days
9  
10 st.title("ISO 27001 Audit Plan Generator")
11 …
