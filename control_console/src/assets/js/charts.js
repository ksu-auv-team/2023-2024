const intervalTitle = "6 Second Interval"
let battery_voltage_chart = {}
let battery_amp_chart = {}
let motor_chart = {}
let servo_chart = {}
//------------------------------------------ CHART CONTROLS ------------------------------------------
function clearCharts() {
    battery_voltage_chart.chart.clearChart();
    battery_voltage_chart.chartData = null;
    battery_voltage_chart.chartOptions = null;

    battery_amp_chart.chart.clearChart();
    battery_amp_chart.chartData = null;
    battery_amp_chart.chartOptions = null;

    motor_chart.chart.clearChart();
    motor_chart.chartData = null;
    motor_chart.chartOptions = null;

    servo_chart.chart.clearChart();
    servo_chart.chartData = null;
    servo_chart.chartOptions = null;
    data_charts();

    toggleDialog();
}

function saveCharts() {
    // Check if user left a comment when saving charts
    let userChartComment = "";
    if(dialogOptions.saveCharts.textArea) {
        if(document.getElementById('dialog_text_area').value) {
            userChartComment = "Comments: " + document.getElementById('dialog_text_area').value;
        }
    }


    let chartsHTML = "";
    let chartDivs = document.querySelectorAll('.chart_container');
    chartDivs.forEach((div) => {
        chartsHTML += div.outerHTML;
    })
    const date = getDateTime();

    let htmlContent = `<!DOCTYPE html><html lang="en">
        <head>
            <title>KSU AUV Recorded Data</title>
            <header style="width: 100vw; color: white; text-align: center">
                <h1>AUV Data saved at ${date.month} ${date.day}, ${date.year} at ${date.hours}:${date.minutes}${date.time_period}</h1>
                <p style="font-size: 1.5rem">${userChartComment}</p>
            </header>
        </head>
        <body style="display: flex; flex-wrap: wrap; background-color: #121212; gap: 1rem; justify-content: center;">`;
    htmlContent += chartsHTML;
    htmlContent += '</body></html>';

    let htmlBlob = new Blob([htmlContent], {type: 'text/html'});
    const download_link = document.createElement('a');
    download_link.href = URL.createObjectURL(htmlBlob);
    download_link.download = `${date.year} ${date.month} ${date.day}, ${date.hours}_${date.minutes}_${date.time_period} AUV Data Charts`;
    download_link.click();

    toggleDialog();
}