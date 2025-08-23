from google.generativeai import GenerativeModel
from django.conf import settings
import json

def kitap_önerilerini_alma(kitap_yazar, kitap_turu, kitap_sayfa):

    api_key = settings.GEMINI_API_KEY
    if not api_key:
        raise ValueError("API_Key bulunmamıştır. Lütfen kontrol ediniz.")

    model = GenerativeModel("gemini-1.5-flash")
    
    prompt = (f"Kullanıcının tercihine göre, kitap türü '{kitap_turu}', yazar tarzı '{kitap_yazar}' ve yaklaşık sayfa sayısı '{kitap_sayfa}' olan 3 tane benzersiz Gerçek yazarı olan gerçek kitaplar öner.Her bir öneri için kitap adını ('book_title') ve en az detaylı 50 kelimelik,kitabı anlatan, ilgi çekici **Türkçe** bir açıklamasını ('book_description') ekle.Kesinlikle book_title ve book_description olsun.Yanıtını sadece aşağıdaki formatta, bir JSON listesi olarak döndür:")
    
    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "book_title": {"type": "STRING"},
                            "book_description": {"type": "STRING"}
                        }
                    }
                }
            }
        )

        if response.text:
            öneriler = json.loads(response.text)
            return öneriler
        else:
            print("Gemini'dan boş bir yanıt alındı.")
            return []

    except Exception as e:
        print(f"Gemini'dan öneri alınırken bir hata oluştu: {e}")
        return []
