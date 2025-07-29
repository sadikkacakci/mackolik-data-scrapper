from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
import os
import random
import pandas as pd

def start_selenium():
    # Firefox options
    options = Options()
    # options.add_argument("-headless")  # Headless aktif etmek istersen bunu aç
    # Şu an görünür tarayıcı açılacak

    # Geckodriver path
    gecko_path = os.path.join(os.getcwd(), "geckodriver.exe")
    service = FirefoxService(executable_path=gecko_path)

    # Başlat
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://arsiv.mackolik.com/Puan-Durumu")
    return driver

def reklami_gec(driver, timeout=10):
    """Sayfadaki 'Reklamı Geç' butonuna tıklamaya çalışır."""
    try:
        skip_ad_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Reklamı Geç')]"))
        )
        skip_ad_button.click()
        print("Reklam kapatıldı.")
    except Exception as e:
        print("Reklam bulunamadı veya otomatik geçildi.")

def randomize_sleep_time(hedef_saniye: float, oran: float = 0.2) -> float:
    """
    Verilen saniyenin ±%oran kadar yakınlarında rastgele bir süre döner.
    Örn: hedef_saniye=5, oran=0.2 → 4.0 ile 6.0 arasında.
    """
    minimum = hedef_saniye * (1 - oran)
    maksimum = hedef_saniye * (1 + oran)
    return round(random.uniform(minimum, maksimum), 2)

def open_fikstur_page(driver, timeout=10):
    """
    Sayfadaki 'Fikstür' sekmesini tıklamaya çalışır.
    Başarılı olursa True, aksi halde False döner.
    """
    try:
        fikstur_tab = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Fikstür')]"))
        )
        fikstur_tab.click()
        # Ajax yüklenmesini bekle
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cboWeek"))
        )
        print("Fikstür sekmesine tıklandı.")
        return True
    except Exception as e:
        print("Fikstür sekmesi bulunamadı:", e)
        return False

def accept_cookies(driver, timeout=10):
    """
    Sayfadaki 'Çerezleri Kabul Et' butonuna tıklamaya çalışır.
    Başarılı olursa True, aksi halde False döner.
    """
    try:
        accept_cookies_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "accept-all-btn"))
        )
        accept_cookies_button.click()
        print("Çerezler kabul edildi.")
        return True
    except Exception as e:
        print("Çerez butonu bulunamadı veya zaten kapanmış olabilir.", e)
        return False
    
def get_current_soup(driver):
    """
    Selenium driver ile güncel sayfa kaynağını alır ve BeautifulSoup nesnesi döner.
    """
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    return soup

def get_iddia_ligleri_selection_list(soup):
    """
    BeautifulSoup nesnesinden 'cboLeague' ID'li <select> içindeki
    lig adlarını ve value'larını bir liste olarak döner.
    
    Dönüş: List[Tuple[str, str]] → [(lig_adi, lig_kodu), ...]
    """
    iddaa_ligleri_list = []
    select_ligler = soup.find("select", {"id": "cboLeague"})

    if select_ligler:
        options = select_ligler.find_all("option")
        for option in options:
            lig_adi = option.text.strip()
            # lig_kodu = option.get("value")
            iddaa_ligleri_list.append(lig_adi)

    return iddaa_ligleri_list

def select_iddaa_ligi(driver, selection):
    """
    İddaa Ligi dropdown'ından verilen lig adını seçer.
    Seçimden sonra reklam çıkarsa kapatır ve rastgele bir süre bekler.
    """
    try:
        select_lig_dropdown = Select(driver.find_element(By.ID, "cboLeague"))
        select_lig_dropdown.select_by_visible_text(selection)
        print(f"İddaa Ligi seçildi: {selection}")
    except Exception as e:
        print("İddaa Ligi seçilemedi:", e)

def get_sezon_weeks(soup):
    """
    BeautifulSoup nesnesinden 'cboWeek' ID'li <select> içindeki
    sezon haftalarını [(hafta_adı, hafta_kodu)] formatında döner.
    """
    sezon_haftalari_list = []
    select_haftalar = soup.find("select", {"id": "cboWeek"})

    if select_haftalar:
        options = select_haftalar.find_all("option")
        for option in options:
            hafta_adi = option.text.strip()       # Görünen metin
            # hafta_kodu = option.get("value")      # Option value
            sezon_haftalari_list.append(hafta_adi)

    return sezon_haftalari_list

def get_sezon_selections(soup):
    """
    BeautifulSoup nesnesinden 'cboSeason' ID'li <select> içindeki
    sezon adlarını ve value'larını [(sezon_adi, sezon_kodu)] şeklinde döner.
    """
    sezon_list = []
    select_sezon = soup.find("select", {"id": "cboSeason"})

    if select_sezon:
        options = select_sezon.find_all("option")
        for option in options:
            sezon_adi = option.text.strip()
            # sezon_kodu = option.get("value")
            sezon_list.append(sezon_adi)

    return sezon_list

def select_season(driver, selection_season):
    """
    'cboSeason' dropdown'ından verilen sezon adını seçer.
    
    Parametreler:
    - driver: Selenium WebDriver nesnesi
    - selection_season: Görünür sezon metni (örneğin '2021/2022')
    """
    try:
        sezon_dropdown = Select(driver.find_element(By.ID, "cboSeason"))
        sezon_dropdown.select_by_visible_text(selection_season)
        print(f"Sezon seçildi: {selection_season}")
    except Exception as e:
        print(f"Sezon seçimi başarısız: {selection_season}", e)

def select_week(driver, selection_week):
    """
    'cboWeek' dropdown'ından verilen hafta metnine göre seçim yapar.
    """
    try:
        # DropDown menü etkileşime hazır olana kadar bekle
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "cboWeek"))
        )

        hafta_dropdown = Select(driver.find_element(By.ID, "cboWeek"))
        hafta_dropdown.select_by_visible_text(selection_week)
        print(f"Sezon haftası seçildi: {selection_week}")
    except Exception as e:
        print(f"Sezon haftası seçilemedi: {selection_week}", e)


def parse_fikstur_table(soup):
    """
    'dvPage > dvFixtureInner > table.list-table' yapısındaki fikstür tablosunu parse eder.
    
    Args:
        soup (BeautifulSoup): Sayfanın HTML yapısı
    
    Returns:
        pandas.DataFrame: Maç bilgilerini içeren DataFrame
    """
    match_list = []

    # Belirli yol: dvPage > dvFixtureInner > table.list-table
    fixture_div = soup.find("div", id="dvPage")
    if not fixture_div:
        return pd.DataFrame(match_list)

    inner_div = fixture_div.find("div", id="dvFixtureInner")
    if not inner_div:
        return pd.DataFrame(match_list)

    table = inner_div.find("table", class_="list-table")
    if not table:
        return pd.DataFrame(match_list)

    # Satırları al (header'ı atla)
    rows = table.find_all("tr")[1:]

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 9:
            continue

        # Tarih ve saat
        date_cell = cells[0].get_text(strip=True)
        time_cell = cells[1].get_text(strip=True)

        # Ev sahibi takım
        home_team_link = cells[3].find("a")
        team_home = home_team_link.get_text(strip=True) if home_team_link else cells[3].get_text(strip=True)

        # Skor
        score_link = cells[5].find("a")
        score_text = score_link.get_text(strip=True) if score_link else cells[5].get_text(strip=True)

        # Deplasman takımı
        away_team_link = cells[7].find("a")
        team_away = away_team_link.get_text(strip=True) if away_team_link else cells[7].get_text(strip=True)

        # İlk yarı skoru
        half_score = cells[8].get_text(strip=True)

        match_list.append({
            "Tarih": date_cell,
            "Saat": time_cell,
            "Ev Sahibi": team_home,
            "Skor": score_text,
            "Deplasman": team_away,
            "İlk Yarı Skor": half_score
        })

    return pd.DataFrame(match_list)


def get_all_weeks_data(driver, sezon_haftalari_list):
    """
    Tüm sezon haftalarını gezerek fikstür verilerini çeker ve tek bir DataFrame olarak döner.
    
    Parameters:
        driver: Selenium WebDriver örneği
        sezon_haftalari_list: Seçilecek hafta isimlerini içeren liste

    Returns:
        final_df: Tüm haftaların birleştirilmiş verilerini içeren pandas DataFrame
    """
    all_week_data = []
    print(sezon_haftalari_list)
    for selection_week in sezon_haftalari_list:
        try:
            select_week(driver, selection_week)
            time.sleep(randomize_sleep_time(3))

            soup = get_current_soup(driver)
            time.sleep(randomize_sleep_time(3))
            # print(soup)
            df = parse_fikstur_table(soup)

            if df is not None and not df.empty:
                df["Hafta"] = selection_week  # Hangi haftadan geldiği belli olsun
                all_week_data.append(df)
                print(f"{selection_week} verisi eklendi.")
            else:
                print(f"{selection_week} için veri bulunamadı veya boş.")
        except Exception as e:
            print(f"{selection_week} haftası işlenirken hata oluştu:", e)

    if all_week_data:
        final_df = pd.concat(all_week_data, ignore_index=True)
        return final_df
    else:
        return pd.DataFrame()  # Hiç veri toplanamadıysa boş df döner

def save_to_excel(df, selection_iddia_lig, selection_season):
    """
    DataFrame'i Excel dosyası olarak kaydeder (index olmadan).
    
    Args:
        df (pd.DataFrame): Kaydedilecek veriler
        selection_iddia_lig (str): Lig adı veya kodu
        selection_season (str): Sezon bilgisi
    """
    # Geçersiz karakterleri temizle
    safe_season = selection_season.replace("/", "-")
    
    filename = f"{selection_iddia_lig}_{safe_season}.xlsx"
    try:
        df.to_excel(filename, index=False)
        print(f"Veri Excel dosyasına kaydedildi: {filename}")
    except Exception as e:
        print(f"Excel'e kaydetme hatası: {e}")

def save_to_csv(df, selection_iddia_lig, selection_season):
    """
    DataFrame'i CSV dosyası olarak kaydeder (index olmadan).
    
    Args:
        df (pd.DataFrame): Kaydedilecek veriler
        selection_iddia_lig (str): Lig adı veya kodu
        selection_season (str): Sezon bilgisi
    """
    # Geçersiz karakterleri temizle
    safe_season = selection_season.replace("/", "-")
    
    filename = f"{selection_iddia_lig}_{safe_season}.csv"
    try:
        df.to_csv(filename, index=False)
        print(f"Veri CSV dosyasına kaydedildi: {filename}")
    except Exception as e:
        print(f"CSV'ye kaydetme hatası: {e}")

def format_date(date_str, week_info):
    """
    Tarih string'ini gün/ay/yıl formatına çevirir.
    Hafta bilgisinde iki farklı yıl varsa, tarihin ayına göre doğru yılı seçer.
    
    Args:
        date_str (str): Orijinal tarih string'i (örn: "16/08")
        week_info (str): Hafta bilgisi string'i (örn: "1 (28.12.2019 - 04.01.2020)")
    
    Returns:
        str: Formatlanmış tarih (gün/ay/yıl)
    """
    import re
    from datetime import datetime
    
    if not week_info or "/" not in date_str:
        return date_str
    
    # Tarih string'ini parse et
    parts = date_str.split("/")
    if len(parts) < 2:
        return date_str
    
    day = int(parts[0])
    month = int(parts[1])
    
    # Hafta bilgisinden tüm tarihleri çıkar (örn: "28.12.2019" ve "04.01.2020")
    date_pattern = r'(\d{1,2})\.(\d{1,2})\.(\d{4})'
    date_matches = re.findall(date_pattern, week_info)
    
    if not date_matches:
        # Eski format için fallback (sadece bir yıl varsa)
        year_match = re.search(r'(\d{4})', week_info)
        if year_match:
            year = year_match.group(1)
            return f"{day:02d}/{month:02d}/{year}"
        return date_str
    
    # Hafta aralığındaki tarihleri kontrol et
    possible_years = []
    for match in date_matches:
        match_day, match_month, match_year = int(match[0]), int(match[1]), int(match[2])
        possible_years.append(match_year)
        
        # Eğer gün ve ay tam olarak eşleşiyorsa, o yılı kullan
        if day == match_day and month == match_month:
            return f"{day:02d}/{month:02d}/{match_year}"
    
    # Tam eşleşme yoksa, ayına göre mantıklı yılı seç
    if len(set(possible_years)) > 1:  # İki farklı yıl varsa
        min_year = min(possible_years)
        max_year = max(possible_years)
        
        # Sezon mantığı: Ağustos-Aralık -> eski yıl, Ocak-Temmuz -> yeni yıl
        if month >= 8:  # Ağustos-Aralık
            selected_year = min_year
        else:  # Ocak-Temmuz
            selected_year = max_year
            
        return f"{day:02d}/{month:02d}/{selected_year}"
    
    # Tek yıl varsa onu kullan
    return f"{day:02d}/{month:02d}/{possible_years[0]}"

# """-PIPELINE-"""
# 0. Selenium'u başlat.
# driver = start_selenium()

# # 1. Reklamı Geç butonuna tıklamaya çalış
# reklami_gec(driver)
# time.sleep(randomize_sleep_time(4))

# # 2. Çerezleri kabul et
# accept_cookies(driver,randomize_sleep_time(3))

# # 3. Soup'u al.
# time.sleep(randomize_sleep_time(3))  # sekme geçişinden sonra içerik yüklensin
# soup = get_current_soup(driver)

# # 4. İddia Ligleri Selectionlarını al.
# iddaa_ligleri_list = get_iddia_ligleri_selection_list(soup)

# # 5. İddia Ligleri Selection
# selection_iddia_lig = "ALMANYA Bundesliga"
# # selection_iddia_lig = "BULGARİSTAN 1.Lig"
# select_iddaa_ligi(driver, selection_iddia_lig)
# reklami_gec(driver, randomize_sleep_time(5))
# time.sleep(randomize_sleep_time(3))
# soup = get_current_soup(driver)
# time.sleep(randomize_sleep_time(4))

# # 6. Sezon Seçeneklerini Al.
# sezon_list = get_sezon_selections(soup)
# print(sezon_list)
# time.sleep(randomize_sleep_time(3))

# # 7. Sezon Seçimi Yap.
# selection_season = "2019/2020"
# select_season(driver,selection_season)
# time.sleep(randomize_sleep_time(4))

# # 7. Select Fisktur
# open_fikstur_page(driver, randomize_sleep_time(3))
# time.sleep(randomize_sleep_time(3))
# fikstur_page_soup = get_current_soup(driver)

# # 8. Sezon Haftalarını Al.
# sezon_haftalari_list = get_sezon_weeks(fikstur_page_soup)
# time.sleep(randomize_sleep_time(6))

# # 9. Tüm haftalar için veriyi topla
# final_df = get_all_weeks_data(driver, sezon_haftalari_list)
# print(final_df)
# print(final_df.head())

# # 10. Dosyayı kaydet.
# save_to_excel(final_df, selection_iddia_lig, selection_season)

# # 11. Driver'ı sonlandır.
# driver.quit()
