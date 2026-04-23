import time
import subprocess
import random
from datetime import datetime

FILE_NAME = "data.txt"
BRANCH = "main"

RANDOM_TEXTS = [
    "fix: resolve identified bug in application logic",
    "feat: implement foundational structures for upcoming release",
    "docs: update technical notes and project documentation",
    "refactor: optimize Python scripts for improved efficiency",
    "chore: automated synchronization of repository state",
    "feat: add incremental updates to codebase",
    "style: apply consistent code formatting and linting",
    "feat: initialize core development for new feature set",
    "perf: apply minor adjustments for enhanced system impact",
    "build: update dependencies and build configurations",
    "test: add unit tests for data processing modules"
]

def run_git_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Hata: {result.stderr}")
    return result.returncode

def append_to_file():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FILE_NAME, "a", encoding="utf-8") as f:
        f.write(f"Update: {timestamp}\n")

def git_push():
    commit_message = random.choice(RANDOM_TEXTS)
    
    run_git_command("git add .")
    run_git_command(f'git commit -m "{commit_message}"')
    run_git_command(f"git push origin {BRANCH}")
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Başarıyla pushlandı: {commit_message}")

def is_work_hours():
    now = datetime.now()
    return 9 <= now.hour <= 23

# --- ANA DÖNGÜ ---
print("Profesyonel Auto-Commit Botu başlatıldı...")

while True:
    if is_work_hours():
        if random.random() < 0.8:
            append_to_file()
            git_push()
        else:
            print("🕒 Bu döngü şans eseri atlandı (doğal görünüm için).")
