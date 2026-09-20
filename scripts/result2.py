import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

# Confusion matrix verileri
labels = ["ambigious", "anger", "disgust", "fear", "happy", "sadness", "surprise"]
confusion_matrix_data = np.array([
    [6897, 23, 6, 16, 9, 21, 16],
    [5, 4652, 4, 1, 1, 9, 3],
    [1, 4, 2902, 4, 0, 1, 1],
    [8, 1, 6, 4061, 1, 9, 2],
    [13, 3, 0, 2, 3761, 10, 26],
    [12, 23, 3, 8, 12, 4730, 26],
    [5, 5, 0, 6, 28, 11, 3171],
])

# Confusion matrix görselleştirme
fig, ax = plt.subplots(figsize=(14, 14), dpi=300)  # DPI artırılarak netlik sağlanır
disp = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix_data, display_labels=labels)

# Confusion matrix'i çizme
disp.plot(cmap="viridis", ax=ax, xticks_rotation="vertical", colorbar=True)  # Viridis renk paleti kullanıldı

# Başlık ve etiket boyutlarını büyütme
plt.title("Intent Confusion Matrix", fontsize=24)
plt.xlabel("Predicted Label", fontsize=18)
plt.ylabel("True Label", fontsize=18)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Hücre içindeki sayıların boyutunu ve netliğini artırma
for i in range(confusion_matrix_data.shape[0]):
    for j in range(confusion_matrix_data.shape[1]):
        ax.text(j, i, f"{confusion_matrix_data[i, j]}", ha="center", va="center", fontsize=14, color="black")

# Görselleştirmeyi gösterme
plt.tight_layout()  # Görselleştirme düzenini optimize eder
plt.show()
