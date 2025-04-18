import pywhatkit as kit

#pywhatkit komutları-otomasyon

kit.sendwhatmsg_to_group("Grup adı","grup mesaj",10,31) #Whatsapp web üzerinden istenen zamanda mesaj atar.
kit.playonyt("Video ismi")  # Youtube'dan videoyu direkt oynatır
kit.info("Atatürk", lines=3)  # Wikipedia'dan bilgi çeker
kit.send_mail("Konu", "Mesaj", "mailadresi", "sifre", "hedefmailadres")  # E-posta atar

