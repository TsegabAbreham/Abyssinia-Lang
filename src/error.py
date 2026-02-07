"""
error.py

Utilities and exception classes to use with your parser/lexer/interpreter.

Features:
- ParseError, LexerError, InterpreterError (subclasses of Exception) with rich metadata
- TokenInfo helper to normalize token tuples like (TYPE, VALUE) or (TYPE, VALUE, line, col)
- Reporter class to collect multiple errors and print them nicely
- Convenience functions: raise_parse_error, unexpected_token, assert_token, format_error

Change: prefer line/col instead of pos. For backward compatibility `pos` is accepted and mapped to `line` if needed.
"""

from typing import Optional, Any, Tuple, List
import sys


# ----------------- Base Error Classes -----------------

class BaseError(Exception):
    """Base class for errors produced by the language toolchain."""

    def __init__(self, message: str, token: Optional[Tuple[Any, ...]] = None,
                 pos: Optional[int] = None, line: Optional[int] = None,
                 col: Optional[int] = None, filename: Optional[str] = None,
                 hint: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.token = token
        # Backwards compatibility
        self.pos = pos
        self.line = line if line is not None else (pos if pos is not None else None)
        self.col = col
        self.filename = filename
        self.hint = hint

    def __str__(self) -> str:
        return format_error(self)


class ParseError(BaseError):
    """Raised on parse-time problems (unexpected token, bad syntax)."""


class LexerError(BaseError):
    """Raised by the tokenizer/lexer when encountering invalid input."""


class InterpreterError(BaseError):
    """Raised at runtime when evaluating the AST (e.g. undefined var, type error)."""


# ----------------- Token Translation -----------------

def translate_token_type(token_type: Optional[str]) -> str:
    """Translate a token type string into Amharic."""
    translations = {
        'DOT': 'ነጥብ',
        'SEMICOLON': 'አራት ነጥብ -> ።',
        'LPAREN': 'መክፈቻ ቅንፍ -> (',
        'RPAREN': 'መዝጊያ ቅንፍ -> )',
        'COMMA': 'ነጠላ ሰረዝ -> ፣',
        'LBRACKET': 'መክፈቻ የተጠማዘዘ ቅንፍ -> {',
        'RBRACKET': 'መዝጊያ የተጠማዘዘ ቅንፍ -> }',
        'SLBRACKET': 'መክፈቻ ስኩኤር ቅንፍ -> [',
        'SRBRACKET': 'መዝጊያ ስኩኤር ቅንፍ -> ]',
        'NUMBER': 'ቁጥር'
    }
    if token_type is None:
        return "<None>"
    # ensure non-string token types (e.g., Token objects) are stringified
    key = token_type if isinstance(token_type, str) else str(token_type)
    return translations.get(key, key)


# ----------------- Token Normalization -----------------

def _normalize_token(token: Optional[Tuple[Any, ...]]):
    """Normalize token tuples into a dict with keys: type, value, line, col."""
    if token is None:
        return {"type": None, "value": None, "line": None, "col": None}
    if not isinstance(token, (list, tuple)):
        return {"type": str(token), "value": None, "line": None, "col": None}
    if len(token) >= 4:
        ttype, value, line, col = token[0], token[1], token[2], token[3]
        # coerce type to string when possible for consistent translation
        if not isinstance(ttype, str):
            ttype = str(ttype)
        return {"type": ttype, "value": value, "line": line, "col": col}
    if len(token) == 2:
        ttype, value = token
        if not isinstance(ttype, str):
            ttype = str(ttype)
        return {"type": ttype, "value": value, "line": None, "col": None}
    return {"type": token[0] if len(token) > 0 else None,
            "value": token[1] if len(token) > 1 else None,
            "line": None, "col": None}


# ----------------- Error Formatting -----------------

def format_error(err: BaseError) -> str:
    """Create a readable error message with token translations."""
    t = _normalize_token(err.token)
    loc = ""
    if err.filename:
        loc += f"{err.filename}"

    line = err.line if getattr(err, "line", None) is not None else t.get("line")
    col = err.col if getattr(err, "col", None) is not None else t.get("col")

    if line is not None:
        loc += f":{line}"
        if col is not None:
            loc += f":{col}"
    elif err.pos is not None:
        loc += f" (pos={err.pos})"

    token_info = ""
    if t.get("type") is not None:
        token_info = f"token={translate_token_type(t['type'])}"
        if t.get("value") is not None:
            token_info += f"({repr(t['value'])})"

    parts = [f"ስህተት: {err.message}"]
    if token_info:
        parts.append(token_info)
    if loc:
        parts.append(loc)
    if err.hint:
        parts.append(f"Hint: {err.hint}")

    return " — ".join(parts)


# ----------------- Convenience Functions -----------------

def raise_parse_error(message: str, token: Optional[Tuple[Any, ...]] = None,
                      pos: Optional[int] = None, line: Optional[int] = None,
                      col: Optional[int] = None, filename: Optional[str] = None,
                      hint: Optional[str] = None) -> ParseError:
    """Create and return a ParseError."""
    return ParseError(message, token=token, pos=pos, line=line, col=col,
                      filename=filename, hint=hint)


def unexpected_token(parser_or_token: Any, expected: Optional[str] = None,
                     hint: Optional[str] = None) -> ParseError:
    """Create a ParseError for an unexpected token."""
    token = None
    line = None
    col = None
    filename = None

    if hasattr(parser_or_token, "current"):
        try:
            token = parser_or_token.current()
        except Exception:
            token = None
        line = getattr(parser_or_token, "line", None) or getattr(parser_or_token, "lineno", None)
        col = getattr(parser_or_token, "col", None) or getattr(parser_or_token, "column", None)
        filename = getattr(parser_or_token, "filename", None)
    else:
        token = parser_or_token

    t = _normalize_token(token)
    if line is None and t.get("line") is not None:
        line = t.get("line")
    if col is None and t.get("col") is not None:
        col = t.get("col")

    # translate the found token type (if possible) for human-friendly output
    found_type = translate_token_type(t.get('type')) if t.get('type') is not None else '<EOF>'
    found = f"{found_type}"
    if t.get("value") is not None:
        found += f"({t['value']})"

    msg = f"ያልተጠበቀ ቃል ተገኘ: {found}"
    if expected:
        msg += f", ተጠበቆ የነበረው ቃል፡ {translate_token_type(expected)}"

    # keep token tuple intact, translation handled in format_error
    return raise_parse_error(msg, token=token, line=line, col=col, filename=filename, hint=hint)


def assert_token(parser, expected_type: str, expected_name: Optional[str] = None,
                 hint: Optional[str] = None) -> None:
    """Assert that parser.current() token is expected_type, otherwise raise."""
    type_, value = parser.current()
    if type_ != expected_type:
        raise unexpected_token(parser, expected=expected_name or expected_type, hint=hint)


# ----------------- Reporter Class -----------------

class Reporter:
    """Collects multiple errors and prints them at once."""

    def __init__(self):
        self._errors: List[BaseError] = []

    def add(self, err: BaseError) -> None:
        self._errors.append(err)

    def add_message(self, message: str, token: Optional[Tuple[Any, ...]] = None,
                    line: Optional[int] = None, col: Optional[int] = None,
                    filename: Optional[str] = None,
                    hint: Optional[str] = None) -> None:
        self.add(ParseError(message, token=token, line=line, col=col,
                            filename=filename, hint=hint))

    def has_errors(self) -> bool:
        return len(self._errors) > 0

    def display_all(self, file=None) -> None:
        if file is None:
            file = sys.stderr
        for e in self._errors:
            print(format_error(e), file=file)

    def raise_if_any(self) -> None:
        if self.has_errors():
            messages = [format_error(e) for e in self._errors]
            raise ParseError("Multiple errors:\n" + "\n".join(messages))


# ----------------- Utility -----------------

def fatal(msg: str) -> None:
    """Print a message and exit; a tiny helper for CLI tools and quick scripts."""
    print(msg, file=sys.stderr)
    sys.exit(1)
