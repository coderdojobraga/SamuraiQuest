import re

def update_message(message, user, language):
    match = re.match(r'# Semana \d{2}\/\d{2}\/\d{4} - \d{2}\/\d{2}\/\d{4}\n*(## 😺 Scratch\n*(✅ <@\d+>\n)*)\n*(## 🐍 Python\n*(✅ <@\d+>\n)*)\n*', message)

    updated_message = message

    if match:
        scratch_section = match.group(1) if match.group(1) else ""
        python_section = match.group(2) if match.group(2) else ""
        
        print("Scratch section:", scratch_section)
        print("Python Section:", python_section)         

        if language == "Scratch":
            updated_scratch_section = scratch_section + f"✅ {user}\n"
            updated_message = message.replace(scratch_section, updated_scratch_section)
        else:
            updated_message += f"\n✅ {user}"
            
        return updated_message
    
    else:
        return message
