# Taaza - Agricultural Price Prediction Dashboard

#### 2nd Prize Winner for the Datanyx 24-hour Datathon organized by AWS MJCET

Taza is a web-based dashboard that provides crop price predictions, weather forecasts, and market insights for agricultural commodities. The application helps farmers and traders make informed decisions about buying and selling agricultural products.

Find the Elaborate Project Presentation [here](https://www.canva.com/design/DAGX2Irlfe8/-YC7V8Z9j-SQ1n5kMLRYHg/view?utm_content=DAGX2Irlfe8&utm_campaign=designshare&utm_medium=link&utm_source=editor)

## Features

- **Crop Price Prediction**
  - Real-time price predictions for various agricultural commodities
  - Historical price trend visualization using Tableau
  - Price comparison across different markets

- **Weather Integration**
  - Detailed weather forecasts with temperature, precipitation, and wind data
  - Weather trend visualization using Chart.js
  - Weather-based agricultural insights and alerts

- **Market Insights**
  - Scrolling recommendations for optimal buying/selling times
  - Market trend analysis
  - Crop planning suggestions based on current conditions

- **Interactive Chat Assistant**
  - AI-powered chat support for queries
  - Real-time assistance with price predictions and market information

## Technology Stack

- **Backend**
  - Flask (Python web framework)
  - LightGBM (Machine Learning model)
  - Pandas for data processing

- **Frontend**
  - HTML5/CSS3
  - JavaScript
  - Chart.js for weather visualization
  - Tableau for price trend visualization

## Installation

1. Clone the repository:
   
git clone https://github.com/yourusername/taza.git
 
2. Install required Python packages:

  pip install -r requirements.txt

3. Run the Streamlit application:

  Streamlit run Taza/demand/app_1.py
  Streamlit run Taza/price/app.py

4. Access the dashboard at `http://localhost:5000`

## Project Structure

Taza/

├── demand/

│   └── app_1.py  # Main Streamlit application

├── static/

│ ├── daash.js # Dashboard functionality

│ └── chat.js # Chat widget functionality

├── templates/

│ └── dashboard.html # Main dashboard template

└── model_data.pkl # Trained machine learning model for demand forecasting

└── final_price_prediction_model.pkl # Trained machine learning model for Price Prediction



## Usage

1. Select a commodity from the dropdown menu
2. View current prices and predicted trends
3. Check weather forecasts and their potential impact on prices
4. Read market recommendations for optimal trading decisions
5. Use the chat assistant for any specific queries

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Weather data provided by [Meteoblue Weather Maps](https://www.meteoblue.com/en/weather/maps/index#coords=4/17.38/78.46&map=windAnimation~rainbow~auto~10%20m%20above%20gnd~none)
- Market data sourced from [Taza Agro Dataset](https://github.com/abioz-aiz/taza_agro/blob/main/Datasets/final_final_dataset.csv)
- Tableau Public for visualization support

## Contact

[Zoiba Zia](https://www.linkedin.com/in/zoiba/) - LinkedIn

Project Link: [github.com/abioz-aiz/taza_agro](https://github.com/abioz-aiz/taza_agro)
