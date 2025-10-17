class SecurityConfig(object):
    BLOCKED_DOMAINS = [
        "malicious.com",
        "phishing-site.com",
        "spam-domain.com",
    ]

    ALLOWED_DOMAINS = []

    DANGEROUS_EXTENSIONS = [
        ".exe",
        ".dll",
        ".bat",
        ".cmd",
        ".sh",
        ".ps1",
        ".vbs",
        ".jar",
        ".apk",
        ".msi",
    ]

    SUSPICIOUS_PATTERNS = [
        r"\.\.\/",  # Path traversal
        r"<script",  # XSS attempts
        r"javascript:",  # JavaScript protocol
        r"data:text\/html",  # Data URLs sospechosos
        r"file:\/\/",  # File protocol
        r"ftp:\/\/",  # FTP protocol
    ]

    DANGEROUS_PORTS = [
        22,  # SSH
        23,  # Telnet
        3389,  # RDP
        5900,  # VNC
    ]

    RATE_LIMIT = 60

    DANGEROUS_METHODS = ["TRACE", "CONNECT"]


if __name__ == "__main__":
    pass
