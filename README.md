# Parser Mini-0 - Analizador Sintáctico Recursivo Descendente

**Universidad La Salle - Compiladores**  
**pratica final**  
**Fecha de Entrega:** 28/11/2025

---

## 📋 Descripción

Parser recursivo descendente (LL1) para el lenguaje **Mini-0**, implementado en Python. El parser reconoce programas válidos, detecta errores léxicos y sintácticos, y genera reportes detallados.

### ✨ Características

- ✅ Analizador léxico completo
- ✅ Analizador sintáctico recursivo descendente
- ✅ Tabla de análisis sintáctico LL(1)
- ✅ Manejo robusto de errores con mensajes claros
- ✅ 13 casos de prueba (7 válidos + 6 con errores)
- ✅ 100% de cobertura de reglas gramaticales
- ✅ Documentación técnica completa

---

## 📁 Estructura del Proyecto

```
Trabajo Final/
├── src/
│   ├── lexer_mini0.py       # Analizador léxico
│   ├── parser_mini0.py      # Analizador sintáctico
│   ├── grammar_mini0.py     # Definición de la gramática
│   ├── ll1_table_mini0.py   # Generador de tabla LL1
│   └── main_mini0.py        # Programa principal
├── tests/
│   └── mini0/
│       ├── programa1_simple.mini0
│       ├── programa2_parametros.mini0
│       ├── programa3_ifelse.mini0
│       ├── programa4_while.mini0
│       ├── programa5_expresiones.mini0
│       ├── programa6_arrays.mini0
│       ├── programa7_completo.mini0
│       ├── error1_falta_end.mini0
│       ├── error2_falta_loop.mini0
│       ├── error3_tipo_invalido.mini0
│       ├── error4_expresion_incompleta.mini0
│       ├── error5_parentesis_desbalanceados.mini0
│       └── error6_caracter_invalido.mini0
├── run_tests_mini0.py       # Script de pruebas automatizado
├── INFORME_TECNICO.md       # Informe técnico completo
├── TABLA_LL1.md             # Tabla de análisis sintáctico LL1
├── TESTING_REPORT.md        # Reporte de pruebas
├── README.md                # Este archivo
└── requirements.txt         # Dependencias (ninguna)
```

---

## 🚀 Instalación

### Requisitos

- Python 3.7 o superior
- No se requieren dependencias externas

### Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd "Trabajo Final"
```

---

## 💻 Uso

### 1. Analizar un Programa Individual

Para analizar un archivo `.mini0`:

```bash
python src/main_mini0.py tests/mini0/programa1_simple.mini0
```

**Salida exitosa:**
```
✓ Análisis léxico completado: 21 tokens
✓ Análisis sintáctico completado exitosamente
✓ El programa es sintácticamente correcto
```

**Salida con error:**
```
Error sintáctico en línea 7, columna 1: Se esperaba END, se encontró EOF
```

### 2. Ejecutar Todas las Pruebas

Para ejecutar todos los casos de prueba automáticamente:

```bash
python run_tests_mini0.py
```

**Salida:**
```
================================================================================
RESULTADOS DE LAS PRUEBAS - PARSER MINI-0
================================================================================

📊 RESUMEN:
  Total de pruebas: 13
  ✅ Pasadas: 13
  ❌ Falladas: 0
  Porcentaje de éxito: 100.0%

📝 DETALLE DE PRUEBAS:
--------------------------------------------------------------------------------

1. ✅ programa1_simple.mini0
   Esperado: PASS | Resultado: PASS
   Análisis exitoso

[... más resultados ...]

📄 Reporte generado en: TESTING_REPORT.md
```

### 3. Ver Reporte de Pruebas

El reporte detallado se genera automáticamente en `TESTING_REPORT.md`:

```bash
# En Windows
notepad TESTING_REPORT.md

# En Linux/Mac
cat TESTING_REPORT.md
```

---

## 📝 Ejemplos de Programas Mini-0

### Ejemplo 1: Función Simple

```mini0
fun main(): int
    x: int
    x = 10
    return x
end
```

**Ejecutar:**
```bash
python src/main_mini0.py tests/mini0/programa1_simple.mini0
```

### Ejemplo 2: Función con Parámetros

```mini0
fun suma(a: int, b: int): int
    resultado: int
    resultado = a + b
    return resultado
end
```

**Ejecutar:**
```bash
python src/main_mini0.py tests/mini0/programa2_parametros.mini0
```

### Ejemplo 3: Estructuras de Control

```mini0
fun max(a: int, b: int): int
    if a > b
        return a
    else
        return b
    end
end
```

**Ejecutar:**
```bash
python src/main_mini0.py tests/mini0/programa3_ifelse.mini0
```

### Ejemplo 4: Bucles

```mini0
fun factorial(n: int): int
    resultado: int
    i: int
    resultado = 1
    i = 1
    
    while i <= n
        resultado = resultado * i
        i = i + 1
    loop
    
    return resultado
end
```

**Ejecutar:**
```bash
python src/main_mini0.py tests/mini0/programa4_while.mini0
```

### Ejemplo 5: Arrays

```mini0
fun main(): int
    numeros: []int
    i: int
    suma: int
    
    numeros = new [10] int
    i = 0
    suma = 0
    
    while i < 10
        numeros[i] = i * 2
        suma = suma + numeros[i]
        i = i + 1
    loop
    
    return suma
end
```

**Ejecutar:**
```bash
python src/main_mini0.py tests/mini0/programa6_arrays.mini0
```

---

## 🧪 Casos de Prueba

### Programas Válidos (7)

| # | Archivo | Descripción |
|---|---------|-------------|
| 1 | `programa1_simple.mini0` | Función básica con return |
| 2 | `programa2_parametros.mini0` | Función con parámetros |
| 3 | `programa3_ifelse.mini0` | Estructuras if/else |
| 4 | `programa4_while.mini0` | Bucles while/loop |
| 5 | `programa5_expresiones.mini0` | Expresiones complejas |
| 6 | `programa6_arrays.mini0` | Arrays y acceso a índices |
| 7 | `programa7_completo.mini0` | Programa completo (fibonacci) |

### Programas con Errores (6)

| # | Archivo | Error Detectado |
|---|---------|-----------------|
| 1 | `error1_falta_end.mini0` | Falta END |
| 2 | `error2_falta_loop.mini0` | Falta LOOP |
| 3 | `error3_tipo_invalido.mini0` | Tipo inválido |
| 4 | `error4_expresion_incompleta.mini0` | Expresión incompleta |
| 5 | `error5_parentesis_desbalanceados.mini0` | Paréntesis desbalanceados |
| 6 | `error6_caracter_invalido.mini0` | Carácter inválido |

---

## 📚 Documentación

### Informe Técnico

El informe técnico completo está en `INFORME_TECNICO.md` e incluye:

1. Introducción
2. Gramática original
3. Transformaciones aplicadas
4. Gramática transformada (LL1)
5. Conjuntos FIRST y FOLLOW
6. Tabla de análisis sintáctico LL1
7. Diseño del parser
8. Manejo de errores
9. Casos de prueba
10. Resultados
11. Conclusiones

**Ver informe:**
```bash
# En Windows
notepad INFORME_TECNICO.md

# En Linux/Mac
cat INFORME_TECNICO.md
```

### Tabla LL1

La tabla de análisis sintáctico LL1 completa está en `TABLA_LL1.md`.

**Ver tabla:**
```bash
# En Windows
notepad TABLA_LL1.md

# En Linux/Mac
cat TABLA_LL1.md
```

---

## 🔧 Comandos Útiles

### Analizar un Programa Específico

```bash
# Programa válido
python src/main_mini0.py tests/mini0/programa1_simple.mini0

# Programa con error
python src/main_mini0.py tests/mini0/error1_falta_end.mini0
```

### Ejecutar Todas las Pruebas

```bash
python run_tests_mini0.py
```

### Ver Ayuda

```bash
python src/main_mini0.py --help
```

### Limpiar Archivos Temporales

```bash
# En Windows
del /s /q src\__pycache__

# En Linux/Mac
rm -rf src/__pycache__
```

---

## 📊 Resultados de Pruebas

### Última Ejecución

```
Total de pruebas: 13
✅ Pasadas: 13
❌ Falladas: 0
Porcentaje de éxito: 100.0%
```

### Cobertura de Reglas Gramaticales

- ✅ Declaración de funciones (con y sin parámetros)
- ✅ Declaración de variables (locales y globales)
- ✅ Tipos básicos (int, bool, char, string)
- ✅ Tipos array ([]int, []bool, etc.)
- ✅ Asignaciones
- ✅ Expresiones aritméticas (+, -, *, /)
- ✅ Expresiones relacionales (<, >, <=, >=, =, !=)
- ✅ Expresiones lógicas (and, or, not)
- ✅ Estructuras if/else if/else/end
- ✅ Bucles while/loop
- ✅ Llamadas a funciones
- ✅ Retorno de valores
- ✅ Arrays y acceso a índices
- ✅ Operador new para arrays
- ✅ Precedencia de operadores

---

## 🐛 Manejo de Errores

### Tipos de Errores Detectados

#### Errores Léxicos
- Caracteres no reconocidos
- Comentarios de bloque no cerrados

**Ejemplo:**
```
Error léxico en línea 4, columna 12: Carácter no reconocido: '@'
```

#### Errores Sintácticos
- Tokens inesperados
- Falta de delimitadores
- Estructuras incompletas
- Tipos inválidos

**Ejemplos:**
```
Error sintáctico en línea 7, columna 1: Se esperaba END, se encontró EOF
Error sintáctico en línea 3, columna 8: Se esperaba un tipo (int, bool, char, string)
```

### Códigos de Salida

- **0:** Análisis exitoso
- **1:** Error detectado

---

## 🎯 Características del Lenguaje Mini-0

### Palabras Reservadas

```
fun  if  else  while  loop  return  end
new  true  false
int  bool  char  string
and  or  not
```

### Operadores

**Aritméticos:** `+`, `-`, `*`, `/`  
**Relacionales:** `>`, `<`, `>=`, `<=`, `=`, `!=`  
**Lógicos:** `and`, `or`, `not`  
**Asignación:** `=`

### Delimitadores

`(`, `)`, `[`, `]`, `:`, `,`, salto de línea

### Tipos de Datos

- `int` - Enteros
- `bool` - Booleanos (true, false)
- `char` - Caracteres
- `string` - Cadenas de texto
- `[]tipo` - Arrays (ej: `[]int`, `[][]bool`)

---

## 👥 Autores

- Luigui Alexander Huanca capira    



---

## 📅 Información del Proyecto

- **Universidad:** La Salle
- **Materia:** Compiladores
- **Trabajo:** Práctico 2 - Parser Recursivo Descendente
- **Fecha de Entrega:** 28/11/2025
- **Valor:** 100% del Examen Final

---

## 📄 Licencia

Este proyecto es parte de un trabajo académico para la Universidad La Salle.

---



## ✅ Checklist de Entrega

- [x] Parser recursivo descendente implementado
- [x] Gramática transformada a LL(1)
- [x] Tabla de análisis sintáctico LL1
- [x] Manejo de errores léxicos y sintácticos
- [x] 13 casos de prueba (7 válidos + 6 errores)
- [x] Informe técnico completo
- [x] Código en GitHub
- [x] README con instrucciones
- [x] 100% de pruebas pasando

---

## 📞 Contacto

Para preguntas o comentarios sobre este proyecto, contactar a los autores.
# Trabajo-Final
# Trabajo-Final
