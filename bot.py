import time
import subprocess
import random
from datetime import datetime
import os

# --- AYARLAR ---
FILE_NAME = "data.txt"
BRANCH = "main" # Eğer GitHub'da 'master' ise burayı 'master' yap!

RANDOM_TEXTS = [
    "fix: resolve identified bug in application logic",
    "feat: implement foundational structures for upcoming release",
    "docs: update technical notes and project documentation",
    "refactor: optimize Python scripts for improved efficiency",
    "chore: automated synchronization of repository state",
    "feat: add incremental updates to codebase",
    "style: apply consistent code formatting and linting",
    "feat: initialize core development for new feature set",
    "perf: apply minor adjustments for enhanced system impact"
]

def run_git_command(command):
    """Git komutlarını çalıştırır ve çıktıyı terminale basar."""
    print(f"Executing: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ HATA OLUŞTU: {result.stderr}")
    else:
        if result.stdout:
            print(f"✅ ÇIKTI: {result.stdout.strip()}")
    return result.returncode

def append_to_file(mesaj):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FILE_NAME, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] - {mesaj}\n")

def git_push():
    commit_message = random.choice(RANDOM_TEXTS)
    append_to_file(commit_message)
    
    # Adım adım kontroller
    if run_git_command("git add .") != 0: return
    if run_git_command(f'git commit -m "{commit_message}"') != 0: return
    
    print("🚀 Push işlemi başlatılıyor...")
    # Push sonucunu kontrol et
    push_result = run_git_command(f"git push origin {BRANCH}")
    
    if push_result == 0:
        print(f"✨ TEBRİKLER: '{commit_message}' başarıyla GitHub'a gönderildi!")
    else:
        print("🚨 PUSH BAŞARISIZ! Yukarıdaki hata mesajını kontrol et.")

# --- ANA DÖNGÜ ---
print(f"🚀 Bot başlatıldı. Hedef Dal: {BRANCH}")

# İlk çalıştırmada hemen bir deneme yapalım
git_push()

while True:
    # Test için bekleme süresini 30 saniye yapıyorum, çalışınca artırırsın
    wait_time = 30 
    print(f"\n💤 {wait_time} saniye sonraki commit denemesi bekleniyor...")
    time.sleep(wait_time)
    git_push()