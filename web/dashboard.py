from flask import Flask, render_template_string
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

DATA = {
    "vulns": [],
    "stats": {"SQLi":0, "XSS":0, "HEADERS":0}
}

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>SPBD Dashboard</title>
<style>
body { background:#0d1117; color:#c9d1d9; font-family:monospace; }
h1 { color:#58a6ff; }
.card {
    border:1px solid #30363d;
    padding:10px;
    margin:10px;
    border-radius:8px;
}
.medium { color:orange; }
.low { color:lightgreen; }
</style>
</head>
<body>

<h1>🔥 SPBD Dashboard</h1>

<div id="stats"></div>
<div id="vulns"></div>

<script src="https://cdn.socket.io/4.0.1/socket.io.min.js"></script>
<script>
var socket = io();

socket.on("update", function(data){
    let v = document.getElementById("vulns");
    let s = document.getElementById("stats");

    v.innerHTML = "";
    data.vulns.forEach(item=>{
        v.innerHTML += `
        <div class="card">
            <b>${item.type}</b><br>
            Param: ${item.param || "-"}<br>
            Detail: ${item.detail || "-"}
        </div>`;
    });

    s.innerHTML = `
    <div class="card">
        SQLi: ${data.stats.SQLi} |
        XSS: ${data.stats.XSS} |
        Headers: ${data.stats.HEADERS}
    </div>`;
});
</script>

</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

def run():
    socketio.run(app, host="127.0.0.1", port=5000)
