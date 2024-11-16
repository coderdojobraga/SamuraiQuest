import re
from datetime import datetime, timedelta

def extract_sections(message):
    match = re.search(r'# Semana \d{2}\/\d{2}\/\d{4} - \d{2}\/\d{2}\/\d{4}\n*(## 😺 Scratch Nível 1\n*(✅ <@\d+>\n*)*)\n*(## 😺 Scratch Nível 2\n*(✅ <@\d+>\n*)*)\n*(## 😺 Scratch Nível 3\n*(✅ <@\d+>\n*)*)\n*(## 🐍 Python Nível 1\n*(✅ <@\d+>\n*)*)\n*(## 🐍 Python Nível 2\n*(✅ <@\d+>\n*)*)', message)
    if match:
        scratch_level_1 = match.group(1) if match.group(1) else "## 😺 Scratch Nível 1\n"
        scratch_level_2 = match.group(3) if match.group(3) else "## 😺 Scratch Nível 2\n"
        scratch_level_3 = match.group(5) if match.group(5) else "## 😺 Scratch Nível 3\n"
        python_level_1 = match.group(7) if match.group(7) else "## 🐍 Python Nível 1\n"
        python_level_2 = match.group(9) if match.group(9) else "## 🐍 Python Nível 2\n"
        return scratch_level_1, scratch_level_2, scratch_level_3, python_level_1, python_level_2
    return "## 😺 Scratch Nível 1\n", "## 😺 Scratch Nível 2\n", "## 😺 Scratch Nível 3\n", "## 🐍 Python Nível 1\n", "## 🐍 Python Nível 2\n"

def update_section(section, user):
    lines = section.split('\n')
    title = lines[0]
    participants = lines[1:] if len(lines) > 1 else []
    participants.append(f"✅ {user}")
    return title + '\n' + '\n'.join(participants) + '\n'

def update_message(message, user, language, level):
    scratch_level_1, scratch_level_2, scratch_level_3, python_level_1, python_level_2 = extract_sections(message)
    updated_message = message

    if language == "Scratch":
        if level == 1:
            updated_scratch_section = update_section(scratch_level_1, user)
            updated_message = message.replace(scratch_level_1, updated_scratch_section)
        elif level == 2:
            updated_scratch_section = update_section(scratch_level_2, user)
            updated_message = message.replace(scratch_level_2, updated_scratch_section)
        elif level == 3:
            updated_scratch_section = update_section(scratch_level_3, user)
            updated_message = message.replace(scratch_level_3, updated_scratch_section)
    else:
        if level == 1:
            updated_python_section = update_section(python_level_1, user)
            updated_message = message.replace(python_level_1, updated_python_section)
        elif level == 2:
            updated_python_section = update_section(python_level_2, user)
            updated_message = message.replace(python_level_2, updated_python_section)

    return updated_message

def create_initial_message():
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return (f"# Semana {start_of_week.strftime('%d/%m/%Y')} - {end_of_week.strftime('%d/%m/%Y')}\n"
            "## 😺 Scratch Nível 1\n## 😺 Scratch Nível 2\n## 😺 Scratch Nível 3\n"
            "## 🐍 Python Nível 1\n## 🐍 Python Nível 2\n")
