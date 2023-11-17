import time
from concurrent.futures import ThreadPoolExecutor
from timestamp import timestamp as ts
from main_cantidades import obtener_cantidad
from binance_local import consultas
from binance_local import precision
from binance_local import ordenes
from globales import MARGEN_DE_PERDIDA_ESTANDAR, MARGEN_DE_GANANCIA_ESTANDAR, CALLBACK, TIEMPO
from logs import to_logs
import pandas as pd

MARGEN_DE_PERDIDA = MARGEN_DE_PERDIDA_ESTANDAR
MARGEN_DE_GANANCIA = MARGEN_DE_GANANCIA_ESTANDAR
CALLBACK = CALLBACK
TIEMPO=TIEMPO

class Log_wrapper():
    """
    Clase log, wrapper de to_log pensado para las clases Long
    y Short.
    """
    def __init__(self,par,cantidad): 
        #self.operacion=operacion
        self.par = par
        self.cantidad = cantidad
    def __call__(self,**kwargs):
        if 'sl' in kwargs.keys():
            sl = kwargs['sl']
        else:
            sl=None
        if 'tp' in kwargs.keys():
            tp = kwargs['tp']
        else:
            tp=None

        for k in kwargs.keys():
            if k=='precio_entrada':
                to_logs((str(self.par) + ', ' + str(kwargs[k]) +', ' + 
                         str(self.cantidad) ),
                         'log_precios_de_compra.txt')
            elif k=='compra_market_long': 
                if kwargs[k][0]==1: 
                    to_logs(('LONG' + '->> '+str(self.par) + ', ' +
                             str(self.cantidad) + ', ' + kwargs[k][1]),
                             'log_orden_de_compra.txt') 
                elif kwargs[k][0]==2: 
                    pass #TODO: to be implemented  
                elif kwargs[k][0]==0:
                    to_logs(('LONG' + '->> '+'ERROR ->'+str(self.par) + 
                             ', ' + str(self.cantidad) + ', ' + kwargs[k][1]),
                             'log_orden_de_compra.txt')
            elif k=='compra_market_short': 
                if kwargs[k][0]==1: 
                    to_logs(('SHORT' + '->> '+str(self.par) + ', ' +
                             str(self.cantidad) + ', ' + kwargs[k][1]),
                             'log_ventas_por_tiempo.txt') 
                elif kwargs[k][0]==2: 
                    pass #TODO: to be implemented  
                elif kwargs[k][0]==0:
                    to_logs(('SHORT' + '->> '+'ERROR ->'+str(self.par) + 
                             ', ' + str(self.cantidad) + ', ' + kwargs[k][1]),
                             'log_ventas_por_tiempo.txt')
                elif kwargs[k][0]==3:
                    to_logs(('SHORT->>' + str(self.par) + ',' + kwargs[k][1] +
                             '-->>OVER_RIDE or TOPE'), 'log_ventas_por_tiempo.txt')
            elif k=='compra_sl_short': 
                if kwargs[k][0]==1: 
                    to_logs(('SHORT' + '->> '+str(self.par) + ', ' +
                             str(self.cantidad) + ', ' + 
                             'precio_sl:{}'.format(sl) + ',' + kwargs[k][1]),
                             'log_stop_loss.txt')
                elif kwargs[k][0]==0:
                    to_logs(('SHORT' + '->> '+'ERROR -> '+str(self.par) + ', ' +
                             str(self.cantidad) + ', ' + 
                             'precio_sl:{}'.format(sl) + ',' + kwargs[k][1]),
                             'log_stop_loss.txt')
            elif k=='compra_tp_short': 
                if kwargs[k][0]==1: 
                    to_logs(('SHORT' + '->> '+str(self.par) + ', ' +
                             str(self.cantidad) + ', ' + 
                             'precio_tp:{}'.format(tp) +kwargs[k][1]),
                             'log_take_profit.txt') 
                elif kwargs[k][0]==0: 
                    to_logs(('SHORT' + '->> '+'ERROR -> '+str(self.par) + ', ' +
                             str(self.cantidad) + ', ' + 
                             'precio_tp:{}'.format(tp) +kwargs[k][1]),
                             'log_take_profit.txt') 

            elif k=='venta_market_long':
                if kwargs[k][0]==1:
                    to_logs(('LONG->>' + str(self.par) + ',' + kwargs[k][1]),
                        'log_ventas_por_tiempo.txt')
                elif kwargs[k][0]==0:
                    to_logs(('LONG->>' + 'ERROR->' + str(self.par) + ',' + kwargs[k][1]),
                        'log_ventas_por_tiempo.txt')
                elif kwargs[k][0]==3:
                    to_logs(('LONG->>' + str(self.par) + ',' + kwargs[k][1]
                        + '-->>OVER_RIDE o TOPE'),'log_ventas_por_tiempo.txt')
            elif k=='venta_market_short': 
                if kwargs[k][0]==1: 
                    to_logs(('SHORT' + '->> '+str(self.par) + ', ' +
                             str(self.cantidad) + ', ' + kwargs[k][1]),
                             'log_orden_de_compra.txt') 
                elif kwargs[k][0]==0:
                    to_logs((self.operacion + '->> '+'ERROR ->'+str(self.par) + 
                             ', ' + str(self.cantidad) + ', ' + kwargs[k][1]),
                             'log_orden_de_compra.txt')
            elif k=='venta_sl_long': 
                if kwargs[k][0]==1: 
                    to_logs(('LONG' + '->> '+str(self.par) + ', ' +
                             str(self.cantidad) + ', ' + 
                             'precio_sl:{}'.format(sl) + ',' + kwargs[k][1]),
                             'log_stop_loss.txt')
                elif kwargs[k][0]==0:
                    to_logs(('LONG' + '->> '+'ERROR -> '+str(self.par) + ', ' +
                             str(self.cantidad) + ', ' + 
                             'precio_sl:{}'.format(sl) + ',' + kwargs[k][1]),
                             'log_stop_loss.txt')
            elif k=='venta_tp_long': 
                if kwargs[k][0]==1: 
                    to_logs(('LONG' + '->> '+str(self.par) + ', ' +
                             str(self.cantidad) + ', ' + 
                             'precio_tp:{}'.format(tp) +kwargs[k][1]),
                             'log_take_profit.txt') 
                elif kwargs[k][0]==0: 
                    to_logs(('LONG' + '->> '+'ERROR -> '+str(self.par) + ', ' +
                             str(self.cantidad) + ', ' + 
                             'precio_tp:{}'.format(tp) +kwargs[k][1]),
                             'log_take_profit.txt')

class Time_framework():
    """
    clase para framework temporal. Ejecuta dentro de un marco de tiempo
    ciertas operaciones con multithread en concurrencia.
    """
    def __init__(self,tiempo):
        self.tiempo = tiempo
        self.tasks = []
    def __hold(self,print_time=True):
        time_i = time.time()
        time_f = time.time() - time_i
        while time_f<self.tiempo:
            time_f = time.time() - time_i
            time.sleep(0.01)
            if print_time==True:
                print(time_f, end='\r', flush=True)
        return str(None)

    def add(self,func, **kwargs):
        """
        Agrega a tasks la operacion. 
        """
        self.tasks.append((func,kwargs))  

    def compiler(self):
        workers = len(self.tasks) + 3
        self.tasks_temp = []
        with ThreadPoolExecutor(max_workers=workers) as executor:
            for t in self.tasks:
                self.tasks_temp.append(executor.submit(t[0],**t[1]))
            if self.tiempo!=None:
                self.tasks_temp.append(executor.submit(self.__hold))
        self.tasks=[]
        
    def output(self):
        tasks_temp = []
        long = len(self.tasks_temp)
        if self.tiempo != None:
            for c, i in enumerate(self.tasks_temp):
                if c!=(long-1):
                    tasks_temp.append(i.result())
                else:
                    break
        else:
            for c, i in enumerate(self.tasks_temp):
                tasks_temp.append(i.result())
        self.tasks_temp = []
        return tasks_temp
            
class Par_a_operar():
    def __init__(self,par_a_operar):
        self.par = par_a_operar

class Consulta(Par_a_operar):
    def precio_de_entrada(self):
        intentos=5
        precio = 0
        for i in range(intentos):
            precio = consultas.obtener_precio_de_entrada(self.par)
            if precio == 0:
                continue
            else:
                break      
        return precio, ts()

    def precio_par(self):
        precio_ts = consultas.consultar_precio_ts(self.par)
        precio = precio_ts[0]
        ts = precio_ts[1]#Deberia andar ts() como resultado en return
        return precio, ts

    def cantidad(self):
        cantidad = obtener_cantidad(self.par)
        return cantidad

    def tamanio(self):
        tamanio_posicion = consultas.obtener_tamanio_de_la_pos(self.par)
        return tamanio_posicion

class Comprar(Par_a_operar):
    def market(self,cantidad=None, reducir=None):
        try:
            ordenes.comprar_market(par=self.par,cantidad=cantidad,reducir=reducir)
            output=(1,ts())
        except:
            output=(0,ts())
        return output
    def sl(self,cantidad=None,precio_sl=None, reducir=None):
        try:
            ordenes.comprar_stop_loss(par=self.par, cantidad=cantidad, 
                                      precio_stop=precio_sl,reducir=reducir)
            output=(1,ts())
        except:
            output=(0,ts())
        return output
    def tp(self, cantidad=None,precio_tp=None,reducir=None):
        try:
            ordenes.comprar_take_profit(par=self.par, cantidad=cantidad, 
                                        preciotp=precio_tp,reducir=reducir)
            output=(1,ts())
        except:
            output=(0,ts())
        return output
    def ts(self, cantidad=None, precio_tp=None, callback=None, reducir=None):
        try:
            ordenes.buy_trailing_stop(par=self.par, cantidad=cantidad, 
                                      preciotp=precio_tp, callback=callback,
                                      reducir=reducir)
            output=(1,ts())
        except:
            output=(0,ts())
        return output


class Vender(Par_a_operar):
    def market(self,cantidad=None,reducir=None):
        try:
            ordenes.vender_market(par=self.par,cantidad=cantidad,reducir=reducir)
            output=(1,ts())
        except:
            output=(0,ts())
        return output
    def sl(self,cantidad=None,precio_sl=None,reducir=None):
        try:
            ordenes.vender_stop_loss(par=self.par, cantidad=cantidad, 
                                     precio_stop=precio_sl,reducir=reducir)
            output=(1,ts())
        except:
            output=(0,ts())
        return output
    def tp(self,cantidad=None,precio_tp=None,reducir=None):
        try:
            ordenes.vender_take_profit(par=self.par, cantidad=cantidad, 
                                       preciotp=precio_tp,reducir=reducir)
            output=(1,ts())
        except:
            output=(0,ts())
        return output
    def ts(self, cantidad=None, precio_tp=None, callback=None, reducir=None):
        try:
            ordenes.vender_trailing_stop(par=self.par, cantidad=cantidad, 
                                      preciotp=precio_tp, callback=callback,
                                      reducir=reducir)
            output=(1,ts())
        except:
            output=(0,ts())
        return output



class Long_baseclass(Par_a_operar):
    def __init__(self,par_a_ordenar):
        super().__init__(par_a_ordenar)
        self.consulta_inst = Consulta(self.par)
        self.cantidad = self.consulta_inst.cantidad()
        #self.log_wrapper = Log_wrapper(self.par, self.cantidad)#Sacarlo al final

        time_framework = Time_framework(tiempo=None)
        time_framework.add(Comprar(self.par).market, cantidad=self.cantidad,reducir=False)
        time_framework.add(self.consulta_inst.precio_par)
        time_framework.add(self.consulta_inst.precio_de_entrada)
        time_framework.compiler()
        output = time_framework.output()
        print(output)
        self.compra = output[0]
        self.precio_par = output[1]
        self.precio_entrada_real = output[2]
        if self.precio_entrada_real==0:
            self.precio_entrada = self.precio_par
        else:
            self.precio_entrada = self.precio_entrada_real


    def sl(self,cantidad,margen_de_perdida=MARGEN_DE_PERDIDA):
        decimales = precision.obtener_decimales(self.par)
        sl = f'{self.precio_entrada[0]*(1-margen_de_perdida):.{decimales}f}'
        venta_sl = Vender(self.par).sl(cantidad=cantidad, precio_sl=sl, reducir=True)
        return venta_sl, sl

    def tp(self,cantidad,margen_de_ganancia=MARGEN_DE_GANANCIA):
        decimales = precision.obtener_decimales(self.par)
        pf = f'{self.precio_entrada[0]*(1+margen_de_ganancia):.{decimales}f}'
        venta_tp = Vender(self.par).tp(cantidad=cantidad, precio_tp=pf, reducir=True)
        return venta_tp, pf

    def venta_market(self, cantidad): 
        tamanio = self.consulta_inst.tamanio()
        if tamanio != 0:
            venta_market = Vender(self.par).market(cantidad=cantidad,reducir=True)                    
        else:
            venta_market=(3,ts()) #Fijarse el modo 3 en el log_wrapper
                                  #agregar info de precio venta con get_position?
        return venta_market

    def ts(self, cantidad, margen_de_ganancia=MARGEN_DE_GANANCIA, callback=CALLBACK):
        decimales = precision.obtener_decimales(self.par)
        pf = f'{self.precio_entrada[0]*(1+margen_de_ganancia):.{decimales}f}'
        venta_ts = Vender(self.par).ts(cantidad=cantidad, precio_tp=pf,callback=callback, reducir=False)
        return venta_ts, pf



class Long(Long_baseclass):
    def venta_sl_tp(self,sl=False,tp=False,margen_de_perdida=MARGEN_DE_PERDIDA,margen_de_ganancia=MARGEN_DE_GANANCIA):
        """
        Hace un long vendiendo por sl y/o tp. Si ambos son falsos no vende
        nunca y el long sigue corriendo.
        """
        if sl==True and tp==False:
            venta_sl, sl_precio = self.sl(cantidad=self.cantidad,margen_de_perdida=margen_de_perdida)
            venta_tp, pf_precio = (0,ts()), 0
        if sl==False and tp==True:
            venta_sl, sl_precio = (0,ts()), 0
            venta_tp, pf_precio = self.tp(cantidad=self.cantidad,margen_de_ganancia=margen_de_ganancia)
        if sl==True and tp==True:
            time_framework = Time_framework(tiempo=None)
            time_framework.add(self.sl,cantidad=self.cantidad,margen_de_perdida=margen_de_perdida)
            time_framework.add(self.tp,cantidad=self.cantidad,margen_de_ganancia=margen_de_ganancia)
            time_framework.compiler()
            output = time_framework.output()
            venta_sl, sl_precio = output[0]
            venta_tp, pf_precio = output[1]
        if sl==False and tp==False:
            venta_sl, sl_precio = (0,ts()), 0
            venta_tp, pf_precio = (0,ts()), 0
        return venta_sl, venta_tp, sl_precio, pf_precio

    def venta_por_tiempo(self,tiempo=None):
        """
        Hace un long vendiendo a precio de market dentro de un 
        cierto tiempo.
        """
        def func1(cantidad,tiempo):
            time.sleep(tiempo)
            intentos=5
            for i in range(intentos):
                venta_market=self.venta_market(cantidad=cantidad)
                if venta_market[0]==0:
                    continue
                else:
                    break
            return venta_market
        time_framework = Time_framework(tiempo=tiempo)
        time_framework.add(func1,cantidad=self.cantidad, tiempo=tiempo)
        time_framework.compiler()
        output = time_framework.output()
        return output

    def venta_por_tiempo_con_sl_tp(self,tiempo=None,sl=False,tp=False,
            margen_de_perdida=MARGEN_DE_PERDIDA,margen_de_ganancia=MARGEN_DE_GANANCIA):
        """
        Hace un long vendiendo por sl y/o tp dentro de un plazo de tiempo. 
        Si no se ejecuta ni sl o tp dentro del tiempo establecido, se vende 
        a precio de market al finalizar.
        """
        def func1(cantidad,tiempo):
            time.sleep(tiempo)
            intentos=5
            for i in range(intentos):
                venta_market=self.venta_market(cantidad=cantidad)
                if venta_market[0]==0:
                    continue
                else:
                    break

            return venta_market
        
        time_framework = Time_framework(tiempo=tiempo)
        time_framework.add(self.venta_sl_tp,sl=sl,tp=tp,margen_de_perdida=margen_de_perdida,margen_de_ganancia=margen_de_ganancia)
        time_framework.add(func1,cantidad=self.cantidad, tiempo=tiempo)
        time_framework.compiler()
        output = time_framework.output()
        return output

    def venta_ts(self, margen_de_ganancia=MARGEN_DE_GANANCIA, callback=CALLBACK):
        """
        Hace un long vendiendo por trailing stop. 
        """
        venta_ts, pf_precio = self.ts(cantidad=self.cantidad, margen_de_ganancia=margen_de_ganancia,
                                      callback=callback)
        
        return venta_ts, pf_precio

    def venta_ts_con_sl(self,sl=False, margen_de_ganancia=MARGEN_DE_GANANCIA,
            callback=CALLBACK, margen_de_perdida=MARGEN_DE_PERDIDA):
        """
        Hace un long vendiendo por trailing stop con sl. 
        """
        if sl==True:
            venta_ts, pf_precio = self.ts(cantidad=self.cantidad, margen_de_ganancia=margen_de_ganancia,
                                      callback=callback)
            venta_sl, sl_precio = self.sl(cantidad=self.cantidad,margen_de_perdida=margen_de_perdida)
        else:
            venta_ts, pf_precio = self.ts(cantidad=self.cantidad, margen_de_ganancia=margen_de_ganancia,
                                      callback=callback)
        
        return venta_sl, venta_ts, sl_precio, pf_precio

    def venta_por_tiempo_con_ts(self,tiempo=None, margen_de_ganancia=MARGEN_DE_GANANCIA, callback=CALLBACK):
        """
        Hace un long vendiendo por ts dentro de un plazo de tiempo. 
        Si no se ejecuta el ts dentro del tiempo establecido, se vende 
        a precio de market al finalizar.
        """
        def func1(cantidad,tiempo):
            time.sleep(tiempo)
            intentos=5
            for i in range(intentos):
                venta_market=self.venta_market(cantidad=cantidad)
                if venta_market[0]==0:
                    continue
                else:
                    break

            return venta_market
        
        time_framework = Time_framework(tiempo=tiempo)
        time_framework.add(self.venta_ts,callback=callback,margen_de_ganancia=margen_de_ganancia)
        time_framework.add(func1,cantidad=self.cantidad, tiempo=tiempo)
        time_framework.compiler()
        output = time_framework.output()
        return output


    def custom(self):

        """
        override custom.
        """
        pass

class Short_baseclass(Par_a_operar):
    def __init__(self,par_a_ordenar):
        super().__init__(par_a_ordenar)
        self.consulta_inst = Consulta(self.par)
        self.cantidad = self.consulta_inst.cantidad()
       
        time_framework = Time_framework(tiempo=None)
        time_framework.add(Vender(self.par).market, cantidad=self.cantidad,reducir=False)
        time_framework.add(self.consulta_inst.precio_par)
        time_framework.add(self.consulta_inst.precio_de_entrada)
        time_framework.compiler()
        output = time_framework.output()
        print(output)
        self.venta = output[0]
        self.precio_par = output[1]
        self.precio_entrada_real = output[2]
        if self.precio_entrada_real==0:
            self.precio_entrada = self.precio_par
        else:
            self.precio_entrada = self.precio_entrada_real
#        venta_y_precio = []
#        with ThreadPoolExecutor(max_workers=5) as executor:#TODO:Creo que no va al final
#            venta_y_precio.append(executor.submit(
#                Vender(self.par).market, cantidad=self.cantidad,reducir=False))
#            venta_y_precio.append(executor.submit(
#                self.consulta_inst.precio_de_entrada))
#        self.venta = venta_y_precio[0].result()
#        print('EJECUTO VENTA:',self.venta)
#        self.precio_entrada = venta_y_precio[1].result()

    def sl(self,cantidad,margen_de_perdida=MARGEN_DE_PERDIDA):
        decimales = precision.obtener_decimales(self.par)
        sl = f'{self.precio_entrada[0]*(1+margen_de_perdida):.{decimales}f}'
        compra_sl = Comprar(self.par).sl(cantidad=cantidad, precio_sl=sl, reducir=True)
        return compra_sl, sl

    def tp(self,cantidad,margen_de_ganancia=MARGEN_DE_GANANCIA):
        decimales = precision.obtener_decimales(self.par)
        pf = f'{self.precio_entrada[0]*(1-margen_de_ganancia):.{decimales}f}'
        compra_tp = Comprar(self.par).tp(cantidad=cantidad, precio_tp=pf, reducir=True)
        return compra_tp, pf

    def compra_market(self, cantidad):
        tamanio = self.consulta_inst.tamanio()
        if tamanio != 0:
            compra_market = Comprar(self.par).market(cantidad=cantidad,reducir=True)                    
        else:
            compra_market=(3,ts()) #agregar info de precio venta con get_position?
        return compra_market
    def ts(self, cantidad, margen_de_ganancia=MARGEN_DE_GANANCIA, callback=CALLBACK):
        decimales = precision.obtener_decimales(self.par)
        pf = f'{self.precio_entrada[0]*(1+margen_de_ganancia):.{decimales}f}'
        compra_ts = Comprar(self.par).ts(cantidad=cantidad, precio_tp=pf,callback=callback, reducir=False)
        return compra_ts, pf



class Short(Short_baseclass):
    def compra_sl_tp(self,sl=False,tp=False,margen_de_perdida=MARGEN_DE_PERDIDA,margen_de_ganancia=MARGEN_DE_GANANCIA):
        """
        Hace un short comprando por sl y/o tp. Si ambos son falsos no compra
        nunca y el short sigue corriendo.
        """
        if sl==True and tp==False:
            compra_sl, sl_precio = self.sl(cantidad=self.cantidad,margen_de_perdida=margen_de_perdida)
            compra_tp, pf_precio = (0,ts()), 0
        if sl==False and tp==True:
            compra_sl, sl_precio = (0,ts()), 0
            compra_tp, pf_precio = self.tp(cantidad=self.cantidad,margen_de_ganancia=margen_de_ganancia)
        if sl==True and tp==True:
            #compra_sl_y_tp=[]
            #with ThreadPoolExecutor(max_workers=5) as executor:
            #    compra_sl_y_tp.append(executor.submit(self.sl, cantidad=self.cantidad))
            #    compra_sl_y_tp.append(executor.submit(self.tp, cantidad=self.cantidad))
            #compra_sl, sl_precio = compra_sl_y_tp[0].result()
            #compra_tp, pf_precio = compra_sl_y_tp[1].result()
            time_framework = Time_framework(tiempo=None)
            time_framework.add(self.sl,cantidad=self.cantidad,margen_de_perdida=margen_de_perdida)
            time_framework.add(self.tp,cantidad=self.cantidad,margen_de_ganancia=margen_de_ganancia)
            time_framework.compiler()
            output = time_framework.output()
            compra_sl, sl_precio = output[0]
            compra_tp, pf_precio = output[1]
        if sl==False and tp==False:
            compra_sl, sl_precio = (0,ts()), 0
            compra_tp, pf_precio = (0,ts()), 0
        return compra_sl, compra_tp, sl_precio, pf_precio

    def compra_por_tiempo(self,tiempo=None):
        """
        Hace un short comprando a precio de market dentro de un 
        cierto tiempo.
        """
        def func1(cantidad,tiempo):
            time.sleep(tiempo)
            intentos=5
            for i in range(intentos):
                compra_market=self.compra_market(cantidad=cantidad)
                if compra_market[0]==0:
                    continue
                else:
                    break
            return compra_market
        time_framework = Time_framework(tiempo=tiempo)
        time_framework.add(func1,cantidad=self.cantidad, tiempo=tiempo)
        time_framework.compiler()
        output = time_framework.output()
        return output

    def compra_por_tiempo_con_sl_tp(self,tiempo=None,sl=False,tp=False,
            margen_de_perdida=MARGEN_DE_PERDIDA,margen_de_ganancia=MARGEN_DE_GANANCIA):
        """
        Hace un short comprando por sl y/o tp dentro de un plazo de tiempo. 
        Si no se ejecuta ni sl o tp dentro del tiempo establecido, se compra 
        a precio de market al finalizar.
        """
        def func1(cantidad,tiempo):
            time.sleep(tiempo)
            intentos=5
            for i in range(intentos):
                compra_market=self.compra_market(cantidad=cantidad)
                if compra_market[0]==0:
                    continue
                else:
                    break
            return compra_market
        
        time_framework = Time_framework(tiempo=tiempo)
        time_framework.add(self.compra_sl_tp,sl=sl,tp=tp,margen_de_perdida=margen_de_perdida,
                            margen_de_ganancia=margen_de_ganancia)
        time_framework.add(func1,cantidad=self.cantidad, tiempo=tiempo)
        time_framework.compiler()
        output = time_framework.output()
        return output

    def compra_ts(self, margen_de_ganancia=MARGEN_DE_GANANCIA, callback=CALLBACK):
        """
        Hace un short comprando por trailing stop. 
        """
        compra_ts, pf_precio = self.ts(cantidad=self.cantidad, margen_de_ganancia=margen_de_ganancia,
                                      callback=CALLBACK)
        
        return compra_ts, pf_precio

    def compra_ts_con_sl(self,sl=False, margen_de_ganancia=MARGEN_DE_GANANCIA,
            callback=CALLBACK, margen_de_perdida=MARGEN_DE_PERDIDA):
        """
        Hace un short comprando  por trailing stop con sl. 
        """
        if sl==True:
            compra_ts, pf_precio = self.ts(cantidad=self.cantidad, margen_de_ganancia=margen_de_ganancia,
                                      callback=callback)
            compra_sl, sl_precio = self.sl(cantidad=self.cantidad,margen_de_perdida=margen_de_perdida)
        else:
            compra_ts, pf_precio = self.ts(cantidad=self.cantidad, margen_de_ganancia=margen_de_ganancia,
                                      callback=callback)
        
        return compra_sl, compra_ts, sl_precio, pf_precio

    def compra_por_tiempo_con_ts(self,tiempo=None,
            callback=CALLBACK,margen_de_ganancia=MARGEN_DE_GANANCIA):
        """
        Hace un short comprando por ts dentro de un plazo de tiempo. 
        Si no se ejecuta el ts dentro del tiempo establecido, se compra 
        a precio de market al finalizar.
        """
        def func1(cantidad,tiempo):
            time.sleep(tiempo)
            intentos=5
            for i in range(intentos):
                compra_market=self.compra_market(cantidad=cantidad)
                if compra_market[0]==0:
                    continue
                else:
                    break
            return compra_market
        
        time_framework = Time_framework(tiempo=tiempo)
        time_framework.add(self.compra_ts,callback=callback,
                            margen_de_ganancia=margen_de_ganancia)
        time_framework.add(func1,cantidad=self.cantidad, tiempo=tiempo)
        time_framework.compiler()
        output = time_framework.output()
        return output


    def custom(self):
        """
        override custom.
        """
        pass

class Long_con_Short():
    def __init__(self,par_a_operar):
        self.par = par_a_operar

    def ejecutar_por_precio(self,tiempo_long):
        long = Long(self.par)
        venta_tiempo_sl_tp = long.venta_por_tiempo_con_sl_tp(
                                            tiempo=tiempo_long, sl=False,tp=True)
        short = Short(self.par)
        compra_sl_tp =short.compra_sl_tp(sl=False,tp=True) 
        return long, short, venta_tiempo_sl_tp, compra_sl_tp 

    def ejecutar_por_tiempo(self,tiempo_long,tiempo_short):
        long = Long(self.par)
        venta_tiempo_sl_tp = long.venta_por_tiempo_con_sl_tp(
                                            tiempo=tiempo_long, sl=False,tp=True)
        short = Short(self.par)
        compra_tiempo_sl_tp = short.compra_por_tiempo_con_sl_tp(
                                            tiempo=tiempo_short, sl=False,tp=True)
        return long, short, venta_tiempo_sl_tp, compra_tiempo_sl_tp 
 



def operar_por_tiempo(par_a_operar,tipo_entry):
    if tipo_entry=='LONG':
        #long_por_tiempo(par_a_operar)
        long=Long(par_a_operar)
        venta_por_tiempo = long.venta_por_tiempo(tiempo=TIEMPO)
        print('\n')
        print('COMPRA, PRECIO DE MARKET,PRECIO COMPRA DE ENTRADA:')
        precio_entrada = (long.compra,long.precio_par,long.precio_entrada_real)
        print(precio_entrada)
        print('\n')
        log = Log_wrapper(par_a_operar, long.cantidad)
        log(precio_entrada = precio_entrada, 
            compra_market_long = precio_entrada[0],
            venta_market_long=venta_por_tiempo[0])
    elif tipo_entry=='SHORT':
        short = Short(par_a_operar)
        compra_por_tiempo = short.compra_por_tiempo(tiempo=TIEMPO)
        print('\n')
        print('VENTA, PRECIO DE MARKET,PRECIO VENTA DE ENTRADA:')
        precio_entrada = (short.venta,short.precio_par,short.precio_entrada_real)
        print(precio_entrada)
        print('\n')
        log = Log_wrapper(par_a_operar, short.cantidad)
        log(precio_entrada=precio_entrada,
            venta_market_short = precio_entrada[0],
            compra_market_short=compra_por_tiempo[0])

def operar_por_precio(par_a_operar,tipo_entry,margen_de_perdida=MARGEN_DE_PERDIDA,margen_de_ganancia=MARGEN_DE_GANANCIA):
    if tipo_entry=='LONG':
        #long_por_precio(par_a_operar)
        long=Long(par_a_operar)
        venta_sl_tp = long.venta_sl_tp(sl=True,tp=True,margen_de_perdida=margen_de_perdida,margen_de_ganancia=margen_de_ganancia)
        print('\n')
        print('COMPRA, PRECIO DE MARKET,PRECIO COMPRA DE ENTRADA:')
        precio_entrada = (long.compra,long.precio_par,long.precio_entrada_real)
        print(precio_entrada)
        print('\n')
        log = Log_wrapper(par_a_operar, long.cantidad)
        log(precio_entrada=precio_entrada,
            compra_market_long = precio_entrada[0],
            venta_sl_long=venta_sl_tp[0],sl=venta_sl_tp[2],
            venta_tp_long=venta_sl_tp[1], tp=venta_sl_tp[3])
    elif tipo_entry=='SHORT':
        #short_por_precio(par_a_operar)
        short = Short(par_a_operar)
        compra_sl_tp=short.compra_sl_tp(sl=True,tp=True,margen_de_perdida=margen_de_perdida,margen_de_ganancia=margen_de_ganancia)
        print('\n')
        print('VENTA, PRECIO DE MARKET,PRECIO VENTA DE ENTRADA:')
        precio_entrada = (short.venta,short.precio_par,short.precio_entrada_real)
        print(precio_entrada)
        print('\n')
        log = Log_wrapper(par_a_operar, short.cantidad)
        log(precio_entrada=precio_entrada,
            venta_market_short = precio_entrada[0],
            compra_sl_short=compra_sl_tp[0], sl=compra_sl_tp[2],
            compra_tp_short=compra_sl_tp[1], tp=compra_sl_tp[3])

def operar_por_tiempo_con_tope(par_a_operar,tipo_entry,margen_de_perdida=MARGEN_DE_PERDIDA,margen_de_ganancia=MARGEN_DE_GANANCIA):
    if tipo_entry=='LONG':
        #long_por_tiempo_con_tope(par_a_operar)
        long=Long(par_a_operar)
        venta_tiempo_sl_tp=long.venta_por_tiempo_con_sl_tp(tiempo=TIEMPO,sl=False,tp=True,margen_de_perdida=margen_de_perdida,margen_de_ganancia=margen_de_ganancia)
        print('\n')
        print('COMPRA, PRECIO DE MARKET,PRECIO COMPRA DE ENTRADA:')
        precio_entrada = (long.compra,long.precio_par,long.precio_entrada_real)
        print(precio_entrada)
        print('\n')
        log = Log_wrapper(par_a_operar, long.cantidad)
        log(precio_entrada=precio_entrada,
            compra_market_long = precio_entrada[0],
            venta_sl_long=venta_tiempo_sl_tp[0][0],sl=venta_tiempo_sl_tp[0][2],
            venta_tp_long=venta_tiempo_sl_tp[0][1], tp=venta_tiempo_sl_tp[0][3],
            venta_market_long=venta_tiempo_sl_tp[1])
    elif tipo_entry=='SHORT':
        #short_por_tiempo_con_tope(par_a_operar)
        short = Short(par_a_operar)
        compra_tiempo_sl_tp = short.compra_por_tiempo_con_sl_tp(tiempo=TIEMPO,sl=False,tp=True,margen_de_perdida=margen_de_perdida,margen_de_ganancia=margen_de_ganancia)
        print('\n')
        print('VENTA, PRECIO DE MARKET,PRECIO VENTA DE ENTRADA:')
        precio_entrada = (short.venta,short.precio_par,short.precio_entrada_real)
        print(precio_entrada)
        print('\n')
        log = Log_wrapper(par_a_operar, short.cantidad)
        log(precio_entrada=precio_entrada,
            venta_market_short = precio_entrada[0],
            compra_sl_short=compra_tiempo_sl_tp[0][0], sl=compra_tiempo_sl_tp[0][2],
            compra_tp_short=compra_tiempo_sl_tp[0][1], tp=compra_tiempo_sl_tp[0][3],
            compra_market_short=compra_tiempo_sl_tp[1])

def operar_por_tiempo_con_sl_y_tope(par_a_operar,tipo_entry,margen_de_perdida=MARGEN_DE_PERDIDA,margen_de_ganancia=MARGEN_DE_GANANCIA):
    if tipo_entry=='LONG':
        #long_por_tiempo_con_tope(par_a_operar)
        long=Long(par_a_operar)
        venta_tiempo_sl_tp=long.venta_por_tiempo_con_sl_tp(tiempo=TIEMPO,sl=True,tp=True,margen_de_perdida=margen_de_perdida,margen_de_ganancia=margen_de_ganancia)
        print('\n')
        print('COMPRA, PRECIO DE MARKET,PRECIO COMPRA DE ENTRADA:')
        precio_entrada = (long.compra,long.precio_par,long.precio_entrada_real)
        print(precio_entrada)
        print('\n')
        log = Log_wrapper(par_a_operar, long.cantidad)
        print(precio_entrada,
             precio_entrada[0],
            venta_tiempo_sl_tp[0][0],venta_tiempo_sl_tp[0][2],
            venta_tiempo_sl_tp[0][1], venta_tiempo_sl_tp[0][3],
            venta_tiempo_sl_tp[1])
        log(precio_entrada=precio_entrada,
            compra_market_long = precio_entrada[0],
            venta_sl_long=venta_tiempo_sl_tp[0][0],sl=venta_tiempo_sl_tp[0][2],
            venta_tp_long=venta_tiempo_sl_tp[0][1], tp=venta_tiempo_sl_tp[0][3],
            venta_market_long=venta_tiempo_sl_tp[1])
    elif tipo_entry=='SHORT':
        #short_por_tiempo_con_tope(par_a_operar)
        short = Short(par_a_operar)
        compra_tiempo_sl_tp = short.compra_por_tiempo_con_sl_tp(tiempo=TIEMPO,sl=True,tp=True,margen_de_perdida=margen_de_perdida,margen_de_ganancia=margen_de_ganancia)
        print('\n')
        print('VENTA, PRECIO DE MARKET,PRECIO VENTA DE ENTRADA:')
        precio_entrada = (short.venta,short.precio_par,short.precio_entrada_real)
        print(precio_entrada)
        print('\n')
        log = Log_wrapper(par_a_operar, short.cantidad)
        log(precio_entrada=precio_entrada,
            venta_market_short = precio_entrada[0],
            compra_sl_short=compra_tiempo_sl_tp[0][0], sl=compra_tiempo_sl_tp[0][2],
            compra_tp_short=compra_tiempo_sl_tp[0][1], tp=compra_tiempo_sl_tp[0][3],
            compra_market_short=compra_tiempo_sl_tp[1])

def operar_long_con_short_por_precio(par_a_operar,tipo_entry):
    if tipo_entry=='LONG':
        long_con_short = Long_con_Short(par_a_operar)
        long, short, venta_tiempo_sl_tp, compra_sl_tp = long_con_short.ejecutar_por_precio(
                                                                            tiempo_long=60)

        print('\n')
        print('COMPRA, PRECIO DE MARKET,PRECIO COMPRA DE ENTRADA:')
        precio_entrada = (long.compra,
                          long.precio_par,
                          long.precio_entrada_real)
        print(precio_entrada)
        print('\n')
        log = Log_wrapper(par_a_operar, long.cantidad)
        log(precio_entrada=precio_entrada,
            compra_market_long = precio_entrada[0],
            venta_sl_long=venta_tiempo_sl_tp[0][0],sl=venta_tiempo_sl_tp[0][2],
            venta_tp_long=venta_tiempo_sl_tp[0][1], tp=venta_tiempo_sl_tp[0][3],
            venta_market_long=venta_tiempo_sl_tp[1])
        print('\n')
        print('VENTA, PRECIO DE MARKET,PRECIO VENTA DE ENTRADA:')
        precio_entrada = (short.venta,short.precio_par,short.precio_entrada_real)
        print(precio_entrada)
        print('\n')
        log = Log_wrapper(par_a_operar, short.cantidad)
        log(precio_entrada=precio_entrada,
            venta_market_short = precio_entrada[0],
            compra_sl_short=compra_sl_tp[0], sl=compra_sl_tp[2],
            compra_tp_short=compra_sl_tp[1], tp=compra_sl_tp[3])

def operar_long_con_short_por_tiempo(par_a_operar,tipo_entry):
    if tipo_entry=='LONG':
        long_con_short = Long_con_Short(par_a_operar)
        (long, short, venta_tiempo_sl_tp, 
                compra_tiempo_sl_tp) = long_con_short.ejecutar_por_tiempo(
                                                    tiempo_long=60,tiempo_short=180)

        print('\n')
        print('COMPRA, PRECIO DE MARKET,PRECIO COMPRA DE ENTRADA:')
        precio_entrada = (long.compra,
                          long.precio_par,
                          long.precio_entrada_real)
        print(precio_entrada)
        print('\n')
        log = Log_wrapper(par_a_operar, long.cantidad)
        log(precio_entrada=precio_entrada,
            compra_market_long = precio_entrada[0],
            venta_sl_long=venta_tiempo_sl_tp[0][0],sl=venta_tiempo_sl_tp[0][2],
            venta_tp_long=venta_tiempo_sl_tp[0][1], tp=venta_tiempo_sl_tp[0][3],
            venta_market_long=venta_tiempo_sl_tp[1])
        print('\n')
        print('VENTA, PRECIO DE MARKET,PRECIO VENTA DE ENTRADA:')
        precio_entrada = (short.venta,short.precio_par,short.precio_entrada_real)
        print(precio_entrada)
        print('\n')
        log = Log_wrapper(par_a_operar, short.cantidad)
        log(precio_entrada=precio_entrada,
            venta_market_short = precio_entrada[0],
            compra_sl_short=compra_tiempo_sl_tp[0][0], sl=compra_tiempo_sl_tp[0][2],
            compra_tp_short=compra_tiempo_sl_tp[0][1], tp=compra_tiempo_sl_tp[0][3],
            compra_market_short=compra_tiempo_sl_tp[1])

def operar_por_ts(par_a_operar,tipo_entry,margen_de_ganancia=MARGEN_DE_GANANCIA,callback=CALLBACK):
    if tipo_entry=='LONG':
        #long_por_precio(par_a_operar)
        long=Long(par_a_operar)
        venta_ts = long.venta_ts(callback=callback,margen_de_ganancia=margen_de_ganancia)
        print('\n')
        print('COMPRA, PRECIO DE MARKET,PRECIO COMPRA DE ENTRADA:')
        precio_entrada = (long.compra,long.precio_par,long.precio_entrada_real)
        print(precio_entrada)
        print('\n')
        #TODO: implemetar log para ts
        #log = Log_wrapper(par_a_operar, long.cantidad)
        #log(precio_entrada=precio_entrada,
        #    compra_market_long = precio_entrada[0],
        #    venta_sl_long=venta_sl_tp[0],sl=venta_sl_tp[2],
        #    venta_tp_long=venta_sl_tp[1], tp=venta_sl_tp[3])
    elif tipo_entry=='SHORT':
        #short_por_precio(par_a_operar)
        short = Short(par_a_operar)
        compra_ts=short.compra_ts(callback=callback,margen_de_ganancia=margen_de_ganancia)
        print('\n')
        print('VENTA, PRECIO DE MARKET,PRECIO VENTA DE ENTRADA:')
        precio_entrada = (short.venta,short.precio_par,short.precio_entrada_real)
        print(precio_entrada)
        print('\n')
        #TODO:Implementar log de ts
        #log = Log_wrapper(par_a_operar, short.cantidad)
        #log(precio_entrada=precio_entrada,
        #    venta_market_short = precio_entrada[0],
        #    compra_sl_short=compra_sl_tp[0], sl=compra_sl_tp[2],
        #    compra_tp_short=compra_sl_tp[1], tp=compra_sl_tp[3])


def operar_por_ts_con_sl(par_a_operar,tipo_entry,margen_de_ganancia=MARGEN_DE_GANANCIA,
        callback=CALLBACK, margen_de_perdida=MARGEN_DE_PERDIDA):
    if tipo_entry=='LONG':
        #long_por_precio(par_a_operar)
        long=Long(par_a_operar)
        venta_ts_con_sl = long.venta_ts_con_sl(sl=True, callback=callback,
                margen_de_ganancia=margen_de_ganancia, margen_de_perdida=margen_de_perdida)
        print('\n')
        print('COMPRA, PRECIO DE MARKET,PRECIO COMPRA DE ENTRADA:')
        precio_entrada = (long.compra,long.precio_par,long.precio_entrada_real)
        print(precio_entrada)
        print('\n')
        #TODO: implemetar log para ts
        #log = Log_wrapper(par_a_operar, long.cantidad)
        #log(precio_entrada=precio_entrada,
        #    compra_market_long = precio_entrada[0],
        #    venta_sl_long=venta_sl_tp[0],sl=venta_sl_tp[2],
        #    venta_tp_long=venta_sl_tp[1], tp=venta_sl_tp[3])
    elif tipo_entry=='SHORT':
        #short_por_precio(par_a_operar)
        short = Short(par_a_operar)
        compra_ts_con_sl=short.compra_ts_con_sl(sl=True, callback=callback,
                margen_de_ganancia=margen_de_ganancia, margen_de_perdida=margen_de_perdida)
        print('\n')
        print('VENTA, PRECIO DE MARKET,PRECIO VENTA DE ENTRADA:')
        precio_entrada = (short.venta,short.precio_par,short.precio_entrada_real)
        print(precio_entrada)
        print('\n')
        #TODO:Implementar log de ts
        #log = Log_wrapper(par_a_operar, short.cantidad)
        #log(precio_entrada=precio_entrada,
        #    venta_market_short = precio_entrada[0],
        #    compra_sl_short=compra_sl_tp[0], sl=compra_sl_tp[2],
        #    compra_tp_short=compra_sl_tp[1], tp=compra_sl_tp[3])


def operar_por_tiempo_con_ts(par_a_operar,tipo_entry,callback=CALLBACK,margen_de_ganancia=MARGEN_DE_GANANCIA):
    if tipo_entry=='LONG':
        #long_por_tiempo_con_tope(par_a_operar)
        long=Long(par_a_operar)
        venta_tiempo_ts=long.venta_por_tiempo_con_ts(tiempo=TIEMPO,
                        callback=callback,margen_de_ganancia=margen_de_ganancia)
        print('\n')
        print('COMPRA, PRECIO DE MARKET,PRECIO COMPRA DE ENTRADA:')
        precio_entrada = (long.compra,long.precio_par,long.precio_entrada_real)
        print(precio_entrada)
        print('\n')
        #TODO:Implementar log de ts
        #log = Log_wrapper(par_a_operar, long.cantidad)
        #log(precio_entrada=precio_entrada,
        #    compra_market_long = precio_entrada[0],
        #    venta_sl_long=venta_tiempo_sl_tp[0][0],sl=venta_tiempo_sl_tp[0][2],
        #    venta_tp_long=venta_tiempo_sl_tp[0][1], tp=venta_tiempo_sl_tp[0][3],
        #    venta_market_long=venta_tiempo_sl_tp[1])
    elif tipo_entry=='SHORT':
        #short_por_tiempo_con_tope(par_a_operar)
        short = Short(par_a_operar)
        compra_tiempo_ts = short.compra_por_tiempo_con_ts(tiempo=TIEMPO,
                           callback=callback,margen_de_ganancia=margen_de_ganancia)
        print('\n')
        print('VENTA, PRECIO DE MARKET,PRECIO VENTA DE ENTRADA:')
        precio_entrada = (short.venta,short.precio_par,short.precio_entrada_real)
        print(precio_entrada)
        print('\n')
        #TODO:Implementar log de ts
        #log = Log_wrapper(par_a_operar, short.cantidad)
        #log(precio_entrada=precio_entrada,
        #    venta_market_short = precio_entrada[0],
        #    compra_sl_short=compra_tiempo_sl_tp[0][0], sl=compra_tiempo_sl_tp[0][2],
        #    compra_tp_short=compra_tiempo_sl_tp[0][1], tp=compra_tiempo_sl_tp[0][3],
        #    compra_market_short=compra_tiempo_sl_tp[1])






def operar(par_a_operar=None,tipo_entry=None,operacion=None,
           margen_de_perdida=MARGEN_DE_PERDIDA,margen_de_ganancia=MARGEN_DE_GANANCIA, callback=CALLBACK):
    if operacion == 'tiempo':
        operar_por_tiempo(par_a_operar, tipo_entry)
    elif operacion=='precio':
        operar_por_precio(par_a_operar, tipo_entry,margen_de_perdida=margen_de_perdida,margen_de_ganancia=margen_de_ganancia)
    elif operacion== 'tiempo_con_tope':
        operar_por_tiempo_con_tope(par_a_operar, tipo_entry,margen_de_perdida=margen_de_perdida,margen_de_ganancia=margen_de_ganancia)
    elif operacion== 'tiempo_con_sl_y_tope':
        operar_por_tiempo_con_sl_y_tope(par_a_operar, tipo_entry,margen_de_perdida=margen_de_perdida,margen_de_ganancia=margen_de_ganancia)
    elif operacion== 'long_con_short_por_precio':
        operar_long_con_short_por_precio(par_a_operar, tipo_entry)
    elif operacion== 'long_con_short_por_tiempo':
        operar_long_con_short_por_tiempo(par_a_operar, tipo_entry)
    elif operacion == 'ts':
        operar_por_ts(par_a_operar, tipo_entry, margen_de_ganancia=margen_de_ganancia, callback=callback)
    elif operacion == 'ts_con_sl':
        operar_por_ts_con_sl(par_a_operar, tipo_entry, margen_de_ganancia=margen_de_ganancia, callback=callback, margen_de_perdida=margen_de_perdida)
    elif operacion == 'tiempo_con_ts':
        operar_por_tiempo_con_ts(par_a_operar, tipo_entry,margen_de_ganancia=margen_de_ganancia, callback=callback)


















