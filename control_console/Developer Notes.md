# Developer Notes

_Contact: Discord > Sergio SA_

External Libraries: Google Charts, Axios, VueJS & VueX

## Structure

- 3 Pages | Stream - Data Monitoring - Log ✔
- Header ✔
- Stream
  - Zed Camera Stream - _Wait for completion of server_
  - Batteries ✔
- Notification Center
  - Create functions to create notifications and remove them ✔
- Data Monitoring
  - Batteries - Motors - Servos ✔
  - Visual graphs over time ✔
  - Possibly use a diagram of sub to represent components
  - When saving, also save the data as an excel or similar chart on the html ✔
    - Try passing the data objects instead and reconstruct the charts with JS ✔
- Log
  - TimeDates ✔
  - Highlight Lines ✔
  - Allow Save ✔
  - Create functions to make message logs. Also include notification center messages ✔

### Return Back To

- Onload Listener 
  - Send Get requests on load
    - Useful if user refreshes page or auv is already powered on
    - Do nothing if there is no response from server
- AUV Power Switch
    - Send POST request to turn on/off sub & wait for response
    - When powering off, use dialog to ask if user wants to turn off sub
- Update Data
  - Send GET/POST request to server to get new data
- Log
  - Automatically scroll if needed
  - Allow user to pause automatic scrolling
- HTTP Requests
  - Store.js errorHandler
  - Use global errorMessage state variable for output
  - Create another function for notification & log, then set state variables to null