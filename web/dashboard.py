from flask import Flask, render_template_string
import json

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>SPBD Dashboard</title>
<style>
body {background:#0d1117;color:white;font-family:Arial;}
.card {background:#161b22;padding:20px;margin:10px;border-radius:10px;}
.red{color:red;} .orange{color:orange;}
</style>
</head>
<body>

<h1>SPBD AI Dashboard</h1>

<div class="card">
<h2>Target</h2>
<p>{{d.target}}</p>
</div>

<div class="card">
<h2>Risk</h2>
<p class="red">{{d.risk_score}} / 100</p>
<p>{{d.analysis.level}}</p>
</div>

<div class="card">
<h2>WAF</h2>
<p>{{d.waf}}</p>
</div>

<div class="card">
<h2>Vulnerabilities</h2>
{% for v in d.vulns %}
<p class="orange">{{v.type}} → {{v.param}} ({{v.confidence}}%)</p>
{% endfor %}
</div>

<div class="card">
<h2>Exploits</h2>
{% for e in d.exploits %}
<p>{{e.type}} → {{e.poc}}</p>
{% endfor %}
</div>

</body>
</html>
"""

@app.route("/")
def home():
    d = json.load(open("session.json"))
    return render_template_string(HTML, d=d)
