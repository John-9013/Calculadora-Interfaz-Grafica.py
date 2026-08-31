# Calculadora Interfaz Grafica - Ejemplos y notas

Este branch añade soporte para:
- Operador de potencia `**` (asociatividad derecha)
- Llamadas a funciones matemáticas seguras: sin, cos, tan, sqrt, pow, log, exp, abs
- Comentarios de línea que comienzan con `#`

Ejemplos de uso:

- Aritmética básica:
  - 2 + 3 * 4   -> 14
  - (2 + 3) * 4 -> 20

- Potencia:
  - 2 ** 3      -> 8
  - 2 ** 3 ** 2 -> 2 ** (3 ** 2) = 2 ** 9 = 512   (asociatividad a la derecha)

- Variables:
  - a = 5       -> asigna 5 a a
  - a * 3       -> 15

- Funciones:
  - sin(0)      -> 0.0
  - sqrt(16)    -> 4.0
  - pow(2,3)    -> 8.0
  - log(exp(1)) -> 1.0

- Comentarios:
  - 2 + 2  # esto es un comentario

Errores comunes:
- Division por cero -> lanza ZeroDivisionError
- Variable no definida -> NameError
- Llamada a función con argumentos incorrectos -> TypeError
