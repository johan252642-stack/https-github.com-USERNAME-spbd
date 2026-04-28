def generate_report(data):
    html = f"""
    <html><body style='background:#111;color:white;font-family:sans-serif'>
    <h1>SPBD REPORT</h1>
    <p>Target: {data['target']}</p>
    {''.join([f"<p>[{v['severity']}] {v['type']}</p>" for v in data["vulns"]])}
    </body></html>
    """

    open("report.html","w").write(html)
    print("[✓] Report saved")
