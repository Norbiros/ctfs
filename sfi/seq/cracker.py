import itertools
import subprocess
import string

# Path to your 7z archive
ARCHIVE_PATH = "protected.7z"

# Define character set: ASCII letters, digits, and symbols
CHARSET = string.ascii_letters + string.digits + string.punctuation

# Min and max password length to try
MIN_LEN = 1
MAX_LEN = 8  # Adjust based on expected complexity

def attempt_extract(password: str) -> bool:
    """Attempts to extract the archive with a given password."""
    command = ["7z", "x", ARCHIVE_PATH, f"-p{password}", "-y"]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return "Everything is Ok" in result.stdout.decode(errors='ignore')

def brute_force():
    """Tries different password combinations."""
    for length in range(MIN_LEN, MAX_LEN + 1):
        for attempt in itertools.product(CHARSET, repeat=length):
            password = "".join(attempt)
            print(f"Trying: {password}")
            if attempt_extract(password):
                print(f"Password found: {password}")
                return
    print("Password not found.")

if __name__ == "__main__":
    brute_force()