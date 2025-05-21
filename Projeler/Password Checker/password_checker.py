import hashlib
import requests

#Have I Been Pwned API'si ile şifrenin daha önce sızdırılıp sızdırılmadığını kontrol eder.
# (SHA-1 ile hashleyip ilk 5 karakterini göndererek gizliliği korur).

# Şifre gücünü değerlendiren fonksiyon
def check_strength(password):
    length_ok = len(password) >= 8
    upper = any(c.isupper() for c in password)
    lower = any(c.islower() for c in password)
    digit = any(c.isdigit() for c in password)
    symbol = any(not c.isalnum() for c in password)

    score = sum([length_ok, upper, lower, digit, symbol])

    if score >= 4:
        return "Güçlü ✅"
    elif score == 3:
        return "Orta ⚠️"
    else:
        return "Zayıf ❌"


# Şifrenin hash'ini al ve API’ye gönder
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


# Ana akış
def main():
    password = input("Şifrenizi girin: ")
    print("Şifre gücü:", check_strength(password))
    try:
        count = check_pwned(password)
        if count:
            print(f"⚠️ Bu şifre daha önce {count} kez sızdırılmış!")
        else:
            print("🔐 Bu şifre daha önce sızdırılmamış.")
    except Exception as e:
        print("Bir hata oluştu:", e)


if __name__ == "__main__":
    main()
