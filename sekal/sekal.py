# -*- coding: utf-8 -*-

import time
from threading import Thread

class Track(object):
    def __init__(self, name, called):
        self.name = name
        self.called = called
        self.steps = {}
        self.tick_period_s = 0

    def __getitem__(self, step_sec):
        step = int(step_sec / self.tick_period_s)
        return self.steps.get(step)

    def __setitem__(self, step_sec, value):
        step = int(step_sec / self.tick_period_s)
        self.steps[step] = value

    def call(self, step):
        if step in self.steps:
            self.called(*self.steps[step][0], **self.steps[step][1])


class Sequencer(object):
    def __init__(self, tick_period_s, time_total_s, auto_reload=False):
        self._tick_period_s = tick_period_s
        self._tracks = []
        self._number_of_ticks = int(time_total_s / (tick_period_s))
        self._auto_reload = auto_reload
        self._running = False

        self._thread = Thread(target=self._run)

    def addTrack(self, track):
        self._tracks.append(track)
        track.tick_period_s = self._tick_period_s

    def start(self):
        self._running = True
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread.isAlive():
            self._thread.join()

    def _run(self):
        while True:
            for tick in range(self._number_of_ticks):
                tn = time.time()
        
                for track in self._tracks:
                    track.call(tick)
        
                wait = (self._tick_period_s) - (time.time() - tn)
                time.sleep(max(wait, 0))

                if not self._running:
                    break

            if not self._auto_reload or not self._running:
                break




