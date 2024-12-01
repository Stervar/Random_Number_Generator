import sys
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QLineEdit, 
                             QComboBox, QSpinBox)

class SimpleRandomGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Настройки окна
        self.setWindowTitle('Генератор Случайных Чисел')
        self.setGeometry(100, 100, 400, 300)

        # Основной макет
        layout = QVBoxLayout()

        # Минимальное значение
        layout.addWidget(QLabel('Минимальное значение:'))
        self.min_input = QSpinBox()
        self.min_input.setRange(-1000, 1000)
        layout.addWidget(self.min_input)

        # Максимальное значение
        layout.addWidget(QLabel('Максимальное значение:'))
        self.max_input = QSpinBox()
        self.max_input.setRange(-1000, 1000)
        self.max_input.setValue(100)
        layout.addWidget(self.max_input)

        # Тип генерации
        layout.addWidget(QLabel('Тип генерации:'))
        self.type_select = QComboBox()
        self.type_select.addItems(['Случайное число', 'Последовательность'])
        layout.addWidget(self.type_select)

        # Количество чисел
        layout.addWidget(QLabel('Количество:'))
        self.count_input = QSpinBox()
        self.count_input.setRange(1, 100)
        layout.addWidget(self.count_input)

        # Кнопка генерации
        generate_button = QPushButton('Сгенерировать')
        generate_button.clicked.connect(self.generate_numbers)
        layout.addWidget(generate_button)

        # Результат
        self.result_label = QLabel('Результат:')
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def generate_numbers(self):
        # Получаем параметры
        min_val = self.min_input.value()
        max_val = self.max_input.value()
        gen_type = self.type_select.currentText()
        count = self.count_input.value()

        # Проверка корректности диапазона
        if min_val > max_val:
            self.result_label.setText('Ошибка: Мин. значение больше макс.')
            return

        # Генерация
        try:
            if gen_type == 'Случайное число':
                result = random.randint(min_val, max_val)
                self.result_label.setText(f'Случайное число: {result}')
            else:
                result = [random.randint(min_val, max_val) for _ in range(count)]
                self.result_label.setText(f'Последовательность: {result}')
        except Exception as e:
            self.result_label.setText(f'Ошибка: {str(e)}')

def main():
    app = QApplication(sys.argv)
    generator = SimpleRandomGenerator()
    generator.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()