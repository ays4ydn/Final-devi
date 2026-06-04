# -*- coding: utf-8 -*-
"""
Tarım ve Su Kotası Karar Destek Simülasyonu (Çok Değişkenli İklim ve Kaynak Yönetimi)
----------------------------------------------------------------------------------
Bu simülasyon; verilen su kotası, mevsimsel yağış miktarı, ideal bitki su ihtiyacı
ve günlük baraj sulama çekimi olmak üzere 4 farklı dinamik girdinin rekolte ve
baraj ömrü üzerindeki etkilerini analiz eder.

Antigravity iş akışı analiz araçlarının veri kökenini (data lineage) ve işleme
adımlarını kusursuz şekilde izleyebileceği (traceable) biçimde tasarlanmıştır.

Akademik Kaynakça (APA Formatında):
- Allen, R. G., Pereira, L. S., Raes, D., & Smith, M. (1998). Crop evapotranspiration-Guidelines for computing crop water requirements-FAO Irrigation and drainage paper 56. FAO, Rome, 300(9), D05109.
- Doorenbos, J., & Kassam, A. H. (1979). Yield response to water. FAO Irrigation and Drainage Paper, 33, 257.
- Gleick, P. H. (2003). Global water paths. Water Policy, 5(2), 115-132.
- IPCC. (2023). Climate Change 2023: Synthesis Report. Contribution of Working Groups I, II and III to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change. IPCC, Geneva, Switzerland.
- Loucks, D. P., Van Beek, E., Stedinger, J. R., Dijkman, J. P., & Villars, M. T. (2005). Water resources systems planning and management: An introduction to methods, models and applications. UNESCO.
- Postel, S. L. (2000). Entering an era of water scarcity: The challenges ahead. Ecological Applications, 10(4), 941-948.
- Shiklomanov, I. A. (2000). Appraisal and assessment of world water resources. Water International, 25(1), 11-32.
- Steduto, P., Hsiao, T. C., Fereres, E., & Raes, D. (2012). Crop yield response to water. FAO Irrigation and Drainage Paper, 66.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def simulasyon_motoru(verilen_su_kotasi, dogal_yagis, ideal_su_ihtiyaci, gunluk_baraj_cekimi):
    """
    Antigravity Çok Değişkenli Veri Akış Hattı (Data Pipeline) Giriş ve Dönüşüm Motoru.
    Girdi parametreleri veri hattının başlangıç kaynakları (sources) olarak işlenir.
    """
    # ==========================================
    # # 1. VERİ KAYNAĞI (Data Ingestion)
    # ==========================================
    
    # REFERANS: FAO Irrigation and Drainage Paper No: 56 & IPCC (2023) - Hidrolojik Denge ve İklim Değişkenleri
    # Girdiler doğrultusunda baz verim katsayısı ve 100 tarlalık Numpy başlangıç veri kümesi atanır.
    baz_verim_dekar = 0.8  # Dekar başına düşen ideal baz rekolte (Ton)
    tarla_ids = np.arange(1, 101)

    # ==========================================
    # # 2. VERİ DÖNÜŞÜMÜ (Data Transformation)
    # ==========================================
    
    # Adım A: Tarla Varyasyon Dönüşümü (Deterministik Varyasyon Kuralları)
    # Tarlaların organik verimlilik farkı ve alanları deterministik formüllerle hesaplanır.
    toprak_faktorleri = 1.0 + 0.1 * np.sin(tarla_ids)
    alanlar_dekar = 10 + (tarla_ids % 5)
    
    # Adım B: Biyolojik Verim Oranı Dönüşümü
    # Toplam su = verilen_su_kotasi + dogal_yagis
    # FAO standartlarındaki bitki stres ve kuruma eşiği limitleri dinamik olarak hesaplanır.
    toplam_su = verilen_su_kotasi + dogal_yagis
    ust_limit_su = ideal_su_ihtiyaci + 150
    
    alt_limit_su = ust_limit_su * 0.533
    
    # MATEMATİKSEL DÖNÜŞÜM REFERANSI: FAO Paper 33 & 66, Postel (2000) - Dinamik Bitki Stres ve Kuruma Eşiği
    if toplam_su >= ust_limit_su:
        verim_orani = 1.0
    elif toplam_su >= alt_limit_su:
        verim_orani = toplam_su / ust_limit_su
    else:
        # Kuruma Eşiği: bitki kurumaya başlar ve verim sert düşer
        verim_orani = (toplam_su / ust_limit_su) * 0.3
        
    # Adım C: Baraj Tasarrufu ve Rezervuar Ömrü Dönüşümü (Çok Değişkenli Su Yönetimi)
    # Kısılan su derinliği (mm) = max(0, ideal_su_ihtiyaci - verilen_su_kotasi)
    kisilan_su_mm = max(0.0, ideal_su_ihtiyaci - verilen_su_kotasi)
    
    # OPTİMİZASYON REFERANSI: Loucks (2005), Shiklomanov (2000), Gleick (2003) - Rezervuar İşletme ve Çok Değişkenli Su Talebi Yönetimi
    # 1 mm kısıntı = dekar başına 1 metreküp (m3) su tasarrufu sağlar.
    tasarruflar_m3 = kisilan_su_mm * alanlar_dekar
    
    # Adım D: Üretilen Ürün Hesaplama (Ton)
    uretilen_urunler_ton = alanlar_dekar * baz_verim_dekar * verim_orani * toprak_faktorleri

    # ==========================================
    # # 3. VERİ ÇIKIŞI (Data Sink)
    # ==========================================
    
    # Yapılandırılmış pandas.DataFrame oluşturulması (Lineage Bütünlüğü)
    df = pd.DataFrame({
        'Tarla_ID': tarla_ids,
        'Tarla_Alani_Dekar': alanlar_dekar,
        'Toprak_Faktoru': toprak_faktorleri,
        'Verilen_Su_Kotasi_mm': verilen_su_kotasi,
        'Uretilen_Urun_Ton': uretilen_urunler_ton,
        'Tasarruf_Edilen_Su_m3': tasarruflar_m3
    })
    
    return df, verim_orani

def analiz_ve_gorsellestir(secilen_kota, canli_yagis, canli_ideal_su, canli_cekim, cikis_klasoru="."):
    """
    Simülasyon motorunu çalıştırır, terminale özet istatistikleri yazar,
    farklı girdi durumları için grafikleri su_kotasi_analiz.png adıyla kaydeder.
    """
    # 1. Seçilen girdi seti için simülasyonu çalıştır
    df_secilen, verim_orani = simulasyon_motoru(secilen_kota, canli_yagis, canli_ideal_su, canli_cekim)
    
    # Terminale .describe() çıktısını yazdırma
    print("=" * 90)
    print(f"İL TARIM VE ORMAN MÜDÜRLÜĞÜ ÇOK DEĞİŞKENLİ KARAR DESTEK RAPORU")
    print("=" * 90)
    print(f"Girdi Su Kotası (verilen_su_kotasi)   : {secilen_kota} mm")
    print(f"Doğal Mevsimsel Yağış (dogal_yagis)    : {canli_yagis} mm")
    print(f"İdeal Bitki Su İhtiyacı (ideal_su_iht) : {canli_ideal_su} mm")
    print(f"Günlük Baraj Çekimi (gunluk_cekimi)    : {canli_cekim} m3")
    print("-" * 90)
    print(f"Toplam Su (Kota + Yağış)              : {secilen_kota + canli_yagis:.1f} mm (İdeal Üst Limit: {canli_ideal_su + 150} mm)")
    print(f"Hesaplanan Bitki Verim Oranı          : %{verim_orani * 100:.2f}")
    print(f"Toplam Bölgesel Rekolte (Ürün)       : {df_secilen['Uretilen_Urun_Ton'].sum():.2f} Ton")
    
    toplam_tasarruf = df_secilen['Tasarruf_Edilen_Su_m3'].sum()
    baraj_omru_uzama = toplam_tasarruf / float(canli_cekim)
    print(f"Toplam Baraj Su Tasarrufu            : {toplam_tasarruf:.2f} m3")
    print(f"Baraj Ömrü Uzama Süresi              : {baraj_omru_uzama:.1f} Gün")
    print("-" * 90)
    print(df_secilen[['Tarla_Alani_Dekar', 'Toprak_Faktoru', 'Uretilen_Urun_Ton', 'Tasarruf_Edilen_Su_m3']].describe())
    print("=" * 90)

    # 2. Grafik 1 için Senaryolar: Su Kotası Değişimine Göre Toplam Rekolte (Çizgi Grafik)
    # Diğer 3 canli parametre sabit tutulur.
    kota_araligi_cizgi = np.arange(150, 701, 25)
    toplam_rekolteler = []
    for kota in kota_araligi_cizgi:
        df_sim, _ = simulasyon_motoru(kota, canli_yagis, canli_ideal_su, canli_cekim)
        toplam_rekolteler.append(df_sim['Uretilen_Urun_Ton'].sum())
        
    # 3. Grafik 2 için Seviyeler: Su Kotası Azaldıkça Baraj Ömrü Uzaması (Bar Grafik)
    # Belirlenen seviyeler [600, 500, 400, 300, 200] mm'ye göre hesaplanır.
    kota_araligi_bar = [600, 500, 400, 300, 200]
    baraj_omru_uzama_gunleri_bar = []
    bar_etiketleri = []
    for kota in kota_araligi_bar:
        df_sim, _ = simulasyon_motoru(kota, canli_yagis, canli_ideal_su, canli_cekim)
        tasarruf = df_sim['Tasarruf_Edilen_Su_m3'].sum()
        uzama_gun = tasarruf / float(canli_cekim)
        baraj_omru_uzama_gunleri_bar.append(uzama_gun)
        bar_etiketleri.append(f"{kota} mm")

    # 4. Matplotlib Çizimleri
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Grafik 1: Su Kotası Değişimine Göre Bölgesel Toplam Rekolte (Çizgi)
    ax1.plot(kota_araligi_cizgi, toplam_rekolteler, color='#2ca02c', linewidth=3, marker='o', markevery=2, label='Bölgesel Rekolte (Ton)')
    ax1.axvline(x=secilen_kota, color='#d62728', linestyle='--', linewidth=2, label=f'Seçilen Kota ({secilen_kota} mm)')
    
    # Kuruma Eşiği Sınırı: Toplam su < alt_limit_su => Kota = alt_limit_su - canli_yagis
    alt_limit_su = (canli_ideal_su + 150) * 0.533
    kuruma_kota_siniri = alt_limit_su - canli_yagis
    if kuruma_kota_siniri > 0:
        ax1.axvline(x=kuruma_kota_siniri, color='#ff7f0e', linestyle=':', linewidth=2, label=f'Kuruma Sınırı (Kota: {int(kuruma_kota_siniri)} mm)')
    
    # Seçilen Noktanın Vurgulanması
    secilen_rekolte = df_secilen['Uretilen_Urun_Ton'].sum()
    ax1.scatter(secilen_kota, secilen_rekolte, color='red', s=120, zorder=5)
    ax1.annotate(f"{secilen_rekolte:.1f} Ton", (secilen_kota, secilen_rekolte),
                 textcoords="offset points", xytext=(10,-10), ha='left', fontweight='bold', color='#d62728')
    
    ax1.set_title("Su Kotası Değişimine Göre Bölgesel Toplam Rekolte", fontsize=11, fontweight='bold', pad=15)
    ax1.set_xlabel("Verilen Su Kotası (mm)", fontsize=10)
    ax1.set_ylabel("Toplam Rekolte (Ton)", fontsize=10)
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc='lower right')
    
    # Grafik 2: Su Kotası Azaldıkça Baraj Ömrünün Gün Bazında Uzaması (Bar)
    bars = ax2.bar(bar_etiketleri, baraj_omru_uzama_gunleri_bar, color='#1f77b4', width=0.5, edgecolor='black', alpha=0.8)
    
    # Bar Üstlerine Değerlerin Yazılması
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, height + 10, f"+{int(height)} Gün", ha='center', va='bottom', fontweight='bold', color='#1f77b4')
        
    ax2.set_title("Su Kotası Azaldıkça Baraj Ömrünün Gün Bazında Uzaması", fontsize=11, fontweight='bold', pad=15)
    ax2.set_xlabel("Verilen Su Kotası Seviyeleri (mm)", fontsize=10)
    ax2.set_ylabel("Baraj Ömrü Uzama Süresi (Gün)", fontsize=10)
    ax2.grid(True, linestyle='--', alpha=0.4, axis='y')
    ax2.set_ylim(0, max(baraj_omru_uzama_gunleri_bar) * 1.15)
    
    plt.suptitle("Tarım ve Su Kotası Karar Destek Paneli (Çok Değişkenli İklim Simülasyonu)", fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    
    # Diske Kaydetme
    cikis_yolu = os.path.join(cikis_klasoru, "su_kotasi_analiz.png")
    plt.savefig(cikis_yolu, dpi=150)
    plt.close()
    print(f"\nAnaliz grafiği başarıyla diske kaydedildi: {cikis_yolu}")

if __name__ == "__main__":
    # Varsayılan çok değişkenli girdi parametreleri
    secilen_kota_degeri = 400   # mm
    dogal_yagis_degeri = 150    # mm
    ideal_su_degeri = 600       # mm
    gunluk_cekim_degeri = 500   # m3
    
    # Analizi çalıştır
    analiz_ve_gorsellestir(secilen_kota_degeri, dogal_yagis_degeri, ideal_su_degeri, gunluk_cekim_degeri)
