import re
import math
import sys
import yaml

class ConfigParser:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.constants = {}
        self.data = []

    def parse(self):
        with open(self.input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if not line or self.is_comment(line):
                continue

            if '->' in line:
                self.handle_constant_declaration(line)
            elif '@[' in line:
                self.handle_constant_expression(line)
            elif '({' in line and '})' in line:
                self.handle_array(line)
            else:
                self.handle_value(line)

        # Запишем данные в YAML
        self.write_output()

    def is_comment(self, line):
        return line.startswith('||') or line.startswith('{-')

    def handle_constant_declaration(self, line):
        match = re.match(r'(\w+) -> (.+);', line)
        if match:
            name, value = match.groups()
            self.constants[name] = self.evaluate_expression(value)
            self.data.append(self.constants[name])

    def handle_constant_expression(self, line):
        match = re.match(r'@(\[(.*?)\])', line)
        if match:
            expression = match.group(2)
            result = self.evaluate_expression(expression)
            self.data.append(result)

    def handle_array(self, line):
        match = re.match(r'\(\{(.+)\}\)', line)
        if match:
            values = match.group(1).split(',')
            array = [self.evaluate_expression(value.strip()) for value in values]
            self.data.append(array)  # Добавляем как список

    def handle_value(self, line):
        value = self.evaluate_expression(line)
        self.data.append(value)

    def evaluate_expression(self, expression):
        expression = self.resolve_constants(expression)
        expression = expression.replace("mod", "%").replace("sqrt", "math.sqrt")

        if expression.startswith('@[') and expression.endswith(']'):
            expression = expression[2:-1].strip()

        try:
            result = eval(expression, {"__builtins__": None}, {"math": math, "mod": lambda x, y: x % y})
            return result
        except Exception as e:
            raise SyntaxError(f"Ошибка при вычислении выражения {expression}: {str(e)}")

    def resolve_constants(self, expression):
        for name, value in self.constants.items():
            expression = expression.replace(name, str(value))
        return expression

    def write_output(self):
        # Преобразуем данные в список
        data_for_yaml = self._convert_data(self.data)
        
        # Записываем данные в YAML, выводим как список, а не множества
        with open(self.output_file, 'w', encoding='utf-8') as file:
            yaml.dump(data_for_yaml, file, allow_unicode=True)

    def _convert_data(self, data):
        """Преобразуем все множества (set) в списки (list) перед записью в YAML"""
        converted_data = []
        for item in data:
            if isinstance(item, set):  # Если это множество
                converted_data.append(list(item))  # Преобразуем в список
            else:
                converted_data.append(item)
        return converted_data

def main():
    if len(sys.argv) != 3:
        print("Usage: python config_parser.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    parser = ConfigParser(input_file, output_file)
    try:
        parser.parse()
        print("Конфигурация успешно обработана.")
    except SyntaxError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
