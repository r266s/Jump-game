#--------------------------------------------------------------------------------------------------#
#                                       Made by r266                                               #
import pygame as PYG, math, random

sounds_dir = "./assets - jump/sounds"
image_dir = "./assets - jump/images"

PYG.init()
screen = PYG.display.set_mode((900, 480))
PYG.display.set_icon(PYG.image.load(f"{image_dir}/GI.ico"))
PYG.display.set_caption("Jump!", "wat?")

BG1_image = PYG.image.load(f"{image_dir}/BGs/BG1.png")
reset_BG_image = PYG.image.load(f"{image_dir}/BGs/reset_BG.png")
G_image = PYG.image.load(f"{image_dir}/G.png")
PL_image = PYG.image.load(f"{image_dir}/PL.png")
rand_GVE_image = [
  f"{image_dir}/rand/GVE_tall2.png",
  f"{image_dir}/rand/GVE.png",
  f"{image_dir}/rand/GVE_tall1.png",
  f"{image_dir}/rand/GVE.png",
  f"{image_dir}/rand/GVE_tall2.png",
  f"{image_dir}/rand/GVE_tall1.png"
]

jp_sound = PYG.mixer.Sound(f"{sounds_dir}/PL_jp.mp3")
get_hit = PYG.mixer.Sound(f"{sounds_dir}/lose.mp3")

G_rect = G_image.get_rect()
G_rect.width = G_image.get_width()
G_rect.height = G_image.get_height()
G_rect.x = 0 
G_rect.y = screen.get_height() - 40

PL_Hit = PL_image.get_rect()

reset_gra = -1
gra = 0
vel_y = 0
fall = True
    
class grave(PYG.sprite.Sprite):
  def __init__(self, image : str):
    super().__init__()
    self.image = PYG.transform.scale_by(PYG.image.load(image), 3)
    self.rect = self.image.get_rect()
    self.rect.bottom = G_rect.top
    self.rect.x = screen.get_width()
  def update(self):
    global SE_num
    global stop
    global show
    self.rect.move_ip(-5, 0)

    if self.rect.x is 0:
      SE_num += 1

    if self.rect.x <= -45:
      self.kill()

    if self.rect.colliderect(PL_Hit):
      stop = True
      show = False
      get_hit.play()
      self.kill()

class player(PYG.sprite.Sprite):
  def __init__(self, pos_x : int, pos_y : int):
    super().__init__()
    self.image = PYG.transform.scale_by(PL_image, 2)
    self.rect = self.image.get_rect()
    self.rect.x = pos_x
    self.rect.y = pos_y
    PL_Hit.width = self.rect.width
    PL_Hit.height = self.rect.height
  def update(self):
    global fall
    global vel_y
    global gra
    global reset_gra
    PL_Hit.x = self.rect.x
    PL_Hit.y = self.rect.y

    if fall is True:
      gra = reset_gra
      vel_y -= gra
      self.rect.y += vel_y
      PL_Hit.y = self.rect.y
    else:
      gra = 0
      vel_y = 0

    keys = PYG.key.get_pressed()
    
    if keys[PYG.K_SPACE] or keys[PYG.K_w] or keys[PYG.K_UP]:
      if self.rect.bottom == G_rect.top:
        vel_y -= 20
        fall = True
        jp_sound.play()
    
    if self.rect.colliderect(G_rect):
      self.rect.bottom = G_rect.top
      fall = False

timer_event = PYG.USEREVENT+1
PYG.time.set_timer(timer_event, 1250)

plr = player(10, 200)
add_plr = PYG.sprite.Group()
add_plr.add(plr)

GVE_gp = PYG.sprite.Group()

t = math.ceil(screen.get_width() / G_image.get_width()) + 1
scroll_speed = 0

WM_font = PYG.font.Font(None, 25)
WM_txt = WM_font.render("Made by r266", True, "white")

M_font = PYG.font.Font(None, 65)
M_txt = M_font.render("Jump!", True, "white")

lose_font = PYG.font.Font(None, 45)
lose_txt = lose_font.render("You get hit by a grave!", True, "white")

txt_button_font = PYG.font.Font(None, 50)
txt_button = txt_button_font.render("Start", True, "white")

reset_txt_font = PYG.font.Font(None, 50)
reset_txt = reset_txt_font.render("reset", True, "white")

screen_center_x = screen.get_width() / 2
(txt_M_W, txt_M_H) = M_txt.get_size()
txt_half_W = txt_M_W / 2
txt_center_x = screen_center_x - txt_half_W

button_center_x = txt_center_x - 10
lose_txt_center_x = txt_center_x - 100
txt_button_center_x = button_center_x + 35
YSE_center_x = txt_center_x + 4
start_button = PYG.Rect((button_center_x, 200, 150, 50))
reset_button = PYG.Rect((button_center_x, 200, 150, 50))

SE_num = 0
running = True
start = False
stop = False
show = False

while running:
  PYG.display.flip()
  screen.blit(BG1_image, (0, 0))

  if start is False:
    screen.blit(M_txt, (txt_center_x, 100))
    PYG.draw.rect(screen, (0, 255, 0), start_button)
    screen.blit(txt_button, (txt_button_center_x, 210))

  if show is True:
    SE_font = PYG.font.Font(None, 25)
    SE_text = SE_font.render(f"Score: {str(SE_num)}", True, "white")
    screen.blit(SE_text, (0, 20))

  if stop is True:
    screen.blit(reset_BG_image, (0, 0))
    SE_font = PYG.font.Font(None, 30)
    SE_text = SE_font.render(f"Your score: {str(SE_num)}", True, "white")
    screen.blit(SE_text, (YSE_center_x, 150))
    screen.blit(lose_txt, (lose_txt_center_x, 85))
    PYG.draw.rect(screen, (255, 0, 0), reset_button)
    screen.blit(reset_txt, (txt_button_center_x, 210))

  if stop is False:
    screen.blit(WM_txt, (0, 0))
    GVE_gp.draw(screen)
    GVE_gp.update()
    add_plr.draw(screen)
    add_plr.update()
    scroll_speed -= 5
 
    for i in range(0, t):
      screen.blit(G_image, (i * G_image.get_width() + scroll_speed, 440))

    if abs(scroll_speed) > G_image.get_width():
      scroll_speed = 0

  for events in PYG.event.get():
    if events.type == PYG.QUIT:
      running = False
      PYG.quit()
    if events.type == PYG.MOUSEBUTTONDOWN:
      mouse_pos = PYG.mouse.get_pos()

      if start_button.collidepoint(mouse_pos):
        if start is False:
          start = True
          show = True

      if reset_button.collidepoint(mouse_pos):
        if stop is True:
          SE_num = 0
          show = True
          stop = False
          GVE_gp.empty()

    if events.type == timer_event:
      if start is True:
        GVE = grave(random.choice(rand_GVE_image))
        GVE_gp.add(GVE)
    
  PYG.time.Clock().tick(60)
#--------------------------------------------------------------------------------------------------#
#                                       Made by r266                                               #