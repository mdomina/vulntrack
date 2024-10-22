from pydantic_settings import BaseSettings

class SettingsWord(BaseSettings):
    word_mapping: dict = {
                "Directory Listing": ["directory listing"],
                "Clickjacking": ["frameable response clickjacking"],
                "XSS Reflected": ["cross site scripting reflected"],
                "XSS Stored": ["cross site scripting stored"],
                "RCE": ["slider revolution rce 0day"],
                "Insecure File Upload": [
                    "insecure file upload", 
                    "upload abuse"
                    ],
                "Outdated Software": [
                    "outdated vulnerable server side libraries", 
                    "outdated vulnerable client side libraries"
                    ],
                "Insecure Deserialization": ["java insecure object deserialization"],
                "Information Disclosure": [
                    "information disclosure",
                    "information disclosure web application server default pages", 
                    "information disclosure stack traces and error messages", 
                    "information disclosure swagger documentation",
                    "information disclosure stack traces and error messages"
                    ],
                "Weak TLS": ["tls version 1.0 protocol detection"],
                "HTTP Method": ["http trace method enabled"],
                "SQLi": ["sql injection", "sqli"],
                "Enumerate Admin Interfaces": [
                    "enumerate admin interfaces",
                    "admin dashboard public exposure",
                    "wordpress xmlrpc enabled"
                    ],
                "Business Logic Data Validation": [
                    "business logic vata validation",
                    "business logic constraint violations", 
                    "business logic constraints violation race condition",
                    "business logic constraints violation toctou race condition",
                    ],
                "Bypassing Authorization Schema": [
                    "bypassing authorization Schema",
                    "incorrect privilege separation & validation"],
                "Limit Abuse": [
                    "limit abuse",
                    "message bombing", 
                    "mail bombing"
                    ]
            }
    