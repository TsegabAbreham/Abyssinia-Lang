import re
import unicodedata
from error import LexerError

# Token types (you can expand as needed)
TOKEN_TYPES = [
    'NUMBER', 'IDENTIFIER', 'PLUS', 'MINUS', 'MULT', 'DIV', 'EQUAL',
    'LPAREN', 'RPAREN', 'PRINT', 'SEMICOLON', 'COMMA', 'COMMENT', 'STRING',
    'EOF'
]

# Patterns for multi-character tokens (order matters!)
TOKEN_REGEX = [
    # Comments
    (r'~~([\s\S]*?)~~', 'COMMENT'),           # multi-line comment using ~~
    (r'#.*', 'COMMENT'),                      # single-line comment

    # Conditionals
    (r'ከሆነ\b', 'IF'),
    (r'ካልሆነ\b', 'ELSEIF'),
    (r'ሌላ\b', 'ELSE'),

    # Loops
    (r'እያለ\b', 'WHILE'),
    (r'ለ\b', 'FOR'),
    (r'ከ\b', 'FROM'),
    (r'እስከ\b', 'TO'),

    # Functions
    (r'ተግባር\b', 'FUN'),

    # Keywords
    (r'አሳይ\b', 'PRINT'),
    (r'ጠይቅ\b', 'INPUT'),

    # Imports
    (r'አስገባ\b', 'IMPORT'),
    (r'እንደ\b', 'AS'),

    # Classes
    (r'ክፍል\b', 'CLASS'),

    # Numbers
    (r'\d+', 'NUMBER'),

    # Operators (multi-char first)
    (r'==', 'EQ'),
    (r'!=', 'NEQ'),
    (r'>=', 'GTE'),
    (r'<=', 'LTE'),
    (r'>', 'GT'),
    (r'<', 'LT'),

    (r'&&', 'AND'),
    (r'\|\|', 'OR'),

    (r'\+', 'PLUS'),
    (r'-', 'MINUS'),
    (r'\*', 'MULT'),
    (r'/', 'DIV'),

    (r'=', 'EQUAL'),  # Assignment operator

    # Strings (captures quote in group 1 and content in group 2)
    (r'(["\'])(.*?)\1', 'STRING'),

    # Identifiers including Amharic block
    (r'\b[\wሀ-ፐ]+\b', 'IDENTIFIER'),
]

# Single-character tokens
SINGLE_CHAR_TOKENS = {
    '.': 'DOT',
    ';': 'SEMICOLON',
    '(': 'LPAREN',
    ')': 'RPAREN',
    ',': 'COMMA',
    '{': 'LBRACKET',
    '}': 'RBRACKET',
    '[': 'SLBRACKET',
    ']': 'SRBRACKET'
}

def normalize_code(code: str) -> str:
    code = unicodedata.normalize("NFKC", code)
    code = code.replace("\u00ad", "")

    # Replace single character tokens with UTF
    code = code.replace('።', ';')
    code = code.replace('፣', ',')
    code = code.replace('፡', '.')

    # Replace multi character tokens with UTF
    code = code.replace('እና', '&&')
    code = code.replace('ወይም', '||')

    replacements = {
        "“": '"', "”": '"',
        "‘": "'", "’": "'",
        "‹": "<", "›": ">",
        "«": "<<", "»": ">>",
    }
    for k, v in replacements.items():
        code = code.replace(k, v)
    return code

def tokenize(code: str):
    code = normalize_code(code)
    tokens = []

    i = 0
    line = 1
    col = 1
    length = len(code)

    while i < length:
        ch = code[i]

        # -------- Whitespace handling --------
        if ch.isspace():
            if ch == '\n':
                line += 1
                col = 1
            else:
                col += 1
            i += 1
            continue

        matched = False
        substring = code[i:]

        # -------- Regex tokens --------
        for pattern, type_ in TOKEN_REGEX:
            flags = re.DOTALL if type_ == 'COMMENT' and '~~' in pattern else 0
            match = re.match(pattern, substring, flags)
            if match:
                text = match.group(0)
                start_col = col

                if type_ == "COMMENT":
                    # advance position but emit nothing
                    lines = text.split('\n')
                    if len(lines) > 1:
                        line += len(lines) - 1
                        col = len(lines[-1]) + 1
                    else:
                        col += len(text)
                    i += len(text)
                    matched = True
                    break

                if type_ == "STRING":
                    # inner content without quotes
                    value = match.group(2)
                else:
                    value = text

                tokens.append((type_, value, line, start_col))

                # advance cursor based on consumed text
                lines = text.split('\n')
                if len(lines) > 1:
                    line += len(lines) - 1
                    col = len(lines[-1]) + 1
                else:
                    col += len(text)

                i += len(text)
                matched = True
                break

        # -------- Single-character tokens --------
        if not matched and ch in SINGLE_CHAR_TOKENS:
            tokens.append((SINGLE_CHAR_TOKENS[ch], ch, line, col))
            i += 1
            col += 1
            matched = True

        # -------- Error --------
        if not matched:
            # Provide token and line/col so the error formatting can show location
            raise LexerError(
                f"Unexpected character: {ch!r}",
                token=("CHAR", ch, line, col),
                line=line,
                col=col
            )

    # Append EOF token so parser errors at end-of-file can show last location
    tokens.append(('EOF', None, line, col))

    return tokens
