# Güvenli Kimlik Doğrulama Sistemi (2FA Destekli)

![image](https://github.com/user-attachments/assets/3b59208d-8e69-4dff-acd1-d5dc4b9e34b2)


Bu proje, Flask tabanlı, iki faktörlü kimlik doğrulama (2FA) içeren güvenli bir kullanıcı kayıt ve giriş sistemidir. Kullanıcıların şifreleri `bcrypt` ile hashlenir, giriş sonrası e-posta yoluyla doğrulama kodu gönderilir ve bu kod ile ikinci bir kimlik doğrulama gerçekleştirilir.

## Özellikler

- Kullanıcı kayıt ve giriş  
- Şifrelerin güvenli şekilde hashlenmesi (bcrypt)  
- E-posta ile 2FA doğrulama kodu gönderimi  
- JWT tabanlı güvenli oturum yönetimi  
- Zaman sınırlı 2FA kodları (5 dakika)  
- Flash mesajlar ile kullanıcı bilgilendirme  
- Basit ve kullanıcı dostu arayüz  

## Kurulum ve Çalıştırma

1. Projeyi klonlayın veya indirin:  
   `git clone https://github.com/kullaniciadi/proje-adi.git`  
   `cd proje-adi`  

2. Sanal ortam oluşturup aktif edin (opsiyonel):  
   `python3 -m venv venv`  
   `source venv/bin/activate` (Linux/Mac)  
   `venv\Scripts\activate` (Windows)  

3. Gerekli paketleri yükleyin:  
   `pip install -r requirements.txt`  

4. Ortam değişkenlerini ayarlayın (`.env` veya app config):  
   - MAIL_SERVER  
   - MAIL_PORT  
   - MAIL_USERNAME  
   - MAIL_PASSWORD  
   - SECRET_KEY  
   - JWT_SECRET_KEY  

5. Uygulamayı başlatın:  
   `python app.py`  

## Proje Dosya Yapısı
/app
/templates
base.html
index.html
login.html
register.html
dashboard.html
verify_2fa.html
/static
style.css
app.py
requirements.txt
README.md

![image](https://github.com/user-attachments/assets/8421b5ae-ee93-4974-b6ef-fbcfdf35083f)

![image](https://github.com/user-attachments/assets/59e80e3d-6ca1-4936-ba02-20eca9c94737)

![image](https://github.com/user-attachments/assets/879d4df0-6f43-4737-aa8b-f373b3c63fc9)



