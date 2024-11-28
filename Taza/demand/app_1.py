from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Load the saved model and data
try:
    with open('model_data.pkl', 'rb') as f:
        model_data = pickle.load(f)
        
    lgb_model = model_data['model']
    le = model_data['label_encoder']
    features = model_data['features']
    commodity_stats = model_data['commodity_stats']
    
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    raise

# Default values
DEFAULT_WEATHER = {
    'maxt': 30.0,
    'mint': 20.0,
    'windspeed': 1.7,
    'humidity': 64.1,
    'precipitation': 0.0
}

@app.route('/')
def home():
    return render_template('index.html', 
                         commodities=sorted(commodity_stats.keys()))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get selected commodity
        commodity = request.form['commodity']
        
        # Get current date
        current_date = datetime.now()
        
        # Use default values for prediction
        prediction_data = {
            'maxt': DEFAULT_WEATHER['maxt'],
            'mint': DEFAULT_WEATHER['mint'],
            'windspeed': DEFAULT_WEATHER['windspeed'],
            'humidity_': DEFAULT_WEATHER['humidity'],
            'precipitation': DEFAULT_WEATHER['precipitation'],
            'month': current_date.month,
            'day': current_date.day,
            'festival_name_encoded': le.transform(["new_year's_day"])[0],  # default festival
            'minimum': commodity_stats[commodity]['min_price'],
            'maximum': commodity_stats[commodity]['max_price'],
            'average': commodity_stats[commodity]['avg_price'],
            'price_diff': 0,  # using current average price
            'price_pct_change': 0,  # using current average price
            'units_sold_lag1': commodity_stats[commodity]['last_units_sold']
        }
        
        # Create DataFrame for prediction
        pred_df = pd.DataFrame([prediction_data])[features]
        
        # Make prediction
        prediction = lgb_model.predict(pred_df)[0]
        
        # Calculate percentage change
        avg_demand = commodity_stats[commodity]['avg_demand']
        demand_change_pct = ((prediction - avg_demand) / avg_demand) * 100
        
        result = {
            'commodity': commodity,
            'predicted_demand': round(prediction, 2),
            'average_demand': round(avg_demand, 2),
            'demand_change_percentage': round(demand_change_pct, 2),
            'current_price': round(commodity_stats[commodity]['avg_price'], 2)
        }
        
        return render_template('index.html', 
                             prediction=result,
                             commodities=sorted(commodity_stats.keys()))
    
    except Exception as e:
        return render_template('index.html', 
                             error=str(e),
                             commodities=sorted(commodity_stats.keys()))

if __name__ == '__main__':
    app.run(debug=True)