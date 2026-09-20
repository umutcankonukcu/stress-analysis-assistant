# Türkçe Duygu Analizi

Türkçe metinleri yedi duygu sınıfına ayıran, Rasa NLU ve Tkinter kullanan masaüstü uygulaması. Uygulama; kullanıcı kaydı, mesaj geçmişi, stres skoru ve isteğe bağlı sesli giriş sunar.

## Sınıflar

`anger`, `happy`, `sadness`, `surprise`, `fear`, `disgust`, `ambigious`

## Gereksinimler

- Python 3.10 (eğitilmiş model Rasa 3.6.20 ile oluşturulmuştur)
- Mikrofon özelliği için sistem mikrofon erişimi; Windows'ta gerekirse PyAudio

## Kurulum

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Modeli hazırlama

`models/` klasöründeki eğitilmiş model arşivi 100 MB sınırını aştığı için GitHub deposuna eklenmez. Uygulamayı klonladıktan sonra modeli yeniden eğitin:

```powershell
rasa train nlu
```

Alternatif olarak, mevcut model arşivini haricî depolamadan `models/` klasörüne koyabilirsiniz. Bu bilgisayardaki model korunur; `.gitignore` yalnızca GitHub'a eklenmesini engeller.

## Çalıştırma

İlk terminalde Rasa API'sini başlatın:

```powershell
rasa run --enable-api --cors "*"
```

İkinci terminalde arayüzü açın:

```powershell
python arayuz.py
```

Arayüz, sınıflandırma için `http://localhost:5005/model/parse` adresindeki Rasa API'sine bağlanır.

## Eğitim ve değerlendirme

```powershell
rasa train nlu
rasa test nlu --nlu tests/nlu_test.yml --out reports/evaluation
```

- Ham veri: `datasets/raw/nlu.yml`
- Eğitim verisi: `data/nlu_train.yml`
- Test verisi: `tests/nlu_test.yml`
- Eğitilmiş model çıktısı: `models/` (GitHub'a dahil edilmez)

`scripts/split.py`, ham veri setini eğitim ve test dosyalarına ayırır. `scripts/data_clean.py` yinelenen cümleleri tespit eder. `scripts/result.py` rapor metriklerini, `scripts/result2.py` ise karmaşıklık matrisini görselleştirir.

## GitHub'a yükleme notları

`users.json` yerel kullanıcı mesajlarını ve parolaları içerdiğinden `.gitignore` ile dışlanır. Depoya yalnızca şablon olarak `users.example.json` eklenir. Uygulama, `users.json` bulunmadığında dosyayı ilk kayıt işleminde otomatik oluşturur.

## Proje yapısı

```text
actions/             Rasa özel aksiyonları
data/                Rasa'nın kullandığı eğitim verisi
datasets/raw/        Değiştirilmemiş ham NLU veri kümesi
docs/                Proje raporu ve kaynak bağlantıları
models/              Yerelde üretilen/eğitilmiş Rasa modeli
reports/evaluation/  Değerlendirme çıktıları
scripts/             Veri hazırlama ve analiz betikleri
tests/               NLU test verisi
arayuz.py            Tkinter uygulaması
```
