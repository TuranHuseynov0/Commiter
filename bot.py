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

def timestamp(fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.now().strftime(fmt)

def log(message):
    print(f"[{timestamp('%H:%M:%S')}] {message}")

def run_git_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.returncode

def run_git_commands(commands):
    return all(run_git_command(command) == 0 for command in commands)

def append_to_file(message):
    with open(FILE_NAME, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp()}] - {message}\n")

def git_push():
    message = random.choice(RANDOM_TEXTS)
    append_to_file(message)

    if run_git_commands([
        "git add .",
        f'git commit -m "{message}"',
        f"git push origin {BRANCH}",
    ]):
        log(f"Success: {message}")
        return True
    log("Error: Git commands failed.")
    return False

if __name__ == "__main__":
    print("Auto-Commit Bot executed by GitHub Actions...")
    
    # İnsan davranışını təqlid etmək üçün 90% şansla commit atır.
    # (Əgər hər işə düşəndə mütləq commit atmasını istəyirsinizsə, bu if-else-i silib sadəcə git_push() yaza bilərsiniz)
    if random.random() < 0.90: 
        git_push()
    else:
        log("Action skipped for human-like behavior.")
