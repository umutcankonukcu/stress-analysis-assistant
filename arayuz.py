import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import os
import requests
import speech_recognition as sr
import threading

# -- Değişiklik: İngilizce -> Türkçe duygu çevirisi için sözlük ekliyoruz.
TURKISH_EMOTIONS = {
    "anger": "sinirli",
    "sadness": "üzgün",
    "happy": "mutlu",
    "surprise": "şaşkın",
    "fear": "korkmuş",
    "disgust": "iğrenmiş",
    "ambigious": "duygu içermiyor",
    "belirlenemedi": "belirsiz"  # Rasa'nın tanımadığı bir durum
}

USER_DATA_FILE = "users.json"
RASA_PARSE_URL = "http://localhost:5005/model/parse"
REQUEST_TIMEOUT_SECONDS = 10
root = tk.Tk()

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        try:
            if os.path.getsize(USER_DATA_FILE) > 0:
                with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    for user, info in data.items():
                        if "messages" not in info:
                            info["messages"] = []
                        if "stress_score" not in info:
                            info["stress_score"] = 0
                    return data
        except json.JSONDecodeError:
            return {}
    return {}

def save_user_data(data):
    with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def register_user(username, password):
    users = load_user_data()
    if username in users:
        return False, "Bu kullanıcı adı zaten mevcut."
    users[username] = {"password": password, "stress_score": 0, "messages": []}
    save_user_data(users)
    return True, "Kayıt başarılı."

def authenticate_user(username, password):
    users = load_user_data()
    if username in users and users[username]["password"] == password:
        return True, "Giriş başarılı."
    return False, "Kullanıcı adı veya şifre yanlış."

def show_register_screen():
    root.withdraw()
    register_window = tk.Toplevel(root)
    register_window.title("Kayıt Ol")
    register_window.geometry("400x400")
    register_window.config(bg="#2c3e50")

    def go_back():
        register_window.destroy()
        root.deiconify()

    ttk.Button(register_window, text="Geri Dön", command=go_back).pack(pady=5)

    title_label = tk.Label(register_window, text="Kayıt Ol", font=("Arial", 20, "bold"), bg="#2c3e50", fg="#ecf0f1")
    title_label.pack(pady=20)

    tk.Label(register_window, text="Kullanıcı Adı:", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1").pack(pady=5)
    username_var = tk.StringVar()
    tk.Entry(register_window, textvariable=username_var, font=("Arial", 12), width=30).pack(pady=5)

    tk.Label(register_window, text="Şifre:", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1").pack(pady=5)
    password_var = tk.StringVar()
    tk.Entry(register_window, textvariable=password_var, font=("Arial", 12), width=30, show="*").pack(pady=5)

    def register():
        username = username_var.get()
        password = password_var.get()
        if not username or not password:
            messagebox.showerror("Kayıt Hatası", "Kullanıcı adı ve şifre boş olamaz!")
            return
        success, message = register_user(username, password)
        messagebox.showinfo("Kayıt Durumu", message)
        if success:
            register_window.destroy()
            root.deiconify()

    tk.Button(register_window, text="Kayıt Ol", font=("Arial", 14), bg="#3498db", fg="#ffffff", width=15, command=register).pack(pady=20)

def show_login_screen():
    root.withdraw()
    login_window = tk.Toplevel(root)
    login_window.title("Giriş Yap")
    login_window.geometry("400x400")
    login_window.config(bg="#2c3e50")

    def go_back():
        login_window.destroy()
        root.deiconify()

    ttk.Button(login_window, text="Geri Dön", command=go_back).pack(pady=5)

    title_label = tk.Label(login_window, text="Hoş Geldiniz", font=("Arial", 20, "bold"), bg="#2c3e50", fg="#ecf0f1")
    title_label.pack(pady=20)

    try:
        icon_image = Image.open("icon.png")
        icon_photo = ImageTk.PhotoImage(icon_image.resize((100, 100)))
        icon_label = tk.Label(login_window, image=icon_photo, bg="#2c3e50")
        icon_label.image = icon_photo
        icon_label.pack(pady=10)
    except FileNotFoundError:
        pass

    tk.Label(login_window, text="Kullanıcı Adı:", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1").pack(pady=5)
    username_var = tk.StringVar()
    tk.Entry(login_window, textvariable=username_var, font=("Arial", 12), width=30).pack(pady=5)

    tk.Label(login_window, text="Şifre:", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1").pack(pady=5)
    password_var = tk.StringVar()
    tk.Entry(login_window, textvariable=password_var, font=("Arial", 12), width=30, show="*").pack(pady=5)

    def login():
        username = username_var.get()
        password = password_var.get()
        if not username or not password:
            messagebox.showerror("Giriş Hatası", "Kullanıcı adı ve şifre boş olamaz!")
            return
        success, message = authenticate_user(username, password)
        if success:
            messagebox.showinfo("Giriş Durumu", message)
            login_window.destroy()
            show_user_dashboard(username)
        else:
            messagebox.showerror("Giriş Hatası", message)

    tk.Button(login_window, text="Giriş Yap", font=("Arial", 14), bg="#3498db", fg="#ffffff", width=15, command=login).pack(pady=20)

def show_user_dashboard(username):
    dashboard_window = tk.Toplevel(root)
    dashboard_window.title(f"Hoş Geldiniz, {username}")
    dashboard_window.geometry("500x600")
    dashboard_window.config(bg="#2c3e50")

    def go_back():
        dashboard_window.destroy()
        root.deiconify()

    ttk.Button(dashboard_window, text="Geri Dön", command=go_back).pack(pady=5)

    title_label = tk.Label(dashboard_window, text=f"Merhaba, {username}!", font=("Arial", 20, "bold"), bg="#2c3e50", fg="#ecf0f1")
    title_label.pack(pady=20)

    tk.Label(dashboard_window, text="Burası size özel bir sayfadır.", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1").pack(pady=10)

    # Mesaj gönderme bölümü
    tk.Label(dashboard_window, text="Mesajınız:", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1").pack(pady=5)
    user_input = tk.StringVar()
    tk.Entry(dashboard_window, textvariable=user_input, font=("Arial", 12), width=50).pack(pady=5)

    chat_output = tk.StringVar()
    tk.Label(dashboard_window, textvariable=chat_output, font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1", wraplength=400, justify="left").pack(pady=10)

    def update_stress_and_messages(username, user_message, intent):
        users = load_user_data()
        if username in users:
            user_data = users[username]
            user_data.setdefault("messages", []).append({"message": user_message, "intent": intent})
            # Stres skoru güncellemesi
            if intent in ["anger", "sadness", "fear"]:
                user_data["stress_score"] += 0.05
            else:
                user_data["stress_score"] = max(0, user_data["stress_score"] - 0.05)
            save_user_data(users)

    def open_breathing_exercise():
        exercise_window = tk.Toplevel(dashboard_window)
        exercise_window.title("Nefes Egzersizi")
        exercise_window.geometry("400x250")
        exercise_window.config(bg="#2c3e50")

        tk.Label(exercise_window, text="Nefes Egzersizi", font=("Arial", 16), bg="#2c3e50", fg="#ecf0f1").pack(pady=10)
        tk.Label(exercise_window, text="1. Derin bir nefes alın ve 4 saniye boyunca tutun.", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1").pack(pady=5)
        tk.Label(exercise_window, text="2. Yavaşça nefesinizi 8 saniyede verin.", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1").pack(pady=5)
        tk.Label(exercise_window, text="3. Bu işlemi 5 kez tekrarlayın.", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1").pack(pady=5)

        tk.Button(exercise_window, text="Tamam", font=("Arial", 14), bg="#3498db", fg="#ffffff", command=exercise_window.destroy).pack(pady=20)

    def view_past_messages():
        messages_window = tk.Toplevel(dashboard_window)
        messages_window.title("Geçmiş Mesajlar")
        messages_window.geometry("400x400")
        messages_window.config(bg="#2c3e50")

        tk.Label(messages_window, text="Geçmiş Mesajlar", font=("Arial", 16), bg="#2c3e50", fg="#ecf0f1").pack(pady=10)

        users = load_user_data()
        if username in users:
            messages = users[username].get("messages", [])
            stress_score = users[username].get("stress_score", 0)
            tk.Label(messages_window, text=f"Stres Skoru: {stress_score:.2f}", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1").pack(pady=5)

            message_frame = tk.Frame(messages_window, bg="#2c3e50")
            message_frame.pack(pady=10, fill=tk.BOTH, expand=True)

            for entry in messages:
                if isinstance(entry, dict):
                    message = entry.get("message", "")
                    intent = entry.get("intent", "")
                    tk.Label(message_frame, text=f"{message} - ({intent})", font=("Arial", 10), bg="#2c3e50", fg="#ecf0f1", wraplength=350, justify="left").pack(anchor="w", padx=10)
                else:
                    tk.Label(message_frame, text=f"{entry}", font=("Arial", 10), bg="#2c3e50", fg="#ecf0f1", wraplength=350, justify="left").pack(anchor="w", padx=10)

            def clear_messages():
                if username in users:
                    users[username]["messages"] = []
                    save_user_data(users)
                    messagebox.showinfo("Başarılı", "Geçmiş mesajlar temizlendi!")
                    messages_window.destroy()
                    view_past_messages()

            tk.Button(messages_window, text="Geçmişi Temizle", font=("Arial", 12), bg="#e74c3c", fg="#ffffff", command=clear_messages).pack(pady=10)

    def predict_intent(user_message):
        payload = {"text": user_message}

        try:
            response = requests.post(
                RASA_PARSE_URL,
                json=payload,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            if response.status_code == 200:
                result = response.json()
                intent_name = result.get("intent", {}).get("name", "belirlenemedi")
                confidence = result.get("intent", {}).get("confidence", 0)
                return {"intent": intent_name, "confidence": confidence, "response": result}
            else:
                return {"error": "Rasa API'de bir hata oluştu!"}
        except requests.RequestException:
            return {
                "error": "Rasa sunucusuna ulaşılamadı. Sunucunun çalıştığını kontrol edin."
            }

    def send_message():
        user_message = user_input.get()
        if user_message.strip():
            result = predict_intent(user_message)
            if "error" in result:
                chat_output.set(result["error"])
            else:
                intent_english = result["intent"]
                confidence = result["confidence"]
                
                # -- Değişiklik: Gelen intent'i Türkçe karşılığı ile değiştiriyoruz
                intent_turkish = TURKISH_EMOTIONS.get(intent_english, "belirsiz")

                # Ekrana yazdırırken Türkçe duygu adını kullanıyoruz
                message = f"Duygu: {intent_turkish}\nGüven Skoru: {confidence:.2f}"

                # Stresli duygular
                if intent_english in ["anger", "sadness", "fear"]:
                    message += "\nUYARI: Kullanıcı stresli görünüyor!"
                    open_breathing_exercise()

                update_stress_and_messages(username, user_message, intent_english)
                chat_output.set(message)

    def get_audio_input():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            chat_output.set("Dinliyorum...")
            try:
                audio_data = recognizer.listen(source, timeout=5)
                user_message = recognizer.recognize_google(audio_data, language="tr-TR")
                user_input.set(user_message)
                send_message()
            except sr.UnknownValueError:
                chat_output.set("Ses anlaşılamadı, lütfen tekrar deneyin.")
            except sr.RequestError as e:
                chat_output.set(f"Ses tanıma servisine ulaşılamadı: {e}")
            except Exception as e:
                chat_output.set(f"Hata: {e}")

    tk.Button(dashboard_window, text="Mesaj Gönder", font=("Arial", 14), bg="#3498db", fg="#ffffff", width=15, command=send_message).pack(pady=10)
    tk.Button(dashboard_window, text="Sesi Dinle", font=("Arial", 14), bg="#3498db", fg="#ffffff", width=15, command=get_audio_input).pack(pady=10)
    tk.Button(dashboard_window, text="Geçmiş Mesajları Gör", font=("Arial", 14), bg="#3498db", fg="#ffffff", width=20, command=view_past_messages).pack(pady=10)

def main():
    root.title("Kullanıcı Yönetim Sistemi")
    root.geometry("300x200")
    ttk.Label(root, text="Hoş Geldiniz", font=("Arial", 16)).pack(pady=10)
    ttk.Button(root, text="Kayıt Ol", command=show_register_screen).pack(pady=10)
    ttk.Button(root, text="Giriş Yap", command=show_login_screen).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
