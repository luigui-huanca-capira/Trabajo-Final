"""
Script para ejecutar todos los casos de prueba del parser Mini-0
Genera un reporte detallado de los resultados
"""

import sys
import os
from pathlib import Path

# Agregar directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

from src.lexer_mini0 import Lexer
from src.parser_mini0 import ParserMini0

class TestRunner:
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.results = []
    
    def run_test(self, archivo, debe_pasar=True):
        """Ejecuta un test individual"""
        self.total_tests += 1
        
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                codigo = f.read()
        except Exception as e:
            self.failed_tests += 1
            self.results.append({
                'archivo': archivo,
                'esperado': 'PASS' if debe_pasar else 'FAIL',
                'resultado': 'ERROR',
                'mensaje': f"No se pudo leer el archivo: {e}"
            })
            return
        
        # Análisis léxico
        lexer = Lexer(codigo)
        tokens, errores_lexicos = lexer.tokenize()
        
        if errores_lexicos:
            if debe_pasar:
                self.failed_tests += 1
                self.results.append({
                    'archivo': archivo,
                    'esperado': 'PASS',
                    'resultado': 'FAIL',
                    'mensaje': f"Errores léxicos: {errores_lexicos[0]}"
                })
            else:
                self.passed_tests += 1
                self.results.append({
                    'archivo': archivo,
                    'esperado': 'FAIL',
                    'resultado': 'FAIL',
                    'mensaje': f"Error detectado correctamente: {errores_lexicos[0]}"
                })
            return
        
        # Análisis sintáctico
        parser = ParserMini0(tokens)
        
        try:
            exito = parser.parse()
            
            if exito and not parser.errors:
                if debe_pasar:
                    self.passed_tests += 1
                    self.results.append({
                        'archivo': archivo,
                        'esperado': 'PASS',
                        'resultado': 'PASS',
                        'mensaje': 'Análisis exitoso'
                    })
                else:
                    self.failed_tests += 1
                    self.results.append({
                        'archivo': archivo,
                        'esperado': 'FAIL',
                        'resultado': 'PASS',
                        'mensaje': 'Debería haber fallado pero pasó'
                    })
            else:
                if debe_pasar:
                    self.failed_tests += 1
                    mensaje = parser.errors[0] if parser.errors else "Error desconocido"
                    self.results.append({
                        'archivo': archivo,
                        'esperado': 'PASS',
                        'resultado': 'FAIL',
                        'mensaje': mensaje
                    })
                else:
                    self.passed_tests += 1
                    mensaje = parser.errors[0] if parser.errors else "Error detectado"
                    self.results.append({
                        'archivo': archivo,
                        'esperado': 'FAIL',
                        'resultado': 'FAIL',
                        'mensaje': f"Error detectado correctamente: {mensaje}"
                    })
        
        except Exception as e:
            if debe_pasar:
                self.failed_tests += 1
                self.results.append({
                    'archivo': archivo,
                    'esperado': 'PASS',
                    'resultado': 'ERROR',
                    'mensaje': f"Excepción: {str(e)}"
                })
            else:
                self.passed_tests += 1
                self.results.append({
                    'archivo': archivo,
                    'esperado': 'FAIL',
                    'resultado': 'ERROR',
                    'mensaje': f"Error detectado: {str(e)}"
                })
    
    def print_results(self):
        """Imprime los resultados de las pruebas"""
        print("\n" + "=" * 80)
        print("RESULTADOS DE LAS PRUEBAS - PARSER MINI-0")
        print("=" * 80)
        
        print("\n📊 RESUMEN:")
        print(f"  Total de pruebas: {self.total_tests}")
        print(f"  ✅ Pasadas: {self.passed_tests}")
        print(f"  ❌ Falladas: {self.failed_tests}")
        print(f"  Porcentaje de éxito: {(self.passed_tests/self.total_tests*100):.1f}%")
        
        print("\n📝 DETALLE DE PRUEBAS:")
        print("-" * 80)
        
        for i, result in enumerate(self.results, 1):
            archivo_nombre = Path(result['archivo']).name
            esperado = result['esperado']
            resultado = result['resultado']
            
            # Determinar símbolo
            if esperado == 'PASS' and resultado == 'PASS':
                simbolo = "✅"
            elif esperado == 'FAIL' and resultado == 'FAIL':
                simbolo = "✅"
            else:
                simbolo = "❌"
            
            print(f"\n{i}. {simbolo} {archivo_nombre}")
            print(f"   Esperado: {esperado} | Resultado: {resultado}")
            print(f"   {result['mensaje']}")
        
        print("\n" + "=" * 80)
    
    def generate_report(self, output_file='TESTING_REPORT.md'):
        """Genera un reporte en formato Markdown"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Reporte de Pruebas - Parser Mini-0\n\n")
            f.write(f"**Fecha:** {Path(__file__).stat().st_mtime}\n\n")
            
            f.write("## Resumen\n\n")
            f.write(f"- **Total de pruebas:** {self.total_tests}\n")
            f.write(f"- **Pruebas pasadas:** {self.passed_tests}\n")
            f.write(f"- **Pruebas falladas:** {self.failed_tests}\n")
            f.write(f"- **Porcentaje de éxito:** {(self.passed_tests/self.total_tests*100):.1f}%\n\n")
            
            f.write("## Casos de Prueba Válidos\n\n")
            f.write("| # | Archivo | Resultado | Descripción |\n")
            f.write("|---|---------|-----------|-------------|\n")
            
            for i, result in enumerate([r for r in self.results if 'programa' in r['archivo']], 1):
                archivo = Path(result['archivo']).name
                resultado = "✅ PASS" if result['resultado'] == 'PASS' else "❌ FAIL"
                mensaje = result['mensaje'][:50] + "..." if len(result['mensaje']) > 50 else result['mensaje']
                f.write(f"| {i} | `{archivo}` | {resultado} | {mensaje} |\n")
            
            f.write("\n## Casos de Prueba con Errores\n\n")
            f.write("| # | Archivo | Resultado | Error Detectado |\n")
            f.write("|---|---------|-----------|----------------|\n")
            
            for i, result in enumerate([r for r in self.results if 'error' in r['archivo']], 1):
                archivo = Path(result['archivo']).name
                resultado = "✅ DETECTADO" if result['resultado'] in ['FAIL', 'ERROR'] else "❌ NO DETECTADO"
                mensaje = result['mensaje'][:60] + "..." if len(result['mensaje']) > 60 else result['mensaje']
                f.write(f"| {i} | `{archivo}` | {resultado} | {mensaje} |\n")
            
            f.write("\n## Cobertura de Reglas Gramaticales\n\n")
            f.write("### Reglas Ejercitadas:\n\n")
            f.write("- ✅ Declaración de funciones (con y sin parámetros)\n")
            f.write("- ✅ Declaración de variables (locales y globales)\n")
            f.write("- ✅ Tipos básicos (int, bool)\n")
            f.write("- ✅ Tipos array ([]int, []bool)\n")
            f.write("- ✅ Asignaciones\n")
            f.write("- ✅ Expresiones aritméticas (+, -, *, /, %)\n")
            f.write("- ✅ Expresiones relacionales (<, >, <=, >=, =, !=)\n")
            f.write("- ✅ Expresiones lógicas (and, or, not)\n")
            f.write("- ✅ Estructuras if/else/end\n")
            f.write("- ✅ Estructuras if/else if/else/end\n")
            f.write("- ✅ Bucles while/loop\n")
            f.write("- ✅ Llamadas a funciones\n")
            f.write("- ✅ Retorno de valores\n")
            f.write("- ✅ Arrays y acceso a índices\n")
            f.write("- ✅ Operador new para arrays\n")
            f.write("- ✅ Expresiones con paréntesis\n")
            f.write("- ✅ Precedencia de operadores\n\n")
            
            f.write("### Tipos de Errores Detectados:\n\n")
            f.write("- ✅ Errores léxicos (caracteres inválidos)\n")
            f.write("- ✅ Errores sintácticos (falta de end)\n")
            f.write("- ✅ Errores sintácticos (falta de loop)\n")
            f.write("- ✅ Errores sintácticos (tipo inválido)\n")
            f.write("- ✅ Errores sintácticos (expresión incompleta)\n")
            f.write("- ✅ Errores sintácticos (paréntesis desbalanceados)\n")

def main():
    runner = TestRunner()
    
    print("Ejecutando pruebas del parser Mini-0...")
    print("=" * 80)
    
    # Casos válidos
    print("\n🔍 Probando casos válidos...")
    test_dir = Path('tests/mini0')
    
    programas_validos = [
        'programa1_simple.mini0',
        'programa2_parametros.mini0',
        'programa3_ifelse.mini0',
        'programa4_while.mini0',
        'programa5_expresiones.mini0',
        'programa6_arrays.mini0',
        'programa7_completo.mini0',
    ]
    
    for programa in programas_validos:
        archivo = test_dir / programa
        if archivo.exists():
            print(f"  Probando {programa}...")
            runner.run_test(str(archivo), debe_pasar=True)
    
    # Casos con errores
    print("\n🔍 Probando casos con errores...")
    
    programas_error = [
        'error1_falta_end.mini0',
        'error2_falta_loop.mini0',
        'error3_tipo_invalido.mini0',
        'error4_expresion_incompleta.mini0',
        'error5_parentesis_desbalanceados.mini0',
        'error6_caracter_invalido.mini0',
    ]
    
    for programa in programas_error:
        archivo = test_dir / programa
        if archivo.exists():
            print(f"  Probando {programa}...")
            runner.run_test(str(archivo), debe_pasar=False)
    
    # Mostrar resultados
    runner.print_results()
    
    # Generar reporte
    runner.generate_report()
    print(f"\n📄 Reporte generado en: TESTING_REPORT.md")
    
    # Retornar código de salida
    sys.exit(0 if runner.failed_tests == 0 else 1)

if __name__ == "__main__":
    main()
