import json

# JSON dosyasını yükle
with open('reports/evaluation/intent_report.json', 'r') as file:
    report = json.load(file)

# Accuracy değerini yazdır
accuracy = report.get("accuracy", 0)
print(f"Genel Doğruluk (Accuracy): {accuracy}")

# Macro ve weighted avg metriklerini yazdır
macro_avg = report.get("macro avg", {})
weighted_avg = report.get("weighted avg", {})

print("\nGenel Macro Avg:")
print(f"  Precision: {macro_avg.get('precision', 0)}")
print(f"  Recall: {macro_avg.get('recall', 0)}")
print(f"  F1-score: {macro_avg.get('f1-score', 0)}")

print("\nGenel Weighted Avg:")
print(f"  Precision: {weighted_avg.get('precision', 0)}")
print(f"  Recall: {weighted_avg.get('recall', 0)}")
print(f"  F1-score: {weighted_avg.get('f1-score', 0)}")

# F1 Skoru (Tüm model için macro avg veya weighted avg kullanabilirsiniz)
print("\nModelin Genel F1 Skoru:", macro_avg.get("f1-score", 0))

# Her intent için metrikleri yazdır
for intent, metrics in report.items():
    if intent not in ["accuracy", "macro avg", "weighted avg", "micro avg"]:
        print(f"\nIntent: {intent}")
        print(f"  Precision: {metrics['precision']}")
        print(f"  Recall: {metrics['recall']}")
        print(f"  F1-score: {metrics['f1-score']}")
        print(f"  Support: {metrics['support']}")
        print(f"  Confused with: {metrics.get('confused_with', {})}")
