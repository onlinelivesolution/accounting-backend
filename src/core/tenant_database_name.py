import re


def generate_database_name(email: str) -> str:

    # salespoint@gmail.com
    # ↓
    # salespoint_gmail_com

    database_name = email.lower()

    database_name = database_name.replace("@", "_")
    database_name = database_name.replace(".", "_")

    # remove any remaining special chars
    database_name = re.sub(r"[^a-zA-Z0-9_]", "", database_name)

    return database_name
