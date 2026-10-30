# PhishGuard – Phishing Email Identifier

PhishGuard is a Python-based educational web application designed to help users recognize common phishing email warning signs. It includes an email analyzer, phishing awareness checklist, sample email investigations, and a randomized quiz.

## Features

- **Email Analyzer:** Analyzes pasted email text for suspicious patterns.
- **Urgent Language Detection:** Identifies words and phrases that create pressure or urgency.
- **Suspicious Link Detection:** Checks for shortened links and certain possible mismatches between displayed labels and destinations.
- **Sender Checks:** Identifies missing sender addresses and flags certain unverifiable sender details.
- **Phishing Detection Checklist:** Explains common phishing warning signs.
- **Sample Email Analysis:** Includes four fictional phishing email examples with their suspicious signs.
- **Randomized Quiz:** Selects five random questions from a question bank and displays the score.
- **Learn & Practice:** Provides phishing awareness information and a short findings report.
- **Multi-Page Website:** Includes Home, Analyze Email, Quiz, and Learn & Practice pages.

## Technologies Used

- **Python 3** – Backend server and email text analysis.
- **HTML5** – Web page structure.
- **CSS3** – Website styling and responsive design.
- **JavaScript** – Random quiz generation, answer selection, and scoring.
- **Python Standard Library:**
  - `http.server`
  - `pathlib`
  - `urllib.parse`
  - `html`
  - `re`

No external Python packages or frameworks are required.

## Project Structure

```text
phishing-email-identifier/
│
├── server.py
├── README.md
│
├── templates/
│   ├── home.html
│   ├── analyze.html
│   ├── quiz.html
│   └── learn.html
│
└── static/
    └── style.css
```

## Setup Instructions

### Prerequisites

- Python 3 installed on your computer.
- A web browser such as Google Chrome.
- Git installed (if cloning the repository).

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

### 2. Navigate to the Project Folder

```bash
cd phishing-email-identifier
```

### 3. Run the Python Server

```bash
python server.py
```

For Windows, you can also use:

```bash
py server.py
```

### 4. Open the Website

Open Google Chrome and visit:

```text
http://localhost:8000
```

The PhishGuard application will now run locally.

### 5. Stop the Server

Press `Ctrl + C` in the terminal to stop the server.

## How to Use

1. Open the Home page to explore PhishGuard.
2. Navigate to Analyze Email and paste sample email content.
3. Review the suspicious patterns detected by the analyzer.
4. Visit Learn & Practice to study phishing warning signs and sample email investigations.
5. Open the Quiz section to test your phishing awareness knowledge.

## Project Objective

The objective of this project is to spread cybersecurity awareness by helping users understand how phishing emails work and how to identify suspicious messages before interacting with them.

## GitHub Repository

**Repository Link:** YOUR_GITHUB_REPOSITORY_LINK

## Disclaimer

PhishGuard is an educational demonstration project. Its detection is based on basic text patterns and cannot guarantee that an email is safe or malicious. Always verify suspicious emails through trusted communication channels. Do not enter real passwords, OTPs, or private information into this tool.