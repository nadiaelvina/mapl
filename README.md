# MAPL+ Portfolio Intelligence

Prototype interaktif untuk deteksi product cannibalization dan simulasi revenue portfolio.

## Cara Jalankan

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Jalankan app
streamlit run app.py
```

App akan terbuka otomatis di browser: http://localhost:8501

## Fitur
- **Portfolio Simulator** — slider diskon per produk, kalkulasi real-time
- **Cannibalization Heatmap** — cross-price elasticity matrix antar produk
- **AI Insights** — rekomendasi otomatis berbasis skenario aktif
- **Risk Assessment** — identifikasi pasangan produk berisiko tinggi

## Deploy ke Streamlit Cloud (Gratis)
1. Push folder ini ke GitHub repo
2. Login ke https://share.streamlit.io
3. Pilih repo → `app.py` → Deploy
4. Dapat URL publik dalam ~2 menit

## Upgrade ke Claude API (AI Layer)
Ganti fungsi `generate_ai_insight()` di `app.py` dengan:

```python
import anthropic

def generate_ai_insight(results, total_base, total_new, discounts):
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    
    summary = build_summary(results, total_base, total_new, discounts)
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"Kamu adalah pricing analyst. Berikan rekomendasi bisnis dari data berikut:\n{summary}"
        }]
    )
    return message.content[0].text
```

Tambahkan API key di `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```
