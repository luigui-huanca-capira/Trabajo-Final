"""
Definición de la Gramática Mini-0 (Especificación Oficial)
Gramática transformada para análisis LL(1) con cálculo de FIRST y FOLLOW
"""

from typing import Dict, Set, List

class GrammarMini0:
    """Representa la gramática del lenguaje Mini-0 transformada para LL(1)"""
    
    def __init__(self):
        # Símbolo inicial
        self.start_symbol = 'programa'
        
        # No terminales
        self.non_terminals = {
            'programa', 'nls', 'decl_list', 'decl', 'global', 'funcion',
            'tipo_ret', 'bloque', 'declvars', 'comandos', 'params', 'params_rest',
            'parametro', 'tipo', 'tipo_array', 'tipobase', 'declvar',
            'comando', 'cmdif', 'elseif_list', 'else_opt', 'cmdwhile',
            'cmdatrib', 'llamada', 'listaexp', 'listaexp_rest', 'cmdreturn',
            'exp_opt', 'var', 'var_index', 'nl', 'nl_rest',
            # Expresiones con precedencia
            'exp', 'exp_or', 'exp_or_prime', 'exp_and', 'exp_and_prime',
            'exp_eq', 'exp_eq_prime', 'exp_rel', 'exp_rel_prime',
            'exp_add', 'exp_add_prime', 'exp_mul', 'exp_mul_prime',
            'exp_unary', 'exp_primary'
        }
        
        # Terminales (tokens)
        self.terminals = {
            'if', 'else', 'end', 'while', 'loop', 'fun', 'return', 'new',
            'int', 'bool', 'char', 'string', 'true', 'false',
            'and', 'or', 'not',
            'ID', 'LITNUMERAL', 'LITSTRING',
            '+', '-', '*', '/',
            '>', '<', '>=', '<=', '=', '<>',
            '(', ')', '[', ']', ',', ':',
            'NL', 'ε', '$'
        }
        
        # Producciones de la gramática transformada para LL(1)
        self.productions = {
            'programa': [
                ['nls', 'decl_list']
            ],
            'nls': [
                ['NL', 'nls'],
                ['ε']
            ],
            'decl_list': [
                ['decl', 'decl_list'],
                ['ε']
            ],
            'decl': [
                ['funcion'],
                ['global']
            ],
            'global': [
                ['declvar', 'nl']
            ],
            'funcion': [
                ['fun', 'ID', '(', 'params', ')', 'tipo_ret', 'nl', 'bloque', 'end', 'nl']
            ],
            'tipo_ret': [
                [':', 'tipo'],
                ['ε']
            ],
            'bloque': [
                ['declvars', 'comandos']
            ],
            'declvars': [
                ['declvar', 'nl', 'declvars'],
                ['ε']
            ],
            'comandos': [
                ['comando', 'nl', 'comandos'],
                ['ε']
            ],
            'params': [
                ['parametro', 'params_rest'],
                ['ε']
            ],
            'params_rest': [
                [',', 'parametro', 'params_rest'],
                ['ε']
            ],
            'parametro': [
                ['ID', ':', 'tipo']
            ],
            'tipo': [
                ['tipobase', 'tipo_array']
            ],
            'tipo_array': [
                ['[', ']', 'tipo_array'],
                ['ε']
            ],
            'tipobase': [
                ['int'],
                ['bool'],
                ['char'],
                ['string']
            ],
            'declvar': [
                ['ID', ':', 'tipo']
            ],
            'comando': [
                ['cmdif'],
                ['cmdwhile'],
                ['cmdatrib'],
                ['cmdreturn'],
                ['llamada']
            ],
            'cmdif': [
                ['if', 'exp', 'nl', 'bloque', 'elseif_list', 'else_opt', 'end']
            ],
            'elseif_list': [
                ['else', 'if', 'exp', 'nl', 'bloque', 'elseif_list'],
                ['ε']
            ],
            'else_opt': [
                ['else', 'nl', 'bloque'],
                ['ε']
            ],
            'cmdwhile': [
                ['while', 'exp', 'nl', 'bloque', 'loop']
            ],
            'cmdatrib': [
                ['var', '=', 'exp']
            ],
            'llamada': [
                ['ID', '(', 'listaexp', ')']
            ],
            'listaexp': [
                ['exp', 'listaexp_rest'],
                ['ε']
            ],
            'listaexp_rest': [
                [',', 'exp', 'listaexp_rest'],
                ['ε']
            ],
            'cmdreturn': [
                ['return', 'exp_opt']
            ],
            'exp_opt': [
                ['exp'],
                ['ε']
            ],
            'var': [
                ['ID', 'var_index']
            ],
            'var_index': [
                ['[', 'exp', ']', 'var_index'],
                ['ε']
            ],
            'nl': [
                ['NL', 'nl_rest']
            ],
            'nl_rest': [
                ['NL', 'nl_rest'],
                ['ε']
            ],
            # Expresiones con precedencia (de menor a mayor)
            'exp': [
                ['exp_or']
            ],
            'exp_or': [
                ['exp_and', 'exp_or_prime']
            ],
            'exp_or_prime': [
                ['or', 'exp_and', 'exp_or_prime'],
                ['ε']
            ],
            'exp_and': [
                ['exp_eq', 'exp_and_prime']
            ],
            'exp_and_prime': [
                ['and', 'exp_eq', 'exp_and_prime'],
                ['ε']
            ],
            'exp_eq': [
                ['exp_rel', 'exp_eq_prime']
            ],
            'exp_eq_prime': [
                ['=', 'exp_rel', 'exp_eq_prime'],
                ['<>', 'exp_rel', 'exp_eq_prime'],
                ['ε']
            ],
            'exp_rel': [
                ['exp_add', 'exp_rel_prime']
            ],
            'exp_rel_prime': [
                ['>', 'exp_add', 'exp_rel_prime'],
                ['<', 'exp_add', 'exp_rel_prime'],
                ['>=', 'exp_add', 'exp_rel_prime'],
                ['<=', 'exp_add', 'exp_rel_prime'],
                ['ε']
            ],
            'exp_add': [
                ['exp_mul', 'exp_add_prime']
            ],
            'exp_add_prime': [
                ['+', 'exp_mul', 'exp_add_prime'],
                ['-', 'exp_mul', 'exp_add_prime'],
                ['ε']
            ],
            'exp_mul': [
                ['exp_unary', 'exp_mul_prime']
            ],
            'exp_mul_prime': [
                ['*', 'exp_unary', 'exp_mul_prime'],
                ['/', 'exp_unary', 'exp_mul_prime'],
                ['ε']
            ],
            'exp_unary': [
                ['not', 'exp_unary'],
                ['-', 'exp_unary'],
                ['exp_primary']
            ],
            'exp_primary': [
                ['LITNUMERAL'],
                ['LITSTRING'],
                ['true'],
                ['false'],
                ['var'],
                ['new', '[', 'exp', ']', 'tipo'],
                ['(', 'exp', ')'],
                ['llamada']
            ]
        }
        
        # Conjuntos FIRST y FOLLOW
        self.first_sets: Dict[str, Set[str]] = {}
        self.follow_sets: Dict[str, Set[str]] = {}
        
        self._compute_first_sets()
        self._compute_follow_sets()
    
    def _compute_first_sets(self):
        """Calcula los conjuntos FIRST para todos los símbolos"""
        # Inicializar FIRST para terminales
        for terminal in self.terminals:
            if terminal != 'ε':
                self.first_sets[terminal] = {terminal}
        
        # Inicializar FIRST para no terminales
        for non_terminal in self.non_terminals:
            self.first_sets[non_terminal] = set()
        
        # Iterar hasta que no haya cambios
        changed = True
        max_iterations = 100
        iteration = 0
        
        while changed and iteration < max_iterations:
            changed = False
            iteration += 1
            
            for non_terminal in self.non_terminals:
                for production in self.productions.get(non_terminal, []):
                    old_size = len(self.first_sets[non_terminal])
                    
                    # Calcular FIRST de la producción
                    first_of_production = self._first_of_sequence(production)
                    self.first_sets[non_terminal].update(first_of_production)
                    
                    if len(self.first_sets[non_terminal]) > old_size:
                        changed = True
    
    def _first_of_sequence(self, sequence: List[str]) -> Set[str]:
        """Calcula FIRST de una secuencia de símbolos"""
        if not sequence or sequence[0] == 'ε':
            return {'ε'}
        
        result = set()
        all_have_epsilon = True
        
        for symbol in sequence:
            if symbol in self.terminals:
                result.add(symbol)
                all_have_epsilon = False
                break
            else:
                # Es un no terminal
                symbol_first = self.first_sets.get(symbol, set())
                result.update(symbol_first - {'ε'})
                
                if 'ε' not in symbol_first:
                    all_have_epsilon = False
                    break
        
        if all_have_epsilon:
            result.add('ε')
        
        return result
    
    def _compute_follow_sets(self):
        """Calcula los conjuntos FOLLOW para todos los no terminales"""
        # Inicializar FOLLOW
        for non_terminal in self.non_terminals:
            self.follow_sets[non_terminal] = set()
        
        # FOLLOW del símbolo inicial contiene $
        self.follow_sets[self.start_symbol].add('$')
        
        # Iterar hasta que no haya cambios
        changed = True
        max_iterations = 100
        iteration = 0
        
        while changed and iteration < max_iterations:
            changed = False
            iteration += 1
            
            for non_terminal in self.non_terminals:
                for production in self.productions.get(non_terminal, []):
                    for i, symbol in enumerate(production):
                        if symbol in self.non_terminals:
                            old_size = len(self.follow_sets[symbol])
                            
                            # Resto de la producción después del símbolo
                            beta = production[i + 1:]
                            
                            if beta:
                                # FIRST(beta) - {ε} se agrega a FOLLOW(symbol)
                                first_beta = self._first_of_sequence(beta)
                                self.follow_sets[symbol].update(first_beta - {'ε'})
                                
                                # Si ε está en FIRST(beta), agregar FOLLOW(A)
                                if 'ε' in first_beta:
                                    self.follow_sets[symbol].update(
                                        self.follow_sets[non_terminal]
                                    )
                            else:
                                # Si symbol es el último, agregar FOLLOW(A)
                                self.follow_sets[symbol].update(
                                    self.follow_sets[non_terminal]
                                )
                            
                            if len(self.follow_sets[symbol]) > old_size:
                                changed = True
    
    def get_first(self, symbol: str) -> Set[str]:
        """Retorna el conjunto FIRST de un símbolo"""
        return self.first_sets.get(symbol, set())
    
    def get_follow(self, non_terminal: str) -> Set[str]:
        """Retorna el conjunto FOLLOW de un no terminal"""
        return self.follow_sets.get(non_terminal, set())
    
    def print_productions(self):
        """Imprime todas las producciones de la gramática"""
        print("\n=== Producciones de la Gramática Mini-0 ===")
        for non_terminal in sorted(self.productions.keys()):
            productions = self.productions[non_terminal]
            for i, prod in enumerate(productions):
                prod_str = ' '.join(prod)
                if i == 0:
                    print(f"{non_terminal:20} → {prod_str}")
                else:
                    print(f"{' ':20} | {prod_str}")
    
    def print_first_sets(self):
        """Imprime los conjuntos FIRST"""
        print("\n=== Conjuntos FIRST ===")
        for non_terminal in sorted(self.non_terminals):
            first = sorted(self.first_sets[non_terminal])
            print(f"FIRST({non_terminal:20}) = {{{', '.join(first)}}}")
    
    def print_follow_sets(self):
        """Imprime los conjuntos FOLLOW"""
        print("\n=== Conjuntos FOLLOW ===")
        for non_terminal in sorted(self.non_terminals):
            follow = sorted(self.follow_sets[non_terminal])
            print(f"FOLLOW({non_terminal:20}) = {{{', '.join(follow)}}}")

def main():
    """Función de prueba"""
    grammar = GrammarMini0()
    
    print("=" * 80)
    print("GRAMÁTICA MINI-0 - LL(1)")
    print("=" * 80)
    
    grammar.print_productions()
    grammar.print_first_sets()
    grammar.print_follow_sets()

if __name__ == "__main__":
    main()
