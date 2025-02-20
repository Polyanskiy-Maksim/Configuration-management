# Отчет по эмулятору командной строки

## Описание
Эмулятор реализует базовый интерфейс командной строки с поддержкой следующих команд:
- **ls**: выводит содержимое текущей директории.
- **cd**: изменяет текущую директорию, исключая возможность выхода за верхний уровень файловой системы.
- **exit**: завершает выполнение программы.
- **find**: ищет файлы и директории по имени.
- **uname**: выводит информацию об операционной системе.
- **mkdir**: создает новую директорию.

## Особенности
1. **Защита от выхода за пределы верхнего уровня**:
   - Реализована проверка, чтобы пользователь не мог выйти выше корневой директории виртуальной файловой системы.
2. **Отображение команд**:
   - Каждая введенная команда отображается в консоли перед выполнением.
3. **Поддержка скриптов**:
   - Возможность загрузки и выполнения команд из файла скрипта.
4. **Графический интерфейс**:
   - Используется библиотека `tkinter` для реализации текстового интерфейса.

## Структура файловой системы
- Виртуальная файловая система извлекается из указанного TAR-архива и работает в рамках папки `virtual_fs`.


## Пример использования
- **Запуск**: 
  ```bash
  python emulator.py virtual_fs.tar

