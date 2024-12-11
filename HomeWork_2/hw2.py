import subprocess
import xml.etree.ElementTree as ET
import os

# Чтение конфигурации из XML
def read_config(config_path):
    tree = ET.parse(config_path)
    root = tree.getroot()
    config = {
        'repo_path': root.find('repo_path').text,
        'output_path': root.find('output_path').text
    }
    return config

# Получение информации о коммитах в репозитории
def get_commit_tree(repo_path):
    result = subprocess.run(
        ['git', '-C', repo_path, 'log', '--pretty=format:%H %s', '--reverse'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8' 
    )
    
    if result.returncode != 0:
        print("Ошибка при получении коммитов:", result.stderr)
        return {}

    commits = result.stdout.splitlines()
    commit_info = {}  # информация для каждого коммита
    
    for commit in commits:
        hash_value, message = commit.split(' ', 1)
        commit_info[hash_value] = {
            'message': message,
            'children': [],
            'changes': get_commit_changes(repo_path, hash_value)  # Получаем изменения для коммита
        }

    return commit_info

# Получаем изменения в коммите (добавление, редактирование, удаление файлов)
def get_commit_changes(repo_path, commit_hash):
    result = subprocess.run(
        ['git', '-C', repo_path, 'show', '--name-status', '--pretty=format:', commit_hash],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8' 
    )
    
    if result.returncode != 0:
        print(f"Ошибка при получении изменений для коммита {commit_hash}:", result.stderr)
        return []

    changes = result.stdout.splitlines()
    return changes  # Возвращаем список изменений в формате (тип изменения, файл)

# Генерация кода для диаграммы Mermaid
def generate_mermaid_code(commit_info):
    lines = ["graph TD"]  # Mermaid-диаграмма слева направо
    
    previous_commit = None
    
    for commit_hash, info in commit_info.items():
        short_commit_hash = commit_hash[:7]  # показываем сокращённый хэш коммита
        commit_node = f'    {short_commit_hash}["{info["message"]}\\n{commit_hash}"]'
        lines.append(commit_node)

        # Добавляем стрелочку к предыдущему коммиту
        if previous_commit:
            lines.append(f'    {previous_commit} --> {short_commit_hash}')

        # Добавляем изменения как стрелки
        for change in info['changes']:
            change_type, file_name = change.split('\t')
            change_description = f'"{file_name} ({change_type})"'  # Обрамляем описание изменений в кавычки
            change_node = f'    {short_commit_hash} --> {change_description}'
            lines.append(change_node)

        previous_commit = short_commit_hash

    return "\n".join(lines)

# Запись кода Mermaid в файл
def write_output(output_path, content):
    with open(output_path, 'w') as f:
        f.write(content)

# Главная функция
def main(config_path):
    config = read_config(config_path)
    commit_info = get_commit_tree(config['repo_path'])
    mermaid_code = generate_mermaid_code(commit_info)
    print(mermaid_code)
    write_output(config['output_path'], mermaid_code)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        sys.argv.append("config.xml")
    main(sys.argv[1])
