import pygame
import sys
import settings as sett
from blocker import Blocker
from bullet import Bullet
from enemies_group import EnemiesGroup
from enemy_explosion import EnemyExplosion
from mystery import Mystery
from mystery_explosion import MysteryExplosion
from ship_explosion import ShipExplosion
from text import Text
from ship import Ship
from enemy import Enemy
from life import Life
from button_play import ButtonPlay
from button_hs import ButtonHighScores
from random import choice


class SpaceInvaders(object):
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 4096)
        pygame.init()

        self.clock = pygame.time.Clock()
        self.caption = pygame.display.set_caption('Space Invaders')
        self.screen = sett.SCREEN
        self.background = pygame.image.load(sett.IMAGE_PATH + 'space_bg.jpg').convert()
        self.startGame = False
        self.mainScreen = True
        self.gameOver = False
        #BUTTONS
        self.play_button = ButtonPlay(self.screen, "PLAY")
        self.hs_button = ButtonHighScores(self.screen, "HIGH SCORES")
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.play_button_clicked = self.play_button.rect.collidepoint(self.mouse_x, self.mouse_y)
        self.hs_button_clicked = self.hs_button.rect.collidepoint(self.mouse_x, self.mouse_y)
        # Counter for enemy starting position (increased each new round)
        self.enemyPosition = sett.ENEMY_DEFAULT_POSITION
        self.titleText = Text(sett.FONT, 80, 'SPACE INVADERS', sett.GREEN,
                              15, 50)
        #TEXT
        self.gameOverText = Text(sett.FONT, 50, 'Game Over', sett.WHITE, 250, 270)
        self.nextRoundText = Text(sett.FONT, 50, 'Next Round', sett.WHITE, 240, 270)
        self.enemy1Text = Text(sett.FONT, 25, '   =   10 pts', sett.GREEN, 368, 270)
        self.enemy2Text = Text(sett.FONT, 25, '   =  20 pts', sett.BLUE, 368, 320)
        self.enemy3Text = Text(sett.FONT, 25, '   =  30 pts', sett.PURPLE, 368, 370)
        self.enemy4Text = Text(sett.FONT, 25, '   =  ?????', sett.RED, 368, 420)
        self.scoreText = Text(sett.FONT, 20, 'Score', sett.WHITE, 5, 5)
        self.livesText = Text(sett.FONT, 20, 'Lives ', sett.WHITE, 640, 5)
        #PLAYER LIVES
        self.life1 = Life(715, 3)
        self.life2 = Life(742, 3)
        self.life3 = Life(769, 3)
        self.livesGroup = pygame.sprite.Group(self.life1, self.life2, self.life3)

    def reset(self, score):
        self.player = Ship()
        self.player_group = pygame.sprite.Group(self.player)
        self.explosions_group = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.mystery_ship = Mystery()
        self.mystery_group = pygame.sprite.Group(self.mystery_ship)
        self.enemy_bullets = pygame.sprite.Group()
        self.make_enemies()
        self.all_sprites = pygame.sprite.Group(self.player, self.enemies,
                                               self.livesGroup, self.mystery_ship)
        self.keys = pygame.key.get_pressed()

        self.timer = pygame.time.get_ticks()
        self.note_timer = pygame.time.get_ticks()
        self.ship_timer = pygame.time.get_ticks()
        self.score = score
        self.create_audio()
        self.make_new_ship = False
        self.ship_alive = True

    def make_blockers(self, number):
        blockerGroup = pygame.sprite.Group()
        for row in range(4):
            for column in range(9):
                blocker = Blocker(10, sett.GREEN, row, column)
                blocker.rect.x = 50 + (200 * number) + (column * blocker.width)
                blocker.rect.y = sett.BLOCKERS_POSITION + (row * blocker.height)
                blockerGroup.add(blocker)
        return blockerGroup

    def create_audio(self):
        self.sounds = {}
        for sound_name in ['shoot', 'shoot2', 'invaderkilled', 'mysterykilled',
                           'shipexplosion', 'si_background']:
            self.sounds[sound_name] = pygame.mixer.Sound(
                sett.SOUND_PATH + '{}.wav'.format(sound_name))
            self.sounds[sound_name].set_volume(0.2)

        self.musicNotes = [pygame.mixer.Sound(sett.SOUND_PATH + '{}.wav'.format(i)) for i
                           in range(4)]
        for sound in self.musicNotes:
            sound.set_volume(0.5)

        self.noteIndex = 0

    def play_main_music(self, current_time):
        if current_time - self.note_timer > self.enemies.moveTime:
            self.note = self.musicNotes[self.noteIndex]
            if self.noteIndex < 3:
                self.noteIndex += 1
            else:
                self.noteIndex = 0

            self.note.play()
            self.note_timer += self.enemies.moveTime

    @staticmethod
    def should_exit(evt):
        # type: (pygame.event.EventType) -> bool
        return evt.type == pygame.QUIT or (evt.type == pygame.KEYUP and evt.key == pygame.K_ESCAPE)

    def check_input(self):
        self.keys = pygame.key.get_pressed()
        for e in pygame.event.get():
            if self.should_exit(e):
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if len(self.bullets) == 0 and self.ship_alive:
                        if self.score < 1000:
                            bullet = Bullet(self.player.rect.x + 23,
                                            self.player.rect.y + 5, -1,
                                            15, 'laser', 'center')
                            self.bullets.add(bullet)
                            self.all_sprites.add(self.bullets)
                            self.sounds['shoot'].play()
                        else:
                            left_bullet = Bullet(self.player.rect.x + 8,
                                                 self.player.rect.y + 5, -1,
                                                 15, 'laser', 'left')
                            right_bullet = Bullet(self.player.rect.x + 38,
                                                  self.player.rect.y + 5, -1,
                                                  15, 'laser', 'right')
                            self.bullets.add(left_bullet)
                            self.bullets.add(right_bullet)
                            self.all_sprites.add(self.bullets)
                            self.sounds['shoot2'].play()

    def make_enemies(self):
        enemies = EnemiesGroup(10, 5)
        for row in range(5):
            for column in range(10):
                enemy = Enemy(row, column)
                enemy.rect.x = 157 + (column * 50)
                enemy.rect.y = self.enemyPosition + (row * 45)
                enemies.add(enemy)

        self.enemies = enemies

    def make_enemies_shoot(self):
        if (pygame.time.get_ticks() - self.timer) > 700 and self.enemies:
            enemy = self.enemies.random_bottom()
            self.enemy_bullets.add(
                Bullet(enemy.rect.x + 14, enemy.rect.y + 20, 1, 5,
                       'enemylaser', 'center'))
            self.all_sprites.add(self.enemy_bullets)
            self.timer = pygame.time.get_ticks()

    def calculate_score(self, row):
        scores = {0: 30,
                  1: 20,
                  2: 20,
                  3: 10,
                  4: 10,
                  5: choice([50, 100, 150, 300])
                  }

        score = scores[row]
        self.score += score
        return score

    def create_main_menu(self):
        self.enemy1 = sett.IMAGES['enemy3_1']
        self.enemy1 = pygame.transform.scale(self.enemy1, (40, 40))
        self.enemy2 = sett.IMAGES['enemy2_2']
        self.enemy2 = pygame.transform.scale(self.enemy2, (40, 40))
        self.enemy3 = sett.IMAGES['enemy1_2']
        self.enemy3 = pygame.transform.scale(self.enemy3, (40, 40))
        self.enemy4 = sett.IMAGES['mystery']
        self.enemy4 = pygame.transform.scale(self.enemy4, (80, 40))
        self.screen.blit(self.enemy1, (318, 270))
        self.screen.blit(self.enemy2, (318, 320))
        self.screen.blit(self.enemy3, (318, 370))
        self.screen.blit(self.enemy4, (299, 420))
        if not self.startGame:
            self.play_button.draw_button()
            self.hs_button.draw_button()


    def check_collisions(self):
        pygame.sprite.groupcollide(self.bullets, self.enemy_bullets, True, True)

        #When an alien is hit
        for enemy in pygame.sprite.groupcollide(self.enemies, self.bullets,
                                         True, True).keys():
            self.sounds['invaderkilled'].play()
            self.calculate_score(enemy.row)
            EnemyExplosion(enemy, self.explosions_group)
            self.game_timer = pygame.time.get_ticks()

        #When mystery is hit
        for mystery in pygame.sprite.groupcollide(self.mystery_group, self.bullets,
                                                  True, True).keys():
            mystery.mysteryEntered.stop()
            self.sounds['mysterykilled'].play()
            score = self.calculate_score(mystery.row)
            MysteryExplosion(mystery, score, self.explosions_group)
            new_ship = Mystery()
            self.all_sprites.add(new_ship)
            self.mystery_group.add(new_ship)

        #When player is hit
        for player in pygame.sprite.groupcollide(self.player_group, self.enemy_bullets,
                                                 True, True).keys():
            if self.life3.alive():
                self.life3.kill()
            elif self.life2.alive():
                self.life2.kill()
            elif self.life1.alive():
                self.life1.kill()
            else:
                self.gameOver = True
                self.startGame = False
            self.sounds['shipexplosion'].play()
            ShipExplosion(player, self.explosions_group)
            self.make_new_ship = True
            self.ship_timer = pygame.time.get_ticks()
            self.ship_alive = False

        if self.enemies.bottom >= 540:
            pygame.sprite.groupcollide(self.enemies, self.player_group, True, True)
            if not self.player.alive() or self.enemies.bottom >= 600:
                self.gameOver = True
                self.startGame = False

        pygame.sprite.groupcollide(self.bullets, self.all_blockers, True, True)
        pygame.sprite.groupcollide(self.enemy_bullets, self.all_blockers, True, True)
        if self.enemies.bottom >= sett.BLOCKERS_POSITION:
            pygame.sprite.groupcollide(self.enemies, self.all_blockers, False, True)

    def create_new_ship(self, create_ship, current_time):
        if create_ship and (current_time - self.ship_timer > 900):
            self.player = Ship()
            self.all_sprites.add(self.player)
            self.player_group.add(self.player)
            self.make_new_ship = False
            self.ship_alive = True

    def create_game_over(self, current_time):
        self.screen.blit(self.background, (0, 0))
        passed = current_time - self.timer
        if passed < 750:
            self.gameOverText.draw(self.screen)
        elif 750 < passed < 1500:
            self.screen.blit(self.background, (0, 0))
        elif 1500 < passed < 2250:
            self.gameOverText.draw(self.screen)
        elif 2250 < passed < 2750:
            self.screen.blit(self.background, (0, 0))
        elif passed > 3000:
            self.mainScreen = True

        for e in pygame.event.get():
            if self.should_exit(e):
                sys.exit()

    #Main game function
    def main(self):
        while True:
            if self.mainScreen:
                self.screen.blit(self.background, (0, 0))
                self.titleText.draw(self.screen)
                self.enemy1Text.draw(self.screen)
                self.enemy2Text.draw(self.screen)
                self.enemy3Text.draw(self.screen)
                self.enemy4Text.draw(self.screen)
                self.create_main_menu()
                for e in pygame.event.get():
                    if self.should_exit(e):
                        sys.exit()
                    #When play button is pressed
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                        self.play_button_clicked = self.play_button.rect.collidepoint(self.mouse_x, self.mouse_y)
                        self.hs_button_clicked = self.play_button.rect.collidepoint(self.mouse_x, self.mouse_y)
                        if self.play_button_clicked and not self.startGame:
                            bg_music = pygame.mixer.Sound(sett.SOUND_PATH + 'si_background.wav')
                            bg_music.set_volume(0.5)
                            bg_music.play()
                            # Only create blockers on a new game, not a new round
                            self.all_blockers = pygame.sprite.Group(self.make_blockers(0),
                                                                    self.make_blockers(1),
                                                                    self.make_blockers(2),
                                                                    self.make_blockers(3))
                            self.livesGroup.add(self.life1, self.life2, self.life3)
                            self.reset(0)
                            self.startGame = True
                            self.mainScreen = False

                        #When high scores button is pressed
                        if self.hs_button_clicked and not self.startGame:
                            file_contents = []                      #List to store file contents
                            with open('high_score.txt', 'r') as f:
                                file_contents = f.readlines()
                            file_contents = str(file_contents)      #converts everything to strings
                            remove_char = ["'", "\\n", ",", "[", "]"]
                            for char in remove_char:
                                file_contents = file_contents.replace(char, "")
                            pygame.font.init()
                            text_color = sett.WHITE
                            display_surface = pygame.display.set_mode(sett.screen_width, sett.screen_height, 0, 32)
                            pygame.display.set_caption('HIGH SCORES')
                            font_1 = pygame.font.Font('freesansbold.ttf', 16)
                            text_1 = font_1.render(str(file_contents), True, text_color)
                            text_rect = text_1.get_rect()
                            text_rect.center = (sett.screen_width // 2, sett.screen_height // 2)

                            while True:
                                #Check for the QUIT event.
                                # completely fill the surface object
                                # with white color
                                display_surface.blit(self.background, (0, 0))
                                # display.update()
                                self.highScoreText.draw(self.screen)
                                display_surface.blit(text_1, text_rect)
                                pygame.display.update()
                                pygame.time.sleep(5)
                                # copying the text surface object
                                # to the display surface object
                                # at the center coordinate.
                                # deactivates the pygame library
                                sys.exit()

            elif self.startGame:
                if not self.enemies and not self.explosions_group:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.game_timer < 3000:
                        self.screen.blit(self.background, (0, 0))
                        self.score_text2 = Text(sett.FONT, 20, str(self.score),
                                                sett.GREEN, 85, 5)
                        self.scoreText.draw(self.screen)
                        self.score_text2.draw(self.screen)
                        self.nextRoundText.draw(self.screen)
                        self.livesText.draw(self.screen)
                        self.livesGroup.update()
                        self.check_input()
                    if current_time - self.game_timer > 3000:
                        # Move enemies closer to bottom
                        self.enemyPosition += sett.ENEMY_MOVE_DOWN
                        self.reset(self.score)
                        self.game_timer += 3000
                else:
                    current_time = pygame.time.get_ticks()
                    self.play_main_music(current_time)
                    self.screen.blit(self.background, (0, 0))
                    self.all_blockers.update(self.screen)
                    self.score_text2 = Text(sett.FONT, 20, str(self.score), sett.GREEN,
                                            85, 5)
                    self.scoreText.draw(self.screen)
                    self.score_text2.draw(self.screen)
                    self.livesText.draw(self.screen)
                    self.check_input()
                    self.enemies.update(current_time)
                    self.all_sprites.update(self.keys, current_time)
                    self.explosions_group.update(current_time)
                    self.check_collisions()
                    self.create_new_ship(self.make_new_ship, current_time)
                    self.make_enemies_shoot()

            elif self.gameOver:
                current_time = pygame.time.get_ticks()
                # Reset enemy starting position
                self.enemyPosition = sett.ENEMY_DEFAULT_POSITION
                self.create_game_over(current_time)

            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = SpaceInvaders()
    game.main()
