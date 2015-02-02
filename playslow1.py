from pyo import *
import math, sys

s = Server().boot()
s.start()

def slow(playback_speed):
    dur = 2
    if playback_speed == 0:
        playback_speed = pow(10,-100)
    i = Input()

    def start():
        print "start!"
        rec.play()
        a.play().out()
        tf.stop()

    def stop():
        print "stop!"
        a.stop()
        a.reset()
        tf.play()

    tab = NewTable(dur, chnls=2)
    transpo_to_normal = math.log(1.0 / playback_speed, 2) * 12
    j = Harmonizer(i, transpo=transpo_to_normal)
    k = Gate(j, thresh=-70, falltime=0.02, lookahead=20.0).mix(2)
    rec = TableRec(k, tab)
    a = TableRead(table=tab, freq=playback_speed/dur).stop()
    env = Follower(i)
    th = Thresh(env, .2)
    tf = TrigFunc(th, start)
    tr = TrigFunc(rec['trig'], stop)