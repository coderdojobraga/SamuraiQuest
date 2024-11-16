import re
from datetime import datetime, timedelta

def extract_sections(message):
    match = re.search(r'# Semana \d{2}\/\d{2}\/\d{4} - \d{2}\/\d{2}\/\d{4}\n*(## 😺 Scratch\n*(✅ <@\d+>\n*)*)\n*(## 🐍 Python\n*(✅ <@\d+>\n*)*)', message)
    if match:
        scratch_section = match.group(1) if match.group(1) else "## 😺 Scratch\n"
        python_section = match.group(3) if match.group(3) else "## 🐍 Python\n"
        return scratch_section, python_section
    return "## 😺 Scratch\n", "## 🐍 Python\n"

def update_section(section, user):
    lines = section.split('\n')
    title = lines[0]
    participants = lines[1:] if len(lines) > 1 else []
    participants.append(f"✅ {user}")
    return title + '\n' + '\n'.join(participants) + '\n'

def update_message(message, user, language):
    scratch_section, python_section = extract_sections(message)
    updated_message = message

    if language == "Scratch":
        updated_scratch_section = update_section(scratch_section, user)
        updated_message = message.replace(scratch_section, updated_scratch_section)
    else:
        updated_python_section = update_section(python_section, user)
        updated_message = message.replace(python_section, updated_python_section)

    return updated_message

def create_initial_message():
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return f"# Semana {start_of_week.strftime('%d/%m/%Y')} - {end_of_week.strftime('%d/%m/%Y')}\n## 😺 Scratch\n## 🐍 Python\n"
