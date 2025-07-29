# Mackolik İddaa Fikstur Veri Çekme Botu

Bu proje, Mackolik sitesinden iddaa ligi maç verilerini otomatik olarak çekmek için geliştirilmiş bir Selenium botu ve Tkinter GUI uygulamasıdır.

## Özellikler

- Mackolik sitesinden otomatik veri çekme
- Kullanıcı dostu Tkinter arayüzü
- İddaa liglerini otomatik listeleme
- Sezon seçimi yapabilme
- Maç verilerini Excel/CSV formatında kaydetme
- Hata yönetimi ve durum bildirimleri

## Gereksinimler

- Python 3.x
- Selenium
- BeautifulSoup4
- Tkinter (Python ile birlikte gelir)
- Pandas
- GeckoDriver (veya tercih edilen tarayıcı sürücüsü)

## Kurulum

1. Projeyi bilgisayarınıza indirin
2. Gerekli Python paketlerini yükleyin:

```bash
pip install -r requirements.txt
```

3. ChromeDriver'ı indirin ve PATH'e ekleyin veya proje klasörüne yerleştirin

## Kullanım

### GUI Uygulaması ile Kullanım

1. Uygulamayı başlatın:
```bash
python desktop_app.py
```

2. "Başlat" butonuna tıklayarak Selenium'u başlatın
3. Açılan listeden istediğiniz iddaa ligini seçin
4. "Ligi Seç" butonuna tıklayın
5. Sezon listesinden istediğiniz sezonu seçin
6. "Sezonu Seç" butonuna tıklayın
7. "Veri Çek" butonuna tıklayarak veri çekme işlemini başlatın

### Manuel Kullanım (Pipeline)

Eğer GUI kullanmadan direkt kod ile çalıştırmak isterseniz, pipeline adımları şu şekildedir:

```python
# 0. Selenium'u başlat
driver = start_selenium()

# 1. Reklamı geç
reklami_gec(driver)

# 2. Çerezleri kabul et
accept_cookies(driver, randomize_sleep_time(3))

# 3. Sayfa içeriğini al
soup = get_current_soup(driver)

# 4. İddaa liglerini listele
iddaa_ligleri_list = get_iddia_ligleri_selection_list(soup)

# 5. Lig seçimi yap
selection_iddia_lig = "ALMANYA Bundesliga"
select_iddaa_ligi(driver, selection_iddia_lig)

# 6. Sezon seçeneklerini al
sezon_list = get_sezon_selections(soup)

# 7. Sezon seçimi yap
selection_season = "2019/2020"
select_season(driver, selection_season)

# 8. Fikstur sayfasını aç
open_fikstur_page(driver, randomize_sleep_time(3))

# 9. Sezon haftalarını al
sezon_haftalari_list = get_sezon_weeks(fikstur_page_soup)

# 10. Tüm haftalık verileri topla
final_df = get_all_weeks_data(driver, sezon_haftalari_list)

# 11. Dosyayı kaydet
save_to_excel(final_df, selection_iddia_lig, selection_season)

# 12. Tarayıcıyı kapat
driver.quit()
```

## Dosya Yapısı

```
├── desktop_app.py                   # Ana GUI uygulaması
├── selenium_assistant_functions.py  # Selenium yardımcı fonksiyonları
├── requirements.txt                 # Gerekli Python paketleri
├── README.md                        # Bu dosya
└── output/                          # Çıktı dosyalarının kaydedileceği klasör
```

## Fonksiyonlar

### Ana Fonksiyonlar

- `start_selenium()`: Selenium WebDriver'ı başlatır
- `reklami_gec()`: Sitedeki reklamları geçer
- `accept_cookies()`: Çerez onayını verir
- `get_current_soup()`: Mevcut sayfanın HTML içeriğini alır
- `get_iddia_ligleri_selection_list()`: İddaa liglerini listeler
- `select_iddaa_ligi()`: Seçilen ligi aktif eder
- `get_sezon_selections()`: Mevcut sezonları listeler
- `select_season()`: Seçilen sezonu aktif eder
- `open_fikstur_page()`: Fikstur sayfasını açar
- `get_sezon_weeks()`: Sezon haftalarını listeler
- `get_all_weeks_data()`: Tüm haftalık verileri toplar
- `save_to_excel()`: Verileri Excel formatında kaydeder
- `save_to_csv()`: Verileri CSV formatında kaydeder

## Çıktı Formatı

Uygulama, seçilen lig ve sezon bilgilerine göre maç verilerini aşağıdaki formatta kaydeder:

- **Excel**: `{Lig_Adı}_{Sezon}.xlsx`
- **CSV**: `{Lig_Adı}_{Sezon}.csv`

## Dikkat Edilmesi Gerekenler

- İnternet bağlantınızın stabil olduğundan emin olun
- Mackolik sitesinin yapısı değişirse kodun güncellenmesi gerekebilir
- Çok sık istek göndermeyin, site tarafından engellenebilirsiniz
- ChromeDriver sürümünüzün Chrome tarayıcınızla uyumlu olduğundan emin olun

## Hata Giderme

- **ChromeDriver hatası**: ChromeDriver'ın doğru sürümünü indirdiğinizden emin olun
- **Element bulunamadı hatası**: Sayfanın tam yüklendiğinden emin olun, gerekirse bekleme sürelerini artırın
- **Bağlantı hatası**: İnternet bağlantınızı kontrol edin