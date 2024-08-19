import pygame
import sys
import random



# Oyun açıklaması
def oyun_aciklamasi():
    return """
    TAŞ, KAĞIT, MAKAS OYUNU - AÇIKLAMA:

    Bu oyun iki oyuncu arasında oynanır: Oyuncu ve Bilgisayar.
    Oyun Seçenekleri:

    - Taş: Ellerin yumruk şeklinde kapalı olması.
    - Kağıt: Elin düz açık şekilde tutulması.
    - Makas: İşaret ve orta parmakların açık, diğer parmakların kapalı olması.

    KAZANMA KURALLARI:
    - Taş, makası ezer (Taş > Makas).
    - Kağıt, taşı sarar (Kağıt > Taş).
    - Makas, kağıdı keser (Makas > Kağıt).

    Eğer iki oyuncu aynı seçeneği seçerse, oyun berabere biter.

    AMAÇ:
    - Oyunun amacı, belirli bir sayıda galibiyet kazanmak.
    - Bu oyunda iki galibiyete ulaşan oyuncu oyunun galibi olur.

    Oyunun başında her iki oyuncu da aynı anda bir seçim yapar.
    Oyun döngüsü devam ederken seçimler karşılaştırılır ve kazanan belirlenir.
    """

# Pygame'i başlat
pygame.init()

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Ekran boyutları
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Taş, Kağıt, Makas Oyunu')

# Yazı tipleri
font = pygame.font.SysFont("Arial", 24)
aciklama_font = pygame.font.SysFont("Arial", 20)

# Müzik dosyasını yükle
pygame.mixer.music.load("mymusicfile.mp3")

# Müziği çal
pygame.mixer.music.play()

# Resimleri yükle
try:
    tas_img = pygame.image.load('tas.png')
    kagit_img = pygame.image.load('kagıt.png')
    makas_img = pygame.image.load('makas.png')
    icon = pygame.image.load('rock-paper-scissors-icon-set-.jpg')
    background_image = pygame.image.load('rock-paper-scissors-icon-set-.jpg')
except pygame.error as e:
    print(f"Resim dosyası yüklenemedi: {e}")
    pygame.quit()
    sys.exit()

# Resimleri ölçeklendir
tas_img = pygame.transform.scale(tas_img, (200, 200))
kagit_img = pygame.transform.scale(kagit_img, (200, 200))
makas_img = pygame.transform.scale(makas_img, (200, 200))
background_image = pygame.transform.scale(background_image, (800, 600))

# İkonu ayarla
pygame.display.set_icon(icon)

# Resimlerin konumlarını ayarla
tas_rect = tas_img.get_rect(center=(width // 4, height // 1.75))
kagit_rect = kagit_img.get_rect(center=(width // 2, height // 1.75))
makas_rect = makas_img.get_rect(center=(3 * width // 4, height // 1.75))

# Oyun açıklmasını içeren sayfanın ana hatlarnı oluştur
def oyun_aciklamasi_ekranda(scroll_y):
    screen.fill(WHITE)
    
    aciklama_metni = oyun_aciklamasi()
    
    if aciklama_metni is None:
        print("Açıklama metni yüklenemedi!")
        return None, None, None
    
    global total_height, thumb_height
    line_height = 30
    num_lines = len(aciklama_metni.split('\n'))
    total_height = num_lines * line_height  # Metnin toplam yüksekliği
    
    thumb_height = max(40, (height - 40) * (height / total_height))  # Kaydırma çubuğu parmağı yüksekliği
    
    y_offset = 20 - scroll_y
    for line in aciklama_metni.split('\n'):
        aciklama_yazi = aciklama_font.render(line, True, BLACK)
        screen.blit(aciklama_yazi, (20, y_offset))
        y_offset += line_height
    
    # Kaydırma çubuğu
    scrollbar_rect = pygame.Rect(width - 25, 20, 15, height - 40)
    pygame.draw.rect(screen, GRAY, scrollbar_rect)

    thumb_position = (scroll_y / (total_height - height)) * (height - 40 - thumb_height)
    thumb_rect = pygame.Rect(width - 25, 20 + thumb_position, 15, thumb_height)
    pygame.draw.rect(screen, BLACK, thumb_rect)

    # "Oyuna Başla" butonu
    start_button_rect = pygame.Rect(600, height - 80, 150, 50)
    pygame.draw.rect(screen, GRAY, start_button_rect)
    start_text = font.render("Oyuna Başla", True, BLACK)
    screen.blit(start_text, (start_button_rect.x + 20, start_button_rect.y + 10))
    
    pygame.display.flip()

    return start_button_rect

# Oyun bilgisini içeren sayfa ve sonrasında ne olacağı tercih edilecek butonları oluştur
def bilgi_ekrani():
    aciklama_metni = oyun_aciklamasi()
    
    if aciklama_metni is None:
        print("Açıklama metni yüklenemedi!")
        pygame.quit()
        sys.exit()
    
    line_height = 30
    num_lines = len(aciklama_metni.split('\n'))
    global total_height
    total_height = num_lines * line_height

    scroll_y = 0
    running = True
    dragging = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    scroll_y += 10
                elif event.key == pygame.K_UP:
                    scroll_y -= 10
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                scrollbar_x = width - 20
                scrollbar_y = 10 + (scroll_y / (total_height - height)) * (height - 20 - 20)
                thumb_height = max(20, (height - 20) * (height / total_height))
                thumb_rect = pygame.Rect(scrollbar_x, scrollbar_y, 15, thumb_height)
                if thumb_rect.collidepoint(mouse_x, mouse_y):
                    dragging = True
                    mouse_y_offset = mouse_y - scrollbar_y
                start_button_rect = pygame.Rect(600, height - 80, 150, 50)
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    running = False  # Bilgi ekranından çık ve oyunu başlat
                    oyun_sonucu = oyun_dongusu()  # Oyunu başlat ve sonucu al
                    devam_mi = oyun_sonu_ekrani(oyun_sonucu)  # Oyun sonu ekranına geç
                    if not devam_mi:
                        pygame.quit()
                        sys.exit()
                    return  # Bilgi ekranına geri dönmek için
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                mouse_y = pygame.mouse.get_pos()[1]
                thumb_position = mouse_y - 20
                scroll_y = (thumb_position / (height - 40 - thumb_height)) * (total_height - height)
        
        scroll_y = max(0, min(scroll_y, total_height - height))

        oyun_aciklamasi_ekranda(scroll_y)

# Giriş ekranı oluştur
def giris_ekrani():
    screen.blit(background_image, (0, 0))

    # "OYUNA BAŞLA" butonu
    oyun_button_rect = pygame.Rect(width // 4 - 100, height // 3 + 100, 200, 100)
    pygame.draw.rect(screen, GRAY, oyun_button_rect)
    oyun_text = font.render("OYUNA BAŞLA", True, BLACK)
    screen.blit(oyun_text, (oyun_button_rect.x + 10, oyun_button_rect.y + 35))  # Metni ortalamak için koordinatlarını düzelt

    # "OYUN BİLGİSİ" butonu
    bilgi_button_rect = pygame.Rect(3 * width // 4 - 100, height // 3 + 100, 200, 100)
    pygame.draw.rect(screen, GRAY, bilgi_button_rect)
    bilgi_text = font.render("OYUN BİLGİSİ", True, BLACK)
    screen.blit(bilgi_text, (bilgi_button_rect.x + 10, bilgi_button_rect.y + 35)) # Metni ortalamak için koordinatlarını düzelt

    pygame.display.flip()

    # Butonların koordinatlarını ayrı ayrı döndür
    return oyun_button_rect, bilgi_button_rect

# Oyun ekranını oluştur
def oyun_ekrani():    
    # Ekranı temizle
    screen.fill(WHITE)
    
    # Resimleri ekranda göster
    screen.blit(tas_img, tas_rect)
    screen.blit(kagit_img, kagit_rect)
    screen.blit(makas_img, makas_rect)

    # Butonları ekle
    tas_button_rect = pygame.Rect(width // 4 - 50, height // 1.5 + 100, 100, 40)
    pygame.draw.rect(screen, GRAY, tas_button_rect)
    tas_text = font.render("Taş", True, BLACK)
    screen.blit(tas_text, (tas_button_rect.x + 10, tas_button_rect.y + 5))
    
    kagit_button_rect = pygame.Rect(width // 2 - 50, height // 1.5 + 100, 100, 40)
    pygame.draw.rect(screen, GRAY, kagit_button_rect)
    kagit_text = font.render("Kağıt", True, BLACK)
    screen.blit(kagit_text, (kagit_button_rect.x + 10, kagit_button_rect.y + 5))
    
    makas_button_rect = pygame.Rect(3 * width // 4 - 50, height // 1.5 + 100, 100, 40)
    pygame.draw.rect(screen, GRAY, makas_button_rect)
    makas_text = font.render("Makas", True, BLACK)
    screen.blit(makas_text, (makas_button_rect.x + 10, makas_button_rect.y + 5))
    
    pygame.display.flip()
    
    return tas_button_rect, kagit_button_rect, makas_button_rect

# Oyun döngüsünü oluştur (2 olan kazanır! )
def oyun_dongusu():
    oyuncu_kazanma_sayisi = 0
    bilgisayar_kazanma_sayisi = 0

    while oyuncu_kazanma_sayisi < 2 and bilgisayar_kazanma_sayisi < 2:
        tas_button_rect, kagit_button_rect, makas_button_rect = oyun_ekrani()
        
        oyuncu_secim = None
        bilgisayar_secim = random.choice(["taş", "kağıt", "makas"])

        while oyuncu_secim is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    # Kullanıcı seçimlerini kontrol et
                    if tas_button_rect.collidepoint(mouse_x, mouse_y):
                        oyuncu_secim = "taş"
                    elif kagit_button_rect.collidepoint(mouse_x, mouse_y):
                        oyuncu_secim = "kağıt"
                    elif makas_button_rect.collidepoint(mouse_x, mouse_y):
                        oyuncu_secim = "makas"

        sonuc_text = ""
        
        if oyuncu_secim == bilgisayar_secim:
            sonuc_text = f"Berabere! ({bilgisayar_secim} = {oyuncu_secim})"
        elif (oyuncu_secim == "taş" and bilgisayar_secim == "makas") or \
             (oyuncu_secim == "kağıt" and bilgisayar_secim == "taş") or \
             (oyuncu_secim == "makas" and bilgisayar_secim == "kağıt"):
            sonuc_text = f" Sen kazandın! ({oyuncu_secim} > {bilgisayar_secim})"
            oyuncu_kazanma_sayisi += 1
        else:
            sonuc_text = f" Bilgisayar kazandı! ({bilgisayar_secim} > {oyuncu_secim})"
            bilgisayar_kazanma_sayisi += 1
        
        # Sonucu ekranda göster
        screen.fill(WHITE)
        sonuc_yazi = font.render(sonuc_text, True, BLACK)
        screen.blit(sonuc_yazi, (width // 2 - sonuc_yazi.get_width() // 2, height // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

    if oyuncu_kazanma_sayisi > bilgisayar_kazanma_sayisi:
        sonuc_text = "TEBRİKLER :) Oyunu sen kazandın!"
    else:
        sonuc_text = "MAALESEF :( Bilgisayar oyunu kazandı."

    return sonuc_text

# Oyun sonu ekranı oluştur(Devam et ve Çıkış butonları koy)
def oyun_sonu_ekrani(sonuc_text):
    while True:
        screen.fill(WHITE)
        
        sonuc_yazi = font.render(sonuc_text, True, BLACK)
        screen.blit(sonuc_yazi, (width // 2 - sonuc_yazi.get_width() // 2, height // 2 - 40))
        
        devam_button_rect = pygame.Rect(width // 2 - 100, height // 2 + 20, 200, 50)
        pygame.draw.rect(screen, GRAY, devam_button_rect)
        devam_text = font.render("Devam Et", True, BLACK)
        screen.blit(devam_text, (devam_button_rect.x + 30, devam_button_rect.y + 10))
        
        cikis_button_rect = pygame.Rect(width // 2 - 100, height // 2 + 90, 200, 50)
        pygame.draw.rect(screen, GRAY, cikis_button_rect)
        cikis_text = font.render("Çıkış", True, BLACK)
        screen.blit(cikis_text, (cikis_button_rect.x + 30, cikis_button_rect.y + 10))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                if devam_button_rect.collidepoint(mouse_x, mouse_y):                    
                    return True
                elif cikis_button_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

def main():
    running = True
    
    while running:
        oyun_button_rect, bilgi_button_rect = giris_ekrani()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    if oyun_button_rect.collidepoint(mouse_x, mouse_y):
                        oyun_sonucu = oyun_dongusu()  # Oyun döngüsünü başlat
                        devam = oyun_sonu_ekrani(oyun_sonucu)
                        if not devam:
                            running = False
                        break
                    elif bilgi_button_rect.collidepoint(mouse_x, mouse_y):
                        bilgi_ekrani()  # Bilgi ekranını göster
                        break   # Bilgi ekranından çık ve ana döngüye dön
            else:
                continue
            break

if __name__ == "__main__":
    main()
