local_name = input('Name: ')

from players import *
import keys
import gameclient

def incoming_data_is_new_player(data):
    for player in other_players:
        if data['name'] == player['name']:
            return False
        else:
            continue
    return True

def process_received_data(data):
    global players_latest_stats_from_server, other_players
    if data:
        if data['name'] != local_name and incoming_data_is_new_player(data):
            print('Player %s created' % data['name'])
            other_players[data['name']] = data


def create_remote_player_class_instances(data):
    if incoming_data_is_new_player(data):
        print('Player %s created' % data['name'])
        other_players[data['name']] = Player(data['name'], DWIDTH / 2, DHEIGHT / 2,
                 [random.randint(19900, 20100),random.randint(19900, 20100)],
                 0, 0, 0, False)

def implement_latest_stats_from_server(local_player):
    for playername in players_latest_stats_from_server:
        if playername is not local_player.name:
            other_players[playername].update_from_server(playername)
        else:
            local_player.update_from_server(local_player.name)


aspect_ratio = 1.85
DWIDTH, DHEIGHT = 1280, 800
#DHEIGHT = int(DWIDTH / aspect_ratio)
DISPLAYSIZE = (DWIDTH, DHEIGHT)
MAPWIDTH, MAPHEIGHT = 40000, 40000

pygame.init()
pygame.mixer.init()
music = pygame.mixer.music.load('./sfx/space_music_2.mp3')
pygame.mixer.music.set_volume(0.4)
music = False

MONW, MONH = pygame.display.Info().current_w, pygame.display.Info().current_h

display = pygame.display.set_mode((DWIDTH, DHEIGHT))
clock = pygame.time.Clock()

FPS = True
background = pygame.image.load('./img/spacebg.jpg').convert()
background = pygame.transform.scale(background, (DWIDTH, DHEIGHT))


players_latest_stats_from_server = {}
other_players = {}

player1 = Player(local_name, DWIDTH / 2, DHEIGHT / 2,
                 [random.randint(19900, 20100),random.randint(19900, 20100)],
                 0, 0, 0, True)
particles1 = Particles(1, 1, player1, DWIDTH, DHEIGHT)
particles2 = Particles(2, 2, player1, DWIDTH, DHEIGHT)
particles3 = Particles(3, 4, player1, DWIDTH, DHEIGHT)

if pygame.mixer.music.get_busy() == False and music == True:
    pygame.mixer.music.play(-1)

while True:
    display.blit(background, (0, 0))
    particles3.draw(display)
    particles2.draw(display)
    particles1.draw(display)

    keys.process_keys(player1)
    # implement_latest_stats_from_server(player1)
    player1.draw(display)
    # for player in other_players:
    #     player.draw(display)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif event.key == pygame.K_m:
                if pygame.mixer.music.get_busy() == False:
                    music == True
                    pygame.mixer.music.play(-1)
                else: pygame.mixer.music.pause()


    gameclient.upload_player_stats(player1)
    received_data = gameclient.download_from_server()
    # print(received_data)
    process_received_data(received_data)
    # create_remote_player_class_instances(received_data)


    pygame.display.flip()
    clock.tick(30)

pygame.quit()
