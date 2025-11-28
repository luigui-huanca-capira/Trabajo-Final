"""
Parser Recursivo Descendente para Mini-0
Implementa análisis sintáctico LL(k) con lookahead para resolver conflictos
"""

from typing import List, Optional
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.lexer_mini0 import Lexer, Token, TokenType

class ParseError(Exception):
    """Excepción para errores de parsing"""
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"{message} en línea {token.line}, columna {token.column}")

class ParserMini0:
    """Parser recursivo descendente para Mini-0"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.errors: List[str] = []
    
    def current_token(self) -> Token:
        """Retorna el token actual"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # EOF
    
    def peek_token(self, offset: int = 1) -> Optional[Token]:
        """Mira el token en posición actual + offset (lookahead)"""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def advance(self) -> Token:
        """Avanza al siguiente token"""
        token = self.current_token()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        """Verifica que el token actual sea del tipo esperado y avanza"""
        token = self.current_token()
        if token.type != token_type:
            self.error(f"Se esperaba {token_type.name}, se encontró {token.type.name}")
        return self.advance()
    
    def match(self, *token_types: TokenType) -> bool:
        """Verifica si el token actual coincide con alguno de los tipos dados"""
        return self.current_token().type in token_types
    
    def error(self, message: str):
        """Registra un error de parsing"""
        token = self.current_token()
        error_msg = f"Error sintáctico en línea {token.line}, columna {token.column}: {message}"
        self.errors.append(error_msg)
        raise ParseError(message, token)
    
    def skip_newlines(self):
        """Salta tokens NL (saltos de línea)"""
        while self.match(TokenType.NL):
            self.advance()
    
    def expect_nl(self):
        """Espera al menos un salto de línea"""
        if not self.match(TokenType.NL):
            self.error("Se esperaba un salto de línea")
        while self.match(TokenType.NL):
            self.advance()
    
    # ========== Programa ==========
    
    def parse(self) -> bool:
        """Punto de entrada del parser"""
        try:
            self.parse_programa()
            self.skip_newlines()  # Saltar NLs finales antes de EOF
            if not self.match(TokenType.EOF):
                self.error("Se esperaba fin de archivo")
            return True
        except ParseError:
            return False
    
    def parse_programa(self):
        """programa → nls decl_list"""
        self.skip_newlines()
        self.parse_decl_list()
    
    def parse_decl_list(self):
        """decl_list → decl decl_list | ε"""
        while self.match(TokenType.FUN, TokenType.ID):
            self.parse_decl()
    
    def parse_decl(self):
        """decl → funcion | global"""
        if self.match(TokenType.FUN):
            self.parse_funcion()
        elif self.match(TokenType.ID):
            self.parse_global()
        else:
            self.error("Se esperaba 'fun' o identificador")
    
    # ========== Declaraciones ==========
    
    def parse_global(self):
        """global → declvar nl"""
        self.parse_declvar()
        self.expect_nl()
    
    def parse_funcion(self):
        """funcion → 'fun' ID '(' params ')' tipo_ret nl bloque 'end' nl"""
        self.expect(TokenType.FUN)
        self.expect(TokenType.ID)
        self.expect(TokenType.LPAREN)
        self.parse_params()
        self.expect(TokenType.RPAREN)
        self.parse_tipo_ret()
        self.expect_nl()
        self.parse_bloque()
        self.expect(TokenType.END)
        self.expect_nl()
    
    def parse_params(self):
        """params → parametro params_rest | ε"""
        if self.match(TokenType.ID):
            self.parse_parametro()
            self.parse_params_rest()
    
    def parse_params_rest(self):
        """params_rest → ',' parametro params_rest | ε"""
        while self.match(TokenType.COMMA):
            self.advance()
            self.parse_parametro()
    
    def parse_parametro(self):
        """parametro → ID ':' tipo"""
        self.expect(TokenType.ID)
        self.expect(TokenType.COLON)
        self.parse_tipo()
    
    def parse_tipo_ret(self):
        """tipo_ret → ':' tipo | ε"""
        if self.match(TokenType.COLON):
            self.advance()
            self.parse_tipo()
    
    # ========== Tipos ==========
    
    def parse_tipo(self):
        """tipo → tipo_array tipobase"""
        self.parse_tipo_array()
        self.parse_tipobase()
    
    def parse_tipobase(self):
        """tipobase → 'int' | 'bool' | 'char' | 'string'"""
        if self.match(TokenType.INT, TokenType.BOOL, TokenType.CHAR, TokenType.STRING):
            self.advance()
        else:
            self.error("Se esperaba un tipo (int, bool, char, string)")
    
    def parse_tipo_array(self):
        """tipo_array → '[' ']' tipo_array | ε"""
        while self.match(TokenType.LBRACKET):
            self.advance()
            self.expect(TokenType.RBRACKET)
    
    def parse_declvar(self):
        """declvar → ID ':' tipo"""
        self.expect(TokenType.ID)
        self.expect(TokenType.COLON)
        self.parse_tipo()
    
    # ========== Bloques y Comandos ==========
    
    def parse_bloque(self):
        """bloque → declvars comandos"""
        self.parse_declvars()
        self.parse_comandos()
    
    def parse_declvars(self):
        """declvars → declvar nl declvars | ε"""
        # Lookahead para distinguir declaración de comando
        while self.match(TokenType.ID):
            next_token = self.peek_token(1)
            if next_token and next_token.type == TokenType.COLON:
                # Es una declaración
                self.parse_declvar()
                self.expect_nl()
            else:
                # Es un comando, salir del loop
                break
    
    def parse_comandos(self):
        """comandos → comando nl comandos | ε"""
        while self.match(TokenType.IF, TokenType.WHILE, TokenType.RETURN, TokenType.ID):
            self.parse_comando()
            self.expect_nl()
    
    def parse_comando(self):
        """comando → cmdif | cmdwhile | cmdatrib | cmdreturn | llamada"""
        if self.match(TokenType.IF):
            self.parse_cmdif()
        elif self.match(TokenType.WHILE):
            self.parse_cmdwhile()
        elif self.match(TokenType.RETURN):
            self.parse_cmdreturn()
        elif self.match(TokenType.ID):
            # Lookahead para distinguir asignación de llamada
            next_token = self.peek_token(1)
            if next_token and next_token.type == TokenType.LPAREN:
                self.parse_llamada()
            else:
                self.parse_cmdatrib()
        else:
            self.error("Se esperaba un comando")
    
    def parse_cmdif(self):
        """cmdif → 'if' exp nl bloque elseif_list else_opt 'end'"""
        self.expect(TokenType.IF)
        self.parse_exp()
        self.expect_nl()
        self.parse_bloque()
        self.parse_elseif_list()
        self.parse_else_opt()
        self.expect(TokenType.END)
    
    def parse_elseif_list(self):
        """elseif_list → 'else' 'if' exp nl bloque elseif_list | ε"""
        while self.match(TokenType.ELSE):
            next_token = self.peek_token(1)
            if next_token and next_token.type == TokenType.IF:
                self.advance()  # else
                self.advance()  # if
                self.parse_exp()
                self.expect_nl()
                self.parse_bloque()
            else:
                break
    
    def parse_else_opt(self):
        """else_opt → 'else' nl bloque | ε"""
        if self.match(TokenType.ELSE):
            self.advance()
            self.expect_nl()
            self.parse_bloque()
    
    def parse_cmdwhile(self):
        """cmdwhile → 'while' exp nl bloque 'loop'"""
        self.expect(TokenType.WHILE)
        self.parse_exp()
        self.expect_nl()
        self.parse_bloque()
        self.expect(TokenType.LOOP)
    
    def parse_cmdatrib(self):
        """cmdatrib → var '=' exp"""
        self.parse_var()
        self.expect(TokenType.EQ)
        self.parse_exp()
    
    def parse_cmdreturn(self):
        """cmdreturn → 'return' exp_opt"""
        self.expect(TokenType.RETURN)
        # exp_opt: puede haber expresión o no
        if not self.match(TokenType.NL, TokenType.EOF):
            self.parse_exp()
    
    # ========== Variables y Llamadas ==========
    
    def parse_var(self):
        """var → ID var_index"""
        self.expect(TokenType.ID)
        self.parse_var_index()
    
    def parse_var_index(self):
        """var_index → '[' exp ']' var_index | ε"""
        while self.match(TokenType.LBRACKET):
            self.advance()
            self.parse_exp()
            self.expect(TokenType.RBRACKET)
    
    def parse_llamada(self):
        """llamada → ID '(' listaexp ')'"""
        self.expect(TokenType.ID)
        self.expect(TokenType.LPAREN)
        self.parse_listaexp()
        self.expect(TokenType.RPAREN)
    
    def parse_listaexp(self):
        """listaexp → exp listaexp_rest | ε"""
        if not self.match(TokenType.RPAREN):
            self.parse_exp()
            self.parse_listaexp_rest()
    
    def parse_listaexp_rest(self):
        """listaexp_rest → ',' exp listaexp_rest | ε"""
        while self.match(TokenType.COMMA):
            self.advance()
            self.parse_exp()
    
    # ========== Expresiones ==========
    
    def parse_exp(self):
        """exp → exp_or"""
        self.parse_exp_or()
    
    def parse_exp_or(self):
        """exp_or → exp_and exp_or_prime"""
        self.parse_exp_and()
        self.parse_exp_or_prime()
    
    def parse_exp_or_prime(self):
        """exp_or_prime → 'or' exp_and exp_or_prime | ε"""
        while self.match(TokenType.OR):
            self.advance()
            self.parse_exp_and()
    
    def parse_exp_and(self):
        """exp_and → exp_eq exp_and_prime"""
        self.parse_exp_eq()
        self.parse_exp_and_prime()
    
    def parse_exp_and_prime(self):
        """exp_and_prime → 'and' exp_eq exp_and_prime | ε"""
        while self.match(TokenType.AND):
            self.advance()
            self.parse_exp_eq()
    
    def parse_exp_eq(self):
        """exp_eq → exp_rel exp_eq_prime"""
        self.parse_exp_rel()
        self.parse_exp_eq_prime()
    
    def parse_exp_eq_prime(self):
        """exp_eq_prime → '=' exp_rel exp_eq_prime | '<>' exp_rel exp_eq_prime | ε"""
        while self.match(TokenType.EQ, TokenType.NEQ):
            self.advance()
            self.parse_exp_rel()
    
    def parse_exp_rel(self):
        """exp_rel → exp_add exp_rel_prime"""
        self.parse_exp_add()
        self.parse_exp_rel_prime()
    
    def parse_exp_rel_prime(self):
        """exp_rel_prime → '>' | '<' | '>=' | '<=' exp_add exp_rel_prime | ε"""
        while self.match(TokenType.GT, TokenType.LT, TokenType.GTE, TokenType.LTE):
            self.advance()
            self.parse_exp_add()
    
    def parse_exp_add(self):
        """exp_add → exp_mul exp_add_prime"""
        self.parse_exp_mul()
        self.parse_exp_add_prime()
    
    def parse_exp_add_prime(self):
        """exp_add_prime → '+' | '-' exp_mul exp_add_prime | ε"""
        while self.match(TokenType.PLUS, TokenType.MINUS):
            self.advance()
            self.parse_exp_mul()
    
    def parse_exp_mul(self):
        """exp_mul → exp_unary exp_mul_prime"""
        self.parse_exp_unary()
        self.parse_exp_mul_prime()
    
    def parse_exp_mul_prime(self):
        """exp_mul_prime → '*' | '/' exp_unary exp_mul_prime | ε"""
        while self.match(TokenType.MULT, TokenType.DIV):
            self.advance()
            self.parse_exp_unary()
    
    def parse_exp_unary(self):
        """exp_unary → 'not' exp_unary | '-' exp_unary | exp_primary"""
        if self.match(TokenType.NOT, TokenType.MINUS):
            self.advance()
            self.parse_exp_unary()
        else:
            self.parse_exp_primary()
    
    def parse_exp_primary(self):
        """exp_primary → LITNUMERAL | LITSTRING | 'true' | 'false' | var | 
                         'new' '[' exp ']' tipo | '(' exp ')' | llamada"""
        if self.match(TokenType.LITNUMERAL, TokenType.LITSTRING, 
                     TokenType.TRUE, TokenType.FALSE):
            self.advance()
        elif self.match(TokenType.NEW):
            self.advance()
            self.expect(TokenType.LBRACKET)
            self.parse_exp()
            self.expect(TokenType.RBRACKET)
            self.parse_tipo()
        elif self.match(TokenType.LPAREN):
            self.advance()
            self.parse_exp()
            self.expect(TokenType.RPAREN)
        elif self.match(TokenType.ID):
            # Lookahead para distinguir variable de llamada
            next_token = self.peek_token(1)
            if next_token and next_token.type == TokenType.LPAREN:
                self.parse_llamada()
            else:
                self.parse_var()
        else:
            self.error("Se esperaba una expresión")

def parse_file(filename: str) -> bool:
    """Parsea un archivo Mini-0"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Análisis léxico
        lexer = Lexer(source_code)
        tokens, lex_errors = lexer.tokenize()
        
        if lex_errors:
            print("Errores léxicos encontrados:")
            for error in lex_errors:
                print(f"  {error}")
            return False
        
        print(f"✓ Análisis léxico completado: {len(tokens)} tokens")
        
        # Análisis sintáctico
        parser = ParserMini0(tokens)
        success = parser.parse()
        
        if parser.errors:
            print("\nErrores sintácticos encontrados:")
            for error in parser.errors:
                print(f"  {error}")
            return False
        
        if success:
            print("✓ Análisis sintáctico completado exitosamente")
            print("✓ El programa es sintácticamente correcto")
            return True
        else:
            return False
            
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{filename}'")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False

def main():
    """Función de prueba"""
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python parser_mini0.py <archivo.mini0>")
        return
    
    filename = sys.argv[1]
    success = parse_file(filename)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
