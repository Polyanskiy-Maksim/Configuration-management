# Практическое занятие №2  
---

## Задание 1: Пакет `matplotlib` (Python)

**Описание:**  
1. Вывести служебную информацию о пакете `matplotlib`.  
2. Разобрать основные элементы содержимого файла со служебной информацией из пакета.  
3. Как получить пакет без менеджера пакетов, прямо из репозитория?

**Выполнение:**  
- **Команда для вывода информации о пакете:**  
  ``` python
  pip show matplotlib
  ```
  ![image](https://github.com/user-attachments/assets/225e5e20-e2a9-453a-b966-8de0ce19e351)



- **Основные элементы служебной информации:**  
  Name: Название пакета (например, matplotlib).
Version: Версия пакета (например, 3.4.3).
Summary: Краткое описание пакета.
Home-page: Ссылка на домашнюю страницу пакета.
Author: Автор пакета.
Author-email: Электронная почта автора.
License: Лицензия, под которой распространяется пакет.
Location: Путь к установленному пакету.
Requires: Список зависимостей, необходимых для работы пакета.
Required-by: Список пакетов, которые зависят от данного пакета.

- **Как получить пакет без менеджера пакетов:**  
 ``` python
  it clone https://github.com/matplotlib/matplotlib.git
 ```
 ``` python
  cd matplotlib
  python setup.py install
  ```

---

## Задание 2: Пакет `express` (JavaScript)

**Описание:**  
1. Вывести служебную информацию о пакете `express`.  
2. Разобрать основные элементы содержимого файла со служебной информацией из пакета.  
3. Как получить пакет без менеджера пакетов, прямо из репозитория?

**Выполнение:**  
- **Команда для вывода информации о пакете:**  
  ``` python
  npm view express
  ```
  ![image](https://github.com/user-attachments/assets/2c86c8cf-1688-4435-9637-acb584df7cfc)



- **Основные элементы служебной информации:**  
  Name: Название пакета (например, express).
Version: Версия пакета (например, 4.17.1).
Description: Краткое описание пакета.
Homepage: Ссылка на домашнюю страницу пакета.
License: Лицензия, под которой распространяется пакет.
Dependencies: Список зависимостей, необходимых для работы пакета.
Dist: Объект с информацией о дистрибутиве, включая URL для загрузки.

- **Как получить пакет без менеджера пакетов:**  
  ``` python
  git clone https://github.com/expressjs/express.git
  ```

---

## Задание 3: Зависимости пакетов

**Описание:**  
1. Сформировать graphviz-код для отображения зависимостей пакетов `matplotlib` и `express`.  
2. Получить изображение зависимостей.

**Выполнение:**  
![image](https://github.com/user-attachments/assets/6880bad9-55ad-4366-ac1b-67944e1ffbc3)

  ``` python
  sudo apt install graphviz

  ```
``` python
  dot -Tpng dependencies.dot -o dependencies.png

  ```
![dependencies](https://github.com/user-attachments/assets/92343eae-b221-4bf7-9f4e-1e6a7259f03b)

## Задание 4: MiniZinc - Задача о счастливых билетах

**Описание:**  
1. Установить MiniZinc.  
2. Разобраться с основами синтаксиса и работы в IDE.  
3. Решить задачу о счастливых билетах с ограничением на то, что все цифры должны быть различными.  
4. Найти минимальное решение для суммы 3 цифр.

**Выполнение:**  
![image](https://github.com/user-attachments/assets/8e2eb445-5622-4674-924d-128c21823a1f)


---

## Задание 5: MiniZinc - Зависимости пакетов

**Описание:**  
Решить задачу о зависимостях пакетов для рисунка, приведенного ниже.
![image](https://github.com/user-attachments/assets/3cf0ea24-ef0e-425c-8312-76dbeba444ed)


**Выполнение:**  
![image](https://github.com/user-attachments/assets/3ab1dc04-7d76-411f-bab5-77e7d53d2eab)


---

## Задание 6: MiniZinc - Зависимости пакетов (часть 2)

**Описание:**  
Решить задачу о зависимостях пакетов для следующих данных.
```
root 1.0.0 зависит от foo ^1.0.0 и target ^2.0.0.
foo 1.1.0 зависит от left ^1.0.0 и right ^1.0.0.
foo 1.0.0 не имеет зависимостей.
left 1.0.0 зависит от shared >=1.0.0.
right 1.0.0 зависит от shared <2.0.0.
shared 2.0.0 не имеет зависимостей.
shared 1.0.0 зависит от target ^1.0.0.
target 2.0.0 и 1.0.0 не имеют зависимостей.
```

**Выполнение:**  
```
var int: root_major = 1; 
var int: root_minor = 0; 
var int: root_patch = 0;

set of int: foo_major = {0, 1}; 
var int: foo_major_version; 
var int: foo_minor_version = 0; 
var int: foo_patch_version = 0;

var int: left_major = 1; 
var int: left_minor = 0; 
var int: left_patch = 0;

var int: right_major = 1; 
var int: right_minor = 0; 
var int: right_patch = 0;

set of int: shared_major = {0, 1}; 
var int: shared_major_version; 
var int: shared_minor_version = 0; 
var int: shared_patch_version = 0;

set of int: target_major = {1, 2}; 
var int: target_major_version; 
var int: target_minor_version = 0; 
var int: target_patch_version = 0;

constraint (foo_major_version == 1 -> (target_major_version == 2));
constraint (foo_major_version == 1 -> (left_major == 1) /\ (right_major == 1));
constraint (left_major == 1 -> (shared_major_version >= 1));
constraint (right_major == 1 -> (shared_major_version < 2));

constraint foo_major_version in foo_major;
constraint left_major in {0, 1};
constraint right_major in {0, 1};
constraint shared_major_version in shared_major;
constraint target_major_version in target_major;

solve satisfy;

output [
    "root version: ", show(root_major), ".", show(root_minor), ".", show(root_patch), "\n",
    "foo version: ", show(foo_major_version), ".", show(foo_minor_version), ".", show(foo_patch_version), "\n",
    "left version: ", show(left_major), ".", show(left_minor), ".", show(left_patch), "\n",
    "right version: ", show(right_major), ".", show(right_minor), ".", show(right_patch), "\n",
    "shared version: ", show(shared_major_version), ".", show(shared_minor_version), ".", show(shared_patch_version), "\n",
    "target version: ", show(target_major_version), ".", show(target_minor_version), ".", show(target_patch_version)
];
```
**Выполнение:**  
![image](https://github.com/user-attachments/assets/13305073-65f1-4791-8e18-1601fe8ead83)



---

## Задание 7: Phython - Общая форма задачи о зависимостях пакетов

**Описание:**  
Представить задачу о зависимостях пакетов в общей форме, чтобы конкретный экземпляр задачи описывался только своим набором данных.

**Выполнение:**  
``` python
import pkg_resources

def show_package_dependencies(package_name):
    try:
        # Получаем информацию о пакете
        distribution = pkg_resources.get_distribution(package_name)
        print(f"Package: {distribution.project_name} ({distribution.version})")
        print("Dependencies:")
        
        # Получаем зависимости
        dependencies = distribution.requires()
        if dependencies:
            for dep in dependencies:
                print(f" - {dep}")
        else:
            print(" No dependencies")
    except pkg_resources.DistributionNotFound:
        print(f"Package '{package_name}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Задаем имена пакетов, для которых нужно вывести зависимости
    packages = ["requests", "numpy", "matplotlib"]
    
    for package in packages:
        show_package_dependencies(package)
        print()  # Печатаем пустую строку для разделения вывода

```
![Снимок экрана 2024-10-02 173327](https://github.com/user-attachments/assets/375e2ef2-9b73-4224-8f23-bebc8474c4f1)


