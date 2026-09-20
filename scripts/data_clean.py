import yaml
import re
from collections import Counter

# `nlu.yml` dosyasını oku ve yükle
def load_nlu_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        nlu_data = yaml.safe_load(file)
    return nlu_data

# Cümlelerdeki gereksiz noktalama işaretlerini temizleme
def clean_punctuation(sentence):
    cleaned_sentence = re.sub(r'[^\w\s]', '', sentence)
    return cleaned_sentence

# NLU dosyasındaki yinelenen cümleleri ve gereksiz boşlukları bulma
def detect_issues(nlu_data):
    all_sentences = []

    # Tüm intentlerin cümlelerini toplama
    for intent_data in nlu_data.get('nlu', []):
        if 'examples' in intent_data:
            examples = intent_data['examples'].split('\n')
            for example in examples:
                cleaned_example = example.strip()  # Boşlukları temizle
                if cleaned_example:
                    cleaned_example = clean_punctuation(cleaned_example)
                    all_sentences.append(cleaned_example)

    # Cümlelerin sıklığını kontrol et
    sentence_counts = Counter(all_sentences)
    duplicate_sentences = {sentence: count for sentence, count in sentence_counts.items() if count > 1}

    # Sonuçları yazdır
    print(f"Toplam cümle sayısı: {len(all_sentences)}")
    print(f"Tekrar eden cümle sayısı: {len(duplicate_sentences)}")
    print("Tekrar eden cümleler:")
    for sentence, count in duplicate_sentences.items():
        print(f"- {sentence} (tekrar sayısı: {count})")

# Dosya yolu ve fonksiyon çağrısı
nlu_file_path = 'datasets/raw/nlu.yml'
nlu_data = load_nlu_file(nlu_file_path)
detect_issues(nlu_data)
