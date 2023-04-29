class Scanner:
    def __init__(self, input_str):
        self.input_str = input_str
        self.tokens = []
        self.keywords = {
            "nueva": "NEW",
            "CrearBD": "CREATE_DB",
            "EliminarBD": "DROP_DB",
            "CrearColeccion": "CREATE_COLLECTION",
            "EliminarColeccion": "DROP_COLLECTION",
            "InsertarUnico": "INSERT_ONE",
            "ActualizarUnico": "UPDATE_ONE",
            "EliminarUnico": "DELETE_ONE",
            "BuscarTodo": "FIND_ALL",
            "BuscarUnico": "FIND_ONE"
        }
        self.delimiters = {
            '{': 'LBRACE',
            '}': 'RBRACE',
            '(': 'LPAREN',
            ')': 'RPAREN',
            '=': 'EQUALS',
            ',': 'COMMA',
            '.': 'DOT',
            ';': 'SEMICOLON',
            '"': 'DQUOTE',
            "'": 'SQUOTE',
            ':': 'COLON',
            '$': 'DOLLAR',
            '“': 'OPEN_QUOTE',
            '”': 'CLOSE_QUOTE',
            '-': 'SPACE',
            ' ': 'WHITESPACE',
            '*': 'ASTERISK',
            '/': 'BAR'
        }

    def is_identifier(self, s):
        # A valid identifier is a letter followed by zero or more letters/digits/underscores
        if s[0].isalpha():
            return all(c.isalnum() or c == '_' for c in s[1:])
        return False

    def tokenize(self):
        self.tokens = []
        line_num = 1
        line_start = 0
        i = 0
        n = len(self.input_str)
        first_token = self.input_str.split()[0]
        if not self.is_identifier(first_token) and first_token not in self.keywords:
            raise RuntimeError(f'{first_token!r} no es una palabra clave ni un identificador válido en la línea {line_num}')

        while i < n:
            c = self.input_str[i]

            if c.isalpha():
                j = i + 1
                while j < n and (self.input_str[j].isalnum() or self.input_str[j] == '_'):
                    j += 1
                token = self.input_str[i:j]
                if token in self.keywords:
                    self.tokens.append((self.keywords[token], token, line_num, i, j))
                elif self.is_identifier(token):
                    self.tokens.append(('ID', token, line_num, i, j))
                else:
                    raise RuntimeError(f'{token!r} no es una palabra clave ni un identificador válido en la línea {line_num}')
                i = j
                continue

            if c == '(':
                self.tokens.append(('LPAREN', c, line_num, i, i+1))
            elif c == ')':
                self.tokens.append(('RPAREN', c, line_num, i, i+1))
            elif c == ';':
                self.tokens.append(('SEMICOLON', c, line_num, i, i+1))
            elif c.isspace():
                if c == '\n':
                    line_num += 1
                    line_start = i + 1
                i += 1
                continue
            elif c in self.delimiters:
                self.tokens.append((self.delimiters[c], c, line_num, i, i+1))
            else:
                raise RuntimeError(f'{c!r} inesperado en la línea {line_num}')
            i += 1

        return self.tokens
