# Reporte de Pruebas - Parser Mini-0

**Fecha:** 1764278963.065863

## Resumen

- **Total de pruebas:** 13
- **Pruebas pasadas:** 13
- **Pruebas falladas:** 0
- **Porcentaje de éxito:** 100.0%

## Casos de Prueba Válidos

| # | Archivo | Resultado | Descripción |
|---|---------|-----------|-------------|
| 1 | `programa1_simple.mini0` | ✅ PASS | Análisis exitoso |
| 2 | `programa2_parametros.mini0` | ✅ PASS | Análisis exitoso |
| 3 | `programa3_ifelse.mini0` | ✅ PASS | Análisis exitoso |
| 4 | `programa4_while.mini0` | ✅ PASS | Análisis exitoso |
| 5 | `programa5_expresiones.mini0` | ✅ PASS | Análisis exitoso |
| 6 | `programa6_arrays.mini0` | ✅ PASS | Análisis exitoso |
| 7 | `programa7_completo.mini0` | ✅ PASS | Análisis exitoso |

## Casos de Prueba con Errores

| # | Archivo | Resultado | Error Detectado |
|---|---------|-----------|----------------|
| 1 | `error1_falta_end.mini0` | ✅ DETECTADO | Error detectado correctamente: Error sintáctico en línea 7, ... |
| 2 | `error2_falta_loop.mini0` | ✅ DETECTADO | Error detectado correctamente: Error sintáctico en línea 11,... |
| 3 | `error3_tipo_invalido.mini0` | ✅ DETECTADO | Error detectado correctamente: Error sintáctico en línea 3, ... |
| 4 | `error4_expresion_incompleta.mini0` | ✅ DETECTADO | Error detectado correctamente: Error sintáctico en línea 5, ... |
| 5 | `error5_parentesis_desbalanceados.mini0` | ✅ DETECTADO | Error detectado correctamente: Error sintáctico en línea 5, ... |
| 6 | `error6_caracter_invalido.mini0` | ✅ DETECTADO | Error detectado correctamente: Error léxico en línea 4, colu... |

## Cobertura de Reglas Gramaticales

### Reglas Ejercitadas:

- ✅ Declaración de funciones (con y sin parámetros)
- ✅ Declaración de variables (locales y globales)
- ✅ Tipos básicos (int, bool)
- ✅ Tipos array ([]int, []bool)
- ✅ Asignaciones
- ✅ Expresiones aritméticas (+, -, *, /, %)
- ✅ Expresiones relacionales (<, >, <=, >=, =, !=)
- ✅ Expresiones lógicas (and, or, not)
- ✅ Estructuras if/else/end
- ✅ Estructuras if/else if/else/end
- ✅ Bucles while/loop
- ✅ Llamadas a funciones
- ✅ Retorno de valores
- ✅ Arrays y acceso a índices
- ✅ Operador new para arrays
- ✅ Expresiones con paréntesis
- ✅ Precedencia de operadores

### Tipos de Errores Detectados:

- ✅ Errores léxicos (caracteres inválidos)
- ✅ Errores sintácticos (falta de end)
- ✅ Errores sintácticos (falta de loop)
- ✅ Errores sintácticos (tipo inválido)
- ✅ Errores sintácticos (expresión incompleta)
- ✅ Errores sintácticos (paréntesis desbalanceados)
