import sys
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QLineEdit, 
                             QComboBox, QSpinBox, QGridLayout, 
                             QMessageBox, QTextEdit)
from PyQt5.QtGui import QFont

class RandomGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.is_dark_theme = True
        self.history = []
        self.initUI()

    def initUI(self):
        # Настройки окна
        self.setWindowTitle('Генератор Случайных Чисел')
        self.setGeometry(100, 100, 600, 700)

        # Кнопки управления
        self.theme_button = QPushButton("Светлая тема")
        self.theme_button.clicked.connect(self.toggle_theme)

        self.help_button = QPushButton("?")
        self.help_button.clicked.connect(self.show_help)

        self.export_button = QPushButton("Экспорт")
        self.export_button.clicked.connect(self.export_history)

        # Основной макет
        layout = QGridLayout()
        layout.addWidget(self.theme_button, 0, 0)
        layout.addWidget(self.help_button, 0, 1)
        layout.addWidget(self.export_button, 0, 2)

        # Результат
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setFont(QFont("Arial", 16))
        layout.addWidget(self.result, 1, 0, 1, 5)

        # Минимальное значение
        layout.addWidget(QLabel('Минимальное значение:'), 2, 0)
        self.min_input = QSpinBox()
        self.min_input.setRange(-1000000, 1000000)
        layout.addWidget(self.min_input, 2, 1)

        # Максимальное значение
        layout.addWidget(QLabel('Максимальное значение:'), 2, 2)
        self.max_input = QSpinBox()
        self.max_input.setRange(-1000000, 1000000)
        self.max_input.setValue(100)
        layout.addWidget(self.max_input, 2, 3)

        # Тип генерации
        layout.addWidget(QLabel('Тип генерации:'), 3, 0)
        self.generation_type = QComboBox()
        self.generation_type.addItems([
            'Случайные числа', 
            'Уникальные числа', 
            'Взвешенная генерация'
        ])
        layout.addWidget(self.generation_type, 3, 1)

        # Тип числа
        layout.addWidget(QLabel('Тип числа:'), 3, 2)
        self.type_select = QComboBox()
        self.type_select.addItems(['Целое', 'Вещественное'])
        layout.addWidget(self.type_select, 3, 3)

        # Количество
        layout.addWidget(QLabel('Количество:'), 4, 0)
        self.count_input = QSpinBox()
        self.count_input.setRange(1, 1000)
        self.count_input.setValue(1)
        layout.addWidget(self.count_input, 4, 1)

        # Кнопка генерации
        self.generate_button = QPushButton("Сгенерировать")
        self.generate_button.clicked.connect(self.generate_numbers)
        layout.addWidget(self.generate_button, 5, 0, 1, 5)

        self.setLayout(layout)
        self.apply_theme()

    def generate_numbers(self):
        try:
            min_val = self.min_input.value()
            max_val = self.max_input.value()
            count = self.count_input.value()
            generation_type = self.generation_type.currentText()
            num_type = 'int' if self.type_select.currentText() == 'Целое' else 'float'

            if min_val > max_val:
                self.result.setText("Минимальное значение не может быть больше максимального!")
                return

            if generation_type == 'Случайные числа':
                if num_type == 'int':
                    numbers = [random.randint(min_val, max_val) for _ in range(count)]
                else:
                    numbers = [round(random.uniform(min_val, max_val), 2) for _ in range(count)]
                result_text = f"Сгенерированы числа ({count} шт.):\n{numbers}"

            elif generation_type == 'Уникальные числа':
                numbers = random.sample(range(min_val, max_val + 1), count)
                result_text = f"Сгенерированы уникальные числа:\n{numbers}"

            elif generation_type == 'Взвешенная генерация':
                numbers = [1, 2, 3, 4, 5]
                weights = [0.1, 0.2, 0.3, 0.2, 0.2]
                weighted_numbers = random.choices(numbers, weights=weights, k=count)
                result_text = f"Сгенерированы взвешенные числа:\n{weighted_numbers}"

            self.result.setText(result_text)
            self.history.append(result_text)
        except Exception as e:
            self.result.setText(f"Ошибка: {str(e)}")

    def apply_theme(self):
        if self.is_dark_theme:
            self.setStyleSheet("""
                background-color: #2E2E2E; 
                color: white;
            """)
            self.theme_button.setStyleSheet("""
                background-color: #4C4C4C; 
                color: white;
            """)
            self.help_button.setStyleSheet("""
                background-color: #4C4C4C; 
                color: white;
            """)
            self.export_button.setStyleSheet("""
                background-color: #4C4C4C; 
                color: white;
            """)
            self.result.setStyleSheet("""
                background-color: #1E1E1E; 
                color: white;
            """)
        else:
            self.setStyleSheet("""
                background-color: #FFFFFF; 
                color: black;
            """)
            self.theme_button.setStyleSheet("""
                background-color: #CCCCCC; 
                color: black;
            """)
            self.help_button.setStyleSheet("""
                background-color: #CCCCCC; 
                color: black;
            """)
            self.export_button.setStyleSheet("""
                background-color: #CCCCCC; 
                color: black;
            """)
            self.result.setStyleSheet("""
                background-color: #F0F0F0; 
                color: black;
            """)

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()

    def show_help(self):
        QMessageBox.information(self, "Справка", 
            "Генератор случайных чисел:\n"
            "1. Выберите минимальное и максимальное значения.\n"
            "2. Выберите тип генерации.\n"
            "3. Укажите количество чисел для генерации.\n" "4. Нажмите 'Сгенерировать' для получения результата.")

    def export_history(self):
        with open("history.txt", "w") as file:
            for entry in self.history:
                file.write(entry + "\n")
        QMessageBox.information(self, "Экспорт", "История генерации экспортирована в history.txt")

def main():
    app = QApplication(sys.argv)
    generator = RandomGenerator()
    generator.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()