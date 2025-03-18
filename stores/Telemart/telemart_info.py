class TelemartLocators:
    WACOM_URL = 'https://telemart.ua/ua/search/wacom/'
    XP_PEN_URL = 'https://telemart.ua/ua/search/xp-pen/'
    CONTAINER_LOCATOR = 'catalog-container catalog-container--buble row'
    ITEM_BOX_LOCATOR = 'product-item col-lg-3'
    ITEM_TITLE = 'product-item__title'
    ITEM_PRICE = 'product-cost'
    ITEM_STATUS = 'btn btn-primary preview-product__btn preview-product__btn_cart add-to-cart'
    CONTAINER_LOCATOR_TAG = 'div'
    HEADERS = headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",

        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "referer=https%3A%2F%2Fwww.google.com%2F; landing=%2Fua%2F; PHPSESSID=12114a34d661ae37d4a3a0dc5e3dace3; metrikaHashGuest=884bb2e0ffafa9b77cd31e785ec36a1a; shop_locale=uk_UA; _ga=GA1.1.1011165882.1720802667; products_per_page=36; shop_viewed=210090; _ga_LVBD8HXZNW=GS1.1.1720846072.2.1.1720846407.47.0.0",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",

    }


TELEMART_ARTICLES_WACOM = {'Монітор-планшет Wacom Movink 13 Touch (DTH135K0B) Black': 'DTH135K0B',
                     'Графічний планшет Wacom Intuos Pro L (PTH-860-N) Black': 'PTH-860-N',
                     'Графічний планшет Wacom Intuos M Bluetooth (CTL-6100WLE-N) Pistachio': 'CTL-6100WLE-N',
                     'Монітор-планшет Wacom Cintiq Pro 27 (DTH271K0B-ST) Black': 'DTH271K0B-ST',
                     'Монітор-планшет Wacom Cintiq 16 (DTK1660K0B) Black': 'DTK1660K0B',
                     'Графічний монітор Wacom One 13 Touch (DTH134W0B) Black/White': 'DTH134W0B',
                     'Монітор-планшет Wacom Cintiq Pro 16 (DTH167K0B) Black': 'DTH167K0B',
                     'Монітор-планшет Wacom Cintiq 22 (DTK2260K0A) Black': 'DTK2260K0A',
                     'Графічний монітор Wacom One 12 (DTC121W0B) Black/White': 'DTC121W0B',
                     'Графічний планшет Wacom One by S (CTL-472-N) Black/Red': 'CTL-472-N',
                     'Монітор-планшет Wacom Cintiq Pro 24 (DTK-2420) Black': 'DTK-2420',
                     'Монітор-планшет Wacom Cintiq Pro 17 (DTH172K0B) Black': 'DTH172K0B',
                     'Монітор-планшет Wacom Cintiq Pro 24 Touch (DTH-2420) Black': 'DTH-2420',
                     'Графічний планшет Wacom Intuos S Bluetooth (CTL-4100WLK-N) Black': 'CTL-4100WLK-N',
                     'Графічний планшет Wacom Intuos Pro M (PTH-660-N) Black': 'PTH-660-N',
                     'Планшет для підпису Wacom STU-540 (STU540-CH2) Black': 'STU540-CH2',
                     'Графічний планшет Wacom Intuos Pro S (PTH460K0B) Black': 'PTH460K0B',
                     'Перо Wacom One (CP92303B2Z)': 'CP92303B2Z',
                     'Графічний планшет Wacom One M (CTC6110WLW1B) Black/White': 'CTC6110WLW1B',
                     'Графічний планшет Wacom Intuos S Bluetooth Manga (CTL-4100WLK-M) Black': 'CTL-4100WLK-M',
                     'Графічний планшет Wacom One S (CTC4110WLW1B) Black/White': 'CTC4110WLW1B',
                     'Перо Wacom Pen 2K (LP190K)': 'LP190K', 'Перо Wacom Pro Pen 3 (ACP50000DZ)': 'ACP50000DZ',
                     'Перо Wacom Grip Pen (KP-501)': 'KP-501',
                     'Кабель Wacom USB Type-C to USB Type-C для Wacom Movink 1m (ACK45206Z)': 'ACK45206Z',
                     'Перо Wacom Pro Pen Slim (KP301E00DZ)': 'KP301E00DZ',
                     'Набір наконечників з еластомеру Wacom для Wacom One Standard Pen 10 шт (ACK24918Z)': 'ACK24918Z',
                     'Адаптер Wacom для підставки Flex Arm (Retro Fit Kit) (ACK64804KZ)': 'Retro Fit Kit ',
                     'Підставка Wacom Ergo Stand для Wacom Cintiq Pro 24" (ACK62801K)': 'ACK62801K',
                     'Перо Wacom Pen 4K (LP1100K)': 'LP1100K',
                     'Набір стандартних наконечників Wacom для Wacom Pro Pen 3 5 шт (ACK24801Z)': 'ACK24801Z',
                     'Перо Wacom Pro Pen 2 з пеналом (KP-504E)': 'KP-504E',
                     'Чохол Wacom для Wacom Movink (ACK55200Z)': 'ACK55200Z',
                     'Прищiпка Wacom для Intuos Pro Wacom Paper Clip (ACK42213)': 'ACK42213',
                     'Адаптер живлення Wacom для Wacom One 12/13T та Wacom Movink (ACK44914B)': 'ACK44914B',
                     'Набір змінних стрижнів для ручки Wacom Ballpoint 1.0 для Wacom Pro Paper 3 шт (ACK-22207)': 'ACK-22207',
                     'Складана підставка Wacom для Wacom Movink (ACK652Z)': 'ACK652Z',
                     'Набір змінних наконечників Felt (фломастер) Wacom для Wacom Pro Pen 3 10 шт (ACK24819Z)': 'ACK24819Z',
                     'Набір стандартних наконечників Wacom для Wacom One Standard Pen 10 шт (ACK24911Z)': 'ACK24911Z',
                     'Підставка Wacom для Wacom Cintiq 16" (ACK620K)': 'ACK620K',
                     'Кабель Wacom USB Type-C to USB Type-C для Wacom One 1.8m (ACK4490601Z)': 'ACK4490601Z',
                     'Набір стандартних наконечників Wacom для Wacom Intuos Pro New 10 шт (ACK22211)': 'ACK22211',
                     'Набір повстяних наконечників Wacom для Wacom Intuos Pro New 10 шт (ACK22213)': 'ACK22213',
                     'Набір повстяних наконечників Wacom для Wacom Intuos 5/Pro 5 шт (ACK-20003)': 'ACK-20003',
                     'Набір наконечників для пера Wacom для Wacom One 5 шт (ACK24501Z)': 'ACK24501Z'
                     }

TELEMART_ARTICLES_XP_PEN = {
    'Графічний монітор XP-Pen Artist 22 Plus (MD22FH_EU) Black': 'MD22FH_EU' ,
 'Графічний монітор XP-Pen Artist 14 Pro (2nd Gen) (MD140FH_AD41) Black': 'MD140FH_AD41',
    'Графічний монітор XP-Pen Artist 16 Pen Display (2nd Gen) (JPCD160FH_BK) Black': 'JPCD160FH_BK',
    'Графічний монітор XP-Pen Artist 12 Pen Display (2nd Gen) (JPCD120FH_G) Green': 'JPCD120FH_G',
    'Графічний монітор XP-Pen Artist Pro 16 (2nd Gen) (Artist Pro 16_JP) Black': 'Artist Pro 16_JP',
    'Графічний планшет XP-Pen Deco 640 Black': 'IT640',
    'Графічний планшет XP-Pen Deco 01V3 Pink': 'Deco 01V3 Pink',
    'Графічний планшет XP-Pen Star G960S Plus Black': 'Star G960S Plus',
    'Графічний планшет XP-Pen Deco Fun L Black': 'Deco Fun L_BK',
    'Графічний планшет XP-Pen Deco Fun XS Black': 'Deco Fun XS_BK',
    'Графічний планшет XP-Pen Deco 02 Black': 'DECO 02',
    'Рукавичка для графічного планшета XP-Pen AC08 L (AC08_L)': 'AC08_L',
    'Графічний планшет XP-Pen Deco Pro M Black': 'Deco Pro M',
    'Графічний планшет XP-Pen Deco Fun S Black': 'Deco Fun S_BK',
    'Графічний планшет XP-Pen Deco Pro S Black': 'Deco Pro S',
    'Перо XP-Pen for Deco Fun/Star (PN01_B)': 'PN01_B',
    'Перо XP-Pen for Deco 02/Artist 12 (P06)': 'P06',
    'Захисна плівка для графічного планшета XP-Pen for Artist 12 (2 Gen) 1pcs (ACLF1215B)': 'ACLF1215B',
    'Мультифункціональна підставка для планшета XP-Pen AC18': 'AC18',
    'Рукавичка для графічного планшета XP-Pen AC08 S (AC08_S)': 'AC08_S',
    'Захисна плівка для графічного планшета XP-Pen for Artist Pro 16 2pcs (AD28)': 'AD28',
    'Рукавичка для графічного планшета XP-Pen AC08 M (AC08_M)': 'AC08_M',
    'Набір наконечників для пера для графічного планшета XP-Pen for P02 10pcs (AC17_B)':'AC17_B',
    'Захисна плівка для графічного планшета XP-Pen for Artist 13 Pro (2 Gen) 2pcs (ACFL1302А)': 'ACFL1302А',
    'Адаптер XP-Pen USB Type-C 3 in 1 (USB+HDMI+DP) (ACW01)': 'ACW01',
    'Набір наконечників для пера для графічного планшета XP-Pen for P01/P03/P03S/P05 10pcs (AC04_B)': 'AC04_B',
    'Захисна плівка для графічного планшета XP-Pen for Artist 13 Pro (2 Gen) 1pcs (ACLF1302B)': 'ACLF1302B',
}
