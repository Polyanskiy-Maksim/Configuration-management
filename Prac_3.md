# Практическое занятие №3. Конфигурационные языки  
**П.Н. Советов, РТУ МИРЭА**

## Введение

В рамках данного занятия было изучено понятие программируемых конфигурационных языков, таких как **Jsonnet**, **Dhall** и **CUE**. Основное внимание уделялось принципам **DRY** (Don't Repeat Yourself) и **программируемости**, которые позволяют эффективно управлять конфигурациями.

## Задачи

### Задача 1

**Реализовать на Jsonnet приведенный ниже пример в формате JSON. Использовать в реализации свойство программируемости и принцип DRY.**

#### Исходный JSON:

```json
{
  "groups": [
    "ИКБО-1-20",
    "ИКБО-2-20",
    "ИКБО-3-20",
    "ИКБО-4-20",
    "ИКБО-5-20",
    "ИКБО-6-20",
    "ИКБО-7-20",
    "ИКБО-8-20",
    "ИКБО-9-20",
    "ИКБО-10-20",
    "ИКБО-11-20",
    "ИКБО-12-20",
    "ИКБО-13-20",
    "ИКБО-14-20",
    "ИКБО-15-20",
    "ИКБО-16-20",
    "ИКБО-17-20",
    "ИКБО-18-20",
    "ИКБО-19-20",
    "ИКБО-20-20",
    "ИКБО-21-20",
    "ИКБО-22-20",
    "ИКБО-23-20",
    "ИКБО-24-20"
  ],
  "students": [
    {
      "age": 19,
      "group": "ИКБО-4-20",
      "name": "Иванов И.И."
    },
    {
      "age": 18,
      "group": "ИКБО-5-20",
      "name": "Петров П.П."
    },
    {
      "age": 18,
      "group": "ИКБО-5-20",
      "name": "Сидоров С.С."
    },
    {
      "age": 19,
      "group": "ИКБО-65-23",
      "name": "Полянский М.Д."
    }
  ],
  "subject": "Конфигурационное управление"
}
```
#### Реализация:
```jsonnet
{
local groupTemplate(index) = "ИКБО-" + index + "-20";

local groups = [groupTemplate(i) for i in std.range(1, 24)];

local studentTemplate(name, age, group) = {
  age: age,
  group: group,
  name: name,
};

local students = [
  studentTemplate("Иванов И.И.", 19, "ИКБО-4-20"),
  studentTemplate("Петров П.П.", 18, "ИКБО-5-20"),
  studentTemplate("Сидоров С.С.", 18, "ИКБО-5-20"),
  studentTemplate("Полянский М.Д.", 19, "ИКБО-65-23"),
];

{
  groups: groups,
  students: students,
  subject: "Конфигурационное управление",
}
```
![image](https://github.com/user-attachments/assets/567f49a0-ef55-424b-b0d9-02300b36a1ce)


