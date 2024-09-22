# Prueba técnica Clintell Technology - Simulación simple de mercado económico

Este proyecto de código define un mercado simple, con agentes económicos y un sólo producto (tarjetas gráficas).  El mercado es simulado por iteraciones, en las que los agentes son ordenados de manera aleatoria y, secencialmente, pueden decidir si comprar, vender o no hacer nada. En función de la decisión de cada agente, el precio unitario de las tarjetas gráficas se incrementa, disminuye o permanece estable. Hay cuatro tipos de agentes en función de sus políticas a la hora de decidir sus operaciones económicas:

 * Agentes aleatorios: En cada iteración tienen 1/3 de probabilidades de comprar, 1/3 de
probabilidades de vender y 1/3 de probabilidades de no hacer nada; no tienen en cuenta el precio de las tarjetas o su variación.
 * Agentes tendenciales : Tienen un 75% de probabilidades de comprar y un 25% de probabilidades de no hacer nada si el precio se ha incrementado un 1% o más en la anterior iteración. En caso contrario, tienen un 20% de probabilidades de vender y un 80% de probabilidades de no hacer nada.
 * Agentes anti-tendenciales: 75% de probabilidades de comprar y un 25% de probabilidades de no hacer nada si el precio ha disminuido un 1% o más en la anterior iteración. En caso contrario, tienen un 20% de probabilidades de vender y un 80% de probabilidades de no hacer nada.
 * Agentes optimizadores: Su objetivo es maximizar su balance al final de la simulación y quedarse con un inventario de cero unidades. 

Los campos son parametrizables; sus valores predeterminados son los siguientes:
 * Balance inicial de cada agente: 1000.00
 * Precio inicial de cada tarjeta: 200.00
 * Nº de agentes aleatorios: 51
 * Nº de agentes tendenciales: 24
 * Nº de agentes anti-tendenciales: 24
 * Nº de agentes optimizadores: 24
 * Nº de iteraciones a simular: 1000
 * Stock máximo de tarjetas en total: 100.000

## Estructura del código:

 * Módulo ‘__agentes__’: Contiene la clase Agente, que contiene funcionalidad compartida por todos los tipos de agentes, y de la que heredan las subclases para cada tipo de agente: AgenteAleatorio, AgenteTendencial, AgenteAntiTendencial y AgenteOptimizador.
 * Módulo ‘__gestor_mercado__’: Contiene la clase GestorMercado, que contiene toda ls funcionalidad para generar los agentes económicos y simular las iteraciones de mercado, comunicando la información hacia y desde los agentes y efectuando los cambios pertinentes en stock y precio de las tarjetas. Se ha considerado apropiado condensar esta funcionalidad en una sola clase.  GestorMercado crea los distintos agentes, les envía la información del precio de las tarjetas en una determinada iteración y el cambio de precio con respecto a la iteración anterior, y recibe de cada agente su decisión (comprar, vender o no hacer nada). Aplica estas decisiones al stock y al precio de las tarjetas, almacenando estas variables y calculando el cambio de precio. Por tanto, todos los parámetros relevantes de número de agentes, precio inicial, número de iteraciones, etc., son recogidos en esta clase.
 * Módulo ‘\__\__main\__\__’: Lanza la aplicación y permite la parametrización desde la consola de comandos.


## Diagrama de Clases

![Diagrama de Clases](/Diagrama_Clases.png)


## Uso del paquete

Requerimientos: Python 3.2 o superior.
Modo de empleo: Con la consola de comandos, navegar hasta el directorio que contiene los ficheros de código. Una vez allí, ejecutar el comando python \__\__main\__\__.py.
El código permite pasar parámetros mediante la consola de comandos:

* -h / --help: Muestra todos los posibles argumentos y sus valores predeterminados 
* -v / --verbose: Activa la verbosidad; muestra cada operación de cada agente 
* -i / --informe: Activa el informe final de mercado; muestra el precio unitario final y el balance e inventario de cada agente en la última iteración 
* -aa / --num_agentes_aleatorios: Determina el número de agentes de tipo aleatorio (int) Valor predeterminado: 51
* -at / --num_agentes_tendenciales: Determina el número de agentes de tipo tendencial (int) Valor predeterminado: 24
* -aat / --num_agentes_antitendenciales: Determina el número de agentes de tipo antitendencial (int) Valor predeterminado: 24
* -ao / --num_agentes_optimizadores: Determina el número de agentes de tipo optimizador (int) Valor predeterminado: 24
* -it / --num_iteraciones: Determina el número de iteraciones de mercado a simular (int) Valor predeterminado: 1000
* -ppt / --precio_por_tarjeta: Determina el precio inicial de cada tarjeta (float) Valor predeterminado: 200.00
* -b / --balance_inicial: Determina el balance inicial de cada agente (float) Valor predeterminado: 1000.00
* -cp / --cambio_precio: Determina el porcentaje de precio que cambia al vender/comprar tarjetas (float) Valor predeterminado: 0.0005 (5%)


Ejemplo de uso:

python \__\__main\__\__.py -i -ppt 250 -b 2100 -cp 0.0007

Se muestra el informe final, se cambia el precio por tarjeta a 250.00, se cambia el balance inicial a 2100.00, y se cambia la modificación de precio por venta / compra a 7%. El resto de parámetros se inician con su valor predeterminado.



## Consideraciones

Existen distintas posibilidades sobre las implementaciones concretas de las especificaciones del proyecto. 


### Separación de clases

Es importante diseñar un proyecto de manera que cada clase cumpla con una funcionalidad concreta. En un principio se consideró separar la lógica del funcionamiento de los agentes económicos de la lógica del funcionamiento del mercado en dos clases distintas. En última instancia, se ha considerado que esto puede no ser estrictamente necesario, y para reducir la complejidad se han condensado estas dos funcionalidades en la misma clase, GestorMercado.


### Escalabilidad

Es también importante considerar las posibles adiciones o cambios en un futuro que se puedan realizar a un programa, y diseñar el código de antemano en consecuencia. La mayoría de posibles variables del mercado y agentes han sido parametrizadas. Existen posibles cambios adicionales que no están contemplados en el código, pero que podrían ser considerados. Por ejemplo, tener más de un objeto de compra/venta en el mercado, aparte de las tarjetas gráficas, o tener posibilidad de tener cambios de precio distintos de compra y venta (por ejemplo, que al vender una tarjeta disminuya el precio un 0.5%, pero que al comprar aumente un 2%). Otra posibilidad sería contemplar la compra o venta de más de una unidad en cada iteración.


### Política del agente optimizador

La política customizada del agente optimizador es simple, y está sujeta a, probablemente, una notable mejora, quizás por ejemplo añadíendole un componente estocástico. No obstante, obtiene consistentemente resultados decentes, así que se ha considerado dejarla así.


### Eficiencia

Existen numerosas maneras de hacer el funcionamiento del código más rápido y eficiente. Por ejemplo, usar operaciones distintas a la hora de crear y llenar listas o de realizar operaciones matemáticas, o el uso del atributo __slots__ para acelerar el código y disminuir el uso de la memoria. Al ser un funcionamiento relativamente simple y con bajo coste computacional, no obstante, se ha considerado priorizar la simplicidad y legibilidad del código.


### Resultados

Una posibilidad de mejora es mostrar los resultados de una determinada simulación de mercado de manera más extensa y visual, empleando librerias como seaborn o matplotlib. Se ha creado una función para mostrar dos gráficos de líneas, uno para el balance y otro para el inventario de un determinado agente por cada iteración, para un número determinado de iteraciones. No obstamte, se ha considerado que esto añade un grado importante de complejidad al código, restándole legibilidad, tanto en la clase GestorMercado como para la implementación de la parametrización correspondiente. Por tanto, se ha dejado escrito pero comentado.


### Abstracción y Herencia

Se ha considerado que la mejor manera de modelar las clases de los agentes económicos es tener una clase padre que reúna la funcionalidad común de todos los agentes, y herencia de un nivel con subclases para cada uno de los tipos de agente, con su funcionalidad única.


### Encapsulación

Se ha puesto en práctica el principio de encapsulación asegurando que las variables internas de las clases son tratadas como privadas y tienen los correspondientes métodos accesores (getter).


### Testing

Sería deseable también crear un módulo adicional para realizar unit tests al código para comprobar su correcto funcionamiento.


### Errores y excepciones

Podrían añadirse controles de excepciones en puntos críticos del código para garantizar el flujo correcto para el usuario.


