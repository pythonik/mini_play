#!/usr/bin/env python
import subprocess
import sys
import os
import time
import logging as log
import glob
import signal

from threading import Event, Thread

formatter = log.Formatter('%(asctime)s %(levelname)s %(message)s')

app_log = log.getLogger('app')
app_log.setLevel(log.DEBUG)
hdlr_app = log.FileHandler('debug.log')
hdlr_app.setFormatter(formatter)
app_log.addHandler(hdlr_app)

player_log = log.getLogger('app')
player_log.setLevel(log.DEBUG)
hdlr_player = log.FileHandler('player.log')
hdlr_player.setFormatter(formatter)
player_log.addHandler(hdlr_player)


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
    def __init__(self, stop, pause, resume):
        self.lib = os.path.join(os.path.expanduser('~'), self.LIBDIR)
        os.chdir(self.lib)
        self.song_list = glob.glob('*.mp3')
        self.stop = stop
        self.pause = pause
        self.resume = resume
        Thread.__init__(self)
    
    def run(self):
        app_log.info('player..')
        for song in self.song_list:
            app_log.debug(song)
            if not self.single_replay(self.lib+'/'+song):
                break
        app_log.info(self.song_list)
    
    def stop(self):
        pass
    
    def single_replay(self, name):
        single = subprocess.Popen('afplay %s' % name, shell=True)
        app_log.debug(name)
        while single.poll() is None and not self.stop.is_set():
            if self.pause.is_set():
                single.send_signal(signal.SIGSTOP)
                app_log.info('sent pause')
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
    resume = Event()
    player = Player(stop, pause, resume)
    control = Main(player, stop, pause, resume)
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


