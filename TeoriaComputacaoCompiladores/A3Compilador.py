import re

class Interpreter:
    def __init__(self) -> None:
        with open("cod.txt", "r") as f:
            self.file_content = ''.join(line for line in f)

        self.string_split_line = self.file_content.split("\n")

        self.tokens = {'ID': "[a-zA-Z][a-zA-Z0-9_]*", 'Number': "[0-9]+", "Real": "[0-9]*[.][0-9]+", "Operator": "(\+|-|\*|\/|=|>|<|&|\||%|!|\^|\(|\))", "Symbol": f"'|{chr(34)}|\|@"}
        self.reserved_words = ["if", "while", "True", "False", "for", "print"]
        self.word_buffer = ''
        self.word_end = 0
        self.current_line = 0
        self.in_comment = False
        self.word_location = []

    def append_list(self, token, type_token, line, index, addition):
        self.word_location.append({
            'token': token,
            'type': type_token,
            'line': line + 1,
            'column': (index - len(self.word_buffer)) + addition
        })

    def lex_analysis(self):
        try:
            for lines_i in range(len(self.string_split_line)):
                for chart_i in range(len(self.string_split_line[lines_i])):
                    current_char = self.string_split_line[lines_i][chart_i]
                    
                    if self.current_line!=lines_i:
                        if self.in_comment:
                            self.append_list(self.word_buffer, 'Comment', self.current_line, self.word_end, 2)
                        elif self.word_buffer in self.reserved_words:
                            self.append_list(self.word_buffer, 'Reserved Word', self.current_line, self.word_end, 2)
                        else:
                            for token, pattern in self.tokens.items():
                                if re.fullmatch(pattern, self.word_buffer):
                                    self.append_list(self.word_buffer, token, self.current_line, self.word_end, 2)
                        self.word_buffer = ''
                        self.word_end = 0
                        self.current_line = lines_i
                        self.in_comment = False

                    if self.in_comment:
                        self.word_end = chart_i
                        self.word_buffer += current_char

                    elif re.match("[a-zA-Z0-9_.]", current_char) and self.current_line==lines_i:
                        self.word_end = chart_i
                        self.word_buffer += current_char
                    
                    elif current_char == '#':
                        self.in_comment = True
                        self.append_list(current_char, token, lines_i, chart_i, 1)
                    else:
                        if self.word_buffer in self.reserved_words:
                            self.append_list(self.word_buffer, 'Reserved Word', lines_i, self.word_end, 2)
                        else:
                            for token, pattern in self.tokens.items():
                                if re.fullmatch(pattern, self.word_buffer):
                                    self.append_list(self.word_buffer, token, lines_i, self.word_end, 2)
                        self.word_buffer = ''
                        self.word_end = 0
                        for token, pattern in self.tokens.items():
                            if re.fullmatch(pattern, current_char):
                                self.append_list(current_char, token, lines_i, chart_i, 1)

            print("|{:<15}|{:<15}|{:<15}|{:<10}".format('Token', 'Type', 'Line', 'Column'))
            print("-" * 55)
            for item in self.word_location:
                print("|{:<15}|{:<15}|{:<15}|{:<5}|".format(item['token'], item['type'], item['line'], item['column']))
                print("-" * 55)

        except Exception as e:
            print(e)

    def syntax_analysis(self):
        par_open = 0
        for item in self.word_location:
            if par_open < 0:
                break
            if item['token'] == '(':
                par_open += 1
            
            if item['token'] == ')':
                par_open -= 1
        
        if par_open == 0:
            print("\nO codigo esta correto sintaticamente")
        else:
            print("\nO codigo esta incorreto sintaticamente")
    
    def semantic_analysis(self):
        try:
            print("\nExecutando o código... {")
            exec(self.file_content)
            print("}")
        except Exception as e:
            print(e)
            print("}")

interpreter = Interpreter()
interpreter.lex_analysis()
interpreter.syntax_analysis()
interpreter.semantic_analysis()