from google import genai    
from django.conf import settings
import json

def kitap_önerilerini_alma(kitap_yazar,kitap_turu,kitap_sayfa):
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        raise ValueError("API_Key bulunmamıştır.Lütfen kontrol ettiriniz.")
    client = genai.Client(api_key=api_key) #we created client using api_key.
    prompt = (
        f"Bana '{kitap_turu}' türünde, yaklaşık {kitap_sayfa} sayfa uzunluğunda "
        f"ve '{kitap_yazar}' tarzında 3 tane kitap önerisi yap. "
        f"Yanıtı, sadece kitap isimleri ve kısa açıklamalarından oluşan "
        f"JSON formatında döndür. Her bir öneri için 'book_title' ve 'book_description'"
    )
    try:
        
        response = client.models.generate_content(
        model="gemini-2.5-pro",contents=prompt,
        )
        response_text = response.text.replace("```json\n", "").replace("\n```", "").strip()#
        öneriler = json.loads(response_text)

        return öneriler

    except Exception as e:
        print(f"Gemini'dan öneri alınırken bir hata oluştu: {e}")
        return {"öneriler": []} #boş dönüyor.