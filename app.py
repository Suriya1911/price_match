import streamlit as st
from PIL import Image
import requests
import base64
import io
import os
import zipfile
import tempfile
from dotenv import load_dotenv
import pandas as pd
import re
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load environment variables from .env file
load_dotenv()

st.set_page_config(
    page_title="MatchIt - Smart Price Comparison",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Neon Theme CSS with Enhanced Visuals
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Orbitron:wght@400;500;600;700;800;900&display=swap');

/* Global Styling with Multi-Color Neon */
.stApp {
    background: #0a0a0f;
    background-image: 
        radial-gradient(circle at 15% 15%, rgba(255, 0, 150, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 85% 85%, rgba(0, 255, 200, 0.12) 0%, transparent 50%),
        radial-gradient(circle at 50% 20%, rgba(150, 0, 255, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 20% 80%, rgba(255, 100, 0, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 80% 30%, rgba(0, 150, 255, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 40% 70%, rgba(255, 255, 0, 0.06) 0%, transparent 50%);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    animation: backgroundShift 12s ease-in-out infinite alternate;
}

@keyframes backgroundShift {
    0% {
        background-image: 
            radial-gradient(circle at 15% 15%, rgba(255, 0, 150, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 85% 85%, rgba(0, 255, 200, 0.12) 0%, transparent 50%),
            radial-gradient(circle at 50% 20%, rgba(150, 0, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 20% 80%, rgba(255, 100, 0, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 30%, rgba(0, 150, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 70%, rgba(255, 255, 0, 0.06) 0%, transparent 50%);
    }
    100% {
        background-image: 
            radial-gradient(circle at 25% 25%, rgba(255, 0, 150, 0.2) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, rgba(0, 255, 200, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 60% 30%, rgba(150, 0, 255, 0.12) 0%, transparent 50%),
            radial-gradient(circle at 30% 70%, rgba(255, 100, 0, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 70% 20%, rgba(0, 150, 255, 0.12) 0%, transparent 50%),
            radial-gradient(circle at 50% 80%, rgba(255, 255, 0, 0.08) 0%, transparent 50%);
    }
}

/* Main Container */
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* Enhanced Headers with Multi-Color Glow */
h1 {
    color: #ffffff;
    text-align: center;
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    font-size: 4rem;
    margin-bottom: 0.5rem;
    text-shadow: 
        0 0 10px rgba(255, 0, 150, 0.8),
        0 0 20px rgba(0, 255, 200, 0.6),
        0 0 30px rgba(150, 0, 255, 0.4),
        0 0 40px rgba(255, 100, 0, 0.3);
    letter-spacing: -1px;
    animation: titleRainbow 4s ease-in-out infinite alternate;
}

@keyframes titleRainbow {
    0% {
        text-shadow: 
            0 0 10px rgba(255, 0, 150, 0.8),
            0 0 20px rgba(0, 255, 200, 0.6),
            0 0 30px rgba(150, 0, 255, 0.4),
            0 0 40px rgba(255, 100, 0, 0.3);
    }
    50% {
        text-shadow: 
            0 0 15px rgba(0, 255, 200, 0.9),
            0 0 25px rgba(150, 0, 255, 0.7),
            0 0 35px rgba(255, 100, 0, 0.5),
            0 0 45px rgba(255, 0, 150, 0.4);
    }
    100% {
        text-shadow: 
            0 0 12px rgba(150, 0, 255, 0.8),
            0 0 22px rgba(255, 100, 0, 0.6),
            0 0 32px rgba(255, 0, 150, 0.4),
            0 0 42px rgba(0, 255, 200, 0.3);
    }
}

/* Enhanced Analytics Cards with Different Neon Colors */
.analytics-card, .step-card, .deal-card {
    background: rgba(0, 0, 0, 0.85);
    border: 2px solid rgba(255, 0, 150, 0.4);
    border-radius: 20px;
    padding: 1.5rem;
    text-align: center;
    backdrop-filter: blur(25px);
    box-shadow: 
        0 0 25px rgba(255, 0, 150, 0.3),
        inset 0 0 25px rgba(255, 0, 150, 0.1);
    animation: cardPulse 3s ease-in-out infinite alternate;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.analytics-card::before, .step-card::before, .deal-card::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg, 
        rgba(255, 0, 150, 0.6),
        rgba(0, 255, 200, 0.6),
        rgba(150, 0, 255, 0.6),
        rgba(255, 100, 0, 0.6));
    border-radius: 20px;
    z-index: -1;
    animation: borderRotate 4s linear infinite;
}

@keyframes borderRotate {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes cardPulse {
    0% {
        box-shadow: 
            0 0 25px rgba(255, 0, 150, 0.3),
            inset 0 0 25px rgba(255, 0, 150, 0.1);
    }
    100% {
        box-shadow: 
            0 0 35px rgba(255, 0, 150, 0.4),
            inset 0 0 35px rgba(255, 0, 150, 0.15);
    }
}

.analytics-card:hover, .step-card:hover, .deal-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 
        0 0 50px rgba(255, 0, 150, 0.5),
        inset 0 0 50px rgba(255, 0, 150, 0.2);
}

/* Custom Button Styles */
.stButton > button {
    background: linear-gradient(135deg, 
        rgba(255, 0, 150, 0.8) 0%,
        rgba(150, 0, 255, 0.8) 50%,
        rgba(0, 255, 200, 0.8) 100%) !important;
    color: #ffffff !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 25px !important;
    padding: 0.75rem 2rem !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    box-shadow: 
        0 0 20px rgba(255, 0, 150, 0.4),
        inset 0 0 20px rgba(255, 255, 255, 0.1) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button::before {
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: -100% !important;
    width: 100% !important;
    height: 100% !important;
    background: linear-gradient(90deg, 
        transparent,
        rgba(255, 255, 255, 0.3),
        transparent) !important;
    transition: left 0.5s !important;
}

.stButton > button:hover::before {
    left: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.05) !important;
    box-shadow: 
        0 0 30px rgba(255, 0, 150, 0.6),
        0 0 40px rgba(150, 0, 255, 0.4),
        inset 0 0 30px rgba(255, 255, 255, 0.15) !important;
    border-color: rgba(255, 255, 255, 0.5) !important;
}

.stButton > button:active {
    transform: translateY(-1px) scale(1.02) !important;
}

/* Download Button Specific Styles */
.stDownloadButton > button {
    background: linear-gradient(135deg, 
        rgba(0, 255, 200, 0.9) 0%,
        rgba(0, 150, 255, 0.9) 50%,
        rgba(100, 0, 255, 0.9) 100%) !important;
    color: #ffffff !important;
    border: 2px solid rgba(0, 255, 200, 0.5) !important;
    border-radius: 20px !important;
    padding: 1rem 2.5rem !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    box-shadow: 
        0 0 25px rgba(0, 255, 200, 0.4),
        inset 0 0 25px rgba(255, 255, 255, 0.1) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
}

.stDownloadButton > button::after {
    content: '' !important;
    position: absolute !important;
    top: 50% !important;
    left: 50% !important;
    width: 0 !important;
    height: 0 !important;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.3), transparent) !important;
    transition: all 0.4s !important;
    transform: translate(-50%, -50%) !important;
    border-radius: 50% !important;
}

.stDownloadButton > button:hover::after {
    width: 300px !important;
    height: 300px !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-5px) scale(1.03) !important;
    box-shadow: 
        0 0 35px rgba(0, 255, 200, 0.6),
        0 0 45px rgba(0, 150, 255, 0.4),
        inset 0 0 35px rgba(255, 255, 255, 0.2) !important;
    border-color: rgba(0, 255, 200, 0.8) !important;
}

/* File Uploader Enhancement */
.stFileUploader > div > div {
    background: rgba(0, 0, 0, 0.7) !important;
    border: 2px dashed rgba(0, 255, 200, 0.5) !important;
    border-radius: 20px !important;
    padding: 2rem !important;
    transition: all 0.3s ease !important;
}

.stFileUploader > div > div:hover {
    border-color: rgba(0, 255, 200, 0.8) !important;
    background: rgba(0, 255, 200, 0.05) !important;
    box-shadow: 0 0 20px rgba(0, 255, 200, 0.3) !important;
}

/* Success/Info/Error Messages */
.stSuccess {
    background: linear-gradient(135deg, rgba(0, 255, 150, 0.2), rgba(0, 200, 100, 0.2)) !important;
    border: 1px solid rgba(0, 255, 150, 0.4) !important;
    border-radius: 15px !important;
    box-shadow: 0 0 15px rgba(0, 255, 150, 0.2) !important;
}

.stInfo {
    background: linear-gradient(135deg, rgba(0, 150, 255, 0.2), rgba(100, 0, 255, 0.2)) !important;
    border: 1px solid rgba(0, 150, 255, 0.4) !important;
    border-radius: 15px !important;
    box-shadow: 0 0 15px rgba(0, 150, 255, 0.2) !important;
}

.stError {
    background: linear-gradient(135deg, rgba(255, 100, 100, 0.2), rgba(255, 0, 100, 0.2)) !important;
    border: 1px solid rgba(255, 100, 100, 0.4) !important;
    border-radius: 15px !important;
    box-shadow: 0 0 15px rgba(255, 100, 100, 0.2) !important;
}

/* Input Field Enhancements */
.stTextInput > div > div > input {
    background: rgba(0, 0, 0, 0.7) !important;
    border: 2px solid rgba(150, 0, 255, 0.4) !important;
    border-radius: 15px !important;
    color: #ffffff !important;
    padding: 0.75rem !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: rgba(150, 0, 255, 0.8) !important;
    box-shadow: 0 0 20px rgba(150, 0, 255, 0.3) !important;
    background: rgba(150, 0, 255, 0.05) !important;
}

/* Hide Streamlit Elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.css-1d391kg {display: none;}

/* Metric Large Numbers */
.metric-large {
    font-size: 2.5rem;
    font-weight: 800;
    color: #ffffff;
    text-shadow: 
        0 0 15px rgba(255, 0, 150, 0.8),
        0 0 25px rgba(0, 255, 200, 0.6);
    animation: numberGlow 2s ease-in-out infinite alternate;
}

@keyframes numberGlow {
    0% {
        text-shadow: 
            0 0 15px rgba(255, 0, 150, 0.8),
            0 0 25px rgba(0, 255, 200, 0.6);
    }
    100% {
        text-shadow: 
            0 0 20px rgba(255, 0, 150, 1),
            0 0 30px rgba(0, 255, 200, 0.8),
            0 0 40px rgba(150, 0, 255, 0.4);
    }
}

.metric-label {
    color: #c0c0c0;
    font-size: 0.9rem;
    margin-top: 0.5rem;
    font-weight: 600;
}

/* Excel Preview Section */
.excel-preview-section {
    background: rgba(0, 0, 0, 0.7);
    border: 2px solid rgba(0, 255, 200, 0.3);
    border-radius: 20px;
    padding: 2rem;
    margin: 2rem 0;
    backdrop-filter: blur(15px);
}

.tab-header {
    background: rgba(0, 255, 200, 0.1);
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    border: 1px solid rgba(0, 255, 200, 0.3);
}
</style>
""", unsafe_allow_html=True)

def convert_image_to_text(image, api_key):
    """Convert image to text using Gemini Vision API - Structured Analysis"""
    
    try:
        # Convert image to base64
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        # Gemini API endpoint
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        # Structured analysis prompt
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": """Analyze this image and provide a detailed structured analysis. Format your response like this:

**Store Name:** [Store/Business name]

**Slogan/Motto:** [Any taglines or slogans]

**Featured Products & Prices:**
* **Product Name:** Size/Weight for $Price (Description/Features)
* **Product Name:** Size/Weight for $Price (Description/Features)
[Continue for all products]

**Contact Information:**
* **Address:** [Full address if visible]
* **Website:** [Website URL if visible]  
* **Phone Number:** [Phone number if visible]

**Overall Impression:**
[Describe the design, colors, main message, and overall marketing approach]

Please analyze this image thoroughly and provide all visible information in this structured format."""},
                        {
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": img_base64
                            }
                        }
                    ]
                }
            ]
        }
        
        headers = {"Content-Type": "application/json"}
        
        # Make API request
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                extracted_text = result['candidates'][0]['content']['parts'][0]['text']
                return extracted_text
            else:
                return "No analysis generated"
        else:
            error_info = response.json() if response.content else {"error": "Unknown error"}
            return f"API Error: {error_info.get('error', {}).get('message', 'Request failed')}"
            
    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."
    except Exception as e:
        return f"Error: {str(e)}"

def parse_flyer_data(analysis_text, filename):
    """Extract structured data from flyer analysis"""
    
    # Initialize data structure
    flyer_data = {
        'filename': filename,
        'store_name': '',
        'slogan': '',
        'address': '',
        'website': '',
        'phone': '',
        'products': []
    }
    
    try:
        # Extract store name
        store_match = re.search(r'\*\*Store Name:\*\*\s*(.+?)(?:\n|\*\*)', analysis_text, re.IGNORECASE)
        if store_match:
            flyer_data['store_name'] = store_match.group(1).strip()
        
        # Extract slogan/motto
        slogan_match = re.search(r'\*\*Slogan/Motto:\*\*\s*(.+?)(?:\n|\*\*)', analysis_text, re.IGNORECASE)
        if slogan_match:
            flyer_data['slogan'] = slogan_match.group(1).strip()
        
        # Extract contact info
        address_match = re.search(r'\*\*Address:\*\*\s*(.+?)(?:\n|\*\*)', analysis_text, re.IGNORECASE)
        if address_match:
            flyer_data['address'] = address_match.group(1).strip()
            
        website_match = re.search(r'\*\*Website:\*\*\s*(.+?)(?:\n|\*\*)', analysis_text, re.IGNORECASE)
        if website_match:
            flyer_data['website'] = website_match.group(1).strip()
            
        phone_match = re.search(r'\*\*Phone Number:\*\*\s*(.+?)(?:\n|\*\*)', analysis_text, re.IGNORECASE)
        if phone_match:
            flyer_data['phone'] = phone_match.group(1).strip()
        
        # Extract products - look for the products section with more flexible patterns
        products_section = re.search(r'\*\*Featured Products & Prices:\*\*(.*?)(?:\*\*Contact Information|\*\*Overall Impression|\*\*Address|\*\*Website|\*\*Phone|\Z)', 
                                   analysis_text, re.DOTALL | re.IGNORECASE)
        
        if products_section:
            products_text = products_section.group(1)
            
            # Find all product lines that start with * **Product Name:** or similar patterns
            product_patterns = [
                r'\*\s*\*\*(.+?):\*\*\s*(.+?)(?:\n|\Z)',  # * **Product Name:** details
                r'\*\s*(.+?):\s*(.+?)(?:\n|\Z)',          # * Product Name: details
                r'^\s*\*\s*(.+?)\s*[-–]\s*(.+?)(?:\n|\Z)', # * Product - details
                r'^\s*\*\s*(.+?)\s*:\s*(.+?)(?:\n|\Z)',   # * Product: details
            ]
            
            for pattern in product_patterns:
                product_lines = re.findall(pattern, products_text, re.MULTILINE | re.IGNORECASE)
                if product_lines:
                    break
            
            for product_line in product_lines:
                product_name = product_line[0].strip()
                product_details = product_line[1].strip()
                
                # Skip empty or invalid entries
                if not product_name or not product_details or len(product_name) < 2:
                    continue
                
                # More flexible price extraction
                price_patterns = [
                    r'\$(\d+\.?\d*)',  # $5.99
                    r'(\d+\.?\d*)\s*(?:dollars?|bucks?)',  # 5.99 dollars
                    r'(\d+\.?\d*)\s*(?:for|each|ea)',  # 5.99 for
                    r'(\d+\.?\d*)\s*(?:\$|dollars?)',  # 5.99$
                ]
                
                price = ''
                for pattern in price_patterns:
                    price_match = re.search(pattern, product_details, re.IGNORECASE)
                    if price_match:
                        price = f"${price_match.group(1)}"
                        break
                
                # If no price found, try to extract any number
                if not price:
                    number_match = re.search(r'(\d+\.?\d*)', product_details)
                    if number_match:
                        price = f"${number_match.group(1)}"
                
                # Try to extract size/weight with more comprehensive patterns
                size_patterns = [
                    r'(\d+\.?\d*\s*(?:gal|gallon|gallons)\b)',  # gallons
                    r'(\d+\.?\d*\s*(?:l|liter|liters|litre|litres)\b)',  # liters
                    r'(\d+\.?\d*\s*(?:ml|milliliter|milliliters|millilitre|millilitres)\b)',  # milliliters
                    r'(\d+\.?\d*\s*(?:oz|ounce|ounces|fl\s*oz|fluid\s*ounce)\b)',  # ounces
                    r'(\d+\.?\d*\s*(?:lb|lbs|pound|pounds)\b)',  # pounds
                    r'(\d+\.?\d*\s*(?:kg|kilogram|kilograms)\b)',  # kilograms
                    r'(\d+\.?\d*\s*(?:g|gram|grams)\b)',  # grams
                    r'(\d+\.?\d*\s*(?:pack|count|ct|pieces?|pcs?)\b)',  # count/pack
                    r'(\d+\.?\d*\s*(?:qt|quart|quarts)\b)',  # quarts
                    r'(\d+\.?\d*\s*(?:pt|pint|pints)\b)',  # pints
                    r'(\d+\s*x\s*\d+\.?\d*\s*(?:oz|ml|l|gal))',  # multi-pack like "12 x 12oz"
                    r'(\d+\.?\d*(?:g|kg|ml|l|oz|lb|lbs|pack|count|ct|gal|qt|pt)\b)',  # shorter versions
                ]
                
                size = ''
                for pattern in size_patterns:
                    size_match = re.search(pattern, product_details, re.IGNORECASE)
                    if size_match:
                        size = size_match.group(1).strip()
                        break
                
                # If no size found in product details, try to extract from product name
                if not size and product_name:
                    for pattern in size_patterns:
                        size_match = re.search(pattern, product_name, re.IGNORECASE)
                        if size_match:
                            size = size_match.group(1).strip()
                            break
                
                # Clean up description (remove price and size) with more comprehensive patterns
                description = product_details
                if price:
                    description = re.sub(r'\$\d+\.?\d*', '', description)
                if size:
                    # Remove the found size from description
                    description = re.sub(re.escape(size), '', description, flags=re.IGNORECASE)
                    # Also remove common size patterns
                    description = re.sub(r'\d+\.?\d*\s*(?:g|kg|ml|l|oz|lb|lbs|pack|count|ct|gal|gallon|gallons|liter|liters|litre|litres|milliliter|milliliters|quart|quarts|pint|pints|qt|pt|fl\s*oz|fluid\s*ounce|gram|grams|kilogram|kilograms|milliliter|milliliters|ounce|ounces|pound|pounds)\b', '', description, flags=re.IGNORECASE)
                
                # Clean up common words and extra spaces
                description = re.sub(r'\bfor\b|\(|\)|,|\s+', ' ', description, flags=re.IGNORECASE).strip()
                
                flyer_data['products'].append({
                    'product_name': product_name,
                    'size_weight': size,
                    'price': price if price else 'Price not found',
                    'description': description
                })
        
        # If no products found in structured format, try to extract from raw text
        if not flyer_data['products']:
            # Look for any product-like patterns in the entire text
            lines = analysis_text.split('\n')
            for line in lines:
                # Skip header lines
                if any(header in line.lower() for header in ['store name', 'slogan', 'contact', 'address', 'website', 'phone', 'overall impression']):
                    continue
                
                # Look for lines that might contain products
                if re.search(r'[a-zA-Z]+.*\$?\d+\.?\d*', line):
                    # Extract product name (first part before price)
                    parts = re.split(r'[\$\d]', line, 1)
                    if parts:
                        product_name = parts[0].strip(' -*')
                        if len(product_name) > 2:  # Only if reasonable product name
                            # Try to find price in the line
                            price_match = re.search(r'\$?(\d+\.?\d*)', line)
                            price = f"${price_match.group(1)}" if price_match else 'Price not found'
                            
                            flyer_data['products'].append({
                                'product_name': product_name,
                                'size_weight': '',
                                'price': price,
                                'description': line.strip()
                            })
        
    except Exception as e:
        st.warning(f"Error parsing data from {filename}: {str(e)}")
    
    return flyer_data

def extract_images_from_zip(zip_file):
    """Extract image files from uploaded ZIP file"""
    image_files = []
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
    
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            for file_info in zip_ref.filelist:
                # Check if file is an image
                if any(file_info.filename.lower().endswith(ext) for ext in image_extensions):
                    # Skip system files and folders
                    if not file_info.filename.startswith('__MACOSX') and not file_info.is_dir():
                        try:
                            # Extract file content
                            file_content = zip_ref.read(file_info.filename)
                            # Create a file-like object
                            image_file = io.BytesIO(file_content)
                            image_file.name = os.path.basename(file_info.filename)
                            image_files.append(image_file)
                        except Exception as e:
                            st.warning(f"Could not extract {file_info.filename}: {str(e)}")
                            continue
        
        return image_files
    except zipfile.BadZipFile:
        st.error("Invalid ZIP file uploaded")
        return []
    except Exception as e:
        st.error(f"Error extracting ZIP file: {str(e)}")
        return []

def create_excel_data(all_flyer_data):
    """Create structured Excel data from analyzed flyers"""
    
    # Create stores summary
    stores_data = []
    for flyer in all_flyer_data:
        stores_data.append({
            'Store_Name': flyer['store_name'] if flyer['store_name'] else 'Unknown Store',
            'Slogan': flyer['slogan'],
            'Address': flyer['address'],
            'Website': flyer['website'],
            'Phone': flyer['phone'],
            'Flyer_Source': flyer['filename'],
            'Products_Count': len(flyer['products'])
        })
    
    # Create products data
    products_data = []
    for flyer in all_flyer_data:
        for product in flyer['products']:
            # Extract numeric price for calculations
            price_numeric = 0
            if product['price'] and product['price'] != 'Price not found':
                price_match = re.search(r'(\d+\.?\d*)', str(product['price']))
                if price_match:
                    try:
                        price_numeric = float(price_match.group(1))
                    except:
                        price_numeric = 0
            
            products_data.append({
                'Product_ID': len(products_data) + 1,
                'Product_Name': product['product_name'],
                'Store_Name': flyer['store_name'] if flyer['store_name'] else 'Unknown Store',
                'Price_Text': product['price'],
                'Price_Numeric': price_numeric,
                'Size_Weight': product['size_weight'],
                'Description': product['description'],
                'Flyer_Source': flyer['filename']
            })
    
    # Create price comparison data (products grouped by similar names)
    comparison_data = []
    product_groups = {}
    
    # Group similar products
    for product in products_data:
        product_name = product['Product_Name'].lower().strip()
        # Simple grouping by first word or key terms
        key_words = product_name.split()
        if key_words:
            base_name = key_words[0]
            if base_name not in product_groups:
                product_groups[base_name] = []
            product_groups[base_name].append(product)
    
    # Create comparison entries for groups with multiple stores
    for group_name, products in product_groups.items():
        if len(products) > 1:  # Only include products available in multiple stores
            stores_in_group = set(p['Store_Name'] for p in products)
            if len(stores_in_group) > 1:  # Multiple stores selling similar product
                for product in products:
                    if product['Price_Numeric'] > 0:  # Only include products with valid prices
                        comparison_data.append({
                            'Product_Group': group_name.title(),
                            'Product_Name': product['Product_Name'],
                            'Store_Name': product['Store_Name'],
                            'Price': product['Price_Numeric'],
                            'Size_Weight': product['Size_Weight'],
                            'Stores_Selling': len(stores_in_group)
                        })
    
    return {
        'stores': pd.DataFrame(stores_data),
        'products': pd.DataFrame(products_data),
        'comparisons': pd.DataFrame(comparison_data)
    }

def create_excel_file(excel_data):
    """Create downloadable Excel file with multiple sheets"""
    
    # Create Excel file in memory
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Write each sheet
        excel_data['stores'].to_excel(writer, sheet_name='Stores', index=False)
        excel_data['products'].to_excel(writer, sheet_name='Products', index=False)
        excel_data['comparisons'].to_excel(writer, sheet_name='Price_Comparisons', index=False)
        
        # Format the sheets
        for sheet_name in ['Stores', 'Products', 'Price_Comparisons']:
            worksheet = writer.sheets[sheet_name]
            
            # Adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_name = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_name].width = adjusted_width
    
    output.seek(0)
    return output

# Main App Header
st.markdown("""
<div style='text-align: center; margin: 2rem 0;'>
    <h1 style='font-size: 3rem; margin-bottom: 0.5rem;'>MatchIt</h1>
    <div style='color: #a0a0a0; font-size: 1.1rem;'>
        Intelligent Price Matching and Comparison Platform
    </div>
</div>
""", unsafe_allow_html=True)

# Compact 3-Step Process
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div class='step-card'>
        <div style='color: #ffffff; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;'>Import Data</div>
        <div style='color: #cccccc; font-size: 0.9rem;'>Upload retail flyers and promotional materials</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='step-card'>
        <div style='color: #ffffff; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;'>AI Processing</div>
        <div style='color: #cccccc; font-size: 0.9rem;'>Extract pricing data with machine learning</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='step-card'>
        <div style='color: #ffffff; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;'>Price Intelligence</div>
        <div style='color: #cccccc; font-size: 0.9rem;'>Generate market insights and recommendations</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

# Load API key from environment variable
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    st.markdown("""
    <div style='border: 2px solid rgba(255, 100, 100, 0.4); background: rgba(255, 0, 0, 0.05); border-radius: 16px; padding: 2rem; margin: 2rem 0;'>
        <h3 style='color: #ff6666; margin-bottom: 1rem; text-align: center;'>Configuration Required</h3>
        <p style='margin-bottom: 1.5rem; text-align: center;'>API credentials not detected. Please configure your environment:</p>
        <div style='background: rgba(0, 0, 0, 0.5); padding: 1.5rem; border-radius: 12px; margin: 1rem 0;'>
            <p style='margin: 0; font-family: monospace; color: #00ffff; text-align: center;'>GEMINI_API_KEY=your_api_key_here</p>
        </div>
        <p style='color: #a0a0a0; font-size: 0.9rem; text-align: center;'>
            Obtain your API key from: <a href='https://makersuite.google.com/app/apikey' style='color: #00ffff;'>Google AI Studio</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Upload Section
st.markdown("""
<div class='upload-section'>
    <h3 style='margin-bottom: 1rem; text-align: center; color: #ffffff;'>Upload Your Flyers</h3>
</div>
""", unsafe_allow_html=True)

# Single unified file uploader
uploaded_files = st.file_uploader(
    "Drag and drop files here",
    type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'zip'],
    help="Limit 200MB per file • PNG, JPG, JPEG, GIF, BMP, ZIP",
    accept_multiple_files=True,
    key="unified_uploader"
)

upload_method = ""
final_files = []

if uploaded_files:
    # Process uploaded files silently
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name.lower()
        
        if file_name.endswith('.zip'):
            # Handle ZIP file silently
            with st.spinner("Extracting images from ZIP file..."):
                extracted_files = extract_images_from_zip(uploaded_file)
            
            if extracted_files:
                final_files.extend(extracted_files)
                upload_method = "zip"
            else:
                st.error("No valid image files found in ZIP file")
        else:
            # Handle individual image files
            final_files.append(uploaded_file)
            upload_method = "individual"
    
    uploaded_files = final_files  # Use the processed files

# Process uploaded files
if uploaded_files:
    # Show uploaded flyers preview
    st.markdown("---")
    st.subheader("Uploaded Flyers")
    
    # Create responsive grid for image preview
    cols_per_row = 4
    for i in range(0, len(uploaded_files), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, uploaded_file in enumerate(uploaded_files[i:i+cols_per_row]):
            with cols[j]:
                try:
                    image = Image.open(uploaded_file)
                    st.image(image, caption=getattr(uploaded_file, 'name', f'Flyer {i+j+1}'), use_container_width=True)
                    
                    # Reset file pointer for ZIP extracted files
                    if upload_method == "zip":
                        uploaded_file.seek(0)
                        
                except Exception as e:
                    st.error(f"Could not display {getattr(uploaded_file, 'name', f'Image {i+j+1}')}")
    
    # Show total count and analysis button
    st.info(f"{len(uploaded_files)} flyer(s) ready for analysis")
    
    # Center the button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        # Analysis button
        if st.button("ANALYZE FLYERS", type="primary", key="analyze_button"):
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            all_analyses = []
            
            for idx, uploaded_file in enumerate(uploaded_files):
                # Update progress
                progress = (idx + 1) / len(uploaded_files)
                progress_bar.progress(progress)
                
                file_name = getattr(uploaded_file, 'name', f'Image_{idx+1}')
                status_text.text(f"Analyzing {file_name}... ({idx + 1}/{len(uploaded_files)})")
                
                try:
                    # Analyze individual flyer
                    image = Image.open(uploaded_file)
                    analysis_result = convert_image_to_text(image, api_key)
                    
                    if analysis_result and not analysis_result.startswith("Error"):
                        all_analyses.append({
                            'filename': file_name,
                            'analysis': analysis_result,
                            'status': 'Success'
                        })
                    else:
                        all_analyses.append({
                            'filename': file_name,
                            'analysis': analysis_result,
                            'status': 'Error'
                        })
                except Exception as e:
                    all_analyses.append({
                        'filename': file_name,
                        'analysis': f"Error processing image: {str(e)}",
                        'status': 'Error'
                    })
                
                # Reset file pointer for ZIP extracted files
                if upload_method == "zip":
                    uploaded_file.seek(0)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Parse all flyer data and store in session state
            successful_analyses = [a for a in all_analyses if a['status'] == 'Success']
            
            if successful_analyses:
                all_flyer_data = []
                for analysis in successful_analyses:
                    flyer_data = parse_flyer_data(analysis['analysis'], analysis['filename'])
                    all_flyer_data.append(flyer_data)
                
                # Store in session state for the product search and Excel functionality
                products_data = []
                for flyer in all_flyer_data:
                    for product in flyer['products']:
                        products_data.append({
                            'Product_ID': len(products_data) + 1,
                            'Product_Name': product['product_name'],
                            'Store_Name': flyer['store_name'] if flyer['store_name'] else 'Unknown Store',
                            'Price': product['price'],
                            'Size_Weight': product['size_weight'],
                            'Description': product['description'],
                            'Flyer_Source': flyer['filename']
                        })
                
                st.session_state.products_data = products_data
                st.session_state.all_flyer_data = all_flyer_data  # Store complete flyer data for Excel
                
                st.success(f"Analysis complete! Found {len(products_data)} products from {len(all_flyer_data)} flyers.")
            else:
                st.error("No successful analyses found.")

# EXCEL PREVIEW AND DOWNLOAD SECTION (NEW)
if 'all_flyer_data' in st.session_state and st.session_state.all_flyer_data:
    st.markdown("---")
    
    # Create Excel data
    excel_data = create_excel_data(st.session_state.all_flyer_data)
    
    st.markdown("""
    <div class='excel-preview-section'>
        <h2 style='text-align: center; color: #ffffff; margin-bottom: 2rem;'>📊 Excel Data Preview</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different data views
    tab1, tab2, tab3 = st.tabs(["🏪 Stores Overview", "🛒 Products Catalog", "💰 Price Comparisons"])
    
    with tab1:
        st.markdown("""
        <div class='tab-header'>
            <h4 style='margin: 0; color: #ffffff;'>Stores Information</h4>
            <p style='margin: 0.5rem 0 0 0; color: #cccccc;'>Complete store details extracted from flyers</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not excel_data['stores'].empty:
            st.dataframe(excel_data['stores'], use_container_width=True, height=400)
            
            # Store statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Stores", len(excel_data['stores']))
            with col2:
                st.metric("Stores with Address", len(excel_data['stores'][excel_data['stores']['Address'] != '']))
            with col3:
                st.metric("Stores with Website", len(excel_data['stores'][excel_data['stores']['Website'] != '']))
        else:
            st.warning("No store data available")
    
    with tab2:
        st.markdown("""
        <div class='tab-header'>
            <h4 style='margin: 0; color: #ffffff;'>Products Catalog</h4>
            <p style='margin: 0.5rem 0 0 0; color: #cccccc;'>All products extracted with pricing information</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not excel_data['products'].empty:
            # Display products dataframe
            st.dataframe(excel_data['products'], use_container_width=True, height=400)
            
            # Product statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Products", len(excel_data['products']))
            with col2:
                products_with_prices = len(excel_data['products'][excel_data['products']['Price_Numeric'] > 0])
                st.metric("Products with Prices", products_with_prices)
            with col3:
                avg_price = excel_data['products'][excel_data['products']['Price_Numeric'] > 0]['Price_Numeric'].mean()
                st.metric("Average Price", f"${avg_price:.2f}" if avg_price else "N/A")
            with col4:
                unique_stores = excel_data['products']['Store_Name'].nunique()
                st.metric("Unique Stores", unique_stores)
        else:
            st.warning("No product data available")
    
    with tab3:
        st.markdown("""
        <div class='tab-header'>
            <h4 style='margin: 0; color: #ffffff;'>Price Comparisons</h4>
            <p style='margin: 0.5rem 0 0 0; color: #cccccc;'>Products available across multiple stores for comparison</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not excel_data['comparisons'].empty:
            st.dataframe(excel_data['comparisons'], use_container_width=True, height=400)
            
            # Comparison statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Comparable Products", len(excel_data['comparisons']))
            with col2:
                product_groups = excel_data['comparisons']['Product_Group'].nunique()
                st.metric("Product Categories", product_groups)
            with col3:
                if len(excel_data['comparisons']) > 0:
                    avg_savings = excel_data['comparisons'].groupby('Product_Group')['Price'].apply(lambda x: x.max() - x.min()).mean()
                    st.metric("Avg Potential Savings", f"${avg_savings:.2f}" if avg_savings else "N/A")
        else:
            st.info("No comparable products found across multiple stores")
    
    # Download Section
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; margin: 2rem 0;'>
        <h3 style='color: #ffffff; margin-bottom: 1rem;'>📥 Download Complete Analysis</h3>
        <p style='color: #cccccc; margin-bottom: 2rem;'>Get your complete price analysis in Excel format with all stores, products, and comparisons</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the download button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Create Excel file
        excel_file = create_excel_file(excel_data)
        
        # Generate filename with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"MatchIt_Price_Analysis_{timestamp}.xlsx"
        
        # Download button
        st.download_button(
            label="📊 DOWNLOAD EXCEL REPORT",
            data=excel_file,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_excel"
        )
        
        # File info
        st.caption(f"File: {filename} • Contains 3 sheets: Stores, Products, Price Comparisons")

# PERSISTENT PRODUCT SEARCH (Outside analysis block)
if 'products_data' in st.session_state and st.session_state.products_data:
    st.markdown("---")
    st.subheader("Quick Product Search")
    st.markdown("**Search across all analyzed stores:**")
    
    products_data = st.session_state.products_data
    
    # Search interface
    col_search, col_button = st.columns([4, 1])
    
    with col_search:
        search_product = st.text_input(
            "Product Search",
            placeholder="Search for products (e.g., milk, bread, eggs)",
            key="persistent_search",
            label_visibility="collapsed"
        )
    
    with col_button:
        search_clicked = st.button("Search", type="secondary")
    
    # Available products reference
    all_product_names = list(set([p['Product_Name'].lower() for p in products_data]))[:12]
    st.caption(f"Available: {', '.join(all_product_names)}")
    
    # Perform search
    if search_product:
        # Handle multiple search terms
        search_terms = [term.strip() for term in search_product.split(',') if term.strip()]
        
        st.success(f"Searching for {len(search_terms)} item(s): {', '.join(search_terms)}")
        
        # Process each search term individually and completely separately
        for search_index, search_term in enumerate(search_terms):
            st.markdown(f"### Results for: **{search_term.title()}**")
            
            # Find products for ONLY this specific search term
            single_term_results = []
            for product in products_data:
                if search_term.lower() in product['Product_Name'].lower():
                    price_num = 0
                    if product['Price'] and product['Price'] != 'Price not found':
                        price_match = re.search(r'(\d+\.?\d*)', str(product['Price']))
                        if price_match:
                            try:
                                price_num = float(price_match.group(1))
                            except:
                                price_num = 0
                    
                    single_term_results.append({
                        'Product_Name': product['Product_Name'],
                        'Store_Name': product['Store_Name'],
                        'Price_Text': product['Price'],
                        'Price_Numeric': price_num,
                        'Size_Weight': product['Size_Weight']
                    })
            
            if single_term_results:
                st.success(f"Found {len(single_term_results)} products matching '{search_term}'")
                
                # Filter for valid prices - ONLY for this search term
                chart_data_single = [item for item in single_term_results if item['Price_Numeric'] > 0]
                
                if len(chart_data_single) >= 1:
                    # Create DataFrame with ONLY this search term's data
                    df_single = pd.DataFrame(chart_data_single)
                    
                    # Create completely separate bar chart - NO GROUPING
                    fig_individual = px.bar(
                        df_single,
                        x='Store_Name',
                        y='Price_Numeric',
                        title=f'{search_term.title()} - Price Comparison',
                        labels={'Price_Numeric': 'Price ($)', 'Store_Name': 'Store'},
                        height=400,
                        # Single color gradient - no grouping by search term
                        color='Price_Numeric',
                        color_continuous_scale='Viridis',
                        text='Price_Numeric'
                    )
                    
                    # Style the chart
                    fig_individual.update_traces(
                        texttemplate='$%{text:.2f}',
                        textposition='outside',
                        cliponaxis=False
                    )
                    
                    fig_individual.update_layout(
                        height=400,
                        showlegend=False,
                        xaxis_title="Store",
                        yaxis_title="Price ($)",
                        title_font_size=16,
                        margin=dict(t=80, b=100, l=80, r=80),
                        yaxis=dict(
                            range=[0, max(df_single['Price_Numeric']) * 1.2]
                        ),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        xaxis_tickangle=-45
                    )
                    
                    # Display with completely unique key
                    st.plotly_chart(fig_individual, use_container_width=True, key=f"persistent_chart_{search_index}_{search_term.replace(' ', '_').replace(',', '')}")
                    
                    # Best deals analysis for this specific term
                    if len(chart_data_single) > 1:
                        cheapest_item = min(chart_data_single, key=lambda x: x['Price_Numeric'])
                        expensive_item = max(chart_data_single, key=lambda x: x['Price_Numeric'])
                        savings_amount = expensive_item['Price_Numeric'] - cheapest_item['Price_Numeric']
                        
                        # Deal cards
                        st.markdown(f"""
                        <div style='display: flex; gap: 1rem; margin: 1.5rem 0;'>
                            <div class='deal-card best'>
                                <div style='color: #00ff88; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;'>BEST DEAL</div>
                                <div style='color: #ffffff; font-weight: 600; margin-bottom: 0.5rem;'>{cheapest_item['Store_Name']}</div>
                                <div style='color: #00ff88; font-size: 1.8rem; font-weight: 800;'>${cheapest_item['Price_Numeric']:.2f}</div>
                            </div>
                            <div class='deal-card highest'>
                                <div style='color: #ff6464; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;'>HIGHEST PRICE</div>
                                <div style='color: #ffffff; font-weight: 600; margin-bottom: 0.5rem;'>{expensive_item['Store_Name']}</div>
                                <div style='color: #ff6464; font-size: 1.8rem; font-weight: 800;'>${expensive_item['Price_Numeric']:.2f}</div>
                            </div>
                            <div class='deal-card savings'>
                                <div style='color: #00c8ff; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;'>YOU SAVE</div>
                                <div style='color: #ffffff; font-weight: 600; margin-bottom: 0.5rem;'>Choose Best Deal</div>
                                <div style='color: #00c8ff; font-size: 1.8rem; font-weight: 800;'>${savings_amount:.2f}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Results table for this specific search term
                st.markdown(f"#### All {search_term.title()} Results")
                results_df_single = pd.DataFrame(single_term_results)
                st.dataframe(
                    results_df_single[['Product_Name', 'Store_Name', 'Price_Text', 'Size_Weight']], 
                    use_container_width=True,
                    key=f"persistent_table_{search_index}_{search_term.replace(' ', '_').replace(',', '')}"
                )
                
            else:
                st.warning(f"No results found for '{search_term}'")
            
            # Add separator between search terms (not for the last one)
            if search_index < len(search_terms) - 1:
                st.markdown("---")
                st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

else:
    # Welcome section when no data available AND no files uploaded
    if not uploaded_files:
        st.info("Upload and analyze flyers to start searching products and accessing Excel features!")

# Hide Streamlit elements
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.css-1d391kg {display: none;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)