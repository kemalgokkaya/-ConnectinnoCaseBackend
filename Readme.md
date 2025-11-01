🔹 Backend Bağlantısı ve Veri Yönetimi

Uygulamada kullanıcı bazlı not saklama yapısı bulunmaktadır.
Kullanıcı kimlik doğrulaması Firebase Authentication ile yapılmaktadır.

Not işlemlerinde kullanıcı ID’si mobil taraftan API’ye iletilmektedir.
Güvenli bir mimaride bu ID’nin API tarafında tekrar doğrulanması gerekir, ancak bu bir test case uygulaması olduğu için kullanıcı doğrulama kontrolü API içinde yapılmadan, Firebase’den alınan ID mobil taraftan direkt gönderilmiştir.

🗄 Local Veri Tabanı

Uygulama çevrimdışı kullanılabilsin diye local veritabanı olarak sqflite kullanılmıştır.
Veriler hem localde tutulmakta hem de internet erişimi olduğunda API ile senkronize edilmektedir.

🔧 CRUD İşlemleri

Aşağıdaki veri işlemleri uygulanmıştır:

İşlem	Açıklama
Create	Yeni not oluşturma ve veritabanına ekleme
Read	Not listesini kullanıcıya göre çekme
Update	Var olan bir notu güncelleme
Delete	Notu önce local veritabanından sonra API’den silme

API'yi çalıştırmak içi şu 3 komut sırayla çalıştırılmalıdır;
1- Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
2-venv\Scripts\activate   
3- uvicorn main:app --reload   