// Tarım ve Su Kotası Karar Destek Simülasyonu - Çok Değişkenli JavaScript Motoru

// Sabitler
const BAZ_VERIM_DEKAR = 0.8; // Ton/Dekar

// 100 Tarlanın Verilerini Saklayacak Liste
let tarlas = [];

// Grafik Nesneleri
let yieldChart = null;
let damChart = null;

// ==========================================
// # 1. VERİ KAYNAĞI & BAŞLANGIÇ (Data Ingestion)
// ==========================================
function tarlalariIlkellestir() {
    tarlas = [];
    for (let i = 1; i <= 100; i++) {
        // Tarla Alanı: 10 + (tarla_id % 5) dekar (da)
        let alan = 10 + (i % 5);
        // Toprak Verimlilik Çarpanı: 1.0 + 0.1 * sin(tarla_id) (Deterministik Gürültü)
        let toprakFaktoru = 1.0 + 0.1 * Math.sin(i);
        
        tarlas.push({
            id: i,
            alan: alan,
            toprakFaktoru: toprakFaktoru
        });
    }
}

// ==========================================
// # 2. VERİ DÖNÜŞÜMÜ & SİMÜLASYON MOTORU (Transformation)
// ==========================================
function simulasyonMotoru(secilenKota, canliYagis, canliIdealSu, canliCekim) {
    let toplamSu = secilenKota + canliYagis;
    let ustLimitSu = canliIdealSu + 150;
    let verimOrani = 0.0;
    
    // Biyolojik Verim Oranı (FAO Eşik Modeli)
    let altLimitSu = ustLimitSu * 0.533;
    if (toplamSu >= ustLimitSu) {
        verimOrani = 1.0;
    } else if (toplamSu >= altLimitSu) {
        verimOrani = toplamSu / ustLimitSu;
    } else {
        // Kuruma Eşiği
        verimOrani = (toplamSu / ustLimitSu) * 0.3;
    }
    
    // Kısılan Su
    let kisilanSu = Math.max(0.0, canliIdealSu - secilenKota);
    
    let toplamRekolte = 0;
    let toplamTasarruf = 0;
    
    let hesaplananTarlalar = tarlas.map(tarla => {
        // Üretilen Ürün (Ton) = Alan * Baz Verim * Verim Oranı * Toprak Faktörü
        let uretilenUrun = tarla.alan * BAZ_VERIM_DEKAR * verimOrani * tarla.toprakFaktoru;
        // Tasarruf Edilen Su (m³) = Kısılan Su (mm) * Alan
        let tasarruf = kisilanSu * tarla.alan;
        
        toplamRekolte += uretilenUrun;
        toplamTasarruf += tasarruf;
        
        return {
            id: tarla.id,
            alan: tarla.alan,
            toprakFaktoru: tarla.toprakFaktoru,
            verilenSu: secilenKota,
            uretilenUrun: uretilenUrun,
            tasarruf: tasarruf
        };
    });
    
    // Baraj Ömrü Uzama (Loucks 2005)
    let barajOmruUzama = toplamTasarruf / canliCekim;
    
    return {
        tarlalar: hesaplananTarlalar,
        verimOrani: verimOrani,
        toplamRekolte: toplamRekolte,
        toplamTasarruf: toplamTasarruf,
        barajOmruUzama: barajOmruUzama
    };
}

// ==========================================
// # 3. VERİ ÇIKIŞI & ARAYÜZ GÜNCELLEME (Data Sink)
// ==========================================
function arayuzuGuncelle() {
    // 4 Sürgünün canli değerlerini oku
    let quota = parseInt(document.getElementById("quota-slider").value);
    let release = parseInt(document.getElementById("release-slider").value);
    let rain = parseInt(document.getElementById("rain-slider").value);
    let req = parseInt(document.getElementById("req-slider").value);
    
    const sonuclar = simulasyonMotoru(quota, rain, req, release);
    
    // 1. KPI Kartlarının Güncellenmesi
    document.getElementById("kpi-total-yield").innerText = sonuclar.toplamRekolte.toFixed(2) + " Ton";
    document.getElementById("kpi-total-savings").innerText = sonuclar.toplamTasarruf.toLocaleString("tr-TR") + " m³";
    document.getElementById("kpi-dam-extension").innerText = "+" + sonuclar.barajOmruUzama.toFixed(1) + " Gün";
    
    // Verim Durumu Metni ve Rengi (FAO Stres Modeli)
    let statusText = "";
    let statusClass = "";
    let toplamSu = quota + rain;
    let ustLimitSu = req + 150;
    let altLimitSu = ustLimitSu * 0.533;
    if (toplamSu >= ustLimitSu) {
        statusText = "Optimum Su Kaynağı (%100 Verim)";
        statusClass = "status-optimal";
    } else if (toplamSu >= altLimitSu) {
        statusText = `Sınırlı Su Kaynağı (Verim Oranı: %${(sonuclar.verimOrani * 100).toFixed(1)})`;
        statusClass = "status-limited";
    } else {
        statusText = "Kritik Eşik Aşındı - Kuruma Tehlikesi!";
        statusClass = "status-critical";
    }
    
    const statusLabel = document.getElementById("kpi-status-yield");
    statusLabel.innerText = statusText;
    statusLabel.className = "kpi-subtext " + statusClass;
    
    // 2. Tablonun Güncellenmesi
    const tbody = document.getElementById("fields-table-body");
    tbody.innerHTML = "";
    
    // Tablonun çok büyük olup tarayıcıyı yormaması için ilk 15 tarlayı gösterelim
    const gosterilecekTarlalar = sonuclar.tarlalar.slice(0, 15);
    gosterilecekTarlalar.forEach(tarla => {
        let tr = document.createElement("tr");
        tr.innerHTML = `
            <td>#${tarla.id}</td>
            <td>${tarla.alan} da</td>
            <td>${tarla.toprakFaktoru.toFixed(4)}</td>
            <td>${tarla.verilenSu} mm</td>
            <td style="color: var(--success-color); font-weight: 600;">${tarla.uretilenUrun.toFixed(2)} Ton</td>
            <td style="color: var(--primary-color); font-weight: 600;">${tarla.tasarruf.toLocaleString("tr-TR")} m³</td>
        `;
        tbody.appendChild(tr);
    });
    
    let trEllipsis = document.createElement("tr");
    trEllipsis.innerHTML = `
        <td colspan="6" style="text-align: center; color: var(--text-muted); font-style: italic;">
            ... 100 tarlanın diğer kayıtları arka planda simüle edilmektedir. CSV Olarak Dışa Aktar butonuyla tüm listeyi indirebilirsiniz. ...
        </td>
    `;
    tbody.appendChild(trEllipsis);
    
    // 3. Grafiklerin Güncellenmesi
    grafikleriGuncelle(quota, rain, req, release, sonuclar.toplamRekolte);
}

// CSV İndirme İşlemi (O anki 4 sürgü durumuna göre)
function csvIndir() {
    let quota = parseInt(document.getElementById("quota-slider").value);
    let release = parseInt(document.getElementById("release-slider").value);
    let rain = parseInt(document.getElementById("rain-slider").value);
    let req = parseInt(document.getElementById("req-slider").value);
    
    const sonuclar = simulasyonMotoru(quota, rain, req, release);
    
    let csvContent = "data:text/csv;charset=utf-8,\uFEFF";
    csvContent += "Tarla_ID,Tarla_Alani_Dekar,Toprak_Faktoru,Verilen_Su_Kotasi_mm,Uretilen_Urun_Ton,Tasarruf_Edilen_Su_m3\n";
    
    sonuclar.tarlalar.forEach(t => {
        csvContent += `${t.id},${t.alan},${t.toprakFaktoru.toFixed(6)},${t.verilenSu},${t.uretilenUrun.toFixed(4)},${t.tasarruf.toFixed(2)}\n`;
    });
    
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `tarla_iklim_kaynak_analizi_q${quota}_r${rain}_s${req}_c${release}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// ==========================================
// # 4. GRAFİK KURULUM VE GÜNCELLEME (Chart.js)
// ==========================================
function grafikleriKur() {
    const ctxYield = document.getElementById("yield-chart").getContext("2d");
    yieldChart = new Chart(ctxYield, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Toplam Bölgesel Rekolte (Ton)',
                    data: [],
                    borderColor: '#10b981',
                    borderWidth: 3,
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    fill: true,
                    tension: 0.1,
                    pointRadius: 0
                },
                {
                    label: 'Seçilen Kota Konumu',
                    data: [],
                    borderColor: '#ef4444',
                    backgroundColor: '#ef4444',
                    pointRadius: 7,
                    pointHoverRadius: 9,
                    showLine: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#94a3b8', font: { family: 'Inter', size: 11 } }
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' },
                    title: { display: true, text: 'Su Kotası (mm)', color: '#94a3b8' }
                },
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' },
                    title: { display: true, text: 'Üretim (Ton)', color: '#94a3b8' }
                }
            }
        }
    });

    const ctxDam = document.getElementById("dam-chart").getContext("2d");
    damChart = new Chart(ctxDam, {
        type: 'bar',
        data: {
            labels: ["600 mm", "500 mm", "400 mm", "300 mm", "200 mm"],
            datasets: [{
                label: 'Baraj Ömrü Uzama Süresi (Gün)',
                data: [],
                backgroundColor: [],
                borderColor: [],
                borderWidth: 1,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#94a3b8', font: { family: 'Inter', size: 11 } }
                },
                tooltip: {
                    callbacks: {
                        // # INTERAKTIF VERI IZLEME REFERANSI: Kullanıcı etkileşimi anında aktif senaryo odağının veri hattı üzerinden görsel olarak doğrulanması
                        footer: function(tooltipItems) {
                            let item = tooltipItems[0];
                            let dataIndex = item.dataIndex;
                            let dataset = item.dataset;
                            let color = dataset.backgroundColor[dataIndex];
                            if (color === '#ef4444') {
                                return '📌 Aktif Seçilen Politika Odağı';
                            }
                            return '';
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' },
                    title: { display: true, text: 'Uygulanan Kota Seviyesi', color: '#94a3b8' }
                },
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' },
                    title: { display: true, text: 'Baraj Ömrü Uzaması (Gün)', color: '#94a3b8' }
                }
            }
        }
    });
}

function grafikleriGuncelle(secilenKota, canliYagis, canliIdealSu, canliCekim, aktifRekolte) {
    if (!yieldChart || !damChart) return;
    
    // 1. Rekolte Grafiği Güncelleme (Line chart'ı canli yağış ve ideal su girdilerine göre dinamik yeniden çizme!)
    let kotaAraligi = [];
    let rekolteEgrisi = [];
    // # GÖRSEL VERİ HATTI SENKRONİZASYONU: UI girdi sınırları ile grafik x ekseni veri projeksiyon sınırlarının birebir senkronize edilmesi.
    for (let k = 200; k <= 600; k += 25) {
        kotaAraligi.push(k);
        let res = simulasyonMotoru(k, canliYagis, canliIdealSu, canliCekim);
        rekolteEgrisi.push(res.toplamRekolte);
    }
    
    yieldChart.data.labels = kotaAraligi;
    yieldChart.data.datasets[0].data = rekolteEgrisi;
    yieldChart.data.datasets[1].data = [{ x: secilenKota, y: aktifRekolte }];
    yieldChart.update();
    
    // 2. Baraj Ömrü Grafiği Güncelleme (Bar chart verisini canli çekim ve ideal su durumlarına göre güncelleme!)
    const barSeviyeleri = [600, 500, 400, 300, 200];
    let barVerileri = barSeviyeleri.map(k => {
        let res = simulasyonMotoru(k, canliYagis, canliIdealSu, canliCekim);
        return res.barajOmruUzama;
    });
    
    const backgroundColors = barSeviyeleri.map(k => {
        // Seçilen kota konumundaki barı kırmızıya boya
        return Math.abs(secilenKota - k) < 5 ? '#ef4444' : '#3b82f6';
    });
    
    damChart.data.datasets[0].data = barVerileri;
    damChart.data.datasets[0].backgroundColor = backgroundColors;
    damChart.update();
}

// ==========================================
// # 5. OLAY YÖNETİCİLERİ VE BAŞLANGIÇ
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
    // 1. Tarlaları Başlat
    tarlalariIlkellestir();
    
    // 2. Grafiklerin Temelini Kur
    grafikleriKur();
    
    // 3. Sürgüler, Çıktı Kutuları ve Butonları Bağla
    const sliders = [
        { id: "quota-slider", outputId: "quota-value", suffix: " mm" },
        { id: "release-slider", outputId: "release-value", suffix: " m³" },
        { id: "rain-slider", outputId: "rain-value", suffix: " mm" },
        { id: "req-slider", outputId: "req-value", suffix: " mm" }
    ];
    
    sliders.forEach(s => {
        const sliderEl = document.getElementById(s.id);
        const outputEl = document.getElementById(s.outputId);
        
        // İlk değerleri yaz
        outputEl.innerText = sliderEl.value + s.suffix;
        
        // Değişim dinleyicisi
        sliderEl.addEventListener("input", (e) => {
            outputEl.innerText = e.target.value + s.suffix;
            arayuzuGuncelle();
        });
    });
    
    // CSV Butonu
    document.getElementById("download-csv-btn").addEventListener("click", csvIndir);
    
    // Kaynakça Butonu
    const referencesBtn = document.getElementById("toggle-references-btn");
    const referencesContent = document.getElementById("references-content");
    referencesBtn.addEventListener("click", () => {
        referencesContent.classList.toggle("hidden");
    });
    
    // İlk arayüz çizimi
    arayuzuGuncelle();
});
