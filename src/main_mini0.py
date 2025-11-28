"""
Programa principal para el parser Mini-0
Ejecuta el análisis léxico y sintáctico de programas Mini-0
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.lexer_mini0 import Lexer
from src.parser_mini0 import ParserMini0

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print("Uso: python main_mini0.py <archivo.mini0>", file=sys.stderr)
        print("\nEjemplo: python main_mini0.py tests/mini0/programa1_simple.mini0")
        sys.exit(1)
    
    archivo = sys.argv[1]
    
    # Verificar que el archivo existe
    if not Path(archivo).exists():
        print(f"Error: El archivo '{archivo}' no existe", file=sys.stderr)
        sys.exit(1)
    
    # Leer el código fuente
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
    except Exception as e:
        print(f"Error al leer el archivo: {e}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Analizando archivo: {archivo}")
    print("=" * 60)
    
    # Análisis léxico
    print("\n[1] Análisis Léxico...")
    lexer = Lexer(codigo)
    tokens, errores_lexicos = lexer.tokenize()
    
    if errores_lexicos:
        print("\n❌ Errores léxicos encontrados:")
        for error in errores_lexicos:
            print(f"  {error}", file=sys.stderr)
        sys.exit(1)
    
    print(f"✓ Análisis léxico completado: {len(tokens)} tokens generados")
    
    # Mostrar tokens si se solicita modo verbose
    if '--verbose' in sys.argv or '-v' in sys.argv:
        print("\nTokens generados:")
        for i, token in enumerate(tokens[:20]):  # Mostrar primeros 20
            print(f"  {i+1}. {token}")
        if len(tokens) > 20:
            print(f"  ... y {len(tokens) - 20} tokens más")
    
    # Análisis sintáctico
    print("\n[2] Análisis Sintáctico...")
    parser = ParserMini0(tokens)
    
    try:
        exito = parser.parse()
        
        if exito and not parser.errors:
            print("\n✓ Análisis sintáctico completado exitosamente")
            print("\n" + "=" * 60)
            print("✅ El programa es sintácticamente correcto")
            print("=" * 60)
            sys.exit(0)
        else:
            print("\n❌ Errores sintácticos encontrados:")
            for error in parser.errors:
                print(f"  {error}", file=sys.stderr)
            sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Error durante el análisis sintáctico: {e}", file=sys.stderr)
        if '--debug' in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
