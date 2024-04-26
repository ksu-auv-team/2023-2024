# Ground Control Web Application Documentation

Contact: Sergio • AUV Discord: Sergio SA

## External Libraries
- VueJS : Web Development & Efficiency
- VueX : Global State Variables
- Axios : HTTP Request Handler
  - See [Axios]
- Google ChartsJS : Data Visualization
  - Uses Area Chart from Google ChartsJS
  - [Google Area Chart Documentation][GoogleAreaChart]

## Project Setup (For Development)
``` cd control_console ``` in terminal first

Download Project Dependencies :
``` npm install ```

Build Project for Production :
``` npm run build ```

Display Web Application :
``` npm run serve ```

### Regarding Building & Serving
Access `vue.config.js`

If you want to build for the Flask app, comment the following out.
Otherwise, it will output to the `dist` directory within `control_console`
Similarly, if you want to serve the web application from the project, comment this out.
 
    outputDir: path.resolve(__dirname, '../templates'),
    assetsDir: '../static',

## Project Structure and Functions Overview

---
### App.vue
- Main Entry Point
- Holds Header and defines area for pages in `<router-view>`


- import connection from "@/server/connection"  :  __HTTP Requests__
- import {useStore} from "vuex"  : __Handling Global State Variables__
- import {onMounted, reactive, ref, watchEffect} from "vue" : __Vue Objects__

#### dialogFunctions | Function
- ___Accepts a function___
- Called from dialog box only
- Executes given function and closes the dialog

#### dialogOptions | Constant
- Defines different options for displaying the dialog box when called

#### getActiveSession | Async Function | Can Disregard
- For my personal data testing

#### getDateTime | Function
- Helper function for retrieving date and time

#### onMounted | Vue Object
- Basically a function that executes immediately after the page loads

#### powerButton | Async Function
- Fetches state of power and updates the state variable and button display

#### saveCharts | Function
- Creates an HTML file.
- Saves visual representations of current data.
- Saves log
- Uses _getDateTime_ helper function

#### startDataDemo & stopDataDemo | Functions
- Used for development to test application with dummy data

#### toggleDialog | Function
- Displays or removes dialog box & uses dialogOptions to interact with user

#### updatePowerButton | Function
- Updates power button if they are not matching

#### watchEffect & setTimeout | Vue Object
- Sends notifications if battery is low

---
### Main.js

- Initializes Vue Application
- Attaches Router : For changing pages
- Attaches Store : For Global State Variables
- Imports style.css
  - Only one css file
  - Target areas seperated by comments
  - Web Application not responsive to different devices

---
### Store.js
This is where the global state variables are held

This allows me to update content on the page without creating functions to update or store data

Automatically updates content wherever called
- HTML: {{ store.state.<global variable\> }}
- JavaScript: const variable = store.state.<global variable\>

Note that to be truly reactive, store.state must be paired with Vue's `reactive` object

    const store = useStore();
    const state = reactive(store.state);
    const batteries = ref(state.batteries);

- Imports Google Charts API
- Imports createStore from Vuex : For Global State Variables

#### addChartData | Function
- Defines different data charts
- Does not accept parameters
    - Instead, uses current state of data
    - This function is called by whenever data changes
- Interacts with Google Charts Data Objects
    - state variable: <chart_name>.chart is the main Google chart object
    - state variable: <chart_name>.chartData is the Google chart data object
        - Similar to an array, but uses special functions to interact with
        - See [Google Area Chart Documentation][GoogleAreaChart]
    - Updates charts if they exist on the web page at the moment

#### clearChartData | Function
- Deletes all Google Chart data from state variables
- Called by user when warned with the dialog

#### getDateTime | Function
- Helper function for retrieving date and time

#### newLog | Function
- Accepts message (String)
- Uses `getDateTime` helper function
- Adds the log message to the log state variable array

#### newNotification | Function
- Accepts message (string), severity (string), & highlighted (boolean)
    - Severity interacts with CSS as a class to update background color
- Uses highlighted to highlight as a class log message with CSS
- Automatically clears notifications after 10,000ms (10s)

#### store | VueX Object
- Contains state variables and related functions
    - state: Global State Variables
    - mutations: Related Functions
      - All mutations take in `state` as a parameter to interact with variables and other functions

#### togglePower | Function
- Updates power state variable
- Uses getDateTime helper function
- Creates a notification

___
### router > index.js
- For VueJS
- Defines routes and corresponding files for page links

___
### server > api.js
- Imports axios to handle HTTP requests and returns an axios object
- See [Axios]

### server > connection.js
- Imports axios object from api.js
- Defines my personal database and Orin's URL
- Defines and exports HTTP request functions
- See [Axios]


    await connection.<http function>(parameters if any)

___
### views > streamView.vue
- First page to load
- Displays stream, battery data areas, and notification center
  - uses Vue's `v-for` to create each battery display based on state variable: batteries

#### batteryBorderColor | Function
- Updates battery border color based on current battery life
- Reactive function that interacts with state variables

___
### views > dataView.vue
- Displays batteries, motors, servos, & charts
    - uses Vue's `v-for` to create each data display based on state their variables
- Defines where Google Charts will be located

#### batteryBorderColor | Function
- Updates battery border color based on current battery life
- Reactive function that interacts with state variables

#### chart_colors | Constant
- Defines colors for each data object. (Up to 8 objects)

#### chartSelections | Function
- Iterates over array of chart objects to modify them
- Creates click listeners for charts to select and highlight data

#### drawCharts | Function
- Iterates over array of chart objects and initializes all of them
- Defines appropriate chart size
- Draws charts following [Google Charts documentation][GoogleAreaChart]

#### handleClear | Function
- Responds to `Clear Charts` button
- Toggles dialog to interact with user
    - See `toggleDialog` in `app.vue`

#### handleSave | Function
- Responds to `Save Charts` button
- Toggles dialog to interact with user
    - See `toggleDialog` in `app.vue`

#### initCharts | Function
- Main Function to initialize charts
- Calls drawCharts() and chartSelections()
  - Inputs charts from state variables as an array for a parameter

#### onMounted | Vue Object
- Basically a function that executes immediately after the page loads
- Loads Google Chart Api


___
### views > logView.vue
- Displays log
- Uses Vue's `v-for` to dynamically display state variable log array

#### highlight_message | Function
- Used to highlight or un-highlight log messages when clicked

[//]: # (Links Area)
[GoogleAreaChart]: https://developers-dot-devsite-v2-prod.appspot.com/chart/interactive/docs/gallery/areachart
[Axios]: https://axios-http.com/