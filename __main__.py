from gestor_mercado import GestorMercado
from agentes import Agente, AgenteAleatorio, AgenteTendencial, AgenteAntiTendencial, AgenteOptimizador
import sys

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import warnings
warnings.simplefilter("ignore")



def main(args):
    """
    Módulo main. Recibe argumentos desde la consola; si no se especifican mantienen su valor predeterminado. Ejecuta la simulación de mercado del Gestor de Agentes.
    """

    num_agentes_aleatorios = args.num_agentes_aleatorios if  args.num_agentes_aleatorios>0 else 51
    num_agentes_tendenciales = args.num_agentes_tendenciales if  args.num_agentes_tendenciales>0 else 24
    num_agentes_antitendenciales = args.num_agentes_antitendenciales if  args.num_agentes_antitendenciales>0 else 24
    num_agentes_optimizadores = args.num_agentes_optimizadores if  args.num_agentes_optimizadores>0 else 1
    num_tarjetas = args.num_tarjetas if  args.num_tarjetas>0 else 100000
    num_iteraciones = args.num_iteraciones if  args.num_iteraciones>0 else 1000
    precio_por_tarjeta = args.precio_por_tarjeta if  args.precio_por_tarjeta>0.0 else 200.00
    balance_inicial = args.balance_inicial if  args.balance_inicial>0.0 else 1000.00
    cambio_precio = args.cambio_precio 
    #historico_agente_id = args.historico_agente[0] if args.historico_agente!=None else None
    #historico_agente_iteraciones = args.historico_agente[1] if args.historico_agente!=None else None
    informe = args.informe
    verbose = args.verbose


    GM = GestorMercado(num_agentes_aleatorios,
                         num_agentes_tendenciales,
                         num_agentes_antitendenciales,
                         num_agentes_optimizadores,
                         num_tarjetas, 
                         num_iteraciones, 
                         precio_por_tarjeta,
                         balance_inicial,
                         cambio_precio)

    GM.simular_mercado(1000, verbose=verbose)

    if(informe):
        GM.reporte_final()

    #if(historico_agente_id != None):
    #    GM.mostrar_datos_agente_historico(historico_agente_id, historico_agente_iteraciones)


if __name__ == '__main__':

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-aa", 
                        "--num_agentes_aleatorios", 
                        default="51", 
                        type=int,
                        help="Numero de agentes aleatorios")
    parser.add_argument("-at", 
                        "--num_agentes_tendenciales", 
                        default="24", 
                        type=int,
                        help="Numero de agentes tendenciales")
    parser.add_argument("-aat", 
                        "--num_agentes_antitendenciales", 
                        default="24", 
                        type=int,
                        help="Numero de agentes antitendenciales")
    parser.add_argument("-ao", 
                        "--num_agentes_optimizadores", 
                        default="1", 
                        type=int,
                        help="Numero de agentes optimizadores")
    parser.add_argument("-nt", 
                        "--num_tarjetas", 
                        default="100000", 
                        type=int,
                        help="Numero de unidades totales en stock")
    parser.add_argument("-it", 
                        "--num_iteraciones", 
                        default="1000", 
                        type=int,
                        help="Numero de iteraciones a simular")
    parser.add_argument("-ppt", 
                        "--precio_por_tarjeta", 
                        default="200.00", 
                        type=float,
                        help="Precio inicial por unidad")
    parser.add_argument("-b", 
                        "--balance_inicial", 
                        default="1000.00", 
                        type=float,
                        help="Balance inicial por agente")
    parser.add_argument("-cp", 
                        "--cambio_precio", 
                        type=float,
                        default="0.0005", 
                        help="Porcentaje de cambio de precio por unidad tras comprar/vender. Expresado en 'float' (e.g., 1 por ciento es 0.001)")
    #parser.add_argument("-his", 
    #                    "--historico_agente", 
    #                    nargs='+',
    #                    type=int,
    #                    help="Visualizar histórico de inventario y balance de un agente determinado durante un número de iteraciones determinadas")
    parser.add_argument("-i", 
                        "--informe", 
                        action="store_true",
                        help="Mostrar informe final de mercado (balance e inventario de cada agente)")
    parser.add_argument("-v", 
                        "--verbose", 
                        action="store_true",
                        help="Verbosidad; mostrar las operaciones de cada agente en cada iteración")
    
        
    args = parser.parse_args()
    main(args)

