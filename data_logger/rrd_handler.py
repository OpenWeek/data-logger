from time import time
import rrdtool

FOLDER = "storage/"

def generate_database(args):
    name = generate_rrd_name(args)
    now = str(int(time()) - int(args['step']))
    data_sources = []
    for i in args['ds']:
        data_sources.append(str('DS:' + str(i) + ':GAUGE:120:U:U'))
    rra = []
    for i in args['rra']:
        pdp = i['pdp'] // args['step']
        cdp = int(i['duration'] * (60/pdp) )
        rra.append('RRA:' + i['aggregator_function'] + ':0.5:' + str(pdp) + ':' + str(cdp))
    rrdtool.create(name,
                           "--step", str(args['step']),
                           '--start', now,
                            *data_sources,
                            *rra)

def update_rrd(args):
    print(args)
    values = str(args['time'])
    for i in args['value']:
        values += ':' + str(i)
    try:    
        rrdtool.update(generate_rrd_name(args), values )
    except:
        print("Error rrd")
        
def get_data_rrd(args):
    result = rrdtool.fetch( generate_rrd_name(args), "AVERAGE", "-a", "-r", "30", "-s", str(-args['interval']), "-e", "now")
    start, end, step = result[0]
    ds = result[1]
    rows = result[2]
    ret = []
    ts = start + 30
    for i in range(len(rows)-1):
        ret.append({})
        ret[i]['TIMESTAMP'] = ts 
        for j in range( len( rows[i] )):
            ret[i][ds[j]] = rows[i][j]
        ts += step

    print(ret)
    
def generate_rrd_name(args):
    return FOLDER + str(args['client_id']) + ".rrd"
"""
#example
args = {}
args['client_id'] = 'sensor_id2'
args['step'] = 20 #rafraichissement des data
args['ds'] = ['pressure']
args['rra'] = []
rra1 = {}
rra1['aggregator_function'] = 'LAST' # LAST, MIN, MAX, AVERAGE
rra1['pdp'] = 20  # sauvegarder une valeur toute les X secondes ( tjs un multiple de step)
rra1['duration'] = 720 # en heure 30 * 24   (tjs un multiple de step)
args['rra'].append(rra1)

rra2 = {}
rra2['aggregator_function'] = 'AVERAGE' # LAST, MIN, MAX, AVERAGE
rra2['pdp'] = 300  # sauvegarder une valeur toute les X secondes ( tjs un multiple de step)
rra2['duration'] = 8640 # en heure 12 * 30 * 24   (tjs un multiple de step) ( une année)
args['rra'].append(rra2)

rra3 = {}
rra3['aggregator_function'] = 'LAST' # LAST, MIN, MAX, AVERAGE
rra3['pdp'] = 1800  # sauvegarder une valeur toute les X secondes ( tjs un multiple de step)
rra3['duration'] = 43200 # en heure 60 * 12 * 24 * 2   (tjs un multiple de step)
args['rra'].append(rra3)


#generate_database(args)

args2 = {}
args2['time'] = int(time())
args2['value'] = [30, 45, 25]
args2['client_id'] = '1'
args2['project_id'] = '2'

update_rrd(args2)
"""
args3 = {}
args3['client_id'] = 'sensor_id'
args3['interval'] = 360
get_data_rrd(args3)

