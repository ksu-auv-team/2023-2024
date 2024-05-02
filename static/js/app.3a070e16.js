(function(){"use strict";var t={226:function(t,e,a){var r=a(751),o=a(641),n=a(33),i=a.p+"../static/img/power-off.d3ba7341.svg",s=a(250),l=t=>s.A.create({baseURL:t});const c=l("https://sanchezalvarez.dev/api"),d=l("http://192.168.1.16:5000");var h={togglePower(){return c.post("/auv/power/toggle")},checkActiveSession(){return c.get("/auv/log/checkSession")},testAPI(){return d.get("/testAPI")},handlePower(){return d.get("/handlePower")},fetchPower(){return d.get("/fetchPower")},getInputData(){return d.get("/get_input_data")}},u=a.p+"../static/img/power-on.1bfc76ed.svg",m=a.p+"../static/img/power-wait.2eb41256.svg",g=a.p+"../static/img/power-error.111780f5.svg",p=a(278),v=a(953);const _=["disabled"],f=["disabled"],y=(0,o.Lk)("img",{id:"power_svg",src:i,alt:"Power OFF"},null,-1),w=[y],b=(0,o.Lk)("span",{id:"example_chart_size"},null,-1),k=(0,o.Lk)("dialog",{id:"dialog"},[(0,o.Lk)("div",{id:"dialog_content"})],-1);var C={__name:"App",setup(t){const e=(0,p.Pj)(),r=(0,v.Kh)(e.state),s=(0,v.KR)(null);let l;const c=(0,v.KR)(r.batteries),d=(0,v.KR)(!1),y=(0,v.KR)(!1),C=(0,v.KR)(!1),E=async()=>{y.value=!0;try{const t=new Promise(((t,e)=>{setTimeout((()=>{e(new Error("404"))}),4e3)})),a=h.testAPI(),r=await Promise.race([a,t]);r.data.hasOwnProperty("errorCode")?await e.dispatch("relayErrors",{errorCode:r.data.errorCode,errorMessage:r.data.errorMessage,officialErrorMessage:r.data.officialErrorMessage}):e.commit("newNotification",{message:"Connection OK"})}catch(t){await e.dispatch("handleErrors",t)}finally{y.value=!1}},F=async()=>{C.value=!0;const t=document.getElementById("power_svg");t.src=m,t.alt="Waiting";try{const a=new Promise(((t,e)=>{setTimeout((()=>{e(new Error("404"))}),4e3)})),o=h.handlePower(),n=await Promise.race([o,a]);if(n.data.hasOwnProperty("errorCode"))await e.dispatch("relayErrors",{errorCode:n.data.errorCode,errorMessage:n.data.errorMessage,officialErrorMessage:n.data.officialErrorMessage});else{const a=n.data.status;let o;a?(t.src=u,t.alt="Power ON",D.value=()=>$("powerAUV"),L(),setTimeout((()=>{d.value=!0}),5500)):(t.src=i,t.alt="Power OFF",D.value=()=>F(),O(),d.value=!1),o=!1===r.power?"OFF":"ON",a!==r.power?e.commit("togglePower"):e.commit("newNotification",{message:`AUV ${o}`,highlighted:!0})}}catch(a){await e.dispatch("handleErrors",a),t.src=g,t.alt="Power OFF"}finally{C.value=!1}},D=(0,v.KR)(F),x=async()=>{try{const t=new Promise(((t,e)=>{setTimeout((()=>{e(new Error("404"))}),4e3)})),a=h.fetchPower(),r=await Promise.race([a,t]);if(r.data.hasOwnProperty("errorCode"))await e.dispatch("relayErrors",{errorCode:r.data.errorCode,errorMessage:r.data.errorMessage,officialErrorMessage:r.data.officialErrorMessage});else{const t=document.getElementById("power_svg");!0===r.data.status&&(t.src=u,t.alt="Power ON",L(),setTimeout((()=>{d.value=!0}),5500),e.commit("togglePower"),e.commit("newNotification",{message:`Fetched Power: ${e.state.power}`,highlighted:!0}))}}catch(t){await e.dispatch("handleErrors",t)}};(0,o.nT)((()=>{d.value&&c.value.forEach((t=>{t.voltage<=15&&e.commit("newNotification",{message:`Battery ${t.id} Low`,severity:"notification_alert"})}))}));const L=()=>{l=setInterval((function(){e.state.batteries.forEach((function(t){t.voltage=parseFloat((50*Math.random()).toFixed(2)),t.amps=parseFloat((30*Math.random()).toFixed(2))})),e.state.motors.forEach((function(t){t.pwm=Math.floor(100*Math.random())+1})),e.state.servos.forEach((function(t){t.pwm=Math.floor(100*Math.random())+1})),e.commit("addChartData")}),5e3),console.log("Timeout Started")},O=()=>{clearInterval(l),console.log("Timeout Stopped")};function A(){const t=new Date,e=["January","February","March","April","May","June","July","August","September","October","November","December"],a=t.getHours()<12?"am":"pm",r=e[t.getMonth()],o=t.getDate(),n=t.getFullYear();let i=t.getHours(),s=t.getMinutes();return i>12&&(i-=12),0===i&&(i=12),s<10&&(s=`0${s}`),{month:r,day:o,year:n,hours:i,minutes:s,time_period:a}}const M={clearCharts:{title:"Clear Charts",message:"Are you sure you want to clear the charts? All data related to the charts will be lost.",buttons:["Proceed"],button_functions:[e.commit.bind(e,"clearChartData")],textArea:!1,textAreaFunctionIndex:null,textAreaMessage:null},saveCharts:{title:"Save Charts",message:"Would you like to add any comments? Comments will appear at the top of the page.",buttons:["Proceed"],button_functions:[S],textArea:!0,textAreaFunctionIndex:0,textAreaMessage:null},powerAUV:{title:"Power Off AUV",message:"Are you sure you want to power of the AUV?",buttons:["Proceed"],button_functions:[F],textArea:!1,textAreaFunctionIndex:null,textAreaMessage:null}},P=(0,v.KR)(!1);function $(t){const e=document.getElementById("dialog"),a=document.getElementById("dialog_content");let r;if(P.value)e.style.display="none",P.value=!1,a.innerHTML="";else{switch(t){case"clear_charts":r=M.clearCharts;break;case"save_charts":r=M.saveCharts;break;case"powerAUV":r=M.powerAUV;break;default:break}if(r){const t=document.createElement("h1");t.innerText=r.title;const e=document.createElement("p");let o;e.innerText=r.message,r.textArea&&(o=document.createElement("textarea"),o.id="dialog_text_area");const n=document.createElement("div");n.classList.add("dialog_buttons");let i=document.createElement("button");i.innerText="Cancel",i.onclick=$,n.appendChild(i);for(let a=0;a<r.buttons.length;a++){let t=document.createElement("button");t.innerText=r.buttons[a],t.onclick=()=>I(r.button_functions[a]),n.appendChild(t)}n.id="dialog_buttons",a.appendChild(t),a.appendChild(e),r.textArea&&a.appendChild(o),a.appendChild(n)}e.style.display="flex",P.value=!0}}function I(t){t(),$()}function S(){let t="";M.saveCharts.textArea&&document.getElementById("dialog_text_area").value&&(t="Comments: "+document.getElementById("dialog_text_area").value);let e="",a=document.querySelectorAll(".chart_container");a.forEach((t=>{e+=t.outerHTML}));let o="<hr><div style='padding: 0 2rem'> <h2>Log</h2>";r.log.forEach((t=>{if(!0===t.highlighted){let e="<p style='background-color: #343434; font-size: 1.5rem'>"+t.message+" <span style='color: #E2A300; font-size: 2rem'>&bull;</span></p>";o+=e}else{let e="<p style='font-size: 1.5rem'>"+t.message+"</p>";o+=e}})),o+=" </div>";const n=A();let i=`<!DOCTYPE html><html lang="en">\n        <head>\n            <title>KSU AUV Recorded Data</title>\n            <header style="width: 100vw; color: white; text-align: center">\n                <h1>AUV Data saved at ${n.month} ${n.day}, ${n.year} at ${n.hours}:${n.minutes}${n.time_period}</h1>\n                <p style="font-size: 1.25rem">${t}</p>\n            </header>\n        </head>\n        <body style="background-color: #121212; color: #D1D1D1">\n            <div style="display: flex; flex-wrap: wrap; gap: 1rem; justify-content: center;">`;i+=e,i+="</div><div>",i+=o,i+="</div></body></html>";let s=new Blob([i],{type:"text/html"});const l=document.createElement("a");l.href=URL.createObjectURL(s),l.download=`${n.year} ${n.month} ${n.day}, ${n.hours}_${n.minutes}_${n.time_period} AUV Data Charts.html`,l.click(),$(),$()}return(0,o.sV)((()=>{x()})),(t,e)=>{const r=(0,o.g2)("router-link"),i=(0,o.g2)("router-view");return(0,o.uX)(),(0,o.CE)(o.FK,null,[(0,o.Lk)("header",{style:(0,n.Tr)({backgroundImage:`url(${a(869)}`})},[(0,o.Lk)("nav",null,[(0,o.bF)(r,{to:"/"},{default:(0,o.k6)((()=>[(0,o.eW)("Stream")])),_:1}),(0,o.bF)(r,{to:"/data"},{default:(0,o.k6)((()=>[(0,o.eW)("Data Monitoring")])),_:1}),(0,o.bF)(r,{to:"/log"},{default:(0,o.k6)((()=>[(0,o.eW)("Log")])),_:1})]),(0,o.Lk)("div",null,[(0,o.Lk)("button",{id:"test_connection",onClick:E,disabled:y.value},"Test Connection",8,_),(0,o.Lk)("button",{id:"power_button",onClick:e[0]||(e[0]=(...t)=>D.value&&D.value(...t)),disabled:C.value},w,8,f)])],4),(0,o.bF)(i,{ref_key:"currentView",ref:s,onToggleDialog:$},null,512),b,k],64)}}};const E=C;var F=E,D=a(220),x=a.p+"../static/img/disconnected.58c32818.svg",L=a.p+"../static/img/depth_ex.fbd05571.jpg";const O={class:"active",id:"stream_main"},A={id:"stream"},M=(0,o.Fv)('<div class="video_stream"><div class="stream_header"><h2 class="camera_title">Regular View</h2></div><hr><div class="stream_container"><img id="camera_feed_1" src="'+x+'" alt="Regular Stream"></div></div>',1),P={class:"data_container",id:"battery_data"},$=["id"],I={class:"voltage"},S={class:"amps"},T=(0,o.Fv)('<div class="video_stream"><div class="stream_header"><h2 class="camera_title">Depth Sensor</h2></div><hr><div class="stream_container"><img id="camera_feed_2" src="'+L+'" alt="Depth Sensor"></div></div>',1),R={id:"notification_center"};var V={__name:"streamView",setup(t){const e=(0,p.Pj)(),a=(0,v.Kh)(e.state),r=(0,v.KR)(a.batteries),i=(0,v.KR)(a.notifications),s=t=>t.voltage>40?"Green":t.voltage>15?"Darkgoldenrod":t.voltage>0?"Red":"White";return(t,e)=>((0,o.uX)(),(0,o.CE)("main",O,[(0,o.Lk)("div",A,[M,(0,o.Lk)("div",P,[((0,o.uX)(!0),(0,o.CE)(o.FK,null,(0,o.pI)(r.value,((t,e)=>((0,o.uX)(),(0,o.CE)("div",{key:t.id,id:"battery_"+(e+1),class:"battery",style:(0,n.Tr)({borderColor:s(t)})},[(0,o.Lk)("h2",null,"Battery "+(0,n.v_)(t.id),1),(0,o.Lk)("p",null,[(0,o.eW)("Voltage: "),(0,o.Lk)("span",I,(0,n.v_)(t.voltage)+"V",1)]),(0,o.Lk)("p",null,[(0,o.eW)("Amps: "),(0,o.Lk)("span",S,(0,n.v_)(t.amps)+"A",1)])],12,$)))),128))]),T]),(0,o.Lk)("div",R,[((0,o.uX)(!0),(0,o.CE)(o.FK,null,(0,o.pI)(i.value,((t,e)=>((0,o.uX)(),(0,o.CE)("p",{key:e,class:(0,n.C4)(t.severity)},(0,n.v_)(t.message),3)))),128))])]))}};const K=V;var U=K;const j={id:"data_main"},B=(0,o.Lk)("h1",null,"Data Monitoring",-1),N={id:"data_monitoring"},W={class:"data_container",id:"battery_data_2"},X=["id"],z=(0,o.Lk)("h2",null,"Battery",-1),J={class:"voltage"},H={class:"amps"},Y={class:"data_container",id:"motor_data"},q=["id"],G=(0,o.Lk)("h2",null,"Motor 1",-1),Z={class:"data_container",id:"servo_data"},Q=["id"],tt=(0,o.Lk)("h2",null,"Servo 1",-1),et=(0,o.Lk)("h1",null,"Data Charts",-1),at=(0,o.Fv)('<div id="data_charts"><div class="chart_container"><div id="battery_voltage"></div></div><div class="chart_container"><div id="battery_amp"></div></div><div class="chart_container"><div id="motor_pwm"></div></div><div class="chart_container"><div id="servo_pwm"></div></div></div>',1);var rt={__name:"dataView",emits:["toggleDialog"],setup(t,{emit:e}){const a=(0,p.Pj)(),r=e,i=(0,v.Kh)(a.state),s=(0,v.KR)(i.batteries),l=(0,v.KR)(i.motors),c=(0,v.KR)(i.servos),d=(0,v.KR)(i.charts.battery_voltage_chart),h=(0,v.KR)(i.charts.battery_amp_chart),u=(0,v.KR)(i.charts.motor_chart),m=(0,v.KR)(i.charts.servo_chart),g=t=>t.voltage>40?"Green":t.voltage>15?"Darkgoldenrod":t.voltage>0?"Red":"White",_={0:{color:"#0000FF"},1:{color:"#FF0000"},2:{color:"#FFFF00"},3:{color:"#008000"},4:{color:"#FF00FF"},5:{color:"#00FFFF"},6:{color:"#FFA500"},7:{color:"#800080"}};function f(){y([d.value,h.value,u.value,m.value]),w([d.value,h.value,u.value,m.value])}function y(t){const e=window.getComputedStyle(document.getElementById("example_chart_size"));t.forEach((t=>{if(null===t.chartData){t.chartData=new google.visualization.DataTable;for(let e=0;e<=t.column_count;e++)0===e?t.chartData.addColumn("number",t.y_title):t.chartData.addColumn("number",t.subject+e)}t.chartOptions={backgroundColor:"#343434",title:t.title,titleTextStyle:{color:"white"},legend:{textStyle:{color:"#FFFFFF"},position:"in"},hAxis:{title:t.x_title,titleTextStyle:{color:"white"},textStyle:{color:"white"},baselineColor:"white",gridLines:{color:"#FFFFFF"}},vAxis:{title:t.y_title,titleTextStyle:{color:"white"},textStyle:{color:"white"},minValue:0,maxValue:t.y_max+10},width:parseInt(e.getPropertyValue("width")),height:parseInt(e.getPropertyValue("height")),chartArea:{width:"70%",height:"85%",left:70,right:25},explorer:{actions:["dragToZoom","rightClickToReset"],axis:"horizontal",keepInBounds:!0,maxZoomIn:10},series:_},t.chart=new google.visualization.AreaChart(document.getElementById(t.container_id)),t.chart.draw(t.chartData,t.chartOptions)}))}function w(t){t.forEach((t=>{google.visualization.events.addListener(t.chart,"click",(function(){let e=JSON.parse(JSON.stringify(_));setTimeout((()=>{let a=t.chart.getSelection();if(!a)return t.chartOptions.series=e,void t.chart.draw(t.chartData,t.chartOptions);if(t.selectionBool)t.chartOptions.series=e,t.chart.draw(t.chartData,t.chartOptions),t.selectionBool=!1;else if(a.length>0){let r=a[0].column-1;if(null!=r){for(let a=0;a<t.chartData.getNumberOfColumns();a++)a!==r&&(e[a]={color:"transparent"});t.chartOptions.series=e,t.chart.draw(t.chartData,t.chartOptions)}t.selectionBool=!0}}),40)}))}))}function b(){r("toggleDialog","clear_charts")}function k(){r("toggleDialog","save_charts")}return(0,o.sV)((()=>{google.charts.load("current",{packages:["corechart"]}),google.charts.setOnLoadCallback(f)})),(t,e)=>((0,o.uX)(),(0,o.CE)("main",j,[(0,o.Lk)("section",null,[B,(0,o.Lk)("div",N,[(0,o.Lk)("div",W,[((0,o.uX)(!0),(0,o.CE)(o.FK,null,(0,o.pI)(s.value,((t,e)=>((0,o.uX)(),(0,o.CE)("div",{key:t.id,id:"battery_"+(e+1),class:"battery",style:(0,n.Tr)({borderColor:g(t)})},[z,(0,o.Lk)("p",null,[(0,o.eW)("Voltage: "),(0,o.Lk)("span",J,(0,n.v_)(t.voltage)+"V",1)]),(0,o.Lk)("p",null,[(0,o.eW)("Amps: "),(0,o.Lk)("span",H,(0,n.v_)(t.amps)+"A",1)])],12,X)))),128))]),(0,o.Lk)("div",Y,[((0,o.uX)(!0),(0,o.CE)(o.FK,null,(0,o.pI)(l.value,((t,e)=>((0,o.uX)(),(0,o.CE)("div",{key:t.id,id:"motor_"+(e+1),class:"motor"},[G,(0,o.Lk)("p",null,"pwm: "+(0,n.v_)(t.pwm)+"%",1)],8,q)))),128))]),(0,o.Lk)("div",Z,[((0,o.uX)(!0),(0,o.CE)(o.FK,null,(0,o.pI)(c.value,((t,e)=>((0,o.uX)(),(0,o.CE)("div",{key:t.id,id:"servo_"+(e+1),class:"servo"},[tt,(0,o.Lk)("p",null,"pwm: "+(0,n.v_)(t.pwm)+"%",1)],8,Q)))),128))])])]),(0,o.Lk)("section",null,[et,(0,o.Lk)("div",{id:"chart_controls"},[(0,o.Lk)("button",{onClick:b},"Clear Charts"),(0,o.Lk)("button",{onClick:k},"Save Charts")]),at])]))}};const ot=rt;var nt=ot,it=a.p+"../static/img/scroll_pause.6e68bedc.svg";const st={id:"log_main"},lt=(0,o.Lk)("button",{id:"log_scroll_control",onclick:"control_scroll()"},[(0,o.Lk)("img",{src:it,alt:"Scroll Control"})],-1),ct=["id","onClick"],dt=(0,o.Lk)("span",{class:"highlight_indicator"},"•",-1);var ht={__name:"logView",setup(t){const e=(0,p.Pj)(),a=(0,v.Kh)(e.state),r=(0,v.KR)(a.log),i=t=>{const e=document.getElementById(t);e.classList.contains("marked")?e.classList.remove("marked"):e.classList.add("marked");const a=t.substring(4);r.value[a].highlighted=!0!==r.value[a].highlighted};return(t,e)=>((0,o.uX)(),(0,o.CE)("main",st,[lt,((0,o.uX)(!0),(0,o.CE)(o.FK,null,(0,o.pI)(r.value,(t=>((0,o.uX)(),(0,o.CE)("p",{key:r.value.indexOf(t),id:"log_"+r.value.indexOf(t),class:(0,n.C4)(["log_message",{marked:t.highlighted}]),onClick:e=>i("log_"+r.value.indexOf(t))},[(0,o.eW)((0,n.v_)(t.message)+" ",1),dt],10,ct)))),128))]))}};const ut=ht;var mt=ut;const gt=[{path:"/",name:"AUV Stream",component:U},{path:"/data",name:"AUV Data",component:nt},{path:"/log",name:"AUV Log",component:mt}],pt=(0,D.aE)({history:(0,D.LA)("/"),routes:gt});var vt=pt;function _t(){const t=new Date,e=["January","February","March","April","May","June","July","August","September","October","November","December"],a=t.getHours()<12?"am":"pm",r=e[t.getMonth()],o=t.getDate(),n=t.getFullYear();let i=t.getHours(),s=t.getMinutes();return i>12&&(i-=12),0===i&&(i=12),s<10&&(s=`0${s}`),{month:r,day:o,year:n,hours:i,minutes:s,time_period:a}}google.charts.load("current",{packages:["corechart"]});const ft=(0,p.y$)({state:{currentError:{errorCode:null,errorMessage:null,officialErrorMessage:null},power:!1,batteries:[{id:1,voltage:0,amps:0},{id:2,voltage:0,amps:0},{id:3,voltage:0,amps:0},{id:4,voltage:0,amps:0}],motors:[{id:1,pwm:0},{id:2,pwm:0},{id:3,pwm:0},{id:4,pwm:0},{id:5,pwm:0},{id:6,pwm:0},{id:7,pwm:0},{id:8,pwm:0}],servos:[{id:1,pwm:0},{id:2,pwm:0}],chartIteration:1,charts:{battery_voltage_chart:{chart:null,chartData:null,chartOptions:null,subject:"Battery",column_count:4,title:"Battery Voltage",x_title:"Per Fetch Iteration",y_title:"Voltage",y_max:50,container_id:"battery_voltage",unit_reference:0,reference_unit:"voltage",selection_bool:!1},battery_amp_chart:{chart:null,chartData:null,chartOptions:null,subject:"Battery",column_count:4,title:"Battery Amps",x_title:"Per Fetch Iteration",y_title:"Amps",y_max:30,container_id:"battery_amp",unit_reference:0,reference_unit:"amps",selection_bool:!1},motor_chart:{chart:null,chartData:null,chartOptions:null,subject:"Motor",column_count:8,title:"Motor PWM",x_title:"Per Fetch Iteration",y_title:"PWM",y_max:100,container_id:"motor_pwm",unit_reference:0,reference_unit:"pwm",selection_bool:!1},servo_chart:{chart:null,chartData:null,chartOptions:null,subject:"Servo",column_count:2,title:"Servo PWM",x_title:"Per Fetch Iteration",y_title:"PWM",y_max:100,container_id:"servo_pwm",unit_reference:0,reference_unit:"pwm",selection_bool:!1}},notifications:[],log:[]},mutations:{togglePower(t){t.power=!t.power;const e=t.power?"ON":"OFF";t.notifications.push({message:`AUV ${e}`,severity:null});const a=_t(),r=`${a.month} ${a.day}, ${a.hours}:${a.minutes}${a.time_period}`,o=`${r} | AUV ${e}`;t.log.push({message:o,highlighted:!0}),setTimeout((()=>{t.notifications.length>0&&t.notifications.shift()}),1e4)},newNotification(t,{message:e,severity:a,highlighted:r}){t.notifications.push({message:e,severity:a});const o=_t(),n=`${o.month} ${o.day}, ${o.hours}:${o.minutes}${o.time_period}`,i=`${n} | ${e}`;r?t.log.push({message:i,highlighted:r}):t.log.push({message:i,highlighted:!1}),setTimeout((()=>{t.notifications.length>0&&t.notifications.shift()}),1e4)},addChartData(t){const e=[t.charts.battery_voltage_chart,t.charts.battery_amp_chart,t.charts.motor_chart,t.charts.servo_chart];e.forEach((t=>{if(null===t.chartData){t.chartData=new google.visualization.DataTable;for(let e=0;e<=t.column_count;e++)0===e?t.chartData.addColumn("number",t.y_title):t.chartData.addColumn("number",t.subject+e)}}));const a=[t.chartIteration],r=[t.chartIteration],o=[t.chartIteration],n=[t.chartIteration];t.chartIteration++,t.batteries.forEach((t=>{a.push(t.voltage),r.push(t.amps)})),t.charts.battery_voltage_chart.chartData.addRow(a),t.charts.battery_amp_chart.chartData.addRow(r),t.motors.forEach((t=>{o.push(t.pwm)})),t.charts.motor_chart.chartData.addRow(o),t.servos.forEach((t=>{n.push(t.pwm)})),t.charts.servo_chart.chartData.addRow(n),null!==t.charts.battery_voltage_chart.chart&&(t.charts.battery_voltage_chart.chart.draw(t.charts.battery_voltage_chart.chartData,t.charts.battery_voltage_chart.chartOptions),t.charts.battery_amp_chart.chart.draw(t.charts.battery_amp_chart.chartData,t.charts.battery_amp_chart.chartOptions),t.charts.motor_chart.chart.draw(t.charts.motor_chart.chartData,t.charts.motor_chart.chartOptions),t.charts.servo_chart.chart.draw(t.charts.servo_chart.chartData,t.charts.servo_chart.chartOptions))},clearChartData(t){const e=t.charts.battery_voltage_chart,a=t.charts.battery_amp_chart,r=t.charts.motor_chart,o=t.charts.servo_chart,n=[e,a,r,o];e.chartData=null,a.chartData=null,r.chartData=null,o.chartData=null,n.forEach((t=>{t.chartData=new google.visualization.DataTable;for(let e=0;e<=t.column_count;e++)0===e?t.chartData.addColumn("number",t.y_title):t.chartData.addColumn("number",t.subject+e);t.chart.draw(t.chartData,t.chartOptions)}))},newLog(t,e){const a=_t(),r=`${a.month} ${a.day}, ${a.hours}:${a.minutes}${a.time_period}`,o=`${r} | ${e}`;t.log.push({message:o,highlighted:!1})}},actions:{handleErrors({dispatch:t},e){e.request&&!e.response?t("relayErrors",{errorCode:"404",errorMessage:"Unable to contact ORIN",officialErrorMessage:e.message}):"404"===e.message?t("relayErrors",{errorCode:"404",errorMessage:"Unable to contact ORIN - Connection Severed",officialErrorMessage:null}):t("relayErrors",{errorCode:"500",errorMessage:"Unable to contact ORIN - Reason Unknown",officialErrorMessage:null})},relayErrors({commit:t},{errorCode:e,errorMessage:a,officialErrorMessage:r}){t("newNotification",{message:`Error Code: ${e} `,severity:"notification_alert",highlighted:!0}),t("newLog",`Error Message: ${a}`),null!==r&&t("newLog",`Official Error Message: ${r}`)}}});var yt=ft;(0,r.Ef)(F).use(vt).use(yt).mount("#app")},869:function(t,e,a){t.exports=a.p+"../static/img/banner.d118616e.png"}},e={};function a(r){var o=e[r];if(void 0!==o)return o.exports;var n=e[r]={exports:{}};return t[r](n,n.exports,a),n.exports}a.m=t,function(){var t=[];a.O=function(e,r,o,n){if(!r){var i=1/0;for(d=0;d<t.length;d++){r=t[d][0],o=t[d][1],n=t[d][2];for(var s=!0,l=0;l<r.length;l++)(!1&n||i>=n)&&Object.keys(a.O).every((function(t){return a.O[t](r[l])}))?r.splice(l--,1):(s=!1,n<i&&(i=n));if(s){t.splice(d--,1);var c=o();void 0!==c&&(e=c)}}return e}n=n||0;for(var d=t.length;d>0&&t[d-1][2]>n;d--)t[d]=t[d-1];t[d]=[r,o,n]}}(),function(){a.d=function(t,e){for(var r in e)a.o(e,r)&&!a.o(t,r)&&Object.defineProperty(t,r,{enumerable:!0,get:e[r]})}}(),function(){a.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(t){if("object"===typeof window)return window}}()}(),function(){a.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)}}(),function(){a.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})}}(),function(){a.p="/"}(),function(){var t={524:0};a.O.j=function(e){return 0===t[e]};var e=function(e,r){var o,n,i=r[0],s=r[1],l=r[2],c=0;if(i.some((function(e){return 0!==t[e]}))){for(o in s)a.o(s,o)&&(a.m[o]=s[o]);if(l)var d=l(a)}for(e&&e(r);c<i.length;c++)n=i[c],a.o(t,n)&&t[n]&&t[n][0](),t[n]=0;return a.O(d)},r=self["webpackChunkcontrol_console"]=self["webpackChunkcontrol_console"]||[];r.forEach(e.bind(null,0)),r.push=e.bind(null,r.push.bind(r))}();var r=a.O(void 0,[504],(function(){return a(226)}));r=a.O(r)})();
//# sourceMappingURL=app.3a070e16.js.map