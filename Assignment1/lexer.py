# -------------------------------------------------------------
# lexer.py
# 
# The lexer scans the input source code and returns tokens with their
# corresponding lexemes (keyword, identifier, integer, real, operator, separator).
# -------------------------------------------------------------
import fsm


#----lexer-----------------------------------------------------
# Process the string into tokens. 
#
# Output:
#       Returns Dict: token - indentiy
#--------------------------------------------------------------
def lexer(code):
    tokens = []
    i = 0

    while i < len(code):
        char = code[i]

        # skip whitespace
        if char.isspace():
            i += 1
            continue

        # skip comments: /* ... */
        if code[i:i+2] == '/*':
            end = code.find('*/', i + 2)
            if end == -1:
                break
            i = end + 2
            continue

        # skip comments: // or #
        if code[i:i+2] == '//' or code[i] == '#':
            end = code.find('\n', i)
            if end == -1:
                break
            i = end + 1
            continue

        # operators (<=, >=, ==, !=)
        if i + 1 < len(code) and fsm.is_operator(code[i:i+2]):
            tokens.append({"token": "operator", "lexeme": code[i:i+2]})
            i += 2
            continue

        # operators (+, -, *, /, %, <, >, =)
        if fsm.is_operator(char): 
            tokens.append({"token": "operator", "lexeme": char})
            i += 1
            continue

        # separator (), {}, [], :, ;, ,
        if fsm.is_separator(char):
            tokens.append({"token": "separator", "lexeme": char})
            i += 1
            continue

        # first letter
        if char.isalpha():
            j = i
            while j < len(code) and (code[j].isalpha() or code[j].isdigit() or code[j] == '_'):
                j += 1
            lexeme = code[i:j]
            if fsm.is_keyword(lexeme):
                tokens.append({"token": "keyword", "lexeme": lexeme})
            else:
                tokens.append({"token": "identifier", "lexeme": lexeme})
            i = j
            continue

        # first number
        if char.isdigit():
            j = i
            while j < len(code) and (code[j].isdigit() or code[j] == '.'):
                j += 1
            lexeme = code[i:j]
            if fsm.is_real(lexeme):
                tokens.append({"token": "real", "lexeme": lexeme})
            elif fsm.is_integer(lexeme):
                tokens.append({"token": "integer", "lexeme": lexeme})
            else:
                tokens.append({"token": "unknown", "lexeme": lexeme})
            i = j
            continue

        # unknown
        tokens.append({"token": "unknown", "lexeme": char})
        i += 1

    return tokens
