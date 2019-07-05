import time
import rrdtool

def generate_database(args):
    name = args['name']
    now = str(int(time.time()) - int(args['step']))
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


#example
args = {}
args['name'] = 'test.rrd'
args['step'] = 60 #rafraichissement des data
args['ds'] = ['temp','humidity','pressure']
args['rra'] = []
rra1 = {}
rra1['aggregator_function'] = 'LAST' # LAST, MIN, MAX, AVERAGE
rra1['pdp'] = 60  # sauvegarder une valeur toute les X secondes ( tjs un multiple de step)
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


