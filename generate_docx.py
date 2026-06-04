# -*- coding: utf-8 -*-
"""
Word (.docx) formatında "Nihai Karar Destek Sistemi Analiz Raporu" oluşturucu betik.
Dosya bozulma risklerini ortadan kaldırmak için şema dışı düşük seviyeli XML modifikasyonları temizlenmiştir.
Tüm formüller, İl Müdürü'nün ve saha personelinin rahatça okuyabileceği temiz yazı formatında sunulmuştur.
"""

import os
import sys

def check_and_install_dependencies():
    try:
        import docx
    except ImportError:
        print("python-docx modülü bulunamadı. Yükleniyor...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])
        print("python-docx başarıyla yüklendi.")

# Bağımlılıkları kontrol et
check_and_install_dependencies()

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_report():
    dest_dir = r"C:\Users\AYŞE\OneDrive\Desktop\FinalÖdevi\simülasyon2"
    doc = Document()
    
    # Sayfa Kenar Boşluklarını Ayarla (Standart 2.54 cm)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Başlık Stili
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_p.add_run("İL TARIM VE ORMAN MÜDÜRLÜĞÜ\nKARAR DESTEK SİMÜLASYONU NİHAİ RAPORU")
    title_run.bold = True
    title_run.font.name = 'Arial'
    title_run.font.size = Pt(16)
    title_run.font.color.rgb = RGBColor(17, 24, 39) # Koyu Gri
    title_p.paragraph_format.space_before = Pt(12)
    title_p.paragraph_format.space_after = Pt(6)

    # Alt Başlık Stili
    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_run = sub_p.add_run("FAO (33, 56, 66) & IPCC Standartlarında Canlı 2026 İklim Modellemesi ve Çok Değişkenli Rezervuar Yönetim Çözümü\n"
                            "Sınırlı Su Kaynakları (Rezervuar Ömrü) ile Bölgesel Rekolte (Gıda Arzı) Arasındaki Optimum Denge Projeksiyonu")
    sub_run.italic = True
    sub_run.font.name = 'Arial'
    sub_run.font.size = Pt(10.5)
    sub_run.font.color.rgb = RGBColor(75, 85, 99) # Orta Gri
    sub_p.paragraph_format.space_after = Pt(18)

    # Üst Bilgi Bloğu
    info_p = doc.add_paragraph()
    info_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    info_run = info_p.add_run(
        "Hazırlayan: Ayşe Aydın (Öğrenci No: 2511317031)\n"
        "Görevi: İl Tarım ve Orman Müdürlüğü Veri Analitiği ve Politika Tasarım Baş Mimarı\n"
        "Hitap Edilen Makam: Sayın İl Tarım ve Orman Müdürü\n"
        "Canlı Simülasyon Paneli (GitHub Pages Linki): https://ayse-agriculture.github.io/tarim-su-simulasyonu/\n"
        "Kaynak Kod Deposu (GitHub Repository Linki): https://github.com/ayse-agriculture/tarim-su-simulasyonu\n"
        "Tarih: 4 Haziran 2026"
    )
    info_run.font.name = 'Arial'
    info_run.font.size = Pt(9.5)
    info_run.font.color.rgb = RGBColor(107, 114, 128)
    info_p.paragraph_format.space_after = Pt(24)

    # Bölüm Başlığı Fonksiyonu
    def add_heading(text, space_before=18):
        h = doc.add_paragraph()
        h_run = h.add_run(text)
        h_run.bold = True
        h_run.font.name = 'Arial'
        h_run.font.size = Pt(13)
        h_run.font.color.rgb = RGBColor(37, 99, 235) # Şık Mavi Renk (Bozulma riski oluşturan XML kenarlık kodu yerine güvenli renklendirme)
        h.paragraph_format.space_before = Pt(space_before)
        h.paragraph_format.space_after = Pt(6)
        return h

    # Alt Başlık Fonksiyonu
    def add_subheading(text):
        h = doc.add_paragraph()
        h_run = h.add_run(text)
        h_run.bold = True
        h_run.font.name = 'Arial'
        h_run.font.size = Pt(11)
        h_run.font.color.rgb = RGBColor(55, 65, 81)
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(4)
        return h

    # Gövde Metni Ekleme Fonksiyonu
    def add_body(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(10.5)
        run.font.color.rgb = RGBColor(31, 41, 55)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        return p

    # Temiz Matematiksel Formül Ekleme Fonksiyonu (Merkez Hizalı, Dolar ve LaTeX Kodsuz)
    def add_formula(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(17, 24, 39)
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        return p

    # Görsel Ekleme Fonksiyonu
    def add_figure(img_path, caption):
        if os.path.exists(img_path):
            img_p = doc.add_paragraph()
            img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            img_run = img_p.add_run()
            img_run.add_picture(img_path, width=Inches(5.5))
            img_p.paragraph_format.space_before = Pt(8)
            img_p.paragraph_format.space_after = Pt(4)
            
            cap_p = doc.add_paragraph()
            cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap_run = cap_p.add_run(caption)
            cap_run.italic = True
            cap_run.font.name = 'Arial'
            cap_run.font.size = Pt(9)
            cap_run.font.color.rgb = RGBColor(107, 114, 128)
            cap_p.paragraph_format.space_after = Pt(10)
        else:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(f"[Görsel Kayıp: {os.path.basename(img_path)} bulunamadı]\n{caption}")
            run.italic = True
            run.font.color.rgb = RGBColor(220, 38, 38)
            p.paragraph_format.space_after = Pt(10)

    # ----------------------------------------------------
    # BÖLÜM 1: YÖNETİCİ ÖZETİ
    # ----------------------------------------------------
    add_heading("BÖLÜM 1: YÖNETİCİ ÖZETİ (EXECUTIVE SUMMARY)", space_before=12)
    add_body("Sayın İl Müdürü,")
    add_body(
        "İl sınırlarımız içerisindeki tarımsal alanların sulanması ve içme suyu sağlayan baraj göllerimizin ömrünün korunması, iklim krizinin etkilerini derinden hissettiğimiz bugünlerde birbirine tamamen zıt iki idari hedefi oluşturmaktadır. Çiftçilerimize destek olmak ve bölgesel ürün üretimini en üst düzeyde çıkarmak adına arazilere sınırsız sulama suyu verilmesi baraj göllerimizin hızla kurumasına sebep olmaktadır. Tam aksine, baraj suyunu korumak adına sulamayı aşırı düzeyde kısmak ise tarlalardaki ürünlerin kurumasına, çiftçilerimizin zarar etmesine ve gıda arzında büyük bir kriz yaşanmasına yol açmaktadır. İl Tarım ve Orman Müdürlüğü olarak idari görevimiz, tarlalardan aldığımız mahsul miktarı ile barajımızda kalan su süresi arasındaki en doğru dengeyi bilimsel verilerle bulmaktır."
    )
    add_body(
        "Bu rapor kapsamında sunulan karar destek simülasyonu, su kotası ve baraj çekim kararlarının bölgesel rekolte ile baraj ömrü üzerindeki etkilerini eşzamanlı ve deterministik olarak tahmin etmektedir. Geliştirilen analitik model, Gıda ve Tarım Örgütü (FAO) standartlarındaki bitki stres tepki algoritmaları ile Loucks hidrolik rezervuar yönetim denklemlerini entegre etmektedir. Politika tasarım mimarisi, karar vericinin idari yetki alanındaki girdileri ile dışsal iklim faktörlerini birleştirerek anlık verim ve tasarruf çıktısı üretmektedir. Raporun sunumu, idari kararların tamamen sayısal verilere dayalı, şeffaf ve bilimsel bir yapıda şekillendirilmesini amaçlamaktadır."
    )

    # ----------------------------------------------------
    # BÖLÜM 2: KARAR VERİCİ ENSTRÜMANLARI
    # ----------------------------------------------------
    add_heading("BÖLÜM 2: KARAR VERİCİ ENSTRÜMANLARI VE DIŞSAL DEĞİŞKENLER")
    add_body(
        "İdari karar alma mekanizmasında kullandığımız girdiler, bizim kontrol edebileceğimiz idari yönetim araçları ve müdahale edemeyeceğimiz dışsal çevresel koşullar olmak üzere iki ana sınıfta tasarlanmıştır. Bu ayrım, kaynak planlamasında risklerin izlenebilirliği açısından büyük önem taşımaktadır."
    )
    
    add_subheading("2.1 Politika ve Kaynak Yönetimi Girdileri (Kontrol Edilebilir Sürgüler)")
    add_body(
        "1. Verilen Su Kotası (verilen_su_kotasi): Bizim tarlalara vanalardan yapay olarak akıttığımız sulama suyu derinliğini ifade eder. Kullanıcı arayüzünde 200 mm ile 600 mm limitleri arasında ayarlanabilmektedir. İdeal planlama değeri 600 mm seviyesindedir. Tıpkı bir çiçeği bardakla sulamak gibidir."
    )
    add_body(
        "2. Günlük Baraj Çekimi (gunluk_baraj_cekimi): Barajımızın sulama şebekesine giden musluğunu ne kadar çok açtığımızı gösterir. Arayüzde 200 m3/gün ile 800 m3/gün arasında değiştirilebilir. Standart planlama değeri 500 m3/gün düzeyindedir. Musluğu çok açarsak baraj hızlı boşalır, az açarsak içindeki suyu korumuş oluruz."
    )
    
    add_subheading("2.2 İklim ve Çevresel Faktörler (Dışsal Girdiler)")
    add_body(
        "1. Doğal Yağış (dogal_yagis): Gökyüzünden bulutlar aracılığıyla arazilere doğrudan düşen yağmur miktarıdır. Bizim kontrolümüz dışındadır. Sürgü aralığı 50 mm ila 300 mm arasında olup, standart mevsim ortalaması 150 mm'dir."
    )
    add_body(
        "2. Bitki İdeal Su İhtiyacı (ideal_su_ihtiyaci): Ekilen ürünün gelişim döngüsünü susuz kalmadan, en mutlu şekilde büyümesi için içmek istediği toplam su derinliğidir. Sürgü aralığı 400 mm ile 800 mm arasında olup, temel hesaplamalarda 600 mm olarak kabul edilmiştir."
    )

    # Şekil 2 Ekle
    fig2_path = os.path.join(dest_dir, "yonetici_paneli.png")
    add_figure(fig2_path, "Şekil 2: Çok Değişkenli Canlı Sürgüler ve Dinamik KPI Gösterge Paneli (yonetici_paneli.png)")

    add_body(
        "Şekil 2'de sunulan web kontrol panelinde, idari veya iklimsel sürgüler kaydırıldığı anda arka planda çalışan matematiksel motor hesaplamaları tetiklemekte ve üç temel KPI göstergesini güncellemektedir. Bu göstergeler sırasıyla; toplam tarımsal üretimi yansıtan 'Toplam Bölgesel Rekolte (Ton)', barajda biriken su hacmini ifade eden 'Toplam Baraj Su Tasarrufu (m3)' ve rezervuarın operasyonel ömründeki artışı gösteren 'Baraj Ömrü Uzama Süresi (Gün)' değerleridir. Dinamik arayüz sayesinde idari kararların makro etkileri eşzamanlı olarak takip edilmektedir."
    )

    # Sürgü Detay Alt Şekilleri
    fig2a_path = os.path.join(dest_dir, "otorite_surguleri.png")
    add_figure(fig2a_path, "Şekil 2a: Otorite Karar ve Kaynak Yönetimi Kontrol Sürgüleri (otorite_surguleri.png)")

    fig2b_path = os.path.join(dest_dir, "iklim_surguleri.png")
    add_figure(fig2b_path, "Şekil 2b: Dışsal İklim ve Çevresel Koşul Kontrol Sürgüleri (iklim_surguleri.png)")

    # ----------------------------------------------------
    # BÖLÜM 3: SİMÜLASYON MATEMATİKSEL ALTYAPISI
    # ----------------------------------------------------
    add_heading("BÖLÜM 3: SİMÜLASYON MATEMATİKSEL ALTYAPISI VE PROJEKSİYON DENKLEMLERİ")
    add_body(
        "Karar destek sisteminin arka planında yer alan tüm veri akış hattı (data pipeline), izlenebilirlik denetim kriterlerine tam uyumlu olarak deterministik denklemlerle kurulmuştur. Modelde rastgele sayı üreten algoritmaların kullanımı veri doğruluğunun korunması amacıyla engellenmiştir."
    )
    
    add_subheading("3.1 Deterministik Veri Ambarı (Rastgelelik Yasağı İspatı)")
    add_body(
        "Simülasyon kapsamında değerlendirilen 100 adet tarımsal arazinin alan ve toprak verimlilik çarpanı değerleri, her çalışma aşamasında aynı sonuçları üretecek şekilde matematiksel olarak formüle edilmiştir. Bölgemizde 100 farklı tarla vardır. Bu tarlaların her birinin büyüklüğü ve toprak kalitesi birbirinden farklıdır. Hocamızın kuralı gereği, bu tarlaları rastgele yazı tura atarak değil, belli matematiksel kurallara göre hazırladık. Arazi indeksini i (i = 1, 2, ..., 100) temsil etmek üzere formüller şu şekildedir:"
    )

    add_body("Her bir arazinin büyüklüğü (da) şu formülle hesaplanır:")
    add_formula("alan_i = 10 + (i mod 5)")
    
    add_body("Bölgedeki tarlaların toplam alanı bu formülden hareketle sabit bir değer almaktadır ve her çalıştırıldığında tam olarak aynı kalmaktadır:")
    add_formula("Toplam_Alan = alan_1 + alan_2 + ... + alan_100 = 1200 dekar (da)")
    
    add_body("Her bir arazinin toprak yapısındaki organik madde ve besin elementi değişkenliğini yansıtan toprak verimlilik çarpanı (toprak_faktoru_i) ise trigonometrik bir dalgalanma (sinüs dalgası) ile belirlenmiştir:")
    add_formula("toprak_faktoru_i = 1.0 + 0.1 * sin(i)")

    # Şekil 3 Ekle
    fig3_path = os.path.join(dest_dir, "tarla_tablosu.png")
    add_figure(fig3_path, "Şekil 3: Deterministik Tarla Veritabanı ve Bireysel Dönüşüm Çizelgesi (tarla_tablosu.png)")

    add_body(
        "Şekil 3'te listelenen tarla detay tablosunda görüldüğü üzere, her bir tarla kendi alan ve toprak çarpanı değerlerini korumaktadır. Bu durum, veri hattı üzerinde rastgele sayıların kullanılmadığının, her tarlanın kendi toprak ve alan faktörünün korunduğunun en büyük ispatıdır. Böylece girdi ve çıktılar arasındaki nedensellik bağı doğrulanmaktadır."
    )

    add_subheading("3.2 Biyolojik Bitki Stres Modeli (FAO 33 & 66)")
    add_body(
        "Tarlaya giren toplam su girdisi (toplam_su), sulama suyu ile doğal yağışın toplamından oluşur. Tıpkı bitkiye hem gökyüzünden yağmur yağması hem de bizim yapay sulama yapmamız gibidir:"
    )
    add_formula("toplam_su = verilen_su_kotasi + dogal_yagis")
    
    add_body(
        "Bitkinin en mutlu olacağı ve maksimum gelişim gösterebileceği su ihtiyacının üst sınırı (ust_limit_su), ideal su ihtiyacına 150 mm eklenerek bulunur:"
    )
    add_formula("ust_limit_su = ideal_su_ihtiyaci + 150")
    
    add_body(
        "Bitkide susuzluk stresinin başladığı ve bitkinin kurumaya yüz tuttuğu kritik tehlike eşiği, dinamik alt limit (alt_limit_su) olarak tanımlanmıştır. Bu eşik, üst limitin 0.533 katıdır. Eğer arazilere verilen su bu sınırın altına düşerse bitki aniden kuruma sürecine girer:"
    )
    add_formula("alt_limit_su = ust_limit_su * 0.533")
    
    add_body(
        "Bitkisel verim oranı (verim_orani), toplam su girdisine bağlı olarak parçalı bir matematiksel fonksiyon halinde hesaplanmaktadır. Bitki verimi, suya göre üç farklı durumda değerlendirilir:"
    )
    add_formula("Toplam su, ust_limit_su değerinden büyük veya eşitse: verim_orani = 1.0")
    add_formula("Toplam su, alt_limit_su ile ust_limit_su arasındaysa: verim_orani = toplam_su / ust_limit_su")
    add_formula("Toplam su, alt_limit_su değerinden küçükse: verim_orani = (toplam_su / ust_limit_su) * 0.3")
    
    add_body(
        "Belirlenen su kotası kritik kuruma eşiğinin (alt_limit_su) altına indiğinde verim oranının aniden düşmesi (0.3 katsayılı ceza fonksiyonu) bitkinin kurumaya başlamasından kaynaklanır ve FAO standartlarına dayanmaktadır. i tarlasından elde edilecek ürün miktarı (Uretilen_Urun_Ton_i), baz verim katsayısı (0.8 Ton/dekar) kullanılarak şu şekilde bulunur:"
    )
    add_formula("Uretilen_Urun_Ton_i = alan_i * 0.8 * verim_orani * toprak_faktoru_i")

    # Şekil 1 Ekle
    fig1_path = os.path.join(dest_dir, "su_kotasi_analiz.png")
    add_figure(fig1_path, "Şekil 1: Matplotlib Tabanlı Statik Karar ve Duyarlılık Analizi Çıktısı (su_kotasi_analiz.png)")

    add_body(
        "Şekil 1'de yer alan sol grafik, su kotasına bağlı olarak bölgesel rekolte değişimini çizmektedir. Kırmızı dikey çizgi anlık planlama değerini temsil ederken, turuncu kesikli çizgi kuruma sınırını göstermektedir. Bu grafik, idari kararların tarımsal üretim üzerindeki risklerini net bir şekilde ortaya koymaktadır."
    )

    add_subheading("3.3 Hidrolik Rezervuar Optimizasyonu (Loucks Modeli)")
    add_body(
        "Tarımsal sulamada yapılan su kısıntısı, baraj rezervuarında hacimsel bir su tasarrufu oluşturmaktadır. Kısılan su miktarı (kisilan_su_mm):"
    )
    add_formula("kisilan_su_mm = En Büyük Değer(0, ideal_su_ihtiyaci - verilen_su_kotasi)")
    
    add_body(
        "Her bir araziden elde edilen hacimsel su tasarrufu (Tasarruf_m3_i), alan ile çarpılarak hesaplanır:"
    )
    add_formula("Tasarruf_m3_i = kisilan_su_mm * alan_i")
    
    add_body(
        "Bölgesel bazda elde edilen toplam su tasarrufu (Toplam_Tasarruf) şu formülle bulunur:"
    )
    add_formula("Toplam_Tasarruf = Tasarruf_m3_1 + Tasarruf_m3_2 + ... + Tasarruf_m3_100")
    
    add_body(
        "Tasarruf edilen suyun, barajın günlük çekim debisine bölünmesiyle rezervuar ömründeki uzama gün sayısı (Baraj_Omru_Uzama) hesaplanmaktadır. Barajdan ne kadar az su çekersek, barajımız o kadar çok gün boyunca su vermeye devam eder:"
    )
    add_formula("Baraj_Omru_Uzama = Toplam_Tasarruf / gunluk_baraj_cekimi")

    # ----------------------------------------------------
    # BÖLÜM 4: KRİZ SENARYOLARI
    # ----------------------------------------------------
    add_heading("BÖLÜM 4: ÇOK DEĞİŞKENLİ KRİZ SENARYOLARI VE DUYARLILIK ANALİZİ")
    add_body(
        "Karar destek sisteminin duyarlılığını test etmek amacıyla, farklı iklim ve idari politika kombinasyonları altında 3 senaryo matematiksel olarak modellenmiştir."
    )
    
    add_subheading("4.1 Senaryo A: Dengeli Politika Yönetimi (Optimum Denge)")
    add_body("Standart iklim koşullarında baraj ömrünün korunması ile kabul edilebilir düzeyde rekolte elde edilmesini öngören temel senaryodur. Bu durumda baraj ömrü de dengeli uzamaktadır.")
    add_body("- Parametreler: verilen_su_kotasi = 400 mm, dogal_yagis = 150 mm, ideal_su_ihtiyaci = 600 mm, gunluk_baraj_cekimi = 500 m3/gün")
    add_body("- Hesaplamalar:")
    add_body("  * Toplam su: 400 + 150 = 550 mm")
    add_body("  * En mutlu bitki su sınırı: 600 + 150 = 750 mm")
    add_body("  * Kuruma sınırı: 750 * 0.533 = 399.75 mm")
    add_body("  * Toplam su (550 mm), alt ve üst limitler arasında yer aldığından doğrusal verim oranı: 550 / 750 = 0.7333 (%73.33 verim).")
    add_body("  * Kısılan su: 600 - 400 = 200 mm. Toplam baraj tasarrufu: 200 mm * 1200 da = 240.000 m3.")
    add_body("  * Baraj ömrü uzaması: 240.000 / 500 = 480.0 Gün.")
    add_body("- Sonuç: Bölgesel toplam rekolte 703.87 Ton seviyesinde gerçekleşirken, baraj ömrü +480.0 Gün uzatılmıştır.")

    add_subheading("4.2 Senaryo B: IPCC İklim Felaketi (Aşırı Kuraklık)")
    add_body("Doğal yağışın neredeyse durduğu ve rezervuarların korunması için su kotasının aşırı kısıldığı kuraklık krizi senaryosudur.")
    add_body("- Parametreler: verilen_su_kotasi = 200 mm, dogal_yagis = 50 mm, ideal_su_ihtiyaci = 600 mm, gunluk_baraj_cekimi = 500 m3/gün")
    add_body("- Hesaplamalar:")
    add_body("  * Toplam su: 200 + 50 = 250 mm")
    add_body("  * En mutlu bitki su sınırı: 750 mm, Kuruma sınırı: 399.75 mm")
    add_body("  * Toplam su (250 mm), kritik kuruma sınırının (399.75 mm) altında kaldığı için bitki kuruma stres fonksiyonu devreye girer: (250 / 750) * 0.3 = 0.1000 (%10.0 verim oranı).")
    add_body("  * Kısılan su: 600 - 200 = 400 mm. Toplam baraj tasarrufu: 400 mm * 1200 da = 480.000 m3.")
    add_body("  * Baraj ömrü uzaması: 480.000 / 500 = 960.0 Gün.")
    add_body("- Sonuç: Bölgesel toplam rekolte 96.00 Ton seviyesine gerileyerek tarımsal üretimi durma noktasına getirmiş, öte yandan baraj rezervi +960.0 Gün uzatılarak içme suyu güvenliği teminat altına alınmıştır.")

    add_subheading("4.3 Senaryo C: Adaptif Yönetim (Akıllı Vana Kurtarma Senaryosu)")
    add_body("Yağış verilerinin anlık takip edilerek su kotasının optimize edildiği ve baraj çekiminin artırıldığı akıllı yönetim modelidir.")
    add_body("- Parametreler: verilen_su_kotasi = 590 mm, dogal_yagis = 220 mm, ideal_su_ihtiyaci = 750 mm, gunluk_baraj_cekimi = 750 m3/gün")
    add_body("- Hesaplamalar:")
    add_body("  * Toplam su: 590 + 220 = 810 mm")
    add_body("  * En mutlu bitki su sınırı: 750 + 150 = 900 mm")
    add_body("  * Kuruma sınırı: 900 * 0.533 = 479.7 mm")
    add_body("  * Toplam su (810 mm) stres sınırları arasında kaldığından: 810 / 900 = 0.9000 (%90.0 verim oranı).")
    add_body("  * Kısılan su: 750 - 590 = 160 mm. Toplam baraj tasarrufu: 160 mm * 1200 da = 192.000 m3.")
    add_body("  * Baraj ömrü uzaması: 192.000 / 750 = 256.0 Gün.")
    add_body("- Sonuç: Tarımsal üretim kaybı minimize edilerek toplam rekolte 863.84 Ton seviyesine ulaştırılmış, günlük çekim debisinin yüksek olmasına rağmen baraj ömrü +256.0 Gün uzatılmıştır.")

    # ----------------------------------------------------
    # BÖLÜM 5: GÖRSEL GÖSTERGELER (5 YAŞ KURALI)
    # ----------------------------------------------------
    add_heading("BÖLÜM 5: GÖRSEL GÖSTERGELERİN BASİTLEŞTİRİLMİŞ AÇIKLAMASI (5 YAŞ KURALI)")
    add_body(
        "Teknik veri analitiği eğitimi almamış karar vericilerin ve saha personelinin yönetim panelini kolaylıkla yorumlayabilmesi adına sistemdeki görsel öğeler günlük hayat benzetmeleriyle sadeleştirilmiştir."
    )
    add_subheading("5.1 Sol Grafik: Toplam Rekolte Dünyası (Çizgi Grafik)")
    add_body(
        "Bu grafiği, arazilerimizin toplam mahsul verme gücünü gösteren bir 'Mahsul Yolu' veya 'Verim Yolu' olarak düşünebiliriz."
    )
    add_body(
        "- Yeşil Çizgi: Su kotasını artırdıkça tarlalardan alacağımız toplam ürünün (Ton) nasıl yükseleceğini belirten yoldur. Sürgüyü sağa doğru kaydırdıkça bu yol boyunca yukarı tırmanırız."
    )
    add_body(
        "- Kırmızı Dikey Çizgi ve Kırmızı Nokta: Şu anda uygulamakta olduğumuz güncel su politikasını temsil eder. Sürgüyü kaydırdıkça bu nokta yeşil yol üzerinde ileri geri hareket eder."
    )
    add_body(
        "- Turuncu Noktalı Düşey Çizgi (Kuruma Sınırı): Tarlalar için susuzluktan 'Kırmızı Alarm' çizgisidir. Belirlenen su kotası bu sınırın soluna geçtiği an bitkiler susuzluktan kurur ve mahsul miktarı uçurumdan düşer gibi ani bir çöküşle dibe vurur."
    )
    
    add_subheading("5.2 Sağ Grafik: Baraj Ömrü Uzaması (Bar Grafik)")
    add_body(
        "Bu grafiği ise barajımızdaki suyu sakladığımız bir 'Rezervuar Kumbarası' olarak düşünebiliriz. Suyu ne kadar az harcarsak kumbaramızda o kadar çok gün birikir."
    )
    add_body(
        "- Mavi Sütunlar: Suyu tasarruflu kullandığımızda barajın çalışma süresinin kaç gün uzayacağını gösterir. Su kotası ne kadar düşükse, mavi sütunlar o kadar uzar."
    )
    add_body(
        "- Kırmızı Sütun Vurgusu: O an seçtiğimiz kota seviyesine karşılık gelen sütun otomatik olarak kırmızı renkle boyanır. Karar verici, uyguladığı politikanın baraj ömrüne tam katkısını bu belirgin renk kodu sayesinde anında takip edebilir."
    )

    # Şekil 4 Ekle
    fig4_path = os.path.join(dest_dir, "tooltip_etkilesimi.png")
    add_figure(fig4_path, "Şekil 4: Chart.js Tooltip Callback Entegrasyonu ve Aktif Politika Vurgusu (tooltip_etkilesimi.png)")

    add_body(
        "Şekil 4'te görüldüğü üzere, fareyle bar grafik sütunlarının üzerine gelindiğinde interaktif bir siyah bilgi kutusu açılmakta ve seçilen politikanın veri hattı üzerindeki konumunu teyit eden '📌 Aktif Seçilen Politika Odağı' ifadesi parıldamaktadır. Bu geri bildirim, idari seçimin matematiksel doğruluğunu arayüz seviyesinde kanıtlamaktadır."
    )

    # ----------------------------------------------------
    # BÖLÜM 6: YAZILIM MİMARİSİ
    # ----------------------------------------------------
    add_heading("BÖLÜM 6: ÇİFT KATMANLI YAZILIM MİMARİSİ (TECHNICAL TWIN)")
    add_body(
        "Karar destek mekanizmasının güvenliğini ve erişilebilirliğini sağlamak amacıyla sistem iki farklı yazılım katmanında eşzamanlı (sayısal ikiz prensibine uygun) şekilde tasarlanmıştır."
    )
    add_subheading("6.1 Analitik Motor Katmanı (simulation.py)")
    add_body(
        "Python ortamında çalışan bu katman, veri bilimciler ve denetim mekanizmaları için tasarlanmış analitik altyapıdır. Pandas veri yapılarını kullanarak bölgedeki 100 tarlanın detaylı hesaplamalarını yapar, istatistik özetlerini terminale yazdırır ve matplotlib kütüphanesi vasıtasıyla statik duyarlılık eğrilerini (su_kotasi_analiz.png) üretir."
    )
    add_subheading("6.2 İnteraktif Arayüz Katmanı (index.html, style.css, app.js)")
    add_body(
        "İl Müdürü makamı ve idari uzmanların tarayıcı üzerinden sistemi doğrudan kontrol edebilmesi amacıyla geliştirilmiş web arayüzüdür. JavaScript altyapısı, Python analitik motorundaki biyolojik stres ve hidrolik modelleri tamamen kopyalayarak milisaniyeler içinde çalıştırır. Sürgüler hareket ettirildiğinde grafikler ve dinamik veri tablosu anlık olarak güncellenmektedir. Web arayüzü herhangi bir localhost veya sunucu gereksinimi duymadan, yerel dosya sistemi (file://) üzerinden bağımsız çalışabilecek yapıda optimize edilmiştir."
    )

    # ----------------------------------------------------
    # BÖLÜM 7: POLİTİKA TEKLİFLERİ
    # ----------------------------------------------------
    add_heading("BÖLÜM 7: POLİTİKA TEKLİFLERİ VE İDARİ TALEP METNİ")
    add_body(
        "Gerçekleştirilen duyarlılık analizleri ve simülasyon çıktıları doğrultusunda, İl Tarım ve Orman Müdürlüğü idaresine sunulan somut politika önerileri ve talepler aşağıda maddeler halinde listelenmiştir:"
    )
    add_body(
        "1. Dinamik İklim-Adaptif Sulama Kotasına Geçilmesi: Bölgedeki tarımsal sulama kotalarının sabit tutulması yerine, mevsimlik doğal yağış (dogal_yagis) tahminleri izlenerek dinamik şekilde güncellenmesi önerilmektedir. Yağışın 220 mm düzeyine yükseldiği Senaryo C koşullarında, sulama kotası 590 mm olarak belirlenerek tarımsal verim %90 seviyesinde tutulurken baraj ömrü de +256 gün korunabilmektedir."
    )
    add_body(
        "2. Kritik Kuruma Alarmı Entegrasyonu: Mevsimlik yağışın düştüğü kuraklık periyotlarında sulama suyunun toplam miktarı hiçbir koşulda biyolojik stres eşiği olan alt_limit_su değerinin altına indirilmemelidir. Eşiğin altına geçilmesi durumunda Senaryo B'de hesaplandığı üzere rekoltede %90 oranında yıkıcı bir çöküş gerçekleşmektedir."
    )
    add_body(
        "3. Yüksek Tasarruflu Sulama Şebekesi Teşvikleri: Günlük baraj çekim debisini (gunluk_baraj_cekimi) minimize etmek adına modern damla sulama altyapısına yönelik hibe desteklerinin artırılması talep edilmektedir. Bu sayede baraj ömrü uzama katsayısı daha da yukarı taşınabilecektir."
    )

    # ----------------------------------------------------
    # BÖLÜM 8: AKADEMİK REFERANSLAR
    # ----------------------------------------------------
    add_heading("BÖLÜM 8: AKADEMİK REFERANSLAR")
    add_body(
        "- Allen, R. G., Pereira, L. S., Raes, D., & Smith, M. (1998). Crop evapotranspiration-Guidelines for computing crop water requirements-FAO Irrigation and drainage paper 56. FAO, Rome, 300(9), D05109."
    )
    add_body(
        "- Doorenbos, J., & Kassam, A. H. (1979). Yield response to water. FAO Irrigation and Drainage Paper, 33, 257."
    )
    add_body(
        "- Gleick, P. H. (2003). Global water paths. Water Policy, 5(2), 115-132."
    )
    add_body(
        "- IPCC. (2023). Climate Change 2023: Synthesis Report. Contribution of Working Groups I, II and III to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change. IPCC, Geneva, Switzerland."
    )
    add_body(
        "- Loucks, D. P., Van Beek, E., Stedinger, J. R., Dijkman, J. P., & Villars, M. T. (2005). Water resources systems planning and management: An introduction to methods, models and applications. UNESCO."
    )
    add_body(
        "- Postel, S. L. (2000). Entering an era of water scarcity: The challenges ahead. Ecological Applications, 10(4), 941-948."
    )
    add_body(
        "- Shiklomanov, I. A. (2000). Appraisal and assessment of world water resources. Water International, 25(1), 11-32."
    )
    add_body(
        "- Steduto, P., Hsiao, T. C., Fereres, E., & Raes, D. (2012). Crop yield response to water. FAO Irrigation and Drainage Paper, 66."
    )

    # Şekil 5 Ekle (Referanslar Arayüzü)
    fig5_path = os.path.join(dest_dir, "akademik_referanslar.png")
    add_figure(fig5_path, "Şekil 5: Akademik Referanslar ve Karar Destek Kaynakçası Arayüzü (akademik_referanslar.png)")

    # Raporu Kaydet (PermissionError durumunda alternatif dosya adı kullanır)
    output_filename = os.path.join(dest_dir, "Tarim_ve_Su_Kotasi_Karar_Destek_Raporu.docx")
    try:
        doc.save(output_filename)
        print(f"Rapor başarıyla oluşturuldu ve kaydedildi: {output_filename}")
    except PermissionError:
        alternative_filename = os.path.join(dest_dir, "Tarim_ve_Su_Kotasi_Karar_Destek_Raporu_Yeni.docx")
        doc.save(alternative_filename)
        print(f"UYARI: Orijinal dosya Word programında açık olduğundan yeni sürüm şuraya kaydedildi: {alternative_filename}")

if __name__ == "__main__":
    create_report()
