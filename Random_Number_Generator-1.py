import sys
import random
import re
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                            QGridLayout, QLineEdit, QLabel, QProgressBar, 
                            QTextEdit, QMessageBox, QComboBox, QSpinBox)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

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

class RandomGenerator(QWidget):
    """
    Класс для создания графического интерфейса генератора случайных чисел.
    """
    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.is_dark_theme = True
        self.setWindowTitle("Генератор Случайных Чисел")
        self.setGeometry(100, 100, 600, 600)

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

        layout.addWidget(QLabel("Тип числа:"), 3, 0)
        self.type_select = QComboBox()
        self.type_select.addItems(['Целое', 'Вещественное'])
        layout.addWidget(self.type_select, 3, 1)

        layout.addWidget(QLabel("Количество чисел:"), 3, 2)
        self.count_input = QSpinBox()
        self.count_input.setRange(1, 1000)
        self.count_input.setValue(1)
        layout.addWidget(self.count_input, 3, 3)

        # Кнопка генерации
        self.generate_button = QPushButton("Сгенерировать")
        self.generate_button.clicked.connect(self.generate_numbers)
        layout.addWidget(self.generate_button, 4, 0, 1, 5)

        self.setLayout(layout)
        self.apply_theme()

    def generate_numbers(self):
        """
        Генерация случайных чисел.
        """
        try:
            min_val = self.min_input.value()
            max_val = self.max_input.value()
            num_type = 'int' if self.type_select.currentText() == 'Целое' else 'float'
            count = self.count_input.value()

            if min_val > max_val:
                self.result.setText("Минимальное значение не может быть больше максимального!")
                return

            if count == 1:
                # Генерация одного числа
                number = RandomNumberGenerator.generate_random_number(min_val, max_val, num_type)
                result_text = f"Сгенерировано число: {number}"
            else:
                # Генерация последовательности
                numbers = RandomNumberGenerator.generate_random_sequence(count, min_val, max_val, num_type)
                result_text = f"Сгенерированы числа ({count} шт.):\n{numbers}"

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
            "1. Вы берите минимальное и максимальное значения.\n"
            "2. Выберите тип числа (целое или вещественное).\n"
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
    