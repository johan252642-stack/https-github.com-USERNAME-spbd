from flask import Flask, render_template_string
import json

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>SPBD Dashboard</title>
<style>
body { background:#0d1117; color:white; font-family:Arial; }
.card { background:#161b22; padding:20px; margin:10px; border-radius:10px; }
.medium { color:orange; font-weight:bold; }
.high { color:red; font-weight:bold; }
</style>
</head>

<body>

<h1>SPBD Dashboard</h1>

<div class="card">
<h2>Target</h2>
<p>{{data.target}}</p>
</div>

<div class="card">
<h2>Vulnerabilities</h2>
{% for v in data.vulns %}
<p class="high">{{v.type}} → {{v.param}}</p>
{% endfor %}
</div>

<div class="card">
<h2>Exploits</h2>
{% if data.exploits %}
    {% for e in data.exploits %}
        <p class="medium">
        {{e.type}} →
        {{ e.result if e.result else e.poc }}
        </p>
    {% endfor %}
{% else %}
<p>No exploit</p>
{% endif %}
</div>

</body>
</html>
"""

@app.route("/")
def home():
    data = json.load(open("session.json"))
    return render_template_string(HTML, data=data)
