from flask import Flask, render_template_string
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

HTML = """
<body style="background:black;color:lime;font-family:monospace">
<h2>SPBD LIVE</h2>
<div id="log"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
<script>
var s=io();
s.on("update",d=>{
 let h="";
 d.vulns.forEach(v=>{
  h+=`<p>${JSON.stringify(v)}</p>`;
 });
 document.getElementById("log").innerHTML=h;
});
</script>
</body>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

def run():
    socketio.run(app,port=5000)
