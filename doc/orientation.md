## Acotaciones iniciales
- Hacer un programa en cualquier lenguaje de programacion (recomendable c o python)
- Tiene que correr en linux sin problema
- Equipos de 2
- Tienen 1 semana para implementarlo


# Orientacion:
## 1. Implementar un scheduler que tenga los 4 algoritmos que dimos en clases
  - FIFO - first come, first serve
  - STF - shortest time first
  - STCF - shortest time to completoion first
  - RR - round robin

## 2. Implementar ambas metricas
  - Turnaround time
  - Response time

## 3. El programa debe leer de la entrada standard e imprimir por la salida standard.

## 4. El formato de entrada:
### Aclaraciones:
- Lineas que comienzan con simbolo # se ignoran
- Lineas en blanco o que solo contengan espacios tambien se ignoran
- Todo lo que venga despues del primer # de cada linea tambien se ignora.
### Formato:
- `N `-> numero de jobs a ejecutar (N > 1 < 1000)
- `Q` -> quantum size, tiempo que dura cada time slice en sistema operativo, en milisegundos (interrupcion de reloj)
- `E1 E2 E3 ...` -> tiempos, multiplos de Q que significan el quantum de tiempo que el sistema operativo le va a dar a cada job.

- Nota, tiene que haber una corrida completa para cada numero

*< No esta claro de que numeros hablan arriba deben ser `E1 E2 ...`>*

```bat
a1 t1 io11-iot11 io12-iot12
...
an tn ion1 iotn1 ....
```
- Requerido: 
  - a1 = tiempo de arrival del job 1
  - t1 = tiempo de completamiento del job 1 (todo en milisegundos)
- Opcional: 
  - io11 = momento en el que va a ocurrir el 1er request IO (bloqueo) para el job 1
  - iot11 = tiempo que va a demorar el 1er bloqueso del job 1


Nota: El tiempo de duracion de un job (proceso) puede no ser multiplo de Q.

## 5. Formato de salida

a) Las primeras `N` lineas deben tener `8` numeros cada una, separados por espacios y en el orden siguiente:
1. **turnaround time** with fifo
2. **response time** with fifo
3. **turnaround time** with stf
4. **response time** with stf
5. **turnaround time** with stcf
6. **response time** with stcf
7. **turnaround time** with rr
8. **response time** with rr 
 
```bat
<1> <2> <3> <4> <5> <6> <7> <8> # line 1
...
<1> <2> <3> <4> <5> <6> <7> <8> # line N
```
b) Despues de lo anterior **una linea en blanco**.

c) Luego 4 lineas (fifo, stf, stcf, rr) con 3 numeros (en milisegundos, redondeando)
1. average turnaround time
2. average response time
3. total time
```bat
<1> <2> <3> # line 1
...
<1> <2> <3> # line 4
```
### Otras aclaraciones:
6. - Si dos o mas jobs son iniciados a la misma vez, el scheduler debe escoger aleatoriamente cual de ellos se ejecuta primero. 
    - El scheduler con una misma entrada, puede tener una salida diferente, en dependencia de la aleatoriedad mencionada anteriormente.

7. El programa debe terminar correctamente cuando termina de leer la entrada (y de imprimir la salida).