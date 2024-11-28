const apiKey = '85d8f1a83eda48bbb85195857242311';
const city = 'Hyderabad';
const weatherContainer = document.getElementById('weather-container');
const chartContext = document.getElementById('weather-graph').getContext('2d');

async function fetchWeatherData() {
    try {
        const response = await fetch(
            `https://api.weatherapi.com/v1/forecast.json?key=${apiKey}&q=${city}&days=7&aqi=yes`
        );
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching weather data:', error);
        return null;
    }
}

function displayWeatherCards(forecast) {
    weatherContainer.innerHTML = '';

    forecast.forecastday.forEach(day => {
        const date = new Date(day.date);
        const card = document.createElement('div');
        card.className = 'weather-card';
        card.innerHTML = `
            <h3>${date.toLocaleDateString('en-US', { weekday: 'short' })}</h3>
            <img src="${day.day.condition.icon}" alt="${day.day.condition.text}">
            <p class="temp">${day.day.avgtemp_c}°C</p>
            <p class="rain">🌧 ${day.day.daily_chance_of_rain}%</p>
        `;
        weatherContainer.appendChild(card);
    });
}

function displayWeatherGraph(forecast) {
    const dates = forecast.forecastday.map(day => new Date(day.date).toLocaleDateString('en-US', { weekday: 'short' }));
    const temps = forecast.forecastday.map(day => day.day.avgtemp_c);
    const rain = forecast.forecastday.map(day => day.day.daily_chance_of_rain);
    const humidity = forecast.forecastday.map(day => day.day.avghumidity);
    const windSpeed = forecast.forecastday.map(day => day.day.maxwind_kph);
    const conditions = forecast.forecastday.map(day => day.day.condition.text);

    new Chart(chartContext, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Temperature (°C)',
                    data: temps,
                    borderColor: '#f44336',
                    backgroundColor: 'rgba(244, 67, 54, 0.1)',
                    tension: 0.4,
                    yAxisID: 'y'
                },
                {
                    label: 'Rain Chance (%)',
                    data: rain,
                    borderColor: '#2196f3',
                    backgroundColor: 'rgba(33, 150, 243, 0.1)',
                    tension: 0.4,
                    yAxisID: 'y1'
                },
                {
                    label: 'Humidity (%)',
                    data: humidity,
                    borderColor: '#4CAF50',
                    backgroundColor: 'rgba(76, 175, 80, 0.1)',
                    tension: 0.4,
                    yAxisID: 'y1',
                    hidden: true
                },
                {
                    label: 'Wind Speed (km/h)',
                    data: windSpeed,
                    borderColor: '#9C27B0',
                    backgroundColor: 'rgba(156, 39, 176, 0.1)',
                    tension: 0.4,
                    yAxisID: 'y2',
                    hidden: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15
                    }
                },
                tooltip: {
                    callbacks: {
                        afterBody: function (context) {
                            const dataIndex = context[0].dataIndex;
                            return `\nCondition: ${conditions[dataIndex]}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Temperature (°C)'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Percentage (%)'
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                },
                y2: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Wind Speed (km/h)'
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                }
            }
        }
    });
}

async function initWeatherDashboard() {
    const data = await fetchWeatherData();
    if (data) {
        displayWeatherCards(data.forecast);
        displayWeatherGraph(data.forecast);
    }
}

// Initialize the dashboard
initWeatherDashboard();

// Refresh data every 30 minutes
setInterval(initWeatherDashboard, 30 * 60 * 1000);


