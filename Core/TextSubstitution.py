marker = 'YL'
char_map = {
    '0': 'ZE', '1': 'ON', '2': 'TV', '3': 'TH', '4': 'FO',
    '5': 'FI', '6': 'SI', '7': 'SE', '8': 'EI', '9': 'NI', ' ': 'SP'
}


def sub(text: str):
    if len(text) < 1:
        return ''

    for char in char_map.values():
        if marker + char in text:
            raise ValueError(f'Text \'{text}\'cannot contain reserved word \'{marker + char}\'')

    return ''.join([marker + char_map[char] if char in char_map.keys() else char for char in text])


def sub_reverse(text: str):
    if len(text) < 1:
        return ''

    for orig, replacement in char_map.items():
        text = text.replace(marker + replacement, orig)

    return text
