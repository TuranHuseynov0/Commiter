import time
import subprocess
import random
from datetime import datetime

# --- AYARLAR ---
FILE_NAME = "data.txt"
BRANCH = "main"

# Profesyonel Commit Mesajları
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
    """Git komutlarını çalıştırır."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Hata: {result.stderr.strip()}")
    return result.returncode

def append_to_file(mesaj):
    """Hem tarihi hem de profesyonel mesajı dosyanın içine yazar."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FILE_NAME, "a", encoding="utf-8") as f:
        # Artık dosyanın içinde sadece tarih değil, mesaj da olacak
        f.write(f"[{timestamp}] - {mesaj}\n")

def git_push():
    """Git işlemlerini yapar."""
    # Listeden rastgele bir mesaj seç
    commit_message = random.choice(RANDOM_TEXTS)
    
    # 1. Önce dosyayı güncelle (içine mesajı yaz)
    append_to_file(commit_message)
    
    # 2. Git komutlarını çalıştır
    run_git_command("git add .")
    run_git_command(f'git commit -m "{commit_message}"')
    run_git_command(f"git push origin {BRANCH}")
    
    print(f"✅ Başarılı: {commit_message}")

def is_work_hours():
    """Botun sadece sabah 09:00 - 23:00 arası çalışmasını sağlar."""
    now = datetime.now()
    return 9 <= now.hour <= 23

# --- ANA DÖNGÜ ---
print("🚀 Gelişmiş Profesyonel Bot Başlatıldı!")
print("💡 Not: Mesajlar artık hem commit başlığında hem de data.txt içinde görünecek.")

while True:
    if is_work_hours():
        # Rastgelelik: %80 ihtimalle commit at (bazı saatleri boş geçmek daha doğal)
        if random.random() < 0.8:
            git_push()
        else:
            print("🕒 Bu döngü 'insansı' görünüm için pas geçildi.")

        # BEKLEME SÜRESİ (ÖNEMLİ): 
        # Test için 10-30 saniye yapmak istersen: random.randint(10, 30)
        # Gerçekçi kullanım için: 1 saat (3600 sn) ile 3 saat (10800 sn) arası
        wait_time = random.randint(1800, 7200) 
        print(f"💤 Sonraki işlem için {wait_time // 60} dakika beklenecek...")
        time.sleep(wait_time)
    else:
        print("🌙 Gece modu: Bot sabah 09:00'a kadar uyuyor...")
        time.sleep(3600)