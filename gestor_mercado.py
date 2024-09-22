from agentes import Agente, AgenteAleatorio, AgenteTendencial, AgenteAntiTendencial, AgenteOptimizador
import random
from decimal import *
import matplotlib.pyplot as plt


class GestorMercado():
    """
    Clase que administra los agentes económicos (el número de cada tipo de agente), envía y recibe información de estos, 
    controla el precio de las tarjetas y simula cada iteración del mercado

    Args:
        num_agentes_aleatorios (int) - Número de agentes económicos de tipo aleatorio
        num_agentes_tendenciales (int) - Número de agentes económicos de tipo tendencial
        num_agentes_antitendenciales (int) - Número de agentes económicos de tipo antitendencial
        num_agentes_optimizadores (int) - Número de agentes económicos de tipo optimizador
        num_tarjetas (int) - Número máximo de unidades de tarjetas en el mercado
        num_iteraciones (int) - Número de iteraciones a simular
        precio_por_tarjeta, (float) - Precio inicial por cada unidad, sujeto a cambio en cada iteración
        balance_inicial (float) - Balance inicial de cada agente
        cambio_precio (float) - Porcentaje en que cambia el precio de las tarjetas tras cada compra o venta. Expresado en float (e.g. 1% -> 0.01)

    """
     
    def __init__(self, 
                 num_agentes_aleatorios, 
                 num_agentes_tendenciales,
                 num_agentes_antitendenciales, 
                 num_agentes_optimizadores,
                 num_tarjetas,
                 num_iteraciones, 
                 precio_por_tarjeta,
                 balance_inicial, 
                 cambio_precio): 
        
        self.num_agentes_aleatorios = num_agentes_aleatorios
        self.num_agentes_tendenciales = num_agentes_tendenciales
        self.num_agentes_antitendenciales = num_agentes_antitendenciales
        self.num_agentes_optimizadores = num_agentes_optimizadores
        self.balance_inicial = balance_inicial
        self.num_tarjetas = num_tarjetas
        self.tarjetas_libres_restantes = num_tarjetas
        self.num_iteraciones = num_iteraciones
        self.precio_por_tarjeta = precio_por_tarjeta
        self.cambio_precio = cambio_precio
        self.lista_agentes = self.generar_agentes()
            
            
    
    def generar_agentes(self):
        """
        Función que genera todos los agentes de cada tipo, en función de los parámetros pasados en el constructor.

        Returns:
            list: La lista con todos los agentes
        """
        lista = []
        
        for i in range(self.num_agentes_aleatorios):  
            lista.append(AgenteAleatorio(i, self.balance_inicial, "Aleatorio"))
            
        for i in range(self.num_agentes_tendenciales):
            lista.append(AgenteTendencial(i+self.num_agentes_aleatorios, self.balance_inicial, "Tendencial"))
            
        for i in range(self.num_agentes_antitendenciales):
            lista.append(AgenteAntiTendencial(i+self.num_agentes_tendenciales
                                              +self.num_agentes_aleatorios, self.balance_inicial, "Anti-tendencial"))
            
        for i in range(self.num_agentes_optimizadores):       
            lista.append(AgenteOptimizador(i+self.num_agentes_antitendenciales
                                           +self.num_agentes_tendenciales
                                           +self.num_agentes_aleatorios, self.balance_inicial, "Optimizador"))
            
        return lista
    
    def _ordenar_agentes(self):
    # Función que ordena de manera aleatoria los agentes. Llamada en cada iteración.
        random.shuffle(self.lista_agentes)
        return self.lista_agentes
        
    def _modificar_precios(self, listaDecisiones=None):
        # Función para ejecutar las decisiones de todos los agentes en una determinada iteración.
        # Returns: Float: El porcentaje de cambio del precio unitario de las tarjetas

        # 1: vender
        # 2: comprar
        # 3: no hacer nada
        
        delta = 0.0
        
        if (listaDecisiones!=None and len(listaDecisiones) > 0):
            for decision in listaDecisiones:
                # Si el agente decide comprar, se incrementa el precio unitario un 0.5% (o la cantidad de cambio seleccionada)
                if (decision==1):
                    # Si se efectúa correctamente la compra, disminuye el número total de unidades restantes en 1
                    if(self.tarjetas_libres_restantes>0):
                        self.tarjetas_libres_restantes = self.tarjetas_libres_restantes-1
                    delta = delta+self.cambio_precio    
                # Si el agente decide vender, se reduce el precio unitario un 0.5% (o la cantidad de cambio seleccionada)
                elif (decision==2):                  
                    delta = delta-self.cambio_precio
            
        self.precio_por_tarjeta = self.precio_por_tarjeta * (1+delta)
        
        return delta
        
        
    
    def get_precio_por_tarjeta(self):
        """
        Función que devuelve el precio unitario por cada tarjeta.

        Returns:
            float: El precio unitario de cada tarjeta
        """
        return self.precio_por_tarjeta
    

    def _gestionar_operacion_agente(self, agente, precio, delta_precio, iteracion_actual, num_iteraciones, verbose=False):
        # Función que ejecuta la decisión de un determinado agente.
        # Returns: Int: La decisión efectuada por cada agente:
        # 1: vender
        # 2: comprar
        # 3: no hacer nada
        decision = agente.efectuar_operacion(precio=precio, 
                                             delta_precio=delta_precio, 
                                             tarjetas_disponibles=self.tarjetas_libres_restantes>0, 
                                             iteracion_actual=iteracion_actual, 
                                             num_iteraciones=num_iteraciones, 
                                             verbose=verbose)
        return decision
    
    def _gestionar_operaciones_agentes(self, precio, delta_precio, iteracion_actual, num_iteraciones, verbose=False):
        # Función que aplica _gestionar_operacion_agente() a todos los agentes de la lista en una determinada iteración
        # Returns: List: La lista de las decisiones de todos los agentes
        lista_decisiones = []
        for agente in self.lista_agentes:
            decision = self._gestionar_operacion_agente(agente, 
                                                      precio=precio, 
                                                      delta_precio=delta_precio, 
                                                      iteracion_actual=iteracion_actual, 
                                                      num_iteraciones=num_iteraciones, 
                                                      verbose=verbose)
            lista_decisiones.append(decision)
        return lista_decisiones
    
    
    def simular_mercado(self, num_iteraciones, verbose=False):
        """
        Función que simula el mercado. En cada iteración, recoge las decisiones de todos los agentes y, en base a los resultados, modifica el precio unitario de manera acorde.

        Args:
            num_iteraciones (int): El número total de iteraciones en la simulación
            verbose (bool): Mostrar cada operación de cada agente
        """
        
        delta_precio = 0
        
        for i in range(num_iteraciones):
            precio = self.get_precio_por_tarjeta()
            self._ordenar_agentes()
            lista_decisiones = self._gestionar_operaciones_agentes(precio=precio, delta_precio=delta_precio, iteracion_actual=i, num_iteraciones=num_iteraciones, verbose=verbose)
            delta_precio = self._modificar_precios(lista_decisiones)
            

     
    def reporte_final(self):
        """
        Función para emitir un informe final, que muestra el balance final y el inventario final de cada agente, ordenados según su id.

        """         
        print("El precio unitario final es: {:.2f}€".format(self.get_precio_por_tarjeta()))  
        lista_ordenada = sorted(self.lista_agentes, key=lambda agente:agente.get_id_agente())
        for agente in lista_ordenada:
            print("El balance final del agente " + str(agente.get_id_agente()) + " (tipo: " + agente.get_tipo_agente() + ") es: {:.2f}€".format(agente.get_balance()))
            print("El inventario final del agente " + str(agente.get_id_agente()) + " (tipo: " + agente.get_tipo_agente() + ") es: " + str(agente.get_inventario_tarjetas()) + " unidades.")
            print("********************************************************************")
    
    def mostrar_datos_agente_historico(self, id_agente, n_iter):
        """
        Función para mostrar un gráfico del histórico del inventario y del balance de un agente concreto durante un número determinado de iteraciones, por iteración. No está implementada por exceso de complejidad, pero la lógica funciona.

        Args:
            id_agente (int)
            n_iter (int)
        """
        raise NotImplementedError()
        '''
        datos_agente_iteraciones = []
        for iteracion in lista_info_agentes_iteraciones:
            numero_iteracion = iteracion[1]
            datos_agente_iteracion = iteracion[0][id_agente]
            datos_agente_iteraciones.append((datos_agente_iteracion, numero_iteracion))
            
        x_balance = [item[1] for item in datos_agente_iteraciones[:n_iter]]
        y_balance = [item[0][0] for item in datos_agente_iteraciones[:n_iter]]

        fig = plt.figure()
        plt.plot(x_balance, y_balance)
        plt.title("Histórico de balance para agente " + str(id_agente))
        plt.ylabel('Balance')
        plt.xlabel('Nº Iteración')
        
        
        x_inventario = [item[1] for item in datos_agente_iteraciones[:n_iter]]
        y_inventario = [item[0][1] for item in datos_agente_iteraciones[:n_iter]]
        
        fig = plt.figure()
        plt.plot(x_inventario, y_inventario)
        plt.title("Histórico de inventario para agente " + str(id_agente))
        plt.ylabel('Nº unidades en inventario')
        plt.xlabel('Nº Iteración')
        '''
