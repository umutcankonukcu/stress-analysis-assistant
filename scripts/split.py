import random
from ruamel.yaml import YAML

# Dosya yolları
input_file = "datasets/raw/nlu.yml"
train_file = "data/nlu_train.yml"
test_file = "tests/nlu_test.yml"

# YAML yükleyici
yaml = YAML()

# Veriyi yükleme
with open(input_file, "r", encoding="utf-8") as file:
    data = yaml.load(file)

# Veriyi karıştır ve ayır
examples = data["nlu"]
random.shuffle(examples)
split_index = int(0.8 * len(examples))
train_data = {"version": data["version"], "nlu": examples[:split_index]}
test_data = {"version": data["version"], "nlu": examples[split_index:]}

# Eğitim verisini yaz
with open(train_file, "w", encoding="utf-8") as file:
    yaml.dump(train_data, file)

# Test verisini yaz
with open(test_file, "w", encoding="utf-8") as file:
    yaml.dump(test_data, file)

print(f"Eğitim verisi '{train_file}' olarak, test verisi ise '{test_file}' olarak kaydedildi.")
