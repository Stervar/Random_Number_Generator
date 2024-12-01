import sys
import random
import re
import secrets
import string
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                            QGridLayout, QLineEdit, QLabel, QProgressBar, 
                            QTextEdit, QMessageBox, QComboBox, QSpinBox, 
                            QCheckBox, QDialog)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class RandomNumberGenerator:
    """
    Класс для генерации случайных чисел.
    """
    @staticmethod
    def generate_random_number(min_val, max_val, num_type='int'):
        """
        Генерация случайного числа.
        """
        try:
            if num_type == 'int':
                return random.randint(min_val, max_val)
            elif num_type == 'float':
                return round(random.uniform(min_val, max_val), 2)
        except Exception as e:
            return f"Ошибка: {str(e)}"

    @staticmethod
    def generate_random_sequence(length, min_val, max_val, num_type='int'):
        """
        Генерация последовательности случайных чисел.
        """
        try:
            if num_type == 'int':
                return [random.randint(min_val, max_val) for _ in range(length)]
            elif num_type == 'float':
                return [round(random.uniform(min_val, max_val), 2) for _ in range(length)]
        except Exception as e:
            return f"Ошибка: {str(e)}"

    @staticmethod
    def generate_unique_numbers(min_val, max_val, count):
        """
        Генерация уникальных случайных чисел
        """
        try:
            return random.sample(range(min_val, max_val + 1), count)
        except ValueError:
            return "Невозможно сгенерировать уникальные числа с заданными параметрами"

    @staticmethod
    def generate_weighted_random(numbers, weights, count):
        """
        Генерация чисел с весовыми коэффициентами
        """
        return random.choices(numbers, weights=weights, k=count)

    @staticmethod
    def generate_advanced_numbers(distribution, count):
        """
        Генерация чисел с расширенными настройками
        """
        if distribution == 'Равномерное':
            return [random.uniform(0, 1) for _ in range(count)]
        elif distribution == 'Нормальное':
            return [random.gauss(0, 1) for _ in range(count)]
        elif distribution == 'Экспоненциальное':
            return [random.expovariate(1) for _ in range(count)]
        elif distribution == 'Пуассона':
            return [random.poisson(3) for _ in range(count)]

    @staticmethod
    def generate_crypto_secure_numbers(min_val, max_val, count):
        """
        Генерация криптографически стойких случайных чисел
        """
        return [secrets.randbelow(max_val - min_val + 1) + min_val 
                for _ in range(count)]

    @staticmethod
    def generate_password(length, use_uppercase=True, use_numbers=True, use_symbols=True):
        """
        Генерация случайных паролей
        """
        characters = string.ascii_lowercase
        if use_uppercase:
            characters += string.ascii_uppercase
        if use_numbers:
            characters += string.digits
        if use_symbols:
            characters += string.punctuation
        
        return [''.join(random.choice(characters) for _ in range(length)) 
                for _ in range(5)]  # Генерируем 5 паролей

class RandomGenerator(QWidget):
    """
    Класс для создания графического интерфейса генератора случайных чисел.
    """
    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.is_dark_theme = True
        self.setWindowTitle("Генератор Случайных Чисел")
        self.setGeometry(100, 100, 800, 800)

        self.history = []
        font = QFont("Arial", 16)

        # Кнопки управления
        self.theme_button = QPushButton("Светлая тема")
        self.theme_button.clicked.connect(self.toggle_theme)

        self.help_button = QPushButton("?")
        self.help_button.clicked.connect(self.show_help)

        self.export_button = QPushButton("Экспорт")
        self.export_button.clicked.connect(self.export_history)

        layout = QGridLayout()
        layout.addWidget(self.theme_button, 0, 0)
        layout.addWidget(self.help_button, 0, 1)
        layout.addWidget(self.export_button, 0, 2)

        # Результат
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setFont(font)
        layout.addWidget(self.result, 1, 0, 1, 5)

        # Элементы управления
        layout.addWidget(QLabel("Минимальное значение:"), 2, 0)
        self.min_input = QSpinBox()
        self.min_input.setRange(-1000000, 1000000)
        layout.addWidget(self.min_input, 2, 1)

        layout.addWidget(QLabel("Максимальное значение:"), 2, 2)
        self.max_input = QSpinBox()
        self.max_input.setRange(-1000000, 1000000)
        self.max_input.setValue(100)
        layout.addWidget(self.max_input, 2, 3)

        # Тип генерации
        layout.addWidget(QLabel("Тип генерации:"), 3, 0)
        self.generation_type = QComboBox()
        self.generation_type.addItems([
            'Случайные числа', 
            'Уникальные числа', 
            'Взвешенная генерация', 
            'Распределение', 
            'Криптостойкие', 
            'Генератор паролей'
        ])
        self.generation_type.currentIndexChanged.connect(self.update_generation_ui)
        layout.addWidget(self.generation_type, 3, 1)

        # Тип числа
        layout.addWidget(QLabel("Тип числа:"), 3, 2)
        self.type_select = QComboBox()
        self.type_select.addItems(['Целое', 'Вещественное'])
        layout.addWidget(self.type_select, 3, 3)

        # Количество
        layout.addWidget(QLabel("Количество:"), 4, 0)
        self.count_input = QSpinBox()
        self.count_input.setRange(1, 1000)
        self.count_input.setValue(1)
        layout.addWidget(self.count_input, 4, 1)

        # Дополнительные элементы для специальных генераций
        self.extra_layout = QGridLayout()
        layout.addLayout(self.extra_layout , 5, 0, 1, 5)

        # Элементы для генерации паролей
        self.uppercase_check = QCheckBox("Заглавные буквы")
        self.numbers_check = QCheckBox("Цифры")
        self.symbols_check = QCheckBox("Спецсимволы")
        self.extra_layout.addWidget(self.uppercase_check, 0, 0)
        self.extra_layout.addWidget(self.numbers_check, 0, 1)
        self.extra_layout.addWidget(self.symbols_check, 0, 2)

        # Элементы для распределения
        self.distribution_select = QComboBox()
        self.distribution_select.addItems([
            'Равномерное', 
            'Нормальное', 
            'Экспоненциальное', 
            'Пуассона'
        ])
        self.extra_layout.addWidget(QLabel("Распределение:"), 1, 0)
        self.extra_layout.addWidget(self.distribution_select, 1, 1)

        # Кнопка генерации
        self.generate_button = QPushButton("Сгенерировать")
        self.generate_button.clicked.connect(self.generate_numbers)
        layout.addWidget(self.generate_button, 6, 0, 1, 5)

        self.setLayout(layout)
        self.apply_theme()

    def update_generation_ui(self):
        """
        Обновление UI в зависимости от выбранного типа генерации.
        """
        selected_type = self.generation_type.currentText()
        self.extra_layout.setEnabled(selected_type in ['Уникальные числа', 'Взвешенная генерация', 'Распределение', 'Генератор паролей'])
        self.uppercase_check.setEnabled(selected_type == 'Генератор паролей')
        self.numbers_check.setEnabled(selected_type == 'Генератор паролей')
        self.symbols_check.setEnabled(selected_type == 'Генератор паролей')
        self.distribution_select.setEnabled(selected_type == 'Распределение')

    def generate_numbers(self):
        """
        Генерация случайных чисел.
        """
        try:
            min_val = self.min_input.value()
            max_val = self.max_input.value()
            count = self.count_input.value()
            generation_type = self.generation_type.currentText()

            if min_val > max_val:
                self.result.setText("Минимальное значение не может быть больше максимального!")
                return

            if generation_type == 'Случайные числа':
                num_type = 'int' if self.type_select.currentText() == 'Целое' else 'float'
                numbers = RandomNumberGenerator.generate_random_sequence(count, min_val, max_val, num_type)
                result_text = f"Сгенерированы числа ({count} шт.):\n{numbers}"

            elif generation_type == 'Уникальные числа':
                unique_numbers = RandomNumberGenerator.generate_unique_numbers(min_val, max_val, count)
                result_text = f"Сгенерированы уникальные числа:\n{unique_numbers}"

            elif generation_type == 'Взвешенная генерация':
                numbers = [1, 2, 3, 4, 5]
                weights = [0.1, 0.2, 0.3, 0.2, 0.2]
                weighted_numbers = RandomNumberGenerator.generate_weighted_random(numbers, weights, count)
                result_text = f"Сгенерированы взвешенные числа:\n{weighted_numbers}"

            elif generation_type == 'Распределение':
                distribution = self.distribution_select.currentText()
                advanced_numbers = RandomNumberGenerator.generate_advanced_numbers(distribution, count)
                result_text = f"Сгенерированы числа по распределению {distribution}:\n{advanced_numbers}"

            elif generation_type == 'Криптостойкие':
                secure_numbers = RandomNumberGenerator.generate_crypto_secure_numbers(min_val, max_val, count)
                result_text = f"Сгенерированы криптографически стойкие числа:\n{secure_numbers}"

            elif generation_type == 'Генератор паролей':
                length = self.count_input.value()
                passwords = RandomNumberGenerator.generate_password(length, self.uppercase_check.isChecked(), self.numbers_check.isChecked(), self.symbols_check.isChecked())
                result_text = f"Сгенерированные пароли:\n{passwords}"

            self.result.setText(result_text)
            self.history.append(result_text)
        except Exception as e:
            self.result.setText(f"Ошибка: {str(e)}")

    def apply_theme(self):
        """
        Применение темы.
        """
        if self.is_dark_theme:
            self.setStyleSheet("background-color: #2E2E2E; color: white;")
            self.theme_button.setStyleSheet("background-color: #4C4C4C; color: white;")
            self.help_button.setStyleSheet("background-color: #4C4C4C; color: white;")
            self.export_button.setStyleSheet("background-color: #4C4C4C; color: white;")
            self.result.setStyleSheet("background-color: #1E1E1E; color: white;")
        else:
            self.setStyleSheet("background-color: #FFFFFF; color: black;")
            self.theme_button.setStyleSheet("background-color: #CCCCCC; color: black;")
            self.help_button.setStyleSheet("background-color: #CCCCCC; color: black;")
            self.export_button.setStyleSheet("background-color: #CCCCCC; color: black;")
            self.result.setStyleSheet("background-color: #F0F0F0; color: black;")

    def toggle_theme(self):
        """
        Переключение темы.
        """
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()

    def show_help(self):
        """
        Показ справки.
        """
        QMessageBox.information(self, "Справка", 
            "Генератор случайных чисел:\n"
            "1. Выберите минимальное и максимальное значения.\n"
            "2. Выберите тип генерации.\n"
            "3. Укажите количество чисел для генерации.\n"
            "4. Нажмите 'Сгенерировать' для получения результата.")

    def export_history(self):
        """
        Экспортировать историю генерации в текстовый файл.
        """
        with open("history.txt", "w") as file:
            for entry in self.history:
                file.write(entry + "\n")
        QMessageBox.information(self, "Экспорт", "История генерации экспортирована в history.txt")

class SplashScreen(QWidget):
    """
    Класс для отображения заставки при запуске приложения.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Загрузка")
        self.setGeometry(100, 100, 600, 600)
        self.setStyleSheet("background-color: #2E2E2E;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Логотип
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("logo.png").scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setStyleSheet("opacity: 0;")
        layout.addWidget(self.logo)

        # Заголовок
        self.title = QLabel("")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: white; font-size: 50px; opacity: 0;")
        layout.addWidget(self.title)

        # Индикатор загрузки
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        # Кнопка с текстом
        self.footer_button = QPushButton('Создано Габеркорн Вадимом')
        self.footer_button.setStyleSheet("""
    QPushButton {
        background-color: #FFD700;  
        color: black; 
        font-size: 18px; 
        font-weight: bold; 
        border: 2px solid #FFA500;  
        border-radius: 10px; 
        padding: 10px 20px;  
        max-width: 350px;   
    }
    QPushButton:hover {
        background-color: #FFA500;  
        border: 2px solid #FF8C00;  
    }
""")
        self.footer_button.setFixedWidth(350)
        self.footer_button.setCursor(Qt.PointingHandCursor)

        layout.addStretch()
        layout.addWidget(self.footer_button, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)

        # Анимация для логотипа
        self.logo_animation = QPropertyAnimation(self.logo, b"opacity")
        self.logo_animation.setDuration(2000)
        self.logo_animation.setStartValue(0)
        self.logo_animation.setEndValue(1)

        # Таймер для обновления индикатора загрузки
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)

        self.show()
        self.logo_animation.start()

        # Инициализация анимации заголовка
        self.title_text = "RANDOM NUMBER GENERATOR"
        self.title_index = 0
        self.title_timer = QTimer()
        self.title_timer.timeout.connect(self.update_title)
        self.title_timer.start(200)

    def update_title(self):
        """
        Обновление заголовка заставки.
        """
        if self.title_index < len(self.title_text):
            self.title.setText(self.title.text() + self.title_text[self.title_index])
            self.title_index += 1
        else:
            self.title_timer.stop()

        if self.title_index == len(self.title_text):
            self.title_animation = QPropertyAnimation(self.title, b"opacity")
            self.title_animation.setDuration(8000)
            self.title_animation.setStartValue(0)
            self.title_animation.setEndValue(1)
            self.title_animation.start()

    def update_progress(self):
        """
        Обновление индикатора загрузки.
        """
        value = self.progress.value() + 4
        if value > 100:
            self.timer.stop()
            self.close()
            self.open_generator()
        self.progress.setValue(value)

    def open_generator(self):
        """
        Открытие основного окна генератора случайных чисел.
        """
        self.generator = RandomGenerator()
        self.generator.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    sys.exit(app.exec_())