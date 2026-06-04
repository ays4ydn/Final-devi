# İL TARIM VE ORMAN MÜDÜRLÜĞÜ KARAR DESTEK SİMÜLASYONU NİHAİ RAPORU
## FAO (33, 56, 66) & IPCC Standartlarında Canlı 2026 İklim Modellemesi ve Çok Değişkenli Rezervuar Yönetim Çözümü
### Sınırlı Su Kaynakları (Rezervuar Ömrü) ile Bölgesel Rekolte (Gıda Arzı) Arasındaki Optimum Denge Projeksiyonu

**Hazırlayan:** Ayşe Aydın (Öğrenci No: 2511317031)  
**Görevi:** İl Tarım ve Orman Müdürlüğü Veri Analitiği ve Politika Tasarım Baş Mimarı  
**Hitap Edilen Makam:** Sayın İl Tarım ve Orman Müdürü  
**Canlı Simülasyon Paneli (GitHub Pages Linki):** https://ayse-agriculture.github.io/tarim-su-simulasyonu/  
**Kaynak Kod Deposu (GitHub Repository Linki):** https://github.com/ayse-agriculture/tarim-su-simulasyonu  
**Tarih:** 4 Haziran 2026  

---

### BÖLÜM 1: YÖNETİCİ ÖZETİ (EXECUTIVE SUMMARY)

Sayın İl Müdürü,

İl sınırlarımız içerisindeki tarımsal alanların sulanması ve içme suyu sağlayan baraj göllerimizin ömrünün korunması, iklim krizinin etkilerini derinden hissettiğimiz bugünlerde birbirine tamamen zıt iki idari hedefi oluşturmaktadır. Çiftçilerimize destek olmak ve bölgesel ürün üretimini en üst düzeyde çıkarmak adına arazilere sınırsız sulama suyu verilmesi baraj göllerimizin hızla kurumasına sebep olmaktadır. Tam aksine, baraj suyunu korumak adına sulamayı aşırı düzeyde kısmak ise tarlalardaki ürünlerin kurumasına, çiftçilerimizin zarar etmesine ve gıda arzında büyük bir kriz yaşanmasına yol açmaktadır. İl Tarım ve Orman Müdürlüğü olarak idari görevimiz, tarlalardan aldığımız mahsul miktarı ile barajımızda kalan su süresi arasındaki en doğru dengeyi bilimsel verilerle bulmaktır.

Bu rapor kapsamında sunulan karar destek simülasyonu, su kotası ve baraj çekim kararlarının bölgesel rekolte ile baraj ömrü üzerindeki etkilerini eşzamanlı ve deterministik olarak tahmin etmektedir. Geliştirilen analitik model, Gıda ve Tarım Örgütü (FAO) standartlarındaki bitki stres tepki algoritmaları ile Loucks hidrolik rezervuar yönetim denklemlerini entegre etmektedir. Politika tasarım mimarisi, karar vericinin idari yetki alanındaki girdileri ile dışsal iklim faktörlerini birleştirerek anlık verim ve tasarruf çıktısı üretmektedir. Raporun sunumu, idari kararların tamamen sayısal verilere dayalı, şeffaf ve bilimsel bir yapıda şekillendirilmesini amaçlamaktadır.

---

### BÖLÜM 2: KARAR VERİCİ ENSTRÜMANLARI VE DIŞSAL DEĞİŞKENLER

İdari karar alma mekanizmasında kullandığımız girdiler, bizim kontrol edebileceğimiz idari yönetim araçları ve müdahale edemeyeceğimiz dışsal çevresel koşullar olmak üzere iki ana sınıfta tasarlanmıştır. Bu ayrım, kaynak planlamasında risklerin izlenebilirliği açısından büyük önem taşımaktadır.

#### 2.1 Politika ve Kaynak Yönetimi Girdileri (Kontrol Edilebilir Sürgüler)
1. **Verilen Su Kotası (verilen_su_kotasi):** Bizim tarlalara vanalardan yapay olarak akıttığımız sulama suyu derinliğini ifade eder. Kullanıcı arayüzünde 200 mm ile 600 mm limitleri arasında ayarlanabilmektedir. İdeal planlama değeri 600 mm seviyesindedir. Tıpkı bir çiçeği bardakla sulamak gibidir.
2. **Günlük Baraj Çekimi (gunluk_baraj_cekimi):** Barajımızın sulama şebekesine giden musluğunu ne kadar çok açtığımızı gösterir. Arayüzde 200 m3/gün ile 800 m3/gün arasında değiştirilebilir. Standart planlama değeri 500 m3/gün düzeyindedir. Musluğu çok açarsak baraj hızlı boşalır, az açarsak içindeki suyu korumuş oluruz.

#### 2.2 İklim ve Çevresel Faktörler (Dışsal Girdiler)
1. **Doğal Yağış (dogal_yagis):** Gökyüzünden bulutlar aracılığıyla arazilere doğrudan düşen yağmur miktarıdır. Bizim kontrolümüz dışındadır. Sürgü aralığı 50 mm ila 300 mm arasında olup, standart mevsim ortalaması 150 mm'dir.
2. **Bitki İdeal Su İhtiyacı (ideal_su_ihtiyaci):** Ekilen ürünün gelişim döngüsünü susuz kalmadan, en mutlu şekilde büyümesi için içmek istediği toplam su derinliğidir. Sürgü aralığı 400 mm ile 800 mm arasında olup, temel hesaplamalarda 600 mm olarak kabul edilmiştir.

![Şekil 2: Çok Değişkenli Canlı Sürgüler ve Dinamik KPI Gösterge Paneli](/yonetici_paneli.png)
*Şekil 2: Çok Değişkenli Canden Canlı Sürgüler ve Dinamik KPI Gösterge Paneli*

Şekil 2'de sunulan web kontrol panelinde, idari veya iklimsel sürgüler kaydırıldığı anda arka planda çalışan matematiksel motor hesaplamaları tetiklemekte ve üç temel KPI göstergesini güncellemektedir. Bu göstergeler sırasıyla; toplam tarımsal üretimi yansıtan 'Toplam Bölgesel Rekolte (Ton)', barajda biriken su hacmini ifade eden 'Toplam Baraj Su Tasarrufu (m3)' ve rezervuarın operasyonel ömründeki artışı gösteren 'Baraj Ömrü Uzama Süresi (Gün)' değerleridir. Dinamik arayüz sayesinde idari kararların makro etkileri eşzamanlı olarak takip edilmektedir.

![Şekil 2a: Otorite Karar ve Kaynak Yönetimi Kontrol Sürgüleri](/otorite_surguleri.png)
*Şekil 2a: Otorite Karar ve Kaynak Yönetimi Kontrol Sürgüleri*

![Şekil 2b: Dışsal İklim ve Çevresel Koşul Kontrol Sürgüleri](/iklim_surguleri.png)
*Şekil 2b: Dışsal İklim ve Çevresel Koşul Kontrol Sürgüleri*

---

### BÖLÜM 3: SİMÜLASYON MATEMATİKSEL ALTYAPISI VE PROJEKSİYON DENKLEMLERİ

Karar destek sisteminin arka planında yer alan tüm veri akış hattı (data pipeline), izlenebilirlik denetim kriterlerine tam uyumlu olarak deterministik denklemlerle kurulmuştur. Modelde rastgele sayı üreten algoritmaların kullanımı veri doğruluğunun korunması amacıyla engellenmiştir.

#### 3.1 Deterministik Veri Ambarı (Rastgelelik Yasağı İspatı)
Simülasyon kapsamında değerlendirilen 100 adet tarımsal arazinin alan ve toprak verimlilik çarpanı değerleri, her çalışma aşamasında aynı sonuçları üretecek şekilde matematiksel olarak formüle edilmiştir. Bölgemizde 100 farklı tarla vardır. Bu tarlaların her birinin büyüklüğü ve toprak kalitesi birbirinden farklıdır. Hocamızın kuralı gereği, bu tarlaları rastgele yazı tura atarak değil, belli matematiksel kurallara göre hazırladık. Arazi indeksini i (i = 1, 2, ..., 100) temsil etmek üzere formüller şu şekildedir:

Her bir arazinin büyüklüğü (da) şu formülle hesaplanır:

alan_i = 10 + (i mod 5)

Bölgedeki tarlaların toplam alanı bu formülden hareketle sabit bir değer almaktadır ve her çalıştırıldığında tam olarak aynı kalmaktadır:

Toplam_Alan = alan_1 + alan_2 + ... + alan_100 = 1200 dekar (da)

Her bir arazinin toprak yapısındaki organik madde ve besin elementi değişkenliğini yansıtan toprak verimlilik çarpanı (toprak_faktoru_i) ise trigonometrik bir dalgalanma (sinüs dalgası) ile belirlenmiştir:

toprak_faktoru_i = 1.0 + 0.1 * sin(i)

![Şekil 3: Deterministik Tarla Veritabanı ve Bireysel Dönüşüm Çizelgesi](/tarla_tablosu.png)
*Şekil 3: Deterministik Tarla Veritabanı ve Bireysel Dönüşüm Çizelgesi*

Şekil 3'te listelenen tarla detay tablosunda görüldüğü üzere, her bir tarla kendi alan ve toprak çarpanı değerlerini korumaktadır. Bu durum, veri hattı üzerinde rastgele sayıların kullanılmadığının, her tarlanın kendi toprak ve alan faktörünün korunduğunun en büyük ispatıdır. Böylece girdi ve çıktılar arasındaki nedensellik bağı doğrulanmaktadır.

#### 3.2 Biyolojik Bitki Stres Modeli (FAO 33 & 66)
Tarlaya giren toplam su girdisi (toplam_su), sulama suyu ile doğal yağışın toplamından oluşur. Tıpkı bitkiye hem gökyüzünden yağmur yağması hem de bizim yapay sulama yapmamız gibidir:

toplam_su = verilen_su_kotasi + dogal_yagis

Bitkinin en mutlu olacağı ve maksimum gelişim gösterebileceği su ihtiyacının üst sınırı (ust_limit_su), ideal su ihtiyacına 150 mm eklenerek bulunur:

ust_limit_su = ideal_su_ihtiyaci + 150

Bitkide susuzluk stresinin başladığı ve bitkinin kurumaya yüz tuttuğu kritik tehlike eşiği, dinamik alt limit (alt_limit_su) olarak tanımlanmıştır. Bu eşik, üst limitin 0.533 katıdır. Eğer arazilere verilen su bu sınırın altına düşerse bitki aniden kuruma sürecine girer:

alt_limit_su = ust_limit_su * 0.533

Bitkisel verim oranı (verim_orani), toplam su girdisine bağlı olarak parçalı bir matematiksel fonksiyon halinde hesaplanmaktadır. Bitki verimi, suya göre üç farklı durumda değerlendirilir:

* Toplam su, ust_limit_su değerinden büyük veya eşitse: verim_orani = 1.0
* Toplam su, alt_limit_su ile ust_limit_su arasındaysa: verim_orani = toplam_su / ust_limit_su
* Toplam su, alt_limit_su değerinden küçükse: verim_orani = (toplam_su / ust_limit_su) * 0.3

Belirlenen su kotası kritik kuruma eşiğinin (alt_limit_su) altına indiğinde verim oranının aniden düşmesi (0.3 katsayılı ceza fonksiyonu) bitkinin kurumaya başlamasından kaynaklanır ve FAO standartlarına dayanmaktadır. i tarlasından elde edilecek ürün miktarı (Uretilen_Urun_Ton_i), baz verim katsayısı (0.8 Ton/dekar) kullanılarak şu şekilde bulunur:

Uretilen_Urun_Ton_i = alan_i * 0.8 * verim_orani * toprak_faktoru_i

![Şekil 1: Matplotlib Tabanlı Statik Karar ve Duyarlılık Analizi Çıktısı](/su_kotasi_analiz.png)
*Şekil 1: Matplotlib Tabanlı Statik Karar ve Duyarlılık Analizi Çıktısı*

Şekil 1'de yer alan sol grafik, su kotasına bağlı olarak bölgesel rekolte değişimini çizmektedir. Kırmızı dikey çizgi anlık planlama değerini temsil ederken, turuncu kesikli çizgi kuruma sınırını göstermektedir. Bu grafik, idari kararların tarımsal üretim üzerindeki risklerini net bir şekilde ortaya koymaktadır.

#### 3.3 Hidrolik Rezervuar Optimizasyonu (Loucks Modeli)
Tarımsal sulamada yapılan su kısıntısı, baraj rezervuarında hacimsel bir su tasarrufu oluşturmaktadır. Kısılan su miktarı (kisilan_su_mm):

kisilan_su_mm = En Büyük Değer(0, ideal_su_ihtiyaci - verilen_su_kotasi)

Her bir araziden elde edilen hacimsel su tasarrufu (Tasarruf_m3_i), alan ile çarpılarak hesaplanır:

Tasarruf_m3_i = kisilan_su_mm * alan_i

Bölgesel bazda elde edilen toplam su tasarrufu (Toplam_Tasarruf) şu formülle bulunur:

Toplam_Tasarruf = Tasarruf_m3_1 + Tasarruf_m3_2 + ... + Tasarruf_m3_100

Tasarruf edilen suyun, barajın günlük çekim debisine bölünmesiyle rezervuar ömründeki uzama gün sayısı (Baraj_Omru_Uzama) hesaplanmaktadır. Barajdan ne kadar az su çekersek, barajımız o kadar çok gün boyunca su vermeye devam eder:

Baraj_Omru_Uzama = Toplam_Tasarruf / gunluk_baraj_cekimi

---

### BÖLÜM 4: ÇOK DEĞİŞKENLİ KRİZ SENARYOLARI VE DUYARLILIK ANALİZİ

Karar destek sisteminin duyarlılığını test etmek amacıyla, farklı iklim ve idari politika kombinasyonları altında 3 senaryo matematiksel olarak modellenmiştir.

#### 4.1 Senaryo A: Dengeli Politika Yönetimi (Optimum Denge)
Standart iklim koşullarında baraj ömrünün korunması ile kabul edilebilir düzeyde rekolte elde edilmesini öngören temel senaryodur. Bu durumda baraj ömrü de dengeli uzamaktadır.
- **Parametreler:** verilen_su_kotasi = 400 mm, dogal_yagis = 150 mm, ideal_su_ihtiyaci = 600 mm, gunluk_baraj_cekimi = 500 m3/gün
- **Hesaplamalar:**
  * Toplam su: 400 + 150 = 550 mm
  * En mutlu bitki su sınırı: 600 + 150 = 750 mm
  * Kuruma sınırı: 750 * 0.533 = 399.75 mm
  * Toplam su (550 mm), alt ve üst limitler arasında yer olduğundan doğrusal verim oranı: 550 / 750 = 0.7333 (%73.33 verim).
  * Kısılan su: 600 - 400 = 200 mm. Toplam baraj tasarrufu: 200 mm * 1200 da = 240.000 m3.
  * Baraj ömrü uzaması: 240.000 / 500 = 480.0 Gün.
- **Sonuç:** Bölgesel toplam rekolte 703.87 Ton seviyesinde gerçekleşirken, baraj ömrü +480.0 Gün uzatılmıştır.

#### 4.2 Senaryo B: IPCC İklim Felaketi (Aşırı Kuraklık)
Doğal yağışın neredeyse durduğu ve rezervuarların korunması için su kotasının aşırı kısıldığı kuraklık krizi senaryosudur.
- **Parametreler:** verilen_su_kotasi = 200 mm, dogal_yagis = 50 mm, ideal_su_ihtiyaci = 600 mm, gunluk_baraj_cekimi = 500 m3/gün
- **Hesaplamalar:**
  * Toplam su: 200 + 50 = 250 mm
  * En mutlu bitki su sınırı: 750 mm, Kuruma sınırı: 399.75 mm
  * Toplam su (250 mm), kritik kuruma sınırının (399.75 mm) altında kaldığı için bitki kuruma stres fonksiyonu devreye girer: (250 / 750) * 0.3 = 0.1000 (%10.0 verim oranı).
  * Kısılan su: 600 - 200 = 400 mm. Toplam baraj tasarrufu: 400 mm * 1200 da = 480.000 m3.
  * Baraj ömrü uzaması: 480.000 / 500 = 960.0 Gün.
- **Sonuç:** Bölgesel toplam rekolte 96.00 Ton seviyesine gerileyerek tarımsal üretimi durma noktasına getirmiş, öte yandan baraj rezervi +960.0 Gün uzatılarak içme suyu güvenliği teminat altına alınmıştır.

#### 4.3 Senaryo C: Adaptif Yönetim (Akıllı Vana Kurtarma Senaryosu)
Yağış verilerinin anlık takip edilerek su kotasının optimize edildiği ve baraj çekiminin artırıldığı akıllı yönetim modelidir.
- **Parametreler:** verilen_su_kotasi = 590 mm, dogal_yagis = 220 mm, ideal_su_ihtiyaci = 750 mm, gunluk_baraj_cekimi = 750 m3/gün
- **Hesaplamalar:**
  * Toplam su: 590 + 220 = 810 mm
  * En mutlu bitki su sınırı: 750 + 150 = 900 mm
  * Kuruma sınırı: 900 * 0.533 = 479.7 mm
  * Toplam su (810 mm) stres sınırları arasında kaldığından: 810 / 900 = 0.9000 (%90.0 verim oranı).
  * Kısılan su: 750 - 590 = 160 mm. Toplam baraj tasarrufu: 160 mm * 1200 da = 192.000 m3.
  * Baraj ömrü uzaması: 192.000 / 750 = 256.0 Gün.
- **Sonuç:** Tarımsal üretim kaybı minimize edilerek toplam rekolte 863.84 Ton seviyesine ulaştırılmış, günlük çekim debisinin yüksek olmasına rağmen baraj ömrü +256.0 Gün uzatılmıştır.

---

### BÖLÜM 5: GÖRSEL GÖSTERGELERİN BASİTLEŞTİRİLMİŞ AÇIKLAMASI (5 YAŞ KURALI)

Teknik veri analitiği eğitimi almamış karar vericilerin ve saha personelinin yönetim panelini kolaylıkla yorumlayabilmesi adına sistemdeki görsel öğeler günlük hayat benzetmeleriyle sadeleştirilmiştir.

#### 5.1 Sol Grafik: Toplam Rekolte Dünyası (Çizgi Grafik)
Bu grafiği, arazilerimizin toplam mahsul verme gücünü gösteren bir "Mahsul Yolu" veya "Verim Yolu" olarak düşünebiliriz.
- **Yeşil Çizgi:** Su kotasını artırdıkça tarlalardan alacağımız toplam ürünün (Ton) nasıl yükseleceğini belirten yoldur. Sürgüyü sağa doğru kaydırdıkça bu yol boyunca yukarı tırmanırız.
- **Kırmızı Dikey Çizgi ve Kırmızı Nokta:** Şu anda uygulamakta olduğumuz güncel su politikasını temsil eder. Sürgüyü kaydırdıkça bu nokta yeşil yol üzerinde ileri geri hareket eder.
- **Turuncu Noktalı Düşey Çizgi (Kuruma Sınırı):** Tarlalar için susuzluktan "Kırmızı Alarm" çizgisidir. Belirlenen su kotası bu sınırın soluna geçtiği an bitkiler susuzluktan kurur ve mahsul miktarı uçurumdan düşer gibi ani bir çöküşle dibe vurur.

#### 5.2 Sağ Grafik: Baraj Ömrü Uzaması (Bar Grafik)
Bu grafiği ise barajımızdaki suyu sakladığımız bir "Rezervuar Kumbarası" olarak düşünebiliriz. Suyu ne kadar az harcarsak kumbaramızda o kadar çok gün birikir.
- **Mavi Sütunlar:** Suyu tasarruflu kullandığımızda barajın çalışma süresinin kaç gün uzayacağını gösterir. Su kotası ne kadar düşükse, mavi sütunlar o kadar uzar.
- **Kırmızı Sütun Vurgusu:** O an seçtiğimiz kota seviyesine karşılık gelen sütun otomatik olarak kırmızı renkle boyanır. Karar verici, uyguladığı politikanın baraj ömrüne tam katkısını bu belirgin renk kodu sayesinde anında takip edebilir.

![Şekil 4: Chart.js Tooltip Callback Entegrasyonu ve Aktif Politika Vurgusu](/tooltip_etkilesimi.png)
*Şekil 4: Chart.js Tooltip Callback Entegrasyonu ve Aktif Politika Vurgusu*

Şekil 4'te sunulduğu üzere, fareyle bar grafik sütunlarının üzerine gelindiğinde interaktif bir siyah bilgi kutusu açılmakta ve seçilen politikanın veri hattı üzerindeki konumunu teyit eden "📌 Aktif Seçilen Politika Odağı" ifadesi parıldamaktadır. Bu geri bildirim, idari seçimin matematiksel doğruluğunu arayüz seviyesinde kanıtlamaktadır.

---

### BÖLÜM 6: ÇİFT KATMANLI YAZILIM MİMARİSİ (TECHNICAL TWIN)

Karar destek mekanizmasının güvenliğini ve erişilebilirliğini sağlamak amacıyla sistem iki farklı yazılım katmanında eşzamanlı (sayısal ikiz prensibine uygun) şekilde tasarlanmıştır.

#### 6.1 Analitik Motor Katmanı (simulation.py)
Python ortamında çalışan bu katman, veri bilimciler ve denetim mekanizmaları için tasarlanmış analitik altyapıdır. Pandas veri yapılarını kullanarak bölgedeki 100 tarlanın detaylı hesaplamalarını yapar, istatistik özetlerini terminale yazdırır ve matplotlib kütüphanesi vasıtasıyla statik duyarlılık eğrilerini (su_kotasi_analiz.png) üretir.

#### 6.2 İnteraktif Arayüz Katmanı (index.html, style.css, app.js)
İl Müdürü makamı ve idari uzmanların tarayıcı üzerinden sistemi doğrudan kontrol edebilmesi amacıyla geliştirilmiş web arayüzüdür. JavaScript altyapısı, Python analitik motorundaki biyolojik stres ve hidrolik modelleri tamamen kopyalayarak milisaniyeler içinde çalıştırır. Sürgüler hareket ettirildiğinde grafikler ve dinamik veri tablosu anlık olarak güncellenmektedir. Web arayüzü herhangi bir localhost veya sunucu gereksinimi duymadan, yerel dosya sistemi (file://) üzerinden bağımsız çalışabilecek yapıda optimize edilmiştir.

---

### BÖLÜM 7: POLİTİKA TEKLİFLERİ VE İDARİ TALEP METNİ

Gerçekleştirilen duyarlılık analizleri ve simülasyon çıktıları doğrultusunda, İl Tarım ve Orman Müdürlüğü idaresine sunulan somut politika önerileri ve talepler aşağıda maddeler halinde listelenmiştir:

1. **Dinamik İklim-Adaptif Sulama Kotasına Geçilmesi:** Bölgedeki tarımsal sulama kotalarının sabit tutulması yerine, mevsimlik doğal yağış (dogal_yagis) tahminleri izlenerek dinamik şekilde güncellenmesi önerilmektedir. Yağışın 220 mm düzeyine yükseldiği Senaryo C koşullarında, sulama kotası 590 mm olarak belirlenerek tarımsal verim %90 seviyesinde tutulurken baraj ömrü de +256 gün korunabilmektedir.
2. **Kritik Kuruma Alarmı Entegrasyonu:** Mevsimlik yağışın düştüğü kuraklık periyotlarında sulama suyunun toplam miktarı hiçbir koşulda biyolojik stres eşiği olan alt_limit_su değerinin altına indirilmemelidir. Eşiğin altına geçilmesi durumunda Senaryo B'de hesaplandığı üzere rekoltede %90 oranında yıkıcı bir çöküş gerçekleşmektedir.
3. **Yüksek Tasarruflu Sulama Şebekesi Teşvikleri:** Günlük baraj çekim debisini (gunluk_baraj_cekimi) minimize etmek adına modern damla sulama altyapısına yönelik hibe desteklerinin artırılması talep edilmektedir. Bu sayede baraj ömrü uzama katsayısı daha da yukarı taşınabilecektir.

---

### BÖLÜM 8: AKADEMİK REFERANSLAR

- Allen, R. G., Pereira, L. S., Raes, D., & Smith, M. (1998). *Crop evapotranspiration-Guidelines for computing crop water requirements-FAO Irrigation and drainage paper 56*. FAO, Rome, 300(9), D05109.
- Doorenbos, J., & Kassam, A. H. (1979). *Yield response to water*. FAO Irrigation and Drainage Paper, 33, 257.
- Gleick, P. H. (2003). Global water paths. *Water Policy*, 5(2), 115-132.
- IPCC. (2023). *Climate Change 2023: Synthesis Report. Contribution of Working Groups I, II and III to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change*. IPCC, Geneva, Switzerland.
- Loucks, D. P., Van Beek, E., Stedinger, J. R., Dijkman, J. P., & Villars, M. T. (2005). *Water resources systems planning and management: An introduction to methods, models and applications*. UNESCO.
- Postel, S. L. (2000). Entering an era of water scarcity: The challenges ahead. *Ecological Applications*, 10(4), 941-948.
- Shiklomanov, I. A. (2000). Appraisal and assessment of world water resources. *Water International*, 25(1), 11-32.
- Steduto, P., Hsiao, T. C., Fereres, E., & Raes, D. (2012). *Crop yield response to water*. FAO Irrigation and Drainage Paper, 66.

![Şekil 5: Akademik Referanslar ve Karar Destek Kaynakçası Arayüzü](/akademik_referanslar.png)
*Şekil 5: Akademik Referanslar ve Karar Destek Kaynakçası Arayüzü*
