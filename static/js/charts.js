const intervalTitle = "6 Second Interval"
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
    battery_voltage_chart = {
        chart: 0,
        chartData: null,
        chartOptions: null,
        subject: "Battery",
        column_count: 4,
        title: "Battery Voltage",
        x_title: intervalTitle,
        y_title: "Voltage",
        y_max: 50,
        container_id: 'battery_voltage',
        unit_reference: batteries,
        reference_unit: 'voltage',
        selection_bool: false
    };

    battery_amp_chart = {
        chart: 1,
        chartData: null,
        chartOptions: null,
        subject: "Battery",
        column_count: 4,
        title: "Battery Amps",
        x_title: intervalTitle,
        y_title: "Amps",
        y_max: 30,
        container_id: 'battery_amp',
        unit_reference: batteries,
        reference_unit: 'amps',
        selection_bool: false
    };

    motor_chart = {
        chart: 2,
        chartData: null,
        chartOptions: null,
        subject: "Motor",
        column_count: 8,
        title: "Motor PWM",
        x_title: intervalTitle,
        y_title: "PWM",
        y_max: 100,
        container_id: 'motor_pwm',
        unit_reference: motors,
        reference_unit: 'pwm',
        selection_bool: false
    };

    servo_chart = {
        chart: 3,
        chartData: null,
        chartOptions: null,
        subject: 'Servo',
        column_count: 2,
        title: "Servo PWM",
        x_title: intervalTitle,
        y_title: "PWM",
        y_max: 100,
        container_id: 'servo_pwm',
        unit_reference: servos,
        reference_unit: 'pwm',
        selection_bool: false
    };
}
function data_charts(callback) {
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
function updateCharts(charts) { //Call this function per get/post request on .then
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