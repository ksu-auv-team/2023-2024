(function(){"use strict";var t={676:function(t,e,a){var r=a(751),o=a(641),n=a(33),l=a.p+"../static/img/power-off.d3ba7341.svg",i=a(250),c=t=>i.A.create({baseURL:t});const s=c("https://sanchezalvarez.dev/api"),h=c("http://192.168.1.16:5000");var u={fetchPower(){return s.get("/auv/power/fetch")},togglePower(){return s.post("/auv/power/toggle")},checkActiveSession(){return s.get("/auv/log/checkSession")},testAPI(){return h.get("/testAPI")}},d=(a.p,a(278)),m=a(953);const g=(0,o.Lk)("img",{id:"power_svg",src:l,alt:"Power OFF"},null,-1),p=[g],v=(0,o.Lk)("span",{id:"example_chart_size"},null,-1),_=(0,o.Lk)("dialog",{id:"dialog"},[(0,o.Lk)("div",{id:"dialog_content"})],-1);var y={__name:"App",setup(t){const e=(0,d.Pj)(),r=(0,m.Kh)(e.state),l=(0,m.KR)(null);const i=(0,m.KR)(r.batteries),c=(0,m.KR)(!1),s=async()=>{try{const t=await u.testAPI();t.data.hasOwnProperty("error")?console.log(t.data.error):console.log("Use the data somehow")}catch(t){t.request&&!t.response?console.log("Network connection error: ",t):console.log("Something went wrong: ",t)}};(0,o.nT)((()=>{c.value&&i.value.forEach((t=>{t.voltage<=15&&e.commit("newNotification",{message:`Battery ${t.id} Low`,severity:"notification_alert"})}))})),setTimeout((()=>{c.value=!0}),5500);function h(){const t=new Date,e=["January","February","March","April","May","June","July","August","September","October","November","December"],a=t.getHours()<12?"am":"pm",r=e[t.getMonth()],o=t.getDate(),n=t.getFullYear();let l=t.getHours(),i=t.getMinutes();return l>12&&(l-=12),0===l&&(l=12),i<10&&(i=`0${i}`),{month:r,day:o,year:n,hours:l,minutes:i,time_period:a}}const g={clearCharts:{title:"Clear Charts",message:"Are you sure you want to clear the charts? All data related to the charts will be lost.",buttons:["Proceed"],button_functions:[e.commit.bind(e,"clearChartData")],textArea:!1,textAreaFunctionIndex:null,textAreaMessage:null},saveCharts:{title:"Save Charts",message:"Would you like to add any comments? Comments will appear at the top of the page.",buttons:["Proceed"],button_functions:[w],textArea:!0,textAreaFunctionIndex:0,textAreaMessage:null}},y=(0,m.KR)(!1);function f(t){const e=document.getElementById("dialog"),a=document.getElementById("dialog_content");let r;if(y.value)e.style.display="none",y.value=!1,a.innerHTML="";else{switch(t){case"clear_charts":r=g.clearCharts;break;case"save_charts":r=g.saveCharts;break;default:break}if(r){const t=document.createElement("h1");t.innerText=r.title;const e=document.createElement("p");let o;e.innerText=r.message,r.textArea&&(o=document.createElement("textarea"),o.id="dialog_text_area");const n=document.createElement("div");n.classList.add("dialog_buttons");let l=document.createElement("button");l.innerText="Cancel",l.onclick=f,n.appendChild(l);for(let a=0;a<r.buttons.length;a++){let t=document.createElement("button");t.innerText=r.buttons[a],t.onclick=()=>b(r.button_functions[a]),n.appendChild(t)}n.id="dialog_buttons",a.appendChild(t),a.appendChild(e),r.textArea&&a.appendChild(o),a.appendChild(n)}e.style.display="flex",y.value=!0}}function b(t){t(),f()}function w(){let t="";g.saveCharts.textArea&&document.getElementById("dialog_text_area").value&&(t="Comments: "+document.getElementById("dialog_text_area").value);let e="",a=document.querySelectorAll(".chart_container");a.forEach((t=>{e+=t.outerHTML}));let o="<hr><div style='padding: 0 2rem'> <h2>Log</h2>";r.log.forEach((t=>{if(!0===t.highlighted){let e="<p style='background-color: #343434; font-size: 1.5rem'>"+t.message+" <span style='color: #E2A300; font-size: 2rem'>&bull;</span></p>";o+=e}else{let e="<p style='font-size: 1.5rem'>"+t.message+"</p>";o+=e}})),o+=" </div>";const n=h();let l=`<!DOCTYPE html><html lang="en">\n        <head>\n            <title>KSU AUV Recorded Data</title>\n            <header style="width: 100vw; color: white; text-align: center">\n                <h1>AUV Data saved at ${n.month} ${n.day}, ${n.year} at ${n.hours}:${n.minutes}${n.time_period}</h1>\n                <p style="font-size: 1.25rem">${t}</p>\n            </header>\n        </head>\n        <body style="background-color: #121212; color: #D1D1D1">\n            <div style="display: flex; flex-wrap: wrap; gap: 1rem; justify-content: center;">`;l+=e,l+="</div><div>",l+=o,l+="</div></body></html>";let i=new Blob([l],{type:"text/html"});const c=document.createElement("a");c.href=URL.createObjectURL(i),c.download=`${n.year} ${n.month} ${n.day}, ${n.hours}_${n.minutes}_${n.time_period} AUV Data Charts.html`,c.click(),f(),f()}return(0,o.sV)((()=>{})),(t,e)=>{const r=(0,o.g2)("router-link"),i=(0,o.g2)("router-view");return(0,o.uX)(),(0,o.CE)(o.FK,null,[(0,o.Lk)("header",{style:(0,n.Tr)({backgroundImage:`url(${a(869)}`})},[(0,o.Lk)("nav",null,[(0,o.bF)(r,{to:"/"},{default:(0,o.k6)((()=>[(0,o.eW)("Stream")])),_:1}),(0,o.bF)(r,{to:"/data"},{default:(0,o.k6)((()=>[(0,o.eW)("Data Monitoring")])),_:1}),(0,o.bF)(r,{to:"/log"},{default:(0,o.k6)((()=>[(0,o.eW)("Log")])),_:1})]),(0,o.Lk)("button",{id:"power_button",onClick:s},p)],4),(0,o.bF)(i,{ref_key:"currentView",ref:l,onToggleDialog:f},null,512),v,_],64)}}};const f=y;var b=f,w=a(220),k=a.p+"../static/img/disconnected.58c32818.svg",C=a.p+"../static/img/depth_ex.fbd05571.jpg";const D={class:"active",id:"stream_main"},F={id:"stream"},x=(0,o.Fv)('<div class="video_stream"><div class="stream_header"><h2 class="camera_title">Regular View</h2></div><hr><div class="stream_container"><img id="camera_feed_1" src="'+k+'" alt="Regular Stream"></div></div>',1),L={class:"data_container",id:"battery_data"},E=["id"],O={class:"voltage"},A={class:"amps"},$=(0,o.Fv)('<div class="video_stream"><div class="stream_header"><h2 class="camera_title">Depth Sensor</h2></div><hr><div class="stream_container"><img id="camera_feed_2" src="'+C+'" alt="Depth Sensor"></div></div>',1),I={id:"notification_center"};var S={__name:"streamView",setup(t){const e=(0,d.Pj)(),a=(0,m.Kh)(e.state),r=(0,m.KR)(a.batteries),l=(0,m.KR)(a.notifications),i=t=>t.voltage>40?"Green":t.voltage>15?"Darkgoldenrod":t.voltage>0?"Red":"White";return(t,e)=>((0,o.uX)(),(0,o.CE)("main",D,[(0,o.Lk)("div",F,[x,(0,o.Lk)("div",L,[((0,o.uX)(!0),(0,o.CE)(o.FK,null,(0,o.pI)(r.value,((t,e)=>((0,o.uX)(),(0,o.CE)("div",{key:t.id,id:"battery_"+(e+1),class:"battery",style:(0,n.Tr)({borderColor:i(t)})},[(0,o.Lk)("h2",null,"Battery "+(0,n.v_)(t.id),1),(0,o.Lk)("p",null,[(0,o.eW)("Voltage: "),(0,o.Lk)("span",O,(0,n.v_)(t.voltage)+"V",1)]),(0,o.Lk)("p",null,[(0,o.eW)("Amps: "),(0,o.Lk)("span",A,(0,n.v_)(t.amps)+"A",1)])],12,E)))),128))]),$]),(0,o.Lk)("div",I,[((0,o.uX)(!0),(0,o.CE)(o.FK,null,(0,o.pI)(l.value,((t,e)=>((0,o.uX)(),(0,o.CE)("p",{key:e,class:(0,n.C4)(t.severity)},(0,n.v_)(t.message),3)))),128))])]))}};const P=S;var T=P;const R={id:"data_main"},K=(0,o.Lk)("h1",null,"Data Monitoring",-1),V={id:"data_monitoring"},M={class:"data_container",id:"battery_data_2"},j=["id"],B=(0,o.Lk)("h2",null,"Battery",-1),X={class:"voltage"},W={class:"amps"},z={class:"data_container",id:"motor_data"},U=["id"],N=(0,o.Lk)("h2",null,"Motor 1",-1),J={class:"data_container",id:"servo_data"},H=["id"],Y=(0,o.Lk)("h2",null,"Servo 1",-1),q=(0,o.Lk)("h1",null,"Data Charts",-1),G=(0,o.Fv)('<div id="data_charts"><div class="chart_container"><div id="battery_voltage"></div></div><div class="chart_container"><div id="battery_amp"></div></div><div class="chart_container"><div id="motor_pwm"></div></div><div class="chart_container"><div id="servo_pwm"></div></div></div>',1);var Z={__name:"dataView",emits:["toggleDialog"],setup(t,{emit:e}){const a=(0,d.Pj)(),r=e,l=(0,m.Kh)(a.state),i=(0,m.KR)(l.batteries),c=(0,m.KR)(l.motors),s=(0,m.KR)(l.servos),h=(0,m.KR)(l.charts.battery_voltage_chart),u=(0,m.KR)(l.charts.battery_amp_chart),g=(0,m.KR)(l.charts.motor_chart),p=(0,m.KR)(l.charts.servo_chart),v=t=>t.voltage>40?"Green":t.voltage>15?"Darkgoldenrod":t.voltage>0?"Red":"White",_={0:{color:"#0000FF"},1:{color:"#FF0000"},2:{color:"#FFFF00"},3:{color:"#008000"},4:{color:"#FF00FF"},5:{color:"#00FFFF"},6:{color:"#FFA500"},7:{color:"#800080"}};function y(){f([h.value,u.value,g.value,p.value]),b([h.value,u.value,g.value,p.value])}function f(t){const e=window.getComputedStyle(document.getElementById("example_chart_size"));t.forEach((t=>{if(null===t.chartData){t.chartData=new google.visualization.DataTable;for(let e=0;e<=t.column_count;e++)0===e?t.chartData.addColumn("number",t.y_title):t.chartData.addColumn("number",t.subject+e)}t.chartOptions={backgroundColor:"#343434",title:t.title,titleTextStyle:{color:"white"},legend:{textStyle:{color:"#FFFFFF"},position:"in"},hAxis:{title:t.x_title,titleTextStyle:{color:"white"},textStyle:{color:"white"},baselineColor:"white",gridLines:{color:"#FFFFFF"}},vAxis:{title:t.y_title,titleTextStyle:{color:"white"},textStyle:{color:"white"},minValue:0,maxValue:t.y_max+10},width:parseInt(e.getPropertyValue("width")),height:parseInt(e.getPropertyValue("height")),chartArea:{width:"70%",height:"85%",left:70,right:25},explorer:{actions:["dragToZoom","rightClickToReset"],axis:"horizontal",keepInBounds:!0,maxZoomIn:10},series:_},t.chart=new google.visualization.AreaChart(document.getElementById(t.container_id)),t.chart.draw(t.chartData,t.chartOptions)}))}function b(t){t.forEach((t=>{google.visualization.events.addListener(t.chart,"click",(function(){let e=JSON.parse(JSON.stringify(_));setTimeout((()=>{let a=t.chart.getSelection();if(!a)return t.chartOptions.series=e,void t.chart.draw(t.chartData,t.chartOptions);if(t.selectionBool)t.chartOptions.series=e,t.chart.draw(t.chartData,t.chartOptions),t.selectionBool=!1;else if(a.length>0){let r=a[0].column-1;if(null!=r){for(let a=0;a<t.chartData.getNumberOfColumns();a++)a!==r&&(e[a]={color:"transparent"});t.chartOptions.series=e,t.chart.draw(t.chartData,t.chartOptions)}t.selectionBool=!0}}),40)}))}))}function w(){r("toggleDialog","clear_charts")}function k(){r("toggleDialog","save_charts")}return(0,o.sV)((()=>{google.charts.load("current",{packages:["corechart"]}),google.charts.setOnLoadCallback(y)})),(t,e)=>((0,o.uX)(),(0,o.CE)("main",R,[(0,o.Lk)("section",null,[K,(0,o.Lk)("div",V,[(0,o.Lk)("div",M,[((0,o.uX)(!0),(0,o.CE)(o.FK,null,(0,o.pI)(i.value,((t,e)=>((0,o.uX)(),(0,o.CE)("div",{key:t.id,id:"battery_"+(e+1),class:"battery",style:(0,n.Tr)({borderColor:v(t)})},[B,(0,o.Lk)("p",null,[(0,o.eW)("Voltage: "),(0,o.Lk)("span",X,(0,n.v_)(t.voltage)+"V",1)]),(0,o.Lk)("p",null,[(0,o.eW)("Amps: "),(0,o.Lk)("span",W,(0,n.v_)(t.amps)+"A",1)])],12,j)))),128))]),(0,o.Lk)("div",z,[((0,o.uX)(!0),(0,o.CE)(o.FK,null,(0,o.pI)(c.value,((t,e)=>((0,o.uX)(),(0,o.CE)("div",{key:t.id,id:"motor_"+(e+1),class:"motor"},[N,(0,o.Lk)("p",null,"pwm: "+(0,n.v_)(t.pwm)+"%",1)],8,U)))),128))]),(0,o.Lk)("div",J,[((0,o.uX)(!0),(0,o.CE)(o.FK,null,(0,o.pI)(s.value,((t,e)=>((0,o.uX)(),(0,o.CE)("div",{key:t.id,id:"servo_"+(e+1),class:"servo"},[Y,(0,o.Lk)("p",null,"pwm: "+(0,n.v_)(t.pwm)+"%",1)],8,H)))),128))])])]),(0,o.Lk)("section",null,[q,(0,o.Lk)("div",{id:"chart_controls"},[(0,o.Lk)("button",{onClick:w},"Clear Charts"),(0,o.Lk)("button",{onClick:k},"Save Charts")]),G])]))}};const Q=Z;var tt=Q,et=a.p+"../static/img/scroll_pause.6e68bedc.svg";const at={id:"log_main"},rt=(0,o.Lk)("button",{id:"log_scroll_control",onclick:"control_scroll()"},[(0,o.Lk)("img",{src:et,alt:"Scroll Control"})],-1),ot=["id","onClick"],nt=(0,o.Lk)("span",{class:"highlight_indicator"},"•",-1);var lt={__name:"logView",setup(t){const e=(0,d.Pj)(),a=(0,m.Kh)(e.state),r=(0,m.KR)(a.log),l=t=>{const e=document.getElementById(t);e.classList.contains("marked")?e.classList.remove("marked"):e.classList.add("marked");const a=t.substring(4);r.value[a].highlighted=!0!==r.value[a].highlighted};return(t,e)=>((0,o.uX)(),(0,o.CE)("main",at,[rt,((0,o.uX)(!0),(0,o.CE)(o.FK,null,(0,o.pI)(r.value,(t=>((0,o.uX)(),(0,o.CE)("p",{key:r.value.indexOf(t),id:"log_"+r.value.indexOf(t),class:(0,n.C4)(["log_message",{marked:t.highlighted}]),onClick:e=>l("log_"+r.value.indexOf(t))},[(0,o.eW)((0,n.v_)(t.message)+" ",1),nt],10,ot)))),128))]))}};const it=lt;var ct=it;const st=[{path:"/",name:"AUV Stream",component:T},{path:"/data",name:"AUV Data",component:tt},{path:"/log",name:"AUV Log",component:ct}],ht=(0,w.aE)({history:(0,w.LA)("/"),routes:st});var ut=ht;function dt(){const t=new Date,e=["January","February","March","April","May","June","July","August","September","October","November","December"],a=t.getHours()<12?"am":"pm",r=e[t.getMonth()],o=t.getDate(),n=t.getFullYear();let l=t.getHours(),i=t.getMinutes();return l>12&&(l-=12),0===l&&(l=12),i<10&&(i=`0${i}`),{month:r,day:o,year:n,hours:l,minutes:i,time_period:a}}google.charts.load("current",{packages:["corechart"]});const mt=(0,d.y$)({state:{power:!1,batteries:[{id:1,voltage:0,amps:0},{id:2,voltage:0,amps:0},{id:3,voltage:0,amps:0},{id:4,voltage:0,amps:0}],motors:[{id:1,pwm:0},{id:2,pwm:0},{id:3,pwm:0},{id:4,pwm:0},{id:5,pwm:0},{id:6,pwm:0},{id:7,pwm:0},{id:8,pwm:0}],servos:[{id:1,pwm:0},{id:2,pwm:0}],chartIteration:1,charts:{battery_voltage_chart:{chart:null,chartData:null,chartOptions:null,subject:"Battery",column_count:4,title:"Battery Voltage",x_title:"Per Fetch Iteration",y_title:"Voltage",y_max:50,container_id:"battery_voltage",unit_reference:0,reference_unit:"voltage",selection_bool:!1},battery_amp_chart:{chart:null,chartData:null,chartOptions:null,subject:"Battery",column_count:4,title:"Battery Amps",x_title:"Per Fetch Iteration",y_title:"Amps",y_max:30,container_id:"battery_amp",unit_reference:0,reference_unit:"amps",selection_bool:!1},motor_chart:{chart:null,chartData:null,chartOptions:null,subject:"Motor",column_count:8,title:"Motor PWM",x_title:"Per Fetch Iteration",y_title:"PWM",y_max:100,container_id:"motor_pwm",unit_reference:0,reference_unit:"pwm",selection_bool:!1},servo_chart:{chart:null,chartData:null,chartOptions:null,subject:"Servo",column_count:2,title:"Servo PWM",x_title:"Per Fetch Iteration",y_title:"PWM",y_max:100,container_id:"servo_pwm",unit_reference:0,reference_unit:"pwm",selection_bool:!1}},notifications:[],log:[]},mutations:{togglePower(t){t.power=!t.power;const e=t.power?"ON":"OFF";t.notifications.push({message:`AUV ${e}`,severity:null});const a=dt(),r=`${a.month} ${a.day}, ${a.hours}:${a.minutes}${a.time_period}`,o=`${r} | AUV ${e}`;t.log.push({message:o,highlighted:!0}),setTimeout((()=>{t.notifications.length>0&&t.notifications.shift()}),1e4)},newNotification(t,{message:e,severity:a,highlighted:r}){t.notifications.push({message:e,severity:a});const o=dt(),n=`${o.month} ${o.day}, ${o.hours}:${o.minutes}${o.time_period}`,l=`${n} | ${e}`;r?t.log.push({message:l,highlighted:r}):t.log.push({message:l,highlighted:!1}),setTimeout((()=>{t.notifications.length>0&&t.notifications.shift()}),1e4)},addChartData(t){const e=[t.charts.battery_voltage_chart,t.charts.battery_amp_chart,t.charts.motor_chart,t.charts.servo_chart];e.forEach((t=>{if(null===t.chartData){t.chartData=new google.visualization.DataTable;for(let e=0;e<=t.column_count;e++)0===e?t.chartData.addColumn("number",t.y_title):t.chartData.addColumn("number",t.subject+e)}}));const a=[t.chartIteration],r=[t.chartIteration],o=[t.chartIteration],n=[t.chartIteration];t.chartIteration++,t.batteries.forEach((t=>{a.push(t.voltage),r.push(t.amps)})),t.charts.battery_voltage_chart.chartData.addRow(a),t.charts.battery_amp_chart.chartData.addRow(r),t.motors.forEach((t=>{o.push(t.pwm)})),t.charts.motor_chart.chartData.addRow(o),t.servos.forEach((t=>{n.push(t.pwm)})),t.charts.servo_chart.chartData.addRow(n),null!==t.charts.battery_voltage_chart.chart&&(t.charts.battery_voltage_chart.chart.draw(t.charts.battery_voltage_chart.chartData,t.charts.battery_voltage_chart.chartOptions),t.charts.battery_amp_chart.chart.draw(t.charts.battery_amp_chart.chartData,t.charts.battery_amp_chart.chartOptions),t.charts.motor_chart.chart.draw(t.charts.motor_chart.chartData,t.charts.motor_chart.chartOptions),t.charts.servo_chart.chart.draw(t.charts.servo_chart.chartData,t.charts.servo_chart.chartOptions))},clearChartData(t){const e=t.charts.battery_voltage_chart,a=t.charts.battery_amp_chart,r=t.charts.motor_chart,o=t.charts.servo_chart,n=[e,a,r,o];e.chartData=null,a.chartData=null,r.chartData=null,o.chartData=null,n.forEach((t=>{t.chartData=new google.visualization.DataTable;for(let e=0;e<=t.column_count;e++)0===e?t.chartData.addColumn("number",t.y_title):t.chartData.addColumn("number",t.subject+e);t.chart.draw(t.chartData,t.chartOptions)}))},newLog(t,e){const a=dt,r=`${a.month} ${a.day}, ${a.hours}:${a.minutes}${a.time_period}`,o=`${r} | ${e}`;t.log.push({message:o,highlighted:!1})}},actions:{}});var gt=mt;(0,r.Ef)(b).use(ut).use(gt).mount("#app")},869:function(t,e,a){t.exports=a.p+"../static/img/banner.d118616e.png"}},e={};function a(r){var o=e[r];if(void 0!==o)return o.exports;var n=e[r]={exports:{}};return t[r](n,n.exports,a),n.exports}a.m=t,function(){var t=[];a.O=function(e,r,o,n){if(!r){var l=1/0;for(h=0;h<t.length;h++){r=t[h][0],o=t[h][1],n=t[h][2];for(var i=!0,c=0;c<r.length;c++)(!1&n||l>=n)&&Object.keys(a.O).every((function(t){return a.O[t](r[c])}))?r.splice(c--,1):(i=!1,n<l&&(l=n));if(i){t.splice(h--,1);var s=o();void 0!==s&&(e=s)}}return e}n=n||0;for(var h=t.length;h>0&&t[h-1][2]>n;h--)t[h]=t[h-1];t[h]=[r,o,n]}}(),function(){a.d=function(t,e){for(var r in e)a.o(e,r)&&!a.o(t,r)&&Object.defineProperty(t,r,{enumerable:!0,get:e[r]})}}(),function(){a.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(t){if("object"===typeof window)return window}}()}(),function(){a.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)}}(),function(){a.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})}}(),function(){a.p="/"}(),function(){var t={524:0};a.O.j=function(e){return 0===t[e]};var e=function(e,r){var o,n,l=r[0],i=r[1],c=r[2],s=0;if(l.some((function(e){return 0!==t[e]}))){for(o in i)a.o(i,o)&&(a.m[o]=i[o]);if(c)var h=c(a)}for(e&&e(r);s<l.length;s++)n=l[s],a.o(t,n)&&t[n]&&t[n][0](),t[n]=0;return a.O(h)},r=self["webpackChunkcontrol_console"]=self["webpackChunkcontrol_console"]||[];r.forEach(e.bind(null,0)),r.push=e.bind(null,r.push.bind(r))}();var r=a.O(void 0,[504],(function(){return a(676)}));r=a.O(r)})();
//# sourceMappingURL=app.23f5a921.js.map