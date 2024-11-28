import pickle
import dill
import pandas as pd
import numpy as np

class PricePredictionModel:
    def __init__(self, model_path='final_price_prediction_model.pkl'):
        # Load the model package
        with open(model_path, 'rb') as f:
            model_package = pickle.load(f)
        
        self.category_models = model_package['category_models']
        self.scaler = model_package['scaler']
        self.features = model_package['features']
        self.prepare_features = dill.loads(model_package['prepare_features'])  # Load the function
    
    def predict(self, input_data):
        """
        Make predictions for input data
        
        Parameters:
        input_data (dict or pd.DataFrame): Input data containing required features
        
        Returns:
        float: Predicted price
        """
        try:
            # Convert dict to DataFrame if necessary
            if isinstance(input_data, dict):
                input_data = pd.DataFrame([input_data])
            
            # Prepare features
            prepared_data = self.prepare_features(input_data)
            X = prepared_data[self.features]
            X_scaled = self.scaler.transform(X)
            
            # Get the category and corresponding model
            category = input_data['commodity_category'].iloc[0]
            if category not in self.category_models:
                raise ValueError(f"Unknown category: {category}")
            
            model = self.category_models[category]
            prediction = model.predict(X_scaled)[0]
            
            return prediction
        except Exception as e:
            raise Exception(f"Prediction error: {str(e)}")

def predict_price(input_data):
    """Wrapper function for making predictions"""
    model = PricePredictionModel()
    return model.predict(input_data)