
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from html import escape
import re

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


def analyze_email(email_text):
    findings = []
    text = email_text.lower()

    # 1. Check for urgent or pressuring language.
    urgent_phrases = [
        "urgent",
        "immediately",
        "within 10 minutes",
        "account will be blocked",
        "verify now",
        "act now",
        "final warning",
        "suspended",
        "permanent account suspension",
        "failure to act"
    ]

    for phrase in urgent_phrases:
        if phrase in text:
            findings.append(
                f"Urgent or pressuring language detected: '{phrase}'"
            )

    # 2. Check for requests for sensitive information.
    sensitive_phrases = [
        "password",
        "one-time password",
        "otp",
        "banking details",
        "credit card",
        "login credentials"
    ]

    for phrase in sensitive_phrases:
        if phrase in text:
            findings.append(
                f"Possible request for sensitive information: '{phrase}'"
            )

    # 3. Extract URLs and check for shortened links.
    urls = re.findall(
        r"https?://[^\s<>\"']+",
        email_text,
        re.IGNORECASE
    )

    shorteners = ["bit.ly", "tinyurl.com", "t.co"]

    for url in urls:
        clean_url = url.rstrip(".,!?)")
        if any(shortener in clean_url.lower() for shortener in shorteners):
            findings.append(
                f"Shortened link detected; inspect carefully: {clean_url}"
            )

    # 4. Check for an explicitly stated sender address.
    sender_match = re.search(
        r"(?im)^\s*(?:from|sender)\s*:\s*.*?([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})",
        email_text
    )

    if sender_match:
        sender_email = sender_match.group(1)
        sender_domain = sender_email.rsplit("@", 1)[-1].lower()

        # Reserved example domains are used for demonstration only.
        if sender_domain.endswith(".invalid"):
            findings.append(
                f"Unverifiable example sender detected: {sender_email}"
            )
        elif sender_domain in [
            "gmail.com",
            "outlook.com",
            "yahoo.com"
        ]:
            findings.append(
                f"Sender uses a public email provider ({sender_domain}); "
                "verify the sender's identity independently."
            )
    else:
        findings.append(
            "Sender address not found in the supplied text; "
            "the sender's identity could not be checked."
        )

    # 5. Check for text that may indicate a displayed link and destination.
    # Example format: Official Bank (https://unrelated.example)
    displayed_links = re.findall(
        r"([A-Za-z0-9 ._-]{2,60})\s*\((https?://[^\s)]+)\)",
        email_text
    )

    for label, url in displayed_links:
        label_lower = label.lower()
        domain = urlparse(url).netloc.lower()

        trusted_brand_words = [
            "bank", "paypal", "microsoft", "google", "amazon"
        ]

        if (
            any(word in label_lower for word in trusted_brand_words)
            and not any(word in domain for word in trusted_brand_words)
        ):
            findings.append(
                f"Possible mismatched link: '{label.strip()}' "
                f"points to {domain}. Verify the destination independently."
            )

    if not findings:
        findings.append(
            "No configured warning patterns detected. "
            "This does not prove the email is safe."
        )

    return findings



class PhishingHandler(BaseHTTPRequestHandler):

    def send_page(self, page_name, replacements=None):
        template_path = TEMPLATE_DIR / page_name
        if not template_path.is_file():
            self.send_error(
                500,
                f"Page {page_name} not found. Check the templates folder."
            )
            return

        page = template_path.read_text(encoding="utf-8")

        # Set default values for placeholders.
        values = {
            "{{RESULT}}": "",
            "{{EMAIL_TEXT}}": ""
        }
        # Apply supplied results BEFORE replacing placeholders.
        if replacements:
            values.update(replacements)
        
        for placeholder, value in values.items():
            page = page.replace(placeholder, value)

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(page.encode("utf-8"))

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/style.css":
            css_path = STATIC_DIR / "style.css"

            if not css_path.is_file():
                self.send_error(404, "CSS file not found")
                return

            self.send_response(200)
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.end_headers()
            self.wfile.write(css_path.read_bytes())
            return

        routes = {
            "/": "home.html",
            "/home": "home.html",
            "/analyze": "analyze.html",
            "/quiz": "quiz.html",
            "/learn": "learn.html"
        }

        page_name = routes.get(path)

        if page_name is None:
            self.send_error(404, "Page not found")
            return

        self.send_page(page_name)

    def do_POST(self):
        path = urlparse(self.path).path

        if path != "/analyze":
            self.send_error(404, "Page not found")
            return

        length = int(self.headers.get("Content-Length", 0))

        if length > 100_000:
            self.send_error(413, "Email text is too large")
            return

        body = self.rfile.read(length).decode(
            "utf-8",
            errors="replace"
        )

        form = parse_qs(body)
        email_text = form.get("email_text", [""])[0].strip()

        if not email_text:
            findings = ["Please enter email text to analyze."]
        else:
            findings = analyze_email(email_text)

        result_html = "".join(
            f"<li>{escape(item)}</li>"
            for item in findings
        )

        self.send_page(
            "analyze.html",
            {
                "{{RESULT}}": result_html,
                "{{EMAIL_TEXT}}": escape(email_text)
            }
        )


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), PhishingHandler)

    print("Phishing Email Identifier V2 is running!")
    print("Open http://localhost:8000 in your browser.")
    print("Press Ctrl+C to stop the server.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
