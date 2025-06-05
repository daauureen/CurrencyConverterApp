# 1) Здесь импортируются библиотеки
import tkinter as tk  # Здесь стандартная библиотека для создания графического интерфейса
from tkinter import ttk, messagebox  # Здесь расширенные виджеты и окна сообщений
import requests  # Это для http запросов к API
import json  # Это для работы с JSON-данными
import logging  # Это для логирования действий
from datetime import datetime  # Это для отображения времени и даты
import os  # Это для работы с файловой системой

# URL внешнего API предоставляющего актуальные курсы валют с базой KZT (я использовал api.exchangerate-api.com)
API_URL = "https://api.exchangerate-api.com/v4/latest/KZT"

# Файл для кэширования полученных данных
CACHE_FILE = "exchange_cache.json"

# Файл логов и тут будут записываться все действия пользователя
LOG_FILE = "log.txt"

# Здесь идет настройка логирования: файл, уровень логирования, формат сообщений
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')


# 2) Это функция получения курса валют
def get_exchange_data():
    """
    Загружает данные о курсах валют с API, а в случае ошибки загружает из кэша (если он есть)
    """
    try:
        response = requests.get(API_URL, timeout=5)  # Отправляем GET-запрос с таймаутом
        response.raise_for_status()  # Генерирует исключение при коде ответа != 200
        data = response.json()  # Преобразуем JSON в словарь Python
        with open(CACHE_FILE, "w") as f:  # Сохраняем полученные данные в файл кэша
            json.dump(data, f)
        logging.info("Данные обновлены с API.")  # Запись успешного получения в лог (то есть в exchange_cache.json)
        return data
    except Exception as e:
        logging.warning(f"Ошибка API: {e}")  # Логируем ошибку
        if os.path.exists(CACHE_FILE):  # Если есть кэш то загружаем из него
            with open(CACHE_FILE, "r") as f:
                data = json.load(f)
            logging.info("Загружены данные из кэша.")
            return data
        else:
            # А если и API не работает, и кэша нет то тут будет показываться ошибка
            messagebox.showerror("Ошибка", "Нет доступа к API и отсутствует кэш.")
            raise


# 3) Добавляем еще класс графического интерфейса
class CurrencyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Агрегатор курсов валют")  # Заголовок окна
        self.geometry("500x300")  # Размер окна
        self.resizable(False, False)  # Запрещаем менять размер окна (можно и расстануть но нужно тогда подстроить динамически а пока просто так)
        self.configure(bg="#f0f0f0")  # Цвет фона

        # Получение данных курсов
        self.data = get_exchange_data()
        self.rates = self.data["rates"]  # Курсы валют
        self.date = self.data["date"]  # Дата обновления

        # Создание всех элементов интерфейса
        self.create_widgets()

    def create_widgets(self):
        """Создает и размещает виджеты (элементы интерфейса)"""
        title = tk.Label(self, text="Конвертер из KZT", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=10)  # Заголовок

        self.amount_entry = tk.Entry(self, font=("Arial", 14), justify="center")  # Поле ввода суммы
        self.amount_entry.pack(pady=5)
        self.amount_entry.insert(0, "1000")  # Значение по умолчанию

        currencies = sorted(self.rates.keys())  # Список валют (отсортированный)
        self.selected_currency = tk.StringVar(value="USD")  # Значение по умолчанию

        # Выпадающий список валют
        dropdown = ttk.Combobox(
            self,
            textvariable=self.selected_currency,
            values=currencies,
            font=("Arial", 12),
            state="readonly",
            justify="center",
            width=10
        )
        dropdown.pack(pady=5)

        # Кнопка для конвертации
        convert_btn = tk.Button(
            self,
            text="Конвертировать",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.convert  # При нажатии запускается метод convert
        )
        convert_btn.pack(pady=10)

        # Метка для вывода результата конвертации
        self.result_label = tk.Label(self, text="", font=("Arial", 14), bg="#f0f0f0")
        self.result_label.pack()

        # Метка для вывода даты, курса и времени запроса
        self.info_label = tk.Label(self, text="", font=("Arial", 10), fg="gray", bg="#f0f0f0")
        self.info_label.pack()

    def convert(self):
        """
        Метод для конвертации введенной суммы в выбранную валюту
        и отображения результата.
        """
        try:
            kzt_amount = float(self.amount_entry.get())  # Получаем сумму в тенге от пользователя
            currency = self.selected_currency.get()  # Получаем выбранную валюту
            rate = self.rates[currency]  # Курс соответствующей валюты
            result = round(kzt_amount * rate, 2)  # Переводим сумму в выбранную валюту

            # Отображение результата в окне
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Текущее время
            self.result_label.config(text=f"{kzt_amount} KZT = {result} {currency}")
            self.info_label.config(text=f"Курс: 1 KZT = {rate:.4f} {currency} | Дата: {self.date}\nВремя запроса: {now}")

            # Логирование действия
            logging.info(f"Конвертация: {kzt_amount} KZT -> {result} {currency} (курс {rate}, дата {self.date})")

        except ValueError:
            # Если введено некорректное значение
            messagebox.showerror("Ошибка ввода", "Введите корректную сумму.")
            logging.warning("Ошибка ввода пользователем.")


# 4) Здесь точка входа в прогу
if __name__ == "__main__":
    app = CurrencyApp()  # Создаем экземпляр приложения
    app.mainloop()  # Запускаем главный цикл обработки событий
