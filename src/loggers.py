import logging as log

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
