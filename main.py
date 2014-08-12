#!/usr/bin/env python
import subprocess
import sys
import os
import time
import logging as log
import glob
import signal

from threading import Event, Thread

log.basicConfig(filename='debug.log',
                level=log.DEBUG)

class Main(Thread):
    '''this thread is created to listen to user input'''
    def __init__(self, player, stop, pause, resume):
        self.player = player
        self.stop = stop
        self.pause = pause
        self.resume = resume
        Thread.__init__(self)

    def run(self):
        self.player.start()
        #comment out 2 lines below
        #to play full song
        time.sleep(10)
        self.pause.set()
        time.sleep(5)
        self.pause.clear()
        self.resume.set()
        self.player.join()

class Player(Thread):
    '''player thread'''
    LIBDIR = 'Music' 
    def __init__(self, stop, pause):
        self.lib = os.path.join(os.path.expanduser('~'), self.LIBDIR)
        self.song_list = glob.glob('*.mp3')
        self.stop = stop
        Thread.__init__(self)
    
    def run(self):
        for song in self.song_list:
            log.debug(song)
            if not self.single_replay(self.lib+'/'+song):
                break
    
    def stop(self):
        pass
    
    def pause(self, single):
        single.send_signal(signal.SIGSTOP)

    def single_replay(self, name):
        single = subprocess.Popen('afplay %s' % name, shell=True)
        log.debug(name)
        while single.poll() is None and not self.stop.is_set():
            if self.pause.is_set():
                single.send_signal(signal.SIGSTOP)
                self.resume.wait()
                single.send_signal(signal.SIGCONT)

            time.sleep(0.001)
        if self.stop.is_set():
            single.kill()
            return False
        return True

def main():
    pause = Event()
    stop = Event()
    player = Player(stop, pause)
    control = Main(player, stop, pause)
    control.start()
    control.join()


def daemonize():
    pid = os.fork()    
    if pid > 0:
        os.wait()
        sys.exit(0)
    
    os.setsid()
    pid = os.fork()
    if pid > 0:
        sys.exit(0)
    main()

if __name__ == '__main__':
    daemonize()


