from flask import Flask, render_template_string
import json, os

app = Flask(__name__)

HTML = """
<h2>🔥 SPBD Dashboard</h2>

{% for url, vulns in data.items() %}
<h3>{{url}}</h3>
<ul>
{% for v in vulns %}
<li>
<b>{{v.type}}</b> - {{v.severity}} <br>
{{v.reason}} <br>
<small>{{v.notes}}</small>
</li>
{% endfor %}
</ul>
{% endfor %}
"""

@app.route("/")
def home():
    if os.path.exists("session.json"):
        data = json.load(open("session.json"))
        return render_template_string(HTML, data=data.get("results", {}))

    return "No data"

if __name__ == "__main__":
    app.run(port=5000)
