
import random

class Agente():
    """
    Clase que recoge el funcionamiento de un determinado agente económico.

    Args:
        _id_agente (int) - Id única de cada agente
        _balance (float) - Balance de cada agente, sujeto a cambios cada iteración
        _inventario_tarjetas (int) - El número de tarjetas en posesión de cada agente, sujeto a cambios con cada iteración

    """
    
    def __init__(self, _id_agente, _balance, _tipo_agente):
        self._id_agente = _id_agente
        self._balance = _balance 
        self._tipo_agente = _tipo_agente
        self._inventario_tarjetas = 0
        
    def _comprar(self, precio, tarjetas_disponibles=True, verbose=False):
        # Función para comprar una tarjeta en una determinada iteración.
        # Args:
        #   precio (float): El precio por tarjeta en una determinada iteración
        #   tarjetas_disponibles (bool): Determina si quedan tarjetas disponibles en stock
        #   verbose (bool): Determina si se muestra información de la operación
        # Returns (int): La decisión del agente (comprar=1)

        # Si no quedan tarjetas, el agente no hace nada
        if(tarjetas_disponibles==False):
            if(verbose):
                print("No quedan tarjetas disponibles para comprar, así que " + str(self._id_agente) + " no hace nada.")
            return self._skip()

        # Si el agente tiene suficiente dinero para comprar una tarjeta, se efectúa la operación
        if (self._balance >= precio):
            self._inventario_tarjetas = self._inventario_tarjetas+1
            self._balance = self._balance - precio

            if(verbose):
                print("Agente " + str(self._id_agente) + " ha decidido comprar")
            return 1
        # En caso contrario, el agente no hace nada
        else:
            if(verbose):
                print("Como agente " + str(self._id_agente) + " no tiene suficiente balance para comprar, ha decidido no hacer nada")
            return self._skip()
        
        
    def _vender(self, precio, verbose=False):
        # Función para vender una tarjeta en una determinada iteración.
        # Args:
        #   precio (float): El precio por tarjeta en una determinada iteración
        #   verbose (bool): Determina si se muestra información de la operación
        # Returns (int): La decisión del agente (vender=2)

        # Si el agente tiene al menos una tarjeta, se efectúa la operación
        if(self._inventario_tarjetas>0):
            self._inventario_tarjetas = self._inventario_tarjetas-1
            self._balance = self._balance + precio
            if(verbose):
                print("Agente " + str(self._id_agente) + " ha decidido vender")
            return 2
        # En caso contrario, el agente no hace nada
        else:
            if(verbose):
                print("Como agente " + str(self._id_agente) + " no tiene suficiente inventario para vender, ha decidido no hacer nada")
            return self._skip()
            
    def _skip(self, verbose=False):
        # Función para no comprar ni vender en una determinada iteración
        # Returns (int): La decisión del agente (no hacer nada=3)
        if(verbose):
            print("Agente " + str(self._id_agente) + " ha decidido no comprar ni vender")
        return 3

    
    def get_balance(self):
        """
        Función para obtener el balance en la presente iteración del agente
        Returns (float): El balance actual
        """
        return self._balance

    
    def get_inventario_tarjetas(self):
        """
        Función para obtener el inventario en la presente iteración del agente
        Returns (int): El inventario actual
        """
        return self._inventario_tarjetas

    
    def get_id_agente(self):
        """
        Función para obtener la id única del agente
        Returns (int): La id del agente
        """
        return self._id_agente
    
    def get_tipo_agente(self):
        """
        Función para obtener el tipo del agente (aleatorio, tendencial, antitendencial u optimizador)
        Returns (str): 
        """
        return self._tipo_agente

    
    def efectuar_operacion(self, precio, delta_precio=None, tarjetas_disponibles=True, iteracion_actual=0, num_iteraciones=1000, verbose=False):
        """
        Función para efectuar una determinada operación. En el caso de las clases hijo, aquí se encuentra la lógica de la determinada política a emplear
        Args:
            precio (float): El precio de cada tarjeta en una determinada iteración
            delta_precio (float): El cambio de precio unitario respecto a la iteración anterior
            tarjetas_disponibles (bool): Determina si quedan tarjetas en stock
            iteracion_actual (int): Número de la presente iteración
            num_iteraciones (int): Número máximo de iteraciones
            verbose (bool): Determina si se muestra información de la operación

        Returns (int): La decisión efectuada (1=comprar, 2=vender, 3=no hacer nada)
        """  
        raise NotImplementedError()


class AgenteAleatorio(Agente):
    """
    Clase que rige el comportamiento de los agentes de tipo aleatorio.
    Hereda de: Agente
    Args:
        _id_agente (int) - Id única de cada agente
        _balance (float) - Balance de cada agente, sujeto a cambios cada iteración
        _inventario_tarjetas (int) - El número de tarjetas en posesión de cada agente, sujeto a cambios con cada iteración
    """
    
    def efectuar_operacion(self, precio, delta_precio=None, tarjetas_disponibles=True, iteracion_actual=0, num_iteraciones=1000, verbose=False):
        """
        Función para efectuar una determinada operación. 
        Funcionalidad adicional: El agente aleatorio tiene 1/3 de probabilides de vender, 1/3 de probabilidades de comprar, y 1/3 de probabilidades de no hacer nada, independientemente del cambio de precio
        Args:
            precio (float): El precio de cada tarjeta en una determinada iteración
            delta_precio (float): El cambio de precio unitario respecto a la iteración anterior
            tarjetas_disponibles (bool): Determina si quedan tarjetas en stock
            iteracion_actual (int): Número de la presente iteración
            num_iteraciones (int): Número máximo de iteraciones
            verbose (bool): Determina si se muestra información de la operación

        Returns (int): La decisión efectuada (1=comprar, 2=vender, 3=no hacer nada)
        """  
    
        decision = random.randint(1, 3)
        if (decision==1):
                return self._comprar(precio,  tarjetas_disponibles, verbose)
        elif (decision==2):       
            return self._vender(precio, verbose)
        elif (decision==3):
            return self._skip(verbose)


class AgenteTendencial(Agente):
    """
    Clase que rige el comportamiento de los agentes de tipo tendencial.
    Hereda de: Agente
    Args:
        _id_agente (int) - Id única de cada agente
        _balance (float) - Balance de cada agente, sujeto a cambios cada iteración
        _inventario_tarjetas (int) - El número de tarjetas en posesión de cada agente, sujeto a cambios con cada iteración
    """
    
    def efectuar_operacion(self, precio, delta_precio=None, tarjetas_disponibles=True, iteracion_actual=0, num_iteraciones=1000, verbose=False):
        """
        Función para efectuar una determinada operación. 
        Funcionalidad adicional: El agente tendencial tiene tienen un 75% de probabilidades de comprar y un 25% de probabilidades de no hacer nada si el precio ha subido un 1% (o más) con respecto al final de la iteración anterior.
        En caso contrario tienen un 20% de probabilidades de vender y un 80% de probabilidades de no hacer nada.
        Args:
            precio (float): El precio de cada tarjeta en una determinada iteración
            delta_precio (float): El cambio de precio unitario respecto a la iteración anterior
            tarjetas_disponibles (bool): Determina si quedan tarjetas en stock
            iteracion_actual (int): Número de la presente iteración
            num_iteraciones (int): Número máximo de iteraciones
            verbose (bool): Determina si se muestra información de la operación

        Returns (int): La decisión efectuada (1=comprar, 2=vender, 3=no hacer nada)
        """ 
        decision = random.randrange(1, 100)
        #print(delta_precio) # DEBUG
        if (delta_precio >= 0.0001):
            if (decision>25):
                return self._comprar(precio, tarjetas_disponibles, verbose)
            else:
                return self._skip(verbose)
        else:
            if (decision>20):
                return self._skip(verbose)
            else:
                return self._vender(precio, verbose)


class AgenteAntiTendencial(Agente):
    """
    Clase que rige el comportamiento de los agentes de tipo antitendencial.
    Hereda de: Agente
    Args:
        _id_agente (int) - Id única de cada agente
        _balance (float) - Balance de cada agente, sujeto a cambios cada iteración
        _inventario_tarjetas (int) - El número de tarjetas en posesión de cada agente, sujeto a cambios con cada iteración
    """
    
    def efectuar_operacion(self, precio, delta_precio=None, tarjetas_disponibles=True, iteracion_actual=0, num_iteraciones=1000, verbose=False):
        """
        Función para efectuar una determinada operación. 
        Funcionalidad adicional: El agente antitendencial tiene tienen un 75% de probabilidades de comprar y un 25% de probabilidades de no hacer nada si el precio ha disminuido un 1% (o más) con respecto al final de la iteración anterior.
        En caso contrario tienen un 20% de probabilidades de vender y un 80% de probabilidades de no hacer nada.
        Args:
            precio (float): El precio de cada tarjeta en una determinada iteración
            delta_precio (float): El cambio de precio unitario respecto a la iteración anterior
            tarjetas_disponibles (bool): Determina si quedan tarjetas en stock
            iteracion_actual (int): Número de la presente iteración
            num_iteraciones (int): Número máximo de iteraciones
            verbose (bool): Determina si se muestra información de la operación

        Returns (int): La decisión efectuada (1=comprar, 2=vender, 3=no hacer nada)
        """ 
        decision = random.randrange(1, 100)
        if (delta_precio <= -0.0001):
            if (decision>25):
                return self._comprar(precio, tarjetas_disponibles, verbose)
            else:
                return self._skip(verbose)
        else:
            if (decision>20):
                return self._skip(verbose)
            else:
                return self._vender(precio, verbose)
                

class AgenteOptimizador(Agente):
    """
    Clase que rige el comportamiento de los agentes de tipo optimizador.
    Hereda de: Agente
    Args:
        _id_agente (int) - Id única de cada agente
        _balance (float) - Balance de cada agente, sujeto a cambios cada iteración
        _inventario_tarjetas (int) - El número de tarjetas en posesión de cada agente, sujeto a cambios con cada iteración
    """
    
    def efectuar_operacion(self, precio, delta_precio=None, tarjetas_disponibles=True, iteracion_actual=0, num_iteraciones=1000, verbose=False):
        """
        Función para efectuar una determinada operación. 
        Funcionalidad adicional: El agente optimizador tiene una fórmula customizada. Dado que su objetivo es maximizar su balance final y quedarse con 0 tarjetas en la última iteración, está reflejado en su política.
        Si el precio ha aumentado 1% o más en la iteración anterior, el agente vende. Si el precio ha disminuido un 1% o más en la iteración anterior, el agente compra. En caso contrario, el agente vende.
        Args:
            precio (float): El precio de cada tarjeta en una determinada iteración
            delta_precio (float): El cambio de precio unitario respecto a la iteración anterior
            tarjetas_disponibles (bool): Determina si quedan tarjetas en stock
            iteracion_actual (int): Número de la presente iteración
            num_iteraciones (int): Número máximo de iteraciones
            verbose (bool): Determina si se muestra información de la operación

        Returns (int): La decisión efectuada (1=comprar, 2=vender, 3=no hacer nada)
        """ 
        decision = random.randrange(1, 100)
        
        #verbose=True # DEBUG

        # Si el número de tarjetas restantes en el inventario es igual o mayor (no debería nunca ser mayor) que el número de iteraciones restantes, la única política es vender, para quedarse con 0 unidades
        if (self._inventario_tarjetas >= (num_iteraciones-1-iteracion_actual)):
            return self._vender(precio, verbose)

        if (delta_precio >= 0.0001):
            return self._vender(precio, verbose)
        elif (delta_precio <= -0.0001):
            return self._comprar(precio, tarjetas_disponibles, verbose)
        else:
            if (self._inventario_tarjetas >= 1):
                return self._vender(precio, verbose)
            return self._skip(verbose)




