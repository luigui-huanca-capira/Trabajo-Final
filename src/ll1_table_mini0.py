"""
Generador de Tabla de Análisis Sintáctico LL(1) para Mini-0
"""

from typing import Dict, Set, Tuple, Optional
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.grammar_mini0 import GrammarMini0

class LL1TableMini0:
    """Genera y valida la tabla de análisis sintáctico LL(1) para Mini-0"""
    
    def __init__(self, grammar: GrammarMini0):
        self.grammar = grammar
        self.table: Dict[Tuple[str, str], list] = {}
        self.conflicts: list = []
        self._build_table()
    
    def _build_table(self):
        """Construye la tabla LL(1)"""
        # Para cada no terminal
        for non_terminal in self.grammar.non_terminals:
            # Para cada producción de ese no terminal
            for production in self.grammar.productions.get(non_terminal, []):
                # Calcular FIRST de la producción
                first_prod = self.grammar._first_of_sequence(production)
                
                # Para cada terminal en FIRST(producción)
                for terminal in first_prod:
                    if terminal != 'ε':
                        # Agregar entrada a la tabla
                        key = (non_terminal, terminal)
                        if key in self.table:
                            # Conflicto detectado
                            self.conflicts.append({
                                'non_terminal': non_terminal,
                                'terminal': terminal,
                                'production1': self.table[key],
                                'production2': production
                            })
                        else:
                            self.table[key] = production
                
                # Si ε está en FIRST(producción)
                if 'ε' in first_prod:
                    # Para cada terminal en FOLLOW(no_terminal)
                    follow_nt = self.grammar.get_follow(non_terminal)
                    for terminal in follow_nt:
                        key = (non_terminal, terminal)
                        if key in self.table:
                            # Conflicto detectado
                            self.conflicts.append({
                                'non_terminal': non_terminal,
                                'terminal': terminal,
                                'production1': self.table[key],
                                'production2': production
                            })
                        else:
                            self.table[key] = production
    
    def get_production(self, non_terminal: str, terminal: str) -> Optional[list]:
        """Obtiene la producción para un par (no_terminal, terminal)"""
        return self.table.get((non_terminal, terminal))
    
    def is_ll1(self) -> bool:
        """Verifica si la gramática es LL(1) (sin conflictos)"""
        return len(self.conflicts) == 0
    
    def print_table(self):
        """Imprime la tabla LL(1) en formato legible"""
        # Obtener todos los terminales únicos
        terminals = sorted(set(term for _, term in self.table.keys()))
        non_terminals = sorted(self.grammar.non_terminals)
        
        # Ancho de columnas
        nt_width = max(len(nt) for nt in non_terminals) + 2
        term_width = 15
        
        print("\n" + "=" * 120)
        print("TABLA DE ANÁLISIS SINTÁCTICO LL(1) - MINI-0")
        print("=" * 120)
        
        # Encabezado
        header = f"{'No Terminal':<{nt_width}}"
        for term in terminals[:10]:  # Limitar a 10 terminales por línea
            header += f"{term:<{term_width}}"
        print(header)
        print("-" * 120)
        
        # Filas
        for nt in non_terminals:
            row = f"{nt:<{nt_width}}"
            for term in terminals[:10]:
                prod = self.get_production(nt, term)
                if prod:
                    prod_str = ' '.join(prod)
                    if len(prod_str) > term_width - 2:
                        prod_str = prod_str[:term_width-5] + "..."
                    row += f"{prod_str:<{term_width}}"
                else:
                    row += f"{'—':<{term_width}}"
            print(row)
        
        print("=" * 120)
        print(f"\n¿Es LL(1)? {'Sí ✓' if self.is_ll1() else 'No ✗'}")
        
        if not self.is_ll1():
            print(f"\nConflictos encontrados: {len(self.conflicts)}")
            for i, conflict in enumerate(self.conflicts[:5], 1):
                print(f"\n  Conflicto {i}:")
                print(f"    No terminal: {conflict['non_terminal']}")
                print(f"    Terminal: {conflict['terminal']}")
                print(f"    Producción 1: {' '.join(conflict['production1'])}")
                print(f"    Producción 2: {' '.join(conflict['production2'])}")
    
    def export_to_markdown(self, filename: str = "docs/tabla_ll1_mini0.md"):
        """Exporta la tabla LL(1) a formato Markdown"""
        # Obtener todos los terminales únicos (limitados para legibilidad)
        all_terminals = sorted(set(term for _, term in self.table.keys()))
        # Seleccionar terminales más importantes
        important_terminals = ['ID', 'LITNUMERAL', 'LITSTRING', 'if', 'while', 'fun', 
                              'return', 'int', 'bool', '+', '-', '(', ')', 'NL', '$']
        terminals = [t for t in important_terminals if t in all_terminals]
        
        non_terminals = sorted(self.grammar.non_terminals)
        
        content = "# Tabla de Análisis Sintáctico LL(1) - Mini-0\n\n"
        content += "Esta tabla se utiliza para el análisis sintáctico predictivo del lenguaje Mini-0.\n\n"
        content += "## Interpretación de la Tabla\n\n"
        content += "- **Filas**: Representan los no terminales de la gramática\n"
        content += "- **Columnas**: Representan los terminales (tokens) de entrada\n"
        content += "- **Celdas**: Contienen la producción a aplicar\n"
        content += "- **—**: Indica un error sintáctico\n\n"
        content += "## Tabla LL(1) (Terminales Principales)\n\n"
        
        # Encabezado
        content += "| No Terminal |"
        for term in terminals:
            content += f" {term} |"
        content += "\n"
        
        content += "|---|"
        for _ in terminals:
            content += "---|"
        content += "\n"
        
        # Filas
        for nt in non_terminals[:20]:  # Limitar a 20 no terminales para legibilidad
            content += f"| **{nt}** |"
            for term in terminals:
                prod = self.get_production(nt, term)
                if prod:
                    prod_str = ' '.join(prod)
                    if len(prod_str) > 30:
                        prod_str = prod_str[:27] + "..."
                    content += f" {nt} → {prod_str} |"
                else:
                    content += " — |"
            content += "\n"
        
        content += "\n## Notas\n\n"
        content += "- **ε** (epsilon) representa la cadena vacía\n"
        content += "- **$** representa el fin de la entrada\n"
        content += "- **NL** representa saltos de línea (significativos en Mini-0)\n"
        content += f"- Esta tabla garantiza que el parser sea determinístico: **{'SIN conflictos ✓' if self.is_ll1() else 'CON conflictos ✗'}**\n"
        content += f"\n**Total de entradas en la tabla:** {len(self.table)}\n"
        content += f"**Total de no terminales:** {len(self.grammar.non_terminals)}\n"
        content += f"**Total de terminales:** {len(all_terminals)}\n"
        
        # Escribir archivo
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filename

def main():
    """Función de prueba"""
    
    print("Generando tabla LL(1) para Mini-0...")
    grammar = GrammarMini0()
    table = LL1TableMini0(grammar)
    
    table.print_table()
    
    if table.is_ll1():
        print("\n✓ La gramática es LL(1) - No hay conflictos")
        filename = table.export_to_markdown()
        print(f"✓ Tabla exportada a: {filename}")
    else:
        print("\n✗ La gramática NO es LL(1) - Se encontraron conflictos")

if __name__ == "__main__":
    main()
