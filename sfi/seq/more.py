import itertools
import subprocess
import string
import multiprocessing
import os

# Path to your 7z archive
ARCHIVE_PATH = "protected.7z"

# Define character set: ASCII letters, digits, and symbols
CHARSET = string.ascii_letters + string.digits + string.punctuation

# Min and max password length to try
MIN_LEN = 6
MAX_LEN = 9  # Adjust based on expected complexity
NUM_PROCESSES = 32  # Adjust based on CPU cores
DEBUG_INTERVAL = 1000000  # Print progress every 10000 attempts
PROGRESS_FILE = "progress.txt"  # Save progress here

def save_progress(index):
    """Save the last attempted password index."""
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(index))

def load_progress():
    """Load last attempted password index from file."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return int(f.read().strip())
    return 0

def attempt_extract(password: str) -> bool:
    """Attempts to extract the archive with a given password."""
    command = ["7z", "x", ARCHIVE_PATH, f"-p{password}", "-y"]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return "Everything is Ok" in result.stdout.decode(errors='ignore')

def password_generator(start_index=0):
    """Generates password combinations, skipping already tested ones."""
    for length in range(MIN_LEN, MAX_LEN + 1):
        for i, attempt in enumerate(itertools.product(CHARSET, repeat=length)):
            if i < start_index:
                continue  # Skip already attempted passwords
            password = "".join(attempt)
            if i % DEBUG_INTERVAL == 0:
                print(f"Checked {i} passwords. Last attempt: {password}")
                save_progress(i)  # Save progress every DEBUG_INTERVAL
            yield password

def worker(password):
    """Process worker function to attempt password extraction."""
    if attempt_extract(password):
        print(f"Password found: {password}")
        save_progress(-1)  # Mark completion
        return password
    return None

def brute_force():
    """Uses multiprocessing to brute-force the password."""
    start_index = load_progress()
    print(f"Resuming from index: {start_index}")

    with multiprocessing.Pool(NUM_PROCESSES) as pool:
        results = pool.map(worker, password_generator(start_index))
        for result in results:
            if result:
                print(f"Password cracked: {result}")
                pool.terminate()  # Stop as soon as the password is found
                return
    print("Password not found.")

if __name__ == "__main__":
    brute_force()
