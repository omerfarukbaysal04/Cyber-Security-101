import hashlib
import requests
import tkinter as tk
from tkinter import ttk, messagebox


def check_strength(password):
    length_ok = len(password) >= 8
    upper = any(c.isupper() for c in password)
    lower = any(c.islower() for c in password)
    digit = any(c.isdigit() for c in password)
    symbol = any(not c.isalnum() for c in password)

    score = sum([length_ok, upper, lower, digit, symbol])

    if score >= 4:
        return "Güçlü ✅", "green"
    elif score == 3:
        return "Orta ⚠️", "orange"
    else:
        return "Zayıf ❌", "red"


def check_pwned(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = sha1_password[:5], sha1_password[5:]

    url = f"https://api.pwnedpasswords.com/range/{first5}"
    response = requests.get(url)

    if response.status_code != 200:
        raise RuntimeError("API hatası:", response.status_code)

    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == tail:
            return int(count)
    return 0


def evaluate_password():
    password = password_var.get()
    if not password:
        messagebox.showwarning("Uyarı", "Lütfen bir şifre girin.")
        return

    strength, color = check_strength(password)
    try:
        count = check_pwned(password)
        if count:
            result = f"Şifre Gücü: {strength}\n⚠️ Bu şifre {count} kez sızdırılmış!"
        else:
            result = f"Şifre Gücü: {strength}\n🔐 Bu şifre daha önce sızdırılmamış."
    except Exception as e:
        result = f"Hata oluştu: {e}"
        color = "red"

    result_label.config(text=result, foreground=color)


def toggle_password_visibility():
    entry.config(show="" if show_password.get() else "*")


# GUI Başlat
root = tk.Tk()
root.title("Şifre Denetleyici")
root.geometry("420x260")
root.resizable(False, False)

# Tema için ttk kullanımı
style = ttk.Style()
style.theme_use("clam")

# Değişkenler
password_var = tk.StringVar()
show_password = tk.BooleanVar()

# Arayüz Elemanları
ttk.Label(root, text="Şifrenizi girin:").pack(pady=(15, 5))
entry = ttk.Entry(root, textvariable=password_var, width=40, show="*")
entry.pack()

ttk.Checkbutton(
    root, text="Şifreyi Göster", variable=show_password,
    command=toggle_password_visibility
).pack(pady=5)

ttk.Button(root, text="Değerlendir", command=evaluate_password).pack(pady=10)

result_label = ttk.Label(root, text="", wraplength=380, justify="center", font=("Segoe UI", 10, "bold"))
result_label.pack(pady=10)

root.mainloop()
