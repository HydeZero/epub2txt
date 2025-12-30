# A dictionary for cleaning up specific characters to their more basic equivalents.
cleanup_dictionary = {
    '“': "\"",
    '”': "\"",
    '’': "'",
    '‘': "'",
    '—': "-",
    '–': "-",
    '…': "...",
    '•': "*",
    '™': "(TM)",
    '\u00A0': " ",  # Non-breaking space. can't be rendered directly here
    '¡': "!",
    '¢': "c",
    '£': "GBP",
    '¤': "currency",
    '¥': "YEN",
    '¦': "|",
    '§': "S",
    '¨': '"', # i honestly have no idea how this character is used so if it renders awkwardly ill just remove it
    '©': "(c)",
    'ª': "a",
    '«': "<<",
    '¬': "not ",
    '®': "(r)",
    '¯': "-", # macron. once again if it renders awkwardly ill just remove it
    '°': " degree",
    '±': "+/-",
    '²': "^2",
    '³': "^3",
    '´': "`", # yes visual studio i know this is a commonly confused character but i meant to type it in this case
    'µ': "u", # micro
    '¶': "P", # pilcrow
    '·': "-", # middle dot
    '¸': ",", # cedilla. if it renders awkwardly ill just remove it... again
    '¹': "^1",
    'º': "o",
    '»': ">>",
    '¼': "1/4",
    '½': "1/2",
    '¾': "3/4",
    '¿': "?",
    '×': "*",
    '÷': "/"
}

accented_replacements = {
    'À': "A",
    'Á': "A",
    'Â': "A",
    'Ã': "A",
    'Ä': "A",
    'Å': "A",
    'Æ': "AE",
    'Ç': "C",
    'È': "E",
    'É': "E",
    'Ê': "E",
    'Ë': "E",
    'Ì': "I",
    'Í': "I",
    'Î': "I",
    'Ï': "I",
    'Ð': "Th", # Eth is often used for "th" sounds
    'Ñ': "N",
    'Ò': "O",
    'Ó': "O",
    'Ô': "O",
    'Õ': "O",
    'Ö': "O",
    'Ø': "O",
    'Ù': "U",
    'Ú': "U",
    'Û': "U",
    'Ü': "U",
    'Ý': "Y",
    'Þ': "Th",
    'ß': "ss",
    'à': "a",
    'á': "a",
    'â': "a",
    'ã': "a",
    'ä': "a",
    'å': "a",
    'æ': "ae",
    'ç': "c",
    'è': "e",
    'é': "e",
    'ê': "e",
    'ë': "e",
    'ì': "i",
    'í': "i",
    'î': "i",
    'ï': "i",
    'ð': "th",
    'ñ': "n",
    'ò': "o",
    'ó': "o",
    'ô': "o",
    'õ': "o",
    'ö': "o",
    'ø': "o",
    'ù': "u",
    'ú': "u",
    'û': "u",
    'ü': "u",
    'ý': "y",
    'þ': "th",
    'ÿ': "y"
}

# This list contains utf-8 characters that SHOULD be printed everywhere with basic utf-8 support (items listed in groups shown in the utf-8 lookup table, so special characters, capital letters, more special characters, lowercase letters, and finally more special characters. Anything beyond or before this are either not common or control characters that should be removed.)
list_of_acceptable_utf_8_characters = ("!\"#$%&'()*+,-./0123456789:;<=>?@", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "[\\]^_`", "abcdefghijklmnopqrstuvwxyz", "{|}~")

def clean_text(text, is_verbose=False, advanced_cleaning=False, keep_accents=False):
    # Do an initial cleanup replacement based on the cleanup dictionary.
    for target, replacement in cleanup_dictionary.items():
        if list_to_keep is None or target not in list_to_keep:
            text = text.replace(target, replacement)
    
    special_character = list_of_acceptable_utf_8_characters[0]
    capital_letter = list_of_acceptable_utf_8_characters[1]
    special_character_2 = list_of_acceptable_utf_8_characters[2]
    lowercase_letter = list_of_acceptable_utf_8_characters[3]
    special_character_3 = list_of_acceptable_utf_8_characters[4]
    
    # Split the text into characters for processing.
    text = list(text)
    
    # Now remove any characters that are not in the acceptable utf-8 characters list.
    for i in range(len(text)):
        character = text[i]
        # please forgive me for this long for statement, it is just for simplicity.
        # anyway this checks if the character is in any of the acceptable utf-8 characters, and if it is not, it replaces it with a space.
        if character in special_character:
            continue
        if character in capital_letter:
            continue
        if character in special_character_2:
            continue
        if character in lowercase_letter:
            continue
        if character in special_character_3:
            continue
        if character == "\n":
            continue # allow new lines
        if advanced_cleaning:
            if ord(character) >= 128:
                # If unicode code point is 128 or higher, replace with space since it's outside the basic latin range.
                text[i] = " "
                if is_verbose:
                    print(f"Replaced character: {character} with space due to advanced cleaning.")
                continue
        # By here, we should have found a match and broken out of the loop. For the special characters that are not matched, we replace them with a space.
        text[i] = " "
        if is_verbose:
            print(f"Replaced character: {character} with space.")
            
    return "".join(text)