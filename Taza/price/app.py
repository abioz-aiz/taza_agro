import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import sys
import traceback

# Page config
st.set_page_config(
    page_title="Taza Price Prediction",
    page_icon="🌿",
    layout="wide"
)

# Initialize session state for debugging
if 'debug_info' not in st.session_state:
    st.session_state.debug_info = []

def safe_predict_price(input_data):
    """Safely wrap the predict_price function with error handling"""
    try:
        # Import here to catch import errors
        from predict import predict_price
        
        # Log the input data for debugging
        st.session_state.debug_info.append(f"Input data: {input_data}")
        
        # Make prediction
        result = predict_price(input_data)
        
        # Log the result
        st.session_state.debug_info.append(f"Prediction result: {result}")
        
        return float(result)
    except ImportError as e:
        st.error("Failed to import predict_price function. Check if predict.py exists and is properly formatted.")
        st.session_state.debug_info.append(f"Import error: {str(e)}")
        raise
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")
        st.session_state.debug_info.append(f"Prediction error: {str(e)}\n{traceback.format_exc()}")
        raise

def calculate_accuracy(predicted, actual):
    """Calculate prediction accuracy"""
    if actual > 0:
        percentage_error = abs(predicted - actual) / actual * 100
        return round(100 - percentage_error, 2)
    return None

def process_single_prediction(input_data):
    """Process single prediction with error handling"""
    try:
        predicted_price = safe_predict_price(input_data)
        accuracy = None
        
        if input_data.get('average', 0) > 0:
            accuracy = calculate_accuracy(predicted_price, input_data['average'])
            
        return {
            'status': 'success',
            'predicted_price': round(predicted_price, 2),
            'commodity': input_data['commodity'],
            'accuracy': accuracy
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def main():
    st.title("Taza Price Prediction System")
    
    # Debug information in sidebar
    with st.sidebar:
        if st.checkbox("Show Debug Info"):
            st.write("Debug Information:")
            for info in st.session_state.debug_info:
                st.text(info)
            if st.button("Clear Debug Info"):
                st.session_state.debug_info = []
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Single Prediction", "Batch Prediction", "API Documentation"])
    
    # Single Prediction Tab
    with tab1:
        st.header("Single Prediction")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.form("prediction_form"):
                try:
                    commodity = st.selectbox(
                        "Commodity",
                        ["tomato_big(nepali)", "potato_red", "onion_dry", "cabbage"]
                    )
                    
                    commodity_category = st.selectbox(
                        "Category",
                        ["vegetables", "fruits"]
                    )
                    
                    col_temp1, col_temp2 = st.columns(2)
                    with col_temp1:
                        maxt = st.number_input("Max Temperature (°C)", value=29.9)
                        mint = st.number_input("Min Temperature (°C)", value=20.1)
                    
                    with col_temp2:
                        windspeed = st.number_input("Wind Speed (m/s)", value=1.7)
                        humidity = st.number_input("Humidity (%)", value=64.1)
                    
                    precipitation = st.number_input("Precipitation (mm)", value=0.0)
                    
                    # Date inputs
                    col_date1, col_date2, col_date3 = st.columns(3)
                    with col_date1:
                        month = st.number_input("Month", min_value=1, max_value=12, value=datetime.now().month)
                    with col_date2:
                        day = st.number_input("Day", min_value=1, max_value=31, value=datetime.now().day)
                    with col_date3:
                        year = st.number_input("Year", min_value=2000, max_value=2100, value=datetime.now().year)
                    
                    actual_price = st.number_input("Actual Price (optional, for accuracy)", value=0.0, min_value=0.0)
                    
                    submitted = st.form_submit_button("Predict Price")
                    
                    if submitted:
                        try:
                            with st.spinner('Calculating prediction...'):
                                input_data = {
                                    'maxt': float(maxt),
                                    'mint': float(mint),
                                    'windspeed': float(windspeed),
                                    'humidity_': float(humidity),
                                    'precipitation': float(precipitation),
                                    'month': int(month),
                                    'day': int(day),
                                    'year': int(year),
                                    'commodity': str(commodity),
                                    'commodity_category': str(commodity_category),
                                    'average': float(actual_price)
                                }
                                
                                # Log input data
                                st.session_state.debug_info.append(f"Processing input data: {input_data}")
                                
                                result = process_single_prediction(input_data)
                                
                                with col2:
                                    if result['status'] == 'success':
                                        st.success("Prediction Complete!")
                                        st.markdown(f"""
                                        <div style='padding: 20px; background-color: #f0f2f6; border-radius: 10px;'>
                                            <h3>Predicted Price: NPR {result['predicted_price']:.2f}</h3>
                                            <p><strong>Commodity:</strong> {result['commodity']}</p>
                                            <p><strong>Date:</strong> {year}-{month:02d}-{day:02d}</p>
                                            {f"<p><strong>Accuracy:</strong> {result['accuracy']}%</p>" if result['accuracy'] else ""}
                                        </div>
                                        """, unsafe_allow_html=True)
                                    else:
                                        st.error(f"Prediction failed: {result['message']}")
                                        st.session_state.debug_info.append(f"Prediction failure: {result['message']}")
                        
                        except Exception as e:
                            st.error(f"Error during prediction: {str(e)}")
                            st.session_state.debug_info.append(f"Error during prediction: {str(e)}\n{traceback.format_exc()}")
                
                except Exception as e:
                    st.error(f"Error in form: {str(e)}")
                    st.session_state.debug_info.append(f"Form error: {str(e)}\n{traceback.format_exc()}")

    # Batch Prediction Tab
    with tab2:
        st.header("Batch Prediction")
        
        uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=['csv'])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.write("Preview of uploaded data:", df.head())
                
                if st.button("Run Batch Prediction"):
                    predictions = []
                    total_accuracy = 0
                    valid_accuracy_count = 0
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, row in df.iterrows():
                        status_text.text(f"Processing row {idx+1}/{len(df)}")
                        
                        try:
                            input_data = {
                                'maxt': float(row['maxt']),
                                'mint': float(row['mint']),
                                'windspeed': float(row['windspeed']),
                                'humidity_': float(row.get('humidity_', row.get('humidity', 0))),
                                'precipitation': float(row['precipitation']),
                                'month': int(row['month']),
                                'day': int(row['day']),
                                'year': int(row['year']),
                                'commodity': str(row['commodity']),
                                'commodity_category': str(row['commodity_category']),
                                'average': float(row.get('average', 0))
                            }
                            
                            result = process_single_prediction(input_data)
                            
                            if result['status'] == 'success':
                                predictions.append({
                                    'commodity': input_data['commodity'],
                                    'predicted_price': result['predicted_price'],
                                    'accuracy': result['accuracy']
                                })
                                
                                if result['accuracy']:
                                    total_accuracy += result['accuracy']
                                    valid_accuracy_count += 1
                            
                        except Exception as e:
                            st.error(f"Error processing row {idx+1}: {str(e)}")
                        
                        progress_bar.progress((idx + 1) / len(df))
                    
                    status_text.text("Processing complete!")
                    
                    if predictions:
                        # Display results
                        results_df = pd.DataFrame(predictions)
                        st.write("Prediction Results:", results_df)
                        
                        # Plot predictions
                        fig = px.bar(results_df, 
                                   x='commodity', 
                                   y='predicted_price',
                                   title='Predicted Prices by Commodity')
                        st.plotly_chart(fig)
                        
                        if valid_accuracy_count > 0:
                            avg_accuracy = round(total_accuracy / valid_accuracy_count, 2)
                            st.success(f"Average Prediction Accuracy: {avg_accuracy}%")
                        
                        # Download results
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            "Download Results",
                            csv,
                            "prediction_results.csv",
                            "text/csv",
                            key='download-csv'
                        )
                    
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    
    # API Documentation Tab
    with tab3:
        st.header("API Documentation")
        
        st.markdown("""
        ### Single Prediction Endpoint
        **URL:** `/predict`  
        **Method:** POST
        
        Example Request:
        ```json
        {
            "maxt": 29.9,
            "mint": 20.1,
            "windspeed": 1.7,
            "humidity": 64.1,
            "precipitation": 0.0,
            "month": 1,
            "day": 1,
            "year": 2024,
            "commodity": "tomato_big(nepali)",
            "commodity_category": "vegetables"
        }
        ```
        
        ### Response Format
        Success Response:
        ```json
        {
            "status": "success",
            "predicted_price": 42.5,
            "commodity": "tomato_big(nepali)"
        }
        ```
        
        Error Response:
        ```json
        {
            "status": "error",
            "message": "Error description"
        }
        ```
        """)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.write("Full error trace:")
        st.code(traceback.format_exc())