from flask import Flask, render_template_string
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

HTML = """
<html>
<head>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
</head>
<body style="background:#111;color:white">

<h1>🔥 SPBD DASHBOARD</h1>
<canvas id="chart"></canvas>
<div id="vulns"></div>

<script>
var socket = io();

var chart = new Chart(document.getElementById("chart"), {
    type: 'bar',
    data: {
        labels:["CRITICAL","HIGH","MEDIUM","LOW"],
        datasets:[{data:[0,0,0,0]}]
    }
});

socket.on("update", function(data){
    chart.data.datasets[0].data=[
        data.stats.CRITICAL,
        data.stats.HIGH,
        data.stats.MEDIUM,
        data.stats.LOW
    ];
    chart.update();

    let html="";
    data.vulns.forEach(v=>{
        html += `<p>[${v.severity}] ${v.type}</p>`;
    });

    document.getElementById("vulns").innerHTML=html;
});
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

def run():
    socketio.run(app, port=5000)
