"""
Analizador Léxico para Mini-0 (Especificación Oficial)
Convierte el código fuente en una secuencia de tokens según la especificación de Mini-0
"""

import re
from enum import Enum, auto
from typing import List, Optional, Tuple

class TokenType(Enum):
    """Tipos de tokens del lenguaje Mini-0"""
    # Palabras reservadas
    IF = auto()
    ELSE = auto()
    END = auto()
    WHILE = auto()
    LOOP = auto()
    FUN = auto()
    RETURN = auto()
    NEW = auto()
    
    # Tipos
    INT = auto()
    BOOL = auto()
    CHAR = auto()
    STRING = auto()
    
    # Valores booleanos
    TRUE = auto()
    FALSE = auto()
    
    # Operadores lógicos
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Identificadores y literales
    ID = auto()
    LITNUMERAL = auto()  # Números (decimal o hexadecimal)
    LITSTRING = auto()   # Cadenas de texto
    
    # Operadores aritméticos
    PLUS = auto()        # +
    MINUS = auto()       # -
    MULT = auto()        # *
    DIV = auto()         # /
    
    # Operadores relacionales
    GT = auto()          # >
    LT = auto()          # <
    GTE = auto()         # >=
    LTE = auto()         # <=
    EQ = auto()          # =
    NEQ = auto()         # <>
    
    # Delimitadores
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    LBRACKET = auto()    # [
    RBRACKET = auto()    # ]
    COMMA = auto()       # ,
    COLON = auto()       # :
    
    # Salto de línea (significativo en Mini-0)
    NL = auto()
    
    # Fin de archivo
    EOF = auto()

class Token:
    """Representa un token con su tipo, valor y posición"""
    def __init__(self, token_type: TokenType, value: str, line: int, column: int):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', {self.line}:{self.column})"
    
    def __str__(self):
        if self.value:
            return f"<{self.type.name}, '{self.value}'>"
        return f"<{self.type.name}>"

class Lexer:
    """Analizador léxico para Mini-0"""
    
    # Palabras reservadas
    KEYWORDS = {
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'end': TokenType.END,
        'while': TokenType.WHILE,
        'loop': TokenType.LOOP,
        'fun': TokenType.FUN,
        'return': TokenType.RETURN,
        'new': TokenType.NEW,
        'int': TokenType.INT,
        'bool': TokenType.BOOL,
        'char': TokenType.CHAR,
        'string': TokenType.STRING,
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
    }
    
    def __init__(self, source_code: str):
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.errors: List[str] = []
        self.last_was_newline = False  # Para manejar múltiples NL consecutivos
    
    def error(self, message: str):
        """Registra un error léxico"""
        error_msg = f"Error léxico en línea {self.line}, columna {self.column}: {message}"
        self.errors.append(error_msg)
    
    def current_char(self) -> Optional[str]:
        """Retorna el carácter actual sin avanzar"""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Mira el siguiente carácter sin avanzar"""
        peek_pos = self.pos + offset
        if peek_pos >= len(self.source):
            return None
        return self.source[peek_pos]
    
    def advance(self) -> Optional[str]:
        """Avanza al siguiente carácter"""
        if self.pos >= len(self.source):
            return None
        
        char = self.source[self.pos]
        self.pos += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        return char
    
    def skip_whitespace_except_newline(self):
        """Salta espacios en blanco y tabulaciones, pero NO saltos de línea"""
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def skip_comment(self) -> bool:
        """Salta comentarios de línea (//) y de bloque (/* */)"""
        if self.current_char() == '/' and self.peek_char() == '/':
            # Comentario de línea
            while self.current_char() and self.current_char() != '\n':
                self.advance()
            return True
        
        if self.current_char() == '/' and self.peek_char() == '*':
            # Comentario de bloque
            self.advance()  # /
            self.advance()  # *
            while self.current_char():
                if self.current_char() == '*' and self.peek_char() == '/':
                    self.advance()  # *
                    self.advance()  # /
                    return True
                self.advance()
            self.error("Comentario de bloque no cerrado")
            return True
        
        return False
    
    def read_string(self) -> Token:
        """Lee una cadena de texto con escapes"""
        start_line = self.line
        start_column = self.column
        string_value = ''
        
        self.advance()  # Saltar comilla inicial "
        
        while self.current_char() and self.current_char() != '"':
            if self.current_char() == '\\':
                # Manejar escapes
                self.advance()
                next_char = self.current_char()
                if next_char == 'n':
                    string_value += '\n'
                    self.advance()
                elif next_char == 't':
                    string_value += '\t'
                    self.advance()
                elif next_char == '\\':
                    string_value += '\\'
                    self.advance()
                elif next_char == '"':
                    string_value += '"'
                    self.advance()
                else:
                    self.error(f"Escape inválido: \\{next_char}")
                    self.advance()
            elif self.current_char() == '\n':
                self.error("Cadena no cerrada antes del fin de línea")
                break
            else:
                string_value += self.current_char()
                self.advance()
        
        if self.current_char() == '"':
            self.advance()  # Saltar comilla final
        else:
            self.error("Cadena no cerrada")
        
        return Token(TokenType.LITSTRING, string_value, start_line, start_column)
    
    def read_number(self) -> Token:
        """Lee un número (decimal o hexadecimal)"""
        start_line = self.line
        start_column = self.column
        num_str = ''
        
        # Verificar si es hexadecimal
        if self.current_char() == '0' and self.peek_char() and self.peek_char().lower() == 'x':
            num_str += self.current_char()
            self.advance()
            num_str += self.current_char()
            self.advance()
            
            # Leer dígitos hexadecimales
            if not (self.current_char() and self.current_char() in '0123456789abcdefABCDEF'):
                self.error("Número hexadecimal inválido")
            
            while self.current_char() and self.current_char() in '0123456789abcdefABCDEF':
                num_str += self.current_char()
                self.advance()
        else:
            # Número decimal
            while self.current_char() and self.current_char().isdigit():
                num_str += self.current_char()
                self.advance()
        
        return Token(TokenType.LITNUMERAL, num_str, start_line, start_column)
    
    def read_identifier(self) -> Token:
        """Lee un identificador o palabra reservada"""
        start_line = self.line
        start_column = self.column
        id_str = ''
        
        # Primer carácter: letra o guión bajo
        if self.current_char() and (self.current_char().isalpha() or self.current_char() == '_'):
            id_str += self.current_char()
            self.advance()
        
        # Siguientes caracteres: letras, dígitos o guión bajo
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            id_str += self.current_char()
            self.advance()
        
        # Verificar si es palabra reservada
        token_type = self.KEYWORDS.get(id_str, TokenType.ID)
        
        return Token(token_type, id_str, start_line, start_column)
    
    def tokenize(self) -> Tuple[List[Token], List[str]]:
        """Convierte el código fuente en una lista de tokens"""
        while self.pos < len(self.source):
            # Saltar espacios en blanco (excepto newline)
            self.skip_whitespace_except_newline()
            
            if self.pos >= len(self.source):
                break
            
            # Saltar comentarios
            if self.skip_comment():
                continue
            
            char = self.current_char()
            start_line = self.line
            start_column = self.column
            
            # Saltos de línea (significativos en Mini-0)
            if char == '\n':
                self.advance()
                # Solo agregar un token NL si el anterior no fue NL
                if not self.last_was_newline:
                    self.tokens.append(Token(TokenType.NL, '\\n', start_line, start_column))
                    self.last_was_newline = True
                continue
            else:
                self.last_was_newline = False
            
            # Strings
            if char == '"':
                self.tokens.append(self.read_string())
                continue
            
            # Números
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Identificadores y palabras reservadas
            if char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Operadores de dos caracteres
            if char == '>' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GTE, '>=', start_line, start_column))
                continue
            
            if char == '<' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LTE, '<=', start_line, start_column))
                continue
            
            if char == '<' and self.peek_char() == '>':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NEQ, '<>', start_line, start_column))
                continue
            
            # Operadores de un carácter
            single_char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULT,
                '/': TokenType.DIV,
                '>': TokenType.GT,
                '<': TokenType.LT,
                '=': TokenType.EQ,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ',': TokenType.COMMA,
                ':': TokenType.COLON,
            }
            
            if char in single_char_tokens:
                token_type = single_char_tokens[char]
                self.advance()
                self.tokens.append(Token(token_type, char, start_line, start_column))
                continue
            
            # Carácter no reconocido
            self.error(f"Carácter no reconocido: '{char}'")
            self.advance()
        
        # Agregar token EOF
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        
        return self.tokens, self.errors

def main():
    """Función de prueba del lexer"""
    test_code = """
    // Programa de prueba Mini-0
    fun main(): int
        x: int
        x = 10
        if x > 5
            y: int
            y = x * 2
        end
        return x
    end
    """
    
    lexer = Lexer(test_code)
    tokens, errors = lexer.tokenize()
    
    if errors:
        print("Errores léxicos encontrados:")
        for error in errors:
            print(f"  {error}")
    else:
        print("Análisis léxico completado sin errores.")
    
    print("\nTokens generados:")
    for token in tokens:
        print(f"  {token}")

if __name__ == "__main__":
    main()
