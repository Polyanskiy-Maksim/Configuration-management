**Задача 1**

Вывести отсортированный в алфавитном порядке список имен пользователей в файле passwd (вам понадобится grep).

Код - grep '.*' /etc/passwd | cut -d: -f1 | sort

Скриншот - ![image](https://github.com/user-attachments/assets/1da1039a-978d-4c26-bc10-8aeb9d924e0d)
__________________________

**Задача 2**

Вывести данные /etc/protocols в отформатированном и отсортированном порядке для 5 наибольших портов, как показано в примере ниже:
[root@localhost etc]# cat /etc/protocols …
142 rohc
141 wesp
140 shim6
139 hip
138 manet

Код - awk '{print $2, $1}' /etc/protocols | sort -nr | head -n 5

Скриншот - ![image](https://github.com/user-attachments/assets/6db09c3f-78c9-4c0b-990a-21092121cdf9)
__________________________

**Задача 3**


Написать программу banner средствами bash для вывода текстов, как в следующем примере (размер баннера должен меняться!):

[root@localhost ~]# ./banner "Hello from RTU MIREA!"
+--------------------+
Hello from RTU MIREA!
+--------------------+
Перед отправкой решения проверьте его в ShellCheck на предупреждения.

Код - 
#!/bin/bash

text=$*
length=${#text}

for i in $(seq 1 $((length + 2))); do
    line+="-"
done

echo "+${line}+"
echo "| ${text} |"
echo "+${line}+"

Скриншот - 
