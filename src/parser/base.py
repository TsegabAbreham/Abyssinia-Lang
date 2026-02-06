# parser/base.py
from error import unexpected_token

class ParserBase:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        # track current line/col for error reporting (updated on eat)
        self.line = None
        self.col = None

    def current(self):
        # Return a (type, value) pair for backward-compatible parser code.
        if self.pos < len(self.tokens):
            tok = self.tokens[self.pos]
            # tok is expected to be (TYPE, VALUE, LINE, COL) but may be (TYPE, VALUE)
            t = tok[0] if len(tok) > 0 else None
            v = tok[1] if len(tok) > 1 else None
            return (t, v)
        return (None, None)

    def peek(self, n=1):
        if self.pos + n < len(self.tokens):
            return self.tokens[self.pos + n][0]
        return None

    def eat(self, token_type):
        # Access the raw token in the token list to get line/col
        if self.pos < len(self.tokens):
            raw = self.tokens[self.pos]
        else:
            raw = (None, None, None, None)

        type_ = raw[0] if len(raw) > 0 else None
        value = raw[1] if len(raw) > 1 else None

        if type_ == token_type:
            # update parser's line/col from the token if available
            if len(raw) >= 4:
                self.line = raw[2]
                self.col = raw[3]
            self.pos += 1
            return value

        raise unexpected_token(self, expected=token_type)
