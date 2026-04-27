<p align="center">
  <img src="IMG_20260426_183855.jpg" width="100%">
</p>

<h1 align="center">SPBD PRO MAX</h1>

🔴 SPBD PRO MAX

🔥 Smart Pipeline Bug Detector (AI Powered)

🚀 Features

- AI-based vulnerability detection
- Smart payload generation (SQLi, XSS, etc)
- Multi-target scanning
- Realtime dashboard
- PDF report export
- Nuclei integration
- Cookie / session support

📦 Installation

Linux / Kali / Ubuntu

git clone https://github.com/johan252642-stack/spbd.git
cd spbd
chmod +x install.sh
./install.sh

📱 Termux (Android)

pkg update && pkg upgrade -y
pkg install git -y

git clone https://github.com/johan252642-stack/spbd.git
cd spbd
chmod +x install.sh
./install.sh

▶️ Usage

Basic scan
spbd

Crawl scan
spbd --crawl

Pro scan
spbd --crawl --pro

Multi target
spbd --targets list.txt --crawl --pro

With cookie
spbd --cookie "PHPSESSID=your_cookie"

📊 Dashboard

Run
python app.py

Open in browser
http://localhost:8000

📁 Report

Export PDF via dashboard

Includes:

- Vulnerability summary
- Chart visualization
- Detailed findings
- AI explanation

⚙️ Tools

- Python 3
- Flask + SocketIO
- Nuclei
- ReportLab
- Matplotlib
- Requests

🔐 Security Notes

- Use only on authorized targets
- Do not expose dashboard without protection
- Secure API if used publicly

⚠️ Disclaimer

SPBD PRO MAX is intended for:

- Educational purposes
- Security research
- Testing on systems you own or have permission to test

You are responsible for your actions.

🚫 Do not use this tool for illegal activities.

👨‍💻 Developer

Johansah Revi Adnan
Security Research & Automation
