<template>
  <main id="data_main">
    <section>
      <h1>Data Monitoring</h1>
      <div id="data_monitoring">
        <!--            4 batteries(voltage:float | amps: int)  |  8 Motors(pwm: int)  |  3 Servos(pwm: int)     -->
        <div class="data_container" id="battery_data_2">
          <div v-for="(battery, index) in batteries" :key="battery.id" :id="'battery_' + (index + 1)" class="battery" :style="{ borderColor: batteryBorderColor(battery) }">
            <h2>Battery</h2>
            <p>Voltage: <span class="voltage">{{ battery.voltage }}V</span></p>
            <p>Amps: <span class="amps">{{ battery.amps }}A</span></p>
          </div>
        </div>

<!--      ----------------------------------------  MOTORS ------------------------------------------>
        <div class="data_container" id="motor_data">
          <div v-for="(motors, index) in motors" :key="motors.id" :id="'motor_' + (index + 1)" class="motor">
            <h2>Motor 1</h2>
            <p>pwm: {{motors.pwm}}%</p>
          </div>
        </div>

<!--      -------------------------------------------  SERVOS  --------------------------------------------->
        <div class="data_container" id="servo_data">
          <div v-for="(servos, index) in servos" :key="servos.id" :id="'servo_' + (index + 1)" class="servo">
            <h2>Servo 1</h2>
            <p>pwm: {{servos.pwm}}%</p>
          </div>

        </div>
      </div>
    </section>

    <section>
      <h1>Data Charts</h1>
      <div id="chart_controls">
        <button @click="handleClear">Clear Charts</button>
        <button @click="toggleDialog('save_charts')">Save Charts</button>
      </div>
      <div id="data_charts">
        <div class="chart_container">
          <div id="battery_voltage"></div>
        </div>

        <div class="chart_container">
          <div id="battery_amp"></div>
        </div>

        <div class="chart_container">
          <div id="motor_pwm"></div>
        </div>

        <div class="chart_container">
          <div id="servo_pwm"></div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
  import {useStore} from "vuex";
  import {onMounted, reactive, ref} from "vue";
  const store = useStore();
  const emits = defineEmits(['toggleDialog']);

  const state = reactive(store.state);
  const batteries = ref(state.batteries);
  const motors = ref(state.motors);
  const servos = ref(state.servos);
  const batteryVChart = ref(state.charts.battery_voltage_chart)
  const batteryAChart = ref(state.charts.battery_amp_chart);
  const motorChart = ref(state.charts.motor_chart);
  const servoChart = ref(state.charts.servo_chart);


  const batteryBorderColor = (battery) => {
    if(battery.voltage > (50*.8)) { // Estimate Battery %. Given that max voltage is 50V
      return "Green";
    } else if(battery.voltage > (50*.3)) {
      return "Darkgoldenrod";
    } else if(battery.voltage > 0) {
      return "Red";
      // createNotification(`Battery ${battery_object.id} Low`, 1);
    } else {
      return "White";
    }
  };

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

  function initCharts() {
    drawCharts([batteryVChart.value, batteryAChart.value, motorChart.value, servoChart.value]);
    chartSelections([batteryVChart.value, batteryAChart.value, motorChart.value, servoChart.value]);
  }

  function drawCharts(charts) {
    const computedSize = window.getComputedStyle(document.getElementById('example_chart_size'));
    charts.forEach((chart) => {
      if(chart.chartData === null) {
        chart.chartData = new google.visualization.DataTable();
        for (let i = 0; i <= chart.column_count; i++) { //Add first row to create title and subject names
          if(i === 0) { chart.chartData.addColumn('number', chart.y_title) } else { chart.chartData.addColumn('number', chart.subject + i); }
        }
      }
      chart.chartOptions = {
        backgroundColor: "#343434",
        title: chart.title,
        titleTextStyle: {color: "white"},
        legend: {textStyle: {color: "#FFFFFF"}, position: 'in'},
        hAxis: {title: chart.x_title,titleTextStyle: {color: "white"}, textStyle: {color: "white"}, baselineColor: "white", gridLines: {color: "#FFFFFF"}},
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

  function handleClear() {
    emits('toggleDialog', 'clear_charts');
  }

  function clearCharts() {
    // Clear chart elements
    state.charts.battery_voltage_chart.chart.clearChart();
    state.charts.battery_amp_chart.chart.clearChart();
    state.charts.motor_chart.chart.clearChart();
    state.charts.servo_chart.chart.clearChart();

    // Clear chartData and chartOptions
    state.charts.battery_voltage_chart.chartData = null;
    state.charts.battery_voltage_chart.chartOptions = null;

    state.charts.battery_amp_chart.chartData = null;
    state.charts.battery_amp_chart.chartOptions = null;

    state.charts.motor_chart.chartData = null;
    state.charts.motor_chart.chartOptions = null;

    state.charts.servo_chart.chartData = null;
    state.charts.servo_chart.chartOptions = null;

    initCharts();

    // toggleDialog();
  }

  onMounted(() => {
    // //Google Chart API
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(initCharts); //Call main chart initializer
  })
</script>
