const apiKey = '85d8f1a83eda48bbb85195857242311'; // Replace with your WeatherAPI key
const city = 'Hyderabad'; // Replace with your desired location
const weatherContainer = document.getElementById('weather-container');
const weatherAlert = document.getElementById('weather-alert');
const weatherAlertMessage = document.getElementById('weather-alert-message');

// Fetch weather data
async function fetchWeather() {
    const url = `https://api.weatherapi.com/v1/forecast.json?key=${apiKey}&q=${city}&days=6`;
    try {
        const response = await fetch(url);
        const data = await response.json();

        // Debugging: log the data to the console
        console.log(data);

        displayWeather(data);
        checkWeatherAlerts(data);
    } catch (error) {
        console.error('Error fetching weather data:', error);
    }
}

// Display current and 5-day forecast
function displayWeather(data) {
    const forecasts = data.forecast.forecastday;
    weatherContainer.innerHTML = ''; // Clear previous content

    // Debugging: Ensure forecast data is available
    if (!forecasts || forecasts.length === 0) {
        weatherContainer.innerHTML = '<p>No weather data available.</p>';
        return;
    }

    forecasts.forEach((forecast) => {
        const date = new Date(forecast.date).toLocaleDateString('en-US', { weekday: 'long' });
        const temp = forecast.day.avgtemp_c;
        const icon = forecast.day.condition.icon;
        const condition = forecast.day.condition.text;

        const weatherCard = document.createElement('div');
        weatherCard.classList.add('weather-card');
        weatherCard.innerHTML = `
            <h3>${date}</h3>
            <img src="https:${icon}" alt="${condition}">
            <p>${temp}°C</p>
            <p>${condition}</p>
        `;
        weatherContainer.appendChild(weatherCard);
    });
}

// Check for severe weather alerts
function checkWeatherAlerts(data) {
    const alerts = data.alerts ? data.alerts.alert : [];
    let alertMessage = '';

    if (alerts.length > 0) {
        alertMessage = alerts[0].headline;
    } else {
        // Custom message for rain or storms based on forecast
        const forecasts = data.forecast.forecastday;
        forecasts.forEach((forecast) => {
            const condition = forecast.day.condition.text.toLowerCase();
            if (condition.includes('rain') || condition.includes('storm')) {
                alertMessage = `Alert: ${condition} expected on ${forecast.date}`;
            }
        });
    }

    if (alertMessage) {
        weatherAlertMessage.textContent = alertMessage;
        weatherAlert.classList.remove('hidden');
        setTimeout(() => {
            weatherAlert.classList.add('hidden');
        }, 10000); // Hide after 10 seconds
    }
}

// Call fetchWeather on page load
window.onload = fetchWeather;
