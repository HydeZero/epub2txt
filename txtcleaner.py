cleanup_dictionary = {
    '“': "\"",
    '”': "\"",
    '’': "'",
    '‘': "'",
    '—': "-",
    '–': "-",
    '…': "..."
}

def clean_text(text):
    for target, replacement in cleanup_dictionary.items():
        text = text.replace(target, replacement)
    return text