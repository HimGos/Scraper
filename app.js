const socket = new WebSocket("ws://localhost:5000"); // Connect to your server

let chartData = {
    labels: [],
    datasets: [{
        label: 'Currency Strength',
        data: [],
        backgroundColor: function(context) {
            const strength = context.dataset.data[context.dataIndex];
            return colorMap[strength] || 'gray'; // Default color
        },

        borderWidth: 1,
        borderRadius: 28
    }]
};

const colorMap = {
    3: '#17AB0B',
    2: '#11E900',
    1: '#B3F607',
    '-1': '#FCE607',
    '-2': '#FCAF07',
    '-3': '#FC5E00'
};

const ctx = document.getElementById('currencyChart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'bar',
    data: chartData,
    options: {
        scales: {
            x:{
                ticks: {
                    font:{
                        size:14,
                        weight: 'bold'
                        }
                    }
            },
            y: {
                min: -3,  // Set the minimum value of the y-axis
                max: 3,   // Set the maximum value of the y-axis
                ticks: {
                    stepSize: 1,
                    callback: function(value, index, values) {
                        return value;
                        }
                    },
                title:{
                    display: true,
                    text:'Strength',
                    padding: 20,
                    font:{
                        family: 'helvetica',
                        size: 22,
                        weight: 'bold'
                        }
                    }
            }
        },
        layout: {
            padding:{
            left:10
            }
        }
    }
});

socket.onmessage = function(event) {
    const updates = JSON.parse(event.data);

    updates.forEach(update => {
        const existingIndex = chartData.labels.indexOf(update.currency);

        if (existingIndex !== -1) {
            chartData.datasets[0].data[existingIndex] = update.strength;
        } else {
            chartData.labels.push(update.currency);
            chartData.datasets[0].data.push(update.strength);
        }
    });

    chart.update();
};

// Update time display every second
function updateTime() {
    const now = new Date();
    const formattedTime = now.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
    const formattedDate = now.toLocaleDateString('en-US', { month: 'short', day: '2-digit' });
    const timeDisplay = document.getElementById('timeDisplay');
    timeDisplay.textContent = 'As of:' + ' ' + formattedDate + ' ' + formattedTime + ' GMT(+05:30)';
}

// Update time display initially and then every second
updateTime();
setInterval(updateTime, 1000);

