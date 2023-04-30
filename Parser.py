from scanner import Scanner

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def accept(self, token_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == token_type:
            token_value = self.tokens[self.pos][1]
            self.pos += 1
            return token_value
        return None

    def accept_json_content(self):
        json_content = []
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] != "SEMICOLON":
            json_content.append(self.tokens[self.pos][1])
            self.pos += 1
        if json_content:
            return "".join(json_content)
        else:
            raise SyntaxError(f"Se esperaba contenido JSON en la línea {self.tokens[self.pos][2]}")

    def expect(self, expected_type):
        if self.pos >= len(self.tokens):
            raise Exception("Error inesperado: fin de archivo")

        token_type, token_value, line_num, start_pos, end_pos = self.tokens[self.pos]

        if token_type == expected_type:
            self.pos += 1
            return token_value
        else:
            raise Exception(f"Error inesperado: {token_type} en la línea {line_num}")

    def parse_string(self):
        self.expect('STRING')
        value = self.tokens[self.pos - 1][1]

        if value.startswith("'") or value.startswith('"'):
            value = value[1:]
        if value.endswith("'") or value.endswith('"'):
            value = value[:-1]

        return value

    def skip_whitespace(self):
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == "SPACE":
            self.pos += 1

    def parse(self):
        statements = []
        try:
            while self.pos < len(self.tokens):
                if self.accept("CREATE_DB"):
                    self.expect("ID")
                    self.skip_whitespace()
                    self.expect("EQUALS")
                    self.expect("NEW")
                    self.expect("CREATE_DB")
                    self.expect("LPAREN")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("CREATE_DB", self.tokens[self.pos - 8][1]))

                elif self.accept("DROP_DB"):
                    self.expect("ID")
                    self.expect("EQUALS")
                    self.expect("NEW")
                    self.expect("DROP_DB")
                    self.expect("LPAREN")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("DROP_DB",))

                elif self.accept("CREATE_COLLECTION"):
                    self.expect("ID")
                    self.skip_whitespace()
                    self.expect("EQUALS")
                    self.expect("NEW")
                    self.expect("CREATE_COLLECTION")
                    self.expect("LPAREN")                    
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    collection_name = self.tokens[self.pos][1]
                    statements.append(("CREATE_COLLECTION", collection_name))

                elif self.accept("DROP_COLLECTION"):
                    self.expect("ID")
                    self.skip_whitespace()
                    self.expect("EQUALS")
                    self.expect("NEW")
                    self.expect("DROP_COLLECTION")
                    self.expect("LPAREN")
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    collection_name = self.tokens[self.pos][1]
                    statements.append(("DROP_COLLECTION", collection_name))

                elif self.accept("INSERT_ONE"):
                    self.expect("ID")
                    self.expect("EQUALS")
                    self.expect("NEW")
                    self.expect("INSERT_ONE")
                    self.expect("LPAREN")
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("COMMA")
                    self.expect("SQUOTE") or self.expect("DQUOTE")
                    self.expect("LBRACE")
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("COLON")
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("COMMA")
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("COLON")
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("RBRACE")
                    self.expect("SQUOTE") or self.expect("DQUOTE")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    json_content = self.accept_json_content()
                    statements.append(("INSERT_ONE", json_content))

                elif self.accept("UPDATE_ONE"):
                    self.expect("ID")
                    self.skip_whitespace()
                    self.expect("EQUALS")
                    json_query = self.accept_json_content()
                    self.expect("NEW")
                    self.expect("UPDATE_ONE")
                    self.expect("LPAREN") 
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("COMMA")
                    self.expect("SQUOTE")
                    self.expect("LBRACE")
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("COLON")
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("RBRACE")
                    self.expect("COMMA")
                    self.expect("LBRACE")
                    self.expect("DOLLAR")
                    self.expect("ID")
                    self.expect("COLON")
                    self.expect("LBRACE")
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("COLON")
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("RBRACE")
                    self.expect("RBRACE")      
                    self.expect("SQUOTE")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    json_update = self.accept_json_content()
                    statements.append(("UPDATE_ONE", json_query, json_update))

                elif self.accept("DELETE_ONE"):
                    self.expect("ID")
                    self.skip_whitespace()
                    self.expect("EQUALS")
                    self.expect("NEW")
                    self.expect("DELETE_ONE")
                    self.expect("LPAREN")
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("COMMA")
                    self.expect("SQUOTE")
                    self.expect("LBRACE")
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("COLON")
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("RBRACE")
                    self.expect("SQUOTE")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    json_query = self.accept_json_content()
                    statements.append(("DELETE_ONE", json_query))

                elif self.accept("FIND_ALL"):
                    self.skip_whitespace()
                    self.expect("EQUALS")
                    self.expect("NEW")
                    self.expect("FIND_ALL")
                    self.expect("LPAREN")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("FIND_ALL",))

                elif self.accept("FIND_ONE"):
                    self.skip_whitespace()
                    self.expect("EQUALS")
                    self.expect("NEW")
                    self.expect("FIND_ONE")
                    self.expect("LPAREN")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    json_query = self.accept_json_content()
                    statements.append(("FIND_ONE", json_query))

                elif self.accept("ID"):
                    self.skip_whitespace()
                    self.expect("EQUALS")
                    self.skip_whitespace()
                    self.expect("ID")
                    self.skip_whitespace()
                    self.expect("SEMICOLON")
                    statements.append(("ASSIGNMENT", self.tokens[self.pos - 3][1], self.tokens[self.pos - 1][1]))

                else:
                    raise SyntaxError(f"Error de sintaxis en la línea {self.tokens[self.pos][2]}")

        except Exception as e:
            print(f"Error: {e}")

        return statements

if __name__ == "__main__":
    with open("input.txt", "r") as file:
        input_str = file.read()

    scanner = Scanner(input_str)
    tokens = scanner.tokenize()

    parser = Parser(tokens)
    parse_tree, errors = parser.parse()

    print(parse_tree)
    print("Errores:")
    for error in errors:
        print(error)

