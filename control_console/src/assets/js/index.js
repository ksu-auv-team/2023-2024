document.addEventListener("DOMContentLoaded", function() {
// -------------------------------------------- Call Anything That Needs To Be Activated On Page Load Here --------------------------------------------
//     createBatteryElements();
//     createMotorElements();
//     createServoElements();
//     initChartProperties();

    // //Google Chart API
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(data_charts); //Call main chart initializer
})
//---------------------------------------------- GLOBAL VARIABLES  | GLOBAL FUNCTIONS ----------------------------------------------

//     -------------------------------------------- GLOBAL VARIABLES  |  START POWER BUTTON --------------------------------------------

function power_on_graphs() {
    if(!initial_power) {
        timer();
    }
}

//---------------------------------------------- END POWER BUTTON | START DIALOG OPTIONS -----------------------------------------------

//--------------------------------------- END POWER BUTTON | START NOTIFICATION CENTER ----------------------------------------

//--------------------------------------- END NOTIFICATION CENTER  |  START BATTERY DATA  ---------------------------------------

//     -------------------------------------------- END BATTERY DATA  |  START MOTOR DATA  --------------------------------------------


//     -------------------------------------------- END MOTOR DATA  |  START SERVO DATA  --------------------------------------------

// ------------------------ END SERVO DATA | START LOG PAGE  ----------------------------


//  -----------------------------------------START DATA DEMO -----------------------------------------




const intervalTitle = "Time"
const chart_colors = {
    0: {color: '#0000FF'},
    1: {color: '#FF0000'},
    2: {color: '#FFFF00'},
    3: {color: '#008000'},
    4: {color: '#FF00FF'},
    5: {color: '#00FFFF'},
    6: {color: '#FFA500'},
    7: {color: '#800080'}

}
let battery_voltage_chart = {}
let battery_amp_chart = {}
let motor_chart = {}
let servo_chart = {}

function initChartProperties() {
}
function data_charts() {
    initChart([battery_voltage_chart, battery_amp_chart, motor_chart, servo_chart]);
    chartSelections([battery_voltage_chart, battery_amp_chart, motor_chart, servo_chart]);
}

function initChart(charts) {
    charts.forEach((chart) => {
        const computedSize = window.getComputedStyle(document.getElementById('example_chart_size'));
        chart.chartData = new google.visualization.DataTable();
        for (let i = 0; i <= chart.column_count; i++) {
            if(i === 0) { chart.chartData.addColumn('number', chart.y_title) } else { chart.chartData.addColumn('number', chart.subject + i); }
        }
        chart.chartOptions = {
            backgroundColor: "#343434",
            title: chart.title,
            titleTextStyle: {color: "white"},
            legend: {textStyle: {color: "#FFFFFF"}, position: 'in'},
            hAxis: {title: intervalTitle,titleTextStyle: {color: "white"}, textStyle: {color: "white"}, baselineColor: "white", gridLines: {color: "#FFFFFF"}},
            vAxis: {title: chart.y_title, titleTextStyle: {color: "white"}, textStyle: {color: "white"}, minValue: 0, maxValue: (chart.y_max+10)},
            width: parseInt(computedSize.getPropertyValue('width')),
            height: parseInt(computedSize.getPropertyValue('height')),
            chartArea: {width: '70%', height: '85%', left: 70, right: 25},
            explorer: {
                actions: ['dragToZoom', 'rightClickToReset'],
                axis: 'horizontal',
                keepInBounds: true,
                maxZoomIn: 10
            },
            series: chart_colors
        }

        chart.chart = new google.visualization.AreaChart(document.getElementById(chart.container_id));
        chart.chart.draw(chart.chartData, chart.chartOptions);
    })
}
function updateCharts(charts) {
    charts.forEach((chart) => {
        let newInsert = [timeActive];
        chart.unit_reference.forEach(function(unit) {
            newInsert.push(unit[chart.reference_unit]);
        });
        chart.chartData.addRow(newInsert);
        chart.chart.draw(chart.chartData, chart.chartOptions);
    })
}

function chartSelections(charts) {
    charts.forEach((chart) => {
        google.visualization.events.addListener(chart.chart, 'click', function () {
            let series = JSON.parse(JSON.stringify(chart_colors));
            setTimeout(() => {
                let selectedItem = chart.chart.getSelection();
                if(!selectedItem) {
                    chart.chartOptions.series = series;
                    chart.chart.draw(chart.chartData, chart.chartOptions);
                    return;
                }
                if(!chart.selectionBool) {
                    if (selectedItem.length > 0) {
                        let columnIndex = selectedItem[0].column - 1;
                        if (columnIndex != null) {
                            for (let i = 0; i < chart.chartData.getNumberOfColumns(); i++) {
                                if (i !== columnIndex) {
                                    series[i] = {color: 'transparent'};
                                }
                            }
                            chart.chartOptions.series = series;
                            chart.chart.draw(chart.chartData, chart.chartOptions);
                        }
                        chart.selectionBool = true;
                    }
                } else {
                    chart.chartOptions.series = series;
                    chart.chart.draw(chart.chartData, chart.chartOptions);
                    chart.selectionBool = false;
                }
            }, 40)
        });
    })
}

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