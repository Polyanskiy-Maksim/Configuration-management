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

Скриншот - ![image](https://github.com/user-attachments/assets/02ceec50-388d-4b94-8489-789610373240)

__________________________

**Задача 4**

#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Используйте: $0 имя_файла"
	exit 1
fi

file="$1"

grep -oE '\b[a-zA-Z_][a-zA-Z0-9_]*\b' "$file" | sort -u

Скриншот - ![image](https://github.com/user-attachments/assets/58c2f11a-e166-4673-9f5a-67d3d693c395)
__________________________

**Задача 5**

#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Используйте: $0 имя команды."
	exit 1
fi

command_name="$1"
command_path="./$command_name"

if [ ! -f "$command_path" ]; then
	echo "Ошибка: файл '$command_path' не найден."
	exit 1
fi

sudo chmod +x "$command_name"
sudo cp "$command_path" /usr/local/bin/

if [ $? -ne 0 ]; then
	echo "Ошибка: не удалось скопировать файл."
	exit 1
fi

sudo chmod 775 /usr/local/bin/"$command_name"

if [ $? -ne 0 ]; then
	echo "Ошибка: не удалось установить права для '$command_name'."
	exit 1
fi

echo "Команда '$command_name' успешно зарегестрирована."

Скриншот - ![image](https://github.com/user-attachments/assets/5cdfbaf0-1ef4-4080-a99a-81fe6555ed47)
__________________________

**Задача 6**

#!/bin/bash

check() {
	local file=$1
	local ext=${file##*.}

	echo "Проверка: $file с расширением: .$ext"
	
	case $ext in
		c)
			if head -n 1 "$file" | grep -q '^\s*//' || head -n 1 "$file" | grep -q '^\s*/\*'; then
				echo "$file: Есть комментарий."
			else
				echo "$file: Нет комментария."
			fi
			;;
		js)
			if head -n 1 "$file" | grep -q '^\s*//'; then
				echo "$file: Есть комментарий."
			else
				echo "$file: Нет комментария."
			fi
			;;
		py)
			if head -n 1 "$file" | grep -q '^\s*#'; then
				echo "$file: Есть комментарий."
			else
				echo "$file: Нет комментария."
			fi
			;;
		*)
			echo "$file: Неподдерживаемый формат."
			;;
	esac
}


if [[ $# -ne 1 ]]; then
	echo "Использование: $0 <имя_файла>."
	exit 1
fi

if [[ -f $1 ]]; then
	check "$1"
else
	echo "Файл $file не найден."
	exit 1
fi

Скриншот - ![image](https://github.com/user-attachments/assets/9d3e47cf-f6d7-40b6-a46c-8d1a0723880b)
__________________________

**Задача 7**

#!/bin/bash

if [[ $# -ne 1 ]]; then
	echo "Использование: $0 /путь/к/каталогу."
	exit 1
fi

directory=$1

if [[ ! -d $directory ]]; then
	echo "Ошибка: каталог $directory не найден."
	exit 1
fi

declare -A file_hashes

while IFS= read -r -d '' file; do
	hash=$(sha256sum "$file" | awk '{ print $1 }')
	file_hashes["$hash"]+="file"$'\n'
done < <(find "$directory" -type f -print0)

found_duplicates=false

for hash in "${!file_hashes[@]}"; do
	files="${file_hashes[$hash]}"
	files_count=$(echo -e "files" | wc -l)


	if [[ $files_count -gt 1 ]]; then
		found_duplicates=true
		echo "Найдены дубликаты:"
		echo -e "$files"
	fi
done

if ! $found_duplicates; then
	echo "Дубликатов не найдено."
	exit 1
fi

Скриншот - ![image](https://github.com/user-attachments/assets/188b4384-aae5-47eb-b0a8-6053b3e8f569)
__________________________

**Задача 8**

#!/bin/bash

if [ "$#" -ne 2 ]; then
	echo "Использование: $0 /путь/к/каталогу <расширение>."
	exit 1
fi

directory="$1"
extension="$2"

if [ ! -d "$directory" ]; then
	echo "Ошибка: указанный каталог '$directory' не существует."
	exit 1
fi

shopt -s nullglob
files=("$directory"/*."$extension")

if [ ${#files[@]} -eq 0 ]; then
	echo "Ошибка: в указанном каталоге '$directory' нет файлов с расширением .'$extension'."
	exit 1
fi

archive_name="${directory%/}.tar"

tar -cvf "$archive_name" -C "$directory" ./*."$extension"

echo "Архив '$archive_name' успешно создан."

Скриншот - ![image](https://github.com/user-attachments/assets/061e9226-a7f0-440c-8243-c14398cc167b)
__________________________

**Задача 9**

#!/bin/bash

if [ "$#" -ne 2 ]; then
	echo "Использование: $0 <входной_файл> <выходной_файл>"
	exit 1
fi

input_file="$1"
output_file="$2"

if [ ! -f "$input_file" ]; then
	echo "Ошибка: '$input_file' не найден."
	exit 1
fi

sed 's/    /\t/g' "$input_file" > "$output_file"

echo "Заменено в файле: '$output_file'"

Скриншот - ![image](https://github.com/user-attachments/assets/b0a9aef7-b38e-42f0-b269-0d9afeb0f9e5)
__________________________

**Задача 10**
#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Использование: $0 /путь/к/каталогу."
	exit 1
fi

directory="$1"

if [ ! -d "$directory" ]; then
	echo: "Ошибка: указанный каталог '$directory' не существует."
	exit 1
fi

find "$directory" -type f -name "*.txt" -empty -exec basename {} \;

Скриншот - ![image](https://github.com/user-attachments/assets/dd1e6002-d7a1-435f-bd14-3d181a6e984b)









