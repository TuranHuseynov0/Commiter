import subprocess
import random
import time  # Bekleme süresi için eklendi
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
    return result.returncode

def append_to_file(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FILE_NAME, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] - {message}\n")

def git_push():
    message = random.choice(RANDOM_TEXTS)
    append_to_file(message)
    
    if run_git_command("git add .") == 0:
        if run_git_command(f'git commit -m "{message}"') == 0:
            if run_git_command(f"git push origin {BRANCH}") == 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Success: {message}")
                return True
    return False

def is_work_hours():
    now = datetime.now()
    # 08:00 ile 23:59 arası çalışma saatleri
    return 8 <= now.hour <= 23

if __name__ == "__main__":
    print("Professional Auto-Commit Bot started (Interval: 30 minutes)...")
    
    while True:  # Sonsuz döngü başlatıldı
        if is_work_hours():
            # Rastgelelik oranını biraz artırdık veya tamamen kaldırabilirsin
            if random.random() < 0.90: 
                git_push()
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Action skipped for human-like behavior.")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Night mode: Skipped.")

        # 30 dakika bekler (30 dakika * 60 saniye = 1800 saniye)
        time.sleep(1800)