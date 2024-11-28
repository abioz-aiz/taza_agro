const apiKey = '85d8f1a83eda48bbb85195857242311'; // Replace with your WeatherAPI or OpenWeather API key
const city = 'Hyderabad'; // Replace with the desired city
const chartContext = document.getElementById('weather-graph').getContext('2d');
const insightsContainer = document.getElementById('insights-container');

async function fetchMonthlyWeather() {
    const url = `https://api.weatherapi.com/v1/forecast.json?key=${apiKey}&q=${city}&days=30`;
    try {
        const response = await fetch(url);
        const data = await response.json();
        console.log(data); // Debugging: Check API response structure

        const dailyForecasts = data.forecast.forecastday;

        // Extract data for the graph
        const dates = dailyForecasts.map(day => day.date);
        const temperatures = dailyForecasts.map(day => day.day.avgtemp_c);
        const rainChances = dailyForecasts.map(day => day.day.daily_chance_of_rain);

        // Display Graph
        displayWeatherGraph(dates, temperatures, rainChances);

        // Generate Insights
        generateInsights(dailyForecasts);
    } catch (error) {
        console.error('Error fetching weather data:', error);
    }
}

function displayWeatherGraph(dates, temperatures, rainChances) {
    new Chart(chartContext, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Average Temperature (°C)',
                    data: temperatures,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.2,
                    yAxisID: 'y',
                },
                {
                    label: 'Chance of Rain (%)',
                    data: rainChances,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    tension: 0.2,
                    yAxisID: 'y1',
                }
            ]
        },
        options: {
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Temperature (°C)' },
                },
                y1: {
                    beginAtZero: true,
                    position: 'right',
                    title: { display: true, text: 'Chance of Rain (%)' },
                },
            },
        },
    });
}

function generateInsights(forecasts) {
    const insights = [];

    // Generate insights based on weather patterns
    forecasts.forEach((forecast) => {
        const condition = forecast.day.condition.text.toLowerCase();
        if (condition.includes('rain') || condition.includes('storm')) {
            insights.push({
                title: 'Rain Alert',
                message: `Rain expected on ${forecast.date}. Plan accordingly.`,
            });
        }
        if (forecast.day.avgtemp_c > 35) {
            insights.push({
                title: 'Heat Advisory',
                message: `High temperature (${forecast.day.avgtemp_c}°C) expected on ${forecast.date}.`,
            });
        }
        if (forecast.day.daily_chance_of_rain > 60) {
            insights.push({
                title: 'Irrigation Alert',
                message: `High chance of rain (${forecast.day.daily_chance_of_rain}%) on ${forecast.date}. Reduce irrigation.`,
            });
        }
    });

    // Display insights
    insightsContainer.innerHTML = '';
    insights.forEach((insight) => {
        const insightDiv = document.createElement('div');
        insightDiv.classList.add('insight-item');
        insightDiv.innerHTML = `
            <h3>${insight.title}</h3>
            <p>${insight.message}</p>
        `;
        insightsContainer.appendChild(insightDiv);
    });
}

// Fetch and render weather on page load
window.onload = fetchMonthlyWeather;
