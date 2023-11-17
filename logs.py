import pandas as pd
import sys
import os
cwd = os.getcwd()
sys.path.append(os.path.dirname(os.path.abspath(cwd)))
ruta = cwd + '/logs' + '/'
def to_logs(raw_input, error_log):
    tipo = error_log[-3:]
    if tipo=='csv':
        df = pd.DataFrame([raw_input])
        df.to_csv(ruta + '{}'.format(error_log), mode='a', index=False, 
                   header=not os.path.exists(ruta + '{}'.format(error_log)))
    elif tipo=='txt':
        with open(ruta +  error_log, 'a') as f:
            string = str(raw_input)
            f.write(string + '\n')



