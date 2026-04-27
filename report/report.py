from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import json, os

def make_pdf():
    if not os.path.exists("session.json"):
        print("No session file")
        return

    data = json.load(open("session.json"))

    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("SPBD Scan Report", styles["Title"]))
    content.append(Spacer(1, 10))

    for url, vulns in data.get("results", {}).items():
        content.append(Paragraph(f"<b>{url}</b>", styles["Heading2"]))

        if not vulns:
            content.append(Paragraph("No issues found", styles["Normal"]))

        for v in vulns:
            txt = f"""
            Type: {v.get('type')} <br/>
            Severity: {v.get('severity')} <br/>
            Confidence: {v.get('confidence')} <br/>
            Notes: {", ".join(v.get("notes", []))}<br/><br/>
            """
            content.append(Paragraph(txt, styles["Normal"]))

        content.append(Spacer(1, 10))

    doc.build(content)
    print("[✓] report.pdf created")
