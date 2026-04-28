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
.high { color:red; font-weight:bold; }
.medium { color:orange; }
</style>
</head>

<body>

<h1>SPBD Dashboard</h1>

<div class="card">
<h2>Target</h2>
<p>{{data.target}}</p>
</div>

<div class="card">
<h2>Risk Score</h2>
<p style="font-size:30px;color:red;">{{data.risk_score}} / 100</p>
</div>

<div class="card">
<h2>WAF</h2>
<p>{{data.waf}}</p>
</div>

<div class="card">
<h2>Vulnerabilities</h2>
{% for v in data.vulns %}
<p class="high">{{v.type}} → {{v.param}}</p>
{% endfor %}
</div>

<div class="card">
<h2>Exploits</h2>
{% for e in data.exploits %}
<p class="medium">{{e.type}} → {{e.poc}}</p>
{% endfor %}
</div>

<div class="card">
<h2>URLs</h2>
{% for u in data.urls %}
<p>{{u}}</p>
{% endfor %}
</div>

</body>
</html>
"""

@app.route("/")
def home():
    data = json.load(open("session.json"))
    return render_template_string(HTML, data=data)
