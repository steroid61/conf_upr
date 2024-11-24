import re
import json
import sys


class ConfigParser:
    def __init__(self):
        self.variables = {}
        self.tokens = []
        self.position = 0

    def parse(self, text):
        self.tokenize(text)
        return self.parse_statements()

    def tokenize(self, text):
        # Удаление комментариев
        text = self.remove_comments(text)
        # Определение токенов
        token_specification = [
            ('NUMBER', r'\d+'),
            ('VAR', r'var'),
            ('SORT', r'sort\(\)'),
            ('INDEX', r'index\(\)'),
            ('NAME', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('ASSIGN', r':='),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('LBRACK', r'\['),
            ('RBRACK', r'\]'),
            ('COMMA', r','),
            ('OP', r'[\+\-\*]'),
            ('SKIP', r'[ \t\n]+'),
            ('MISMATCH', r'.'),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        self.tokens = []
        for mo in re.finditer(tok_regex, text):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NUMBER':
                value = int(value)
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise SyntaxError(f'Unexpected character {value!r}')
            self.tokens.append({'type': kind, 'value': value})

    def remove_comments(self, text):
        # Удаление многострочных комментариев
        text = re.sub(r'\(comment.*?\)', '', text, flags=re.DOTALL)
        # Удаление однострочных комментариев
        text = re.sub(r'#.*', '', text)
        return text

    def parse_statements(self):
        statements = []
        while self.position < len(self.tokens):
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
        return statements

    def parse_statement(self):
        token = self.tokens[self.position]
        if token['type'] == 'VAR':
            return self.parse_var_declaration()
        else:
            raise SyntaxError(f'Unexpected token {token}')

    def parse_var_declaration(self):
        self.expect('VAR')
        name = self.expect('NAME')['value']
        self.expect('ASSIGN')
        value = self.parse_value()
        self.variables[name] = value
        return {'var': name, 'value': value}

    def parse_value(self):
        token = self.tokens[self.position]
        if token['type'] == 'NUMBER':
            return self.consume('NUMBER')['value']
        elif token['type'] == 'LBRACK':
            return self.parse_array()
        elif token['type'] == 'LBRACE':
            return self.parse_expression()
        else:
            raise SyntaxError(f'Expected value at position {self.position}')

    def parse_array(self):
        self.expect('LBRACK')
        array = []
        while self.tokens[self.position]['type'] != 'RBRACK':
            value = self.parse_value()
            array.append(value)
            if self.tokens[self.position]['type'] == 'COMMA':
                self.consume('COMMA')
            else:
                break
        self.expect('RBRACK')
        return array

    def parse_expression(self):
        self.expect('LBRACE')
        stack = []
        while self.tokens[self.position]['type'] != 'RBRACE':
            token = self.tokens[self.position]
            if token['type'] == 'NUMBER':
                stack.append(self.consume('NUMBER')['value'])
            elif token['type'] == 'NAME':
                name = self.consume('NAME')['value']
                value = self.variables.get(name)
                if value is None:
                    raise NameError(f'Undefined variable {name}')
                stack.append(value)
            elif token['type'] == 'OP':
                op = self.consume('OP')['value']
                b = stack.pop()
                a = stack.pop()
                if op == '+':
                    result = a + b
                elif op == '-':
                    result = a - b
                elif op == '*':
                    result = a * b
                stack.append(result)
            elif token['type'] == 'SORT':
                self.consume('SORT')
                array = stack.pop()
                if isinstance(array, list):
                    stack.append(sorted(array))
                else:
                    raise TypeError('sort() can only be applied to arrays')
            elif token['type'] == 'INDEX':
                self.consume('INDEX')
                index = stack.pop()
                array = stack.pop()
                if isinstance(array, list) and isinstance(index, int):
                    try:
                        stack.append(array[index])
                    except IndexError:
                        raise IndexError(f'Index {index} out of range')
                else:
                    raise TypeError('index() requires an array and an integer index')
            else:
                raise SyntaxError(f'Unexpected token {token}')
        self.expect('RBRACE')
        if len(stack) != 1:
            raise SyntaxError('Invalid expression')
        return stack[0]

    def expect(self, token_type):
        if self.position >= len(self.tokens):
            raise SyntaxError(f'Unexpected end of input, expected {token_type}')
        token = self.tokens[self.position]
        if token['type'] == token_type:
            self.position += 1
            return token
        else:
            raise SyntaxError(f'Expected token {token_type}, got {token}')

    def consume(self, token_type):
        return self.expect(token_type)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Config to JSON converter')
    parser.add_argument('-i', '--input', required=True, help='Input config file')
    parser.add_argument('-o', '--output', required=True, help='Output JSON file')
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        text = f.read()

    config_parser = ConfigParser()
    try:
        result = config_parser.parse(text)
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print('Conversion successful.')
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()