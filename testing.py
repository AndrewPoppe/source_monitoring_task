from pyo import *

serv = Server().boot()
serv.start()
mic = Input().out()

serv.gui(locals())