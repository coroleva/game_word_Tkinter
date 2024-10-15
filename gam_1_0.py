import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Для улучшенного стиля кнопок и других элементов

translator = Translator()

# Функция для получения случайного английского слова и его определения
def get_english_words():
    url = "https://randomword.com/"
    try:
        response = requests.get(url)

        # Создаём объект Soup
        soup = BeautifulSoup(response.content, "html.parser")
        # Получаем слово. text.strip удаляет все пробелы из результата
        english_words = soup.find("div", id="random_word").text.strip()
        # Получаем описание слова
        word_definition = soup.find("div", id="random_word_definition").text.strip()
        return {
            "english_words": english_words,
            "word_definition": word_definition
        }
    except:
        messagebox.showerror("Ошибка", "Произошла ошибка при получении данных.")
        return None

# Центрирование окна на экране
def center_window(root, width=600, height=400):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    root.geometry(f'{width}x{height}+{x}+{y}')

# Создание приложения
class WordGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Игра: Угадай слово")
        center_window(self.root)  # Центрируем окно

        # Стиль интерфейса
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10, relief="raised")
        style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 14), padding=10)

        self.root.configure(bg="#f0f0f0")  # Задаём цвет фона окна

        # Создаём интерфейс
        self.label = ttk.Label(root, text="Нажмите кнопку, чтобы получить слово.", style="TLabel")
        self.label.pack(pady=20)

        self.definition_label = ttk.Label(root, text="", style="TLabel", wraplength=500)
        self.definition_label.pack(pady=10)

        self.user_entry = ttk.Entry(root, font=("Helvetica", 14), width=30)
        self.user_entry.pack(pady=10)

        self.submit_button = ttk.Button(root, text="Ответить", command=self.check_word)
        self.submit_button.pack(pady=10)

        self.new_word_button = ttk.Button(root, text="Новое слово", command=self.new_word)
        self.new_word_button.pack(pady=10)

        self.result_label = ttk.Label(root, text="", style="TLabel", foreground="green")
        self.result_label.pack(pady=10)

        self.word = ""
        self.translated_word = ""
        self.new_word()

    # Получить новое слово и описание
    def new_word(self):
        word_data = get_english_words()
        if word_data:
            self.word = word_data["english_words"]
            word_definition = word_data["word_definition"]
            self.translated_word = translator.translate(self.word, src="en", dest="ru").text
            translated_definition = translator.translate(word_definition, src="en", dest="ru").text
            self.definition_label.config(text=f"Значение слова: {translated_definition}")
            self.result_label.config(text="")
            self.user_entry.delete(0, tk.END)

    # Проверить введённое слово
    def check_word(self):
        user_input = self.user_entry.get()
        if user_input.lower() == self.translated_word.lower():
            self.result_label.config(text="Все верно!", foreground="green")
        else:
            self.result_label.config(text=f"Неправильно. Было загадано: {self.translated_word}", foreground="red")


# Создаем окно Tkinter
if __name__ == "__main__":
    root = tk.Tk()
    app = WordGameApp(root)
    root.mainloop()

