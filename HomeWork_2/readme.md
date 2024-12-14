# Визуализатор зависимостей для Git

Этот инструмент анализирует Git-репозиторий, извлекает информацию о коммитах и изменениях в файлах, а затем генерирует граф зависимостей в формате Mermaid.

## Описание
Программа:
1. Получает информацию о коммитах в репозитории.
2. Строит зависимость между коммитами и файлами.
3. Генерирует Mermaid-код для визуализации.

## Структура конфигурационного файла
Конфигурационный файл должен быть в формате XML и содержать пути к репозиторию и файлу для записи результатов:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config>
    <repo_path>путь_к_репозиторию</repo_path>
    <output_path>путь_к_выходному_файлу</output_path>
</config>
```
## Запуск программы
1. Сохраните конфигурационный файл (например, config.xml).
2. Запустите программу с командой:
```bash
python visualizer.py config.xml
```
## Пример вывода
Программа генерирует Mermaid-код, который можно визуализировать с помощью Mermaid Live Editor:

## mermaid
```
graph TD
    abb9af2["Initial commit\nabb9af2528b8e1e31123f3bb7cb1f76fa010604d"]
    abb9af2 --> ".gitattributes (A)"
    380557a["commit1\n380557a92976c0f799dbf34c32b638b2d1675d34"]
    abb9af2 --> 380557a
    380557a --> "test1.txt (A)"
    5ac3fd2["commit2\n5ac3fd2e3920865af17226263ed1b4b63126d319"]
    380557a --> 5ac3fd2
    5ac3fd2 --> "test1.txt (M)"
    5ac3fd2 --> "test2.txt (A)"
    9c5b2d4["commit3\n9c5b2d444cc4793ffba50d4e8548f231d4d27fc5"]
    5ac3fd2 --> 9c5b2d4
    9c5b2d4 --> "test1.txt (D)"
    9c5b2d4 --> "test3.txt (A)"
    5dd4f14["commit4\n5dd4f1495ee04d704f82d03a8dfb40959cf6a8a1"]
    9c5b2d4 --> 5dd4f14
    5dd4f14 --> "test2.txt (D)"
    5dd4f14 --> "test3.txt (M)"
    5dd4f14 --> "test4.txt (A)"
```
## Сгенерированный Mermaid
(![image](https://github.com/user-attachments/assets/ef6148d1-7fa9-4401-a2a2-99dd2936dad0)

