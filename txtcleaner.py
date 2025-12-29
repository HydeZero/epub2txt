# A dictionary for cleaning up specific characters to their more basic equivalents.
cleanup_dictionary = {
    '“': "\"",
    '”': "\"",
    '’': "'",
    '‘': "'",
    '—': "-",
    '–': "-",
    '…': "..."
}

# This list contains utf-8 characters that SHOULD be printed everywhere with basic utf-8 support (items listed in groups shown in the utf-8 lookup table, so special characters, capital letters, more special characters, lowercase letters, and finally more special characters. Anything beyond or before this are either not common or control characters that should be removed.)
list_of_acceptable_utf_8_characters = ("!\"#$%&'()*+,-./0123456789:;<=>?@", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "[\\]^_`", "abcdefghijklmnopqrstuvwxyz", "{|}~")

def clean_text(text):
    # Do an initial cleanup replacement based on the cleanup dictionary.
    for target, replacement in cleanup_dictionary.items():
        text = text.replace(target, replacement)
    
    # Now remove any characters that are not in the acceptable utf-8 characters list.
    for character in text:
        # please forgive me for this long for statement, it is just for simplicity.
        # anyway this checks if the character is in any of the acceptable utf-8 characters, and if it is not, it replaces it with a space.
        for special_character, capital_letter, special_character_2, lowercase_letter, special_character_3 in list_of_acceptable_utf_8_characters[0], list_of_acceptable_utf_8_characters[1], list_of_acceptable_utf_8_characters[2], list_of_acceptable_utf_8_characters[3], list_of_acceptable_utf_8_characters[4]:
            if character == special_character:
                break
            if character == capital_letter:
                break
            if character == special_character_2:
                break
            if character == lowercase_letter:
                break
            if character == special_character_3:
                break
            # By here, we should have found a match and broken out of the loop. For the special characters that are not matched, we replace them with a space.
            text = text.replace(character, " ")
            
    return text