# import re

# TOKENS = [
#     ("ID", r"[a-zA-Z_][a-zA-Z_0-9]*"),
#     ("NUM", r"\d+(\.\d*)?"),
#     ("STRING", r"'((?:''|[^'])*)'"),
#     ("LPAREN", r"\("),
#     ("RPAREN", r"\)"),
#     ("COMMA", r","),
#     ("OPERATOR", r"[=<>!]+"),
#     ("SEMICOLON", r";"),
#     ("COMMENT", r"--.*"),
#     ("WS", r"\s+"),
#     ("UNRECOGNIZED", r"."),
# ]

# KEYWORDS = {'SELECT', 'FROM', 'INSERT', 'INTO', 'VALUES', 'DELETE', 'WHERE', 'AND', 'OR'}
# REGEX = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKENS))

# def lex(input_str):
#     token_iter = REGEX.finditer(input_str)
#     tokens = []
#     for token_match in token_iter:
#         token_type = token_match.lastgroup
#         token_text = token_match.group(token_type)
#         if token_type != "WS":
#             tokens.append((token_type, token_text))
#     return tokens

# def parse(tokens):
#     pos = 0

#     def error(expected):
#         nonlocal pos
#         token_type, token_value = tokens[pos]
#         raise Exception(f"Se esperaba {expected}, pero se encontró {token_type} ('{token_value}') en la posición {pos}.")

#     def match(token_type):
#         nonlocal pos
#         if pos < len(tokens) and tokens[pos][0] == token_type:
#             return tokens[pos]
#         return None

#     def consume_token():
#         nonlocal pos
#         pos += 1

#     def skip_comments_and_whitespace():
#         nonlocal pos
#         while pos < len(tokens) and tokens[pos][0] in ["WS", "COMMENT"]:
#             pos += 1

#     def query():
#         nonlocal pos
#         current_token = tokens[pos][1].upper()
#         if current_token == "INSERT":
#             pos += 1
#             skip_comments_and_whitespace()
#             if match("INTO"):
#                 pos += 1
#                 skip_comments_and_whitespace()
#             else:
#                 error("INTO")
#             return "INSERT"
#         elif current_token == "DELETE":
#             pos += 1
#             skip_comments_and_whitespace()
#             if match("FROM"):
#                 pos += 1
#                 skip_comments_and_whitespace()
#             else:
#                 error("FROM")
#             return "DELETE"
#         elif current_token == "SELECT":
#             pos += 1
#             skip_comments_and_whitespace()
#             return "SELECT"
#         else:
#             error("SELECT, INSERT o DELETE")

#     statements = []
#     while pos < len(tokens):
#         skip_comments_and_whitespace()
#         if match("ID"):
#             statement = query()
#             if statement:
#                 statements.append(statement)
#             skip_comments_and_whitespace()
#         else:
#             break

#     return statements

# def main():
#     input_str = """-- Insert records into users
# INSERT INTO users (id, username, email, age) VALUES (1, 'Alice', 'alice@example.com', 30);
# INSERT INTO users (id, username, email, age) VALUES (2, 'Bob', 'bob@example.com', 25);
# INSERT INTO users (id, username, email, age) VALUES (3, 'Charlie', 'charlie@example.com', 22);

# -- Delete records from users
# DELETE FROM users WHERE age < 25;

# -- Select records from users
# SELECT id, username, email FROM users;
# """

#     tokens = lex(input_str)
#     statements = parse(tokens)
#     print("Statements:", statements)

# if __name__ == "__main__":
#     main()


