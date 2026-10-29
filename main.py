from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
import random 

# Janela
janela = Window(800, 500)
janela.set_title("ping pong")

# Fundo
fundo = GameImage("fundo.png")

# Bola
ball = Sprite("ball.png",1)
ball.set_position((janela.width - ball.width)/2, (janela.height - ball.height)/2)
vel_x = 200
vel_y = 200

# Pads
pad1 = Sprite("pad1.png",1)
pad1.set_position(0, (janela.height - pad1.height)/2)
pad2 = Sprite("pad2.png",1)
pad2.set_position(janela.width - pad2.width, (janela.height - pad2.height)/2)
velpad =  0

padex = Sprite("padex.png")
padex.set_position(janela.width - (janela.width/2 + padex.width/2), (janela.height - padex.height))
padex2 = Sprite("padex2.png")
padex2.set_position(janela.width - (janela.width/2 + padex2.width/2), 0)

# Teclado
teclado = Window.get_keyboard()

# Controle
pause  = False
game_over = False
pontos_direita = 0
pontos_esquerda = 0
vencedor = ""

def gerar_posicoes_aleatorias():
    padex.set_position(random.randint(0, janela.width - padex.width), padex.y)
    padex2.set_position(random.randint(0, janela.width - padex2.width), padex2.y)

while True:
    if not pause:
        ball.x += vel_x * janela.delta_time()
        ball.y += vel_y * janela.delta_time()
    pad2.y += velpad
    fundo.draw()
    ball.draw()
    pad1.draw()
    pad2.draw()
    padex.draw()
    padex2.draw()

    # colisão com padex
    if ball.collided(padex):
        if vel_y > 0: 
            ball.y = padex.y - ball.height 
            vel_y *= -1

    # colisão com padex2
    if ball.collided(padex2):
        if vel_y < 0: 
            ball.y = padex2.y + padex2.height 
            vel_y *= -1

    if not game_over:
        # colisão horizontais
        if ball.y - ball.height >= janela.height:
            vel_y *= 1
            vel_x *= 1
            ball.set_position(ball.x, 0)
        if ball.y + ball.height <= 0:
            vel_y *= 1
            vel_x *= 1
            ball.set_position(ball.x, 0)

        # pad esquerda perde
        if ball.x <= -(ball.width):
            ball.set_position((janela.width - ball.width)/2, (janela.height - ball.height)/2)
            pad1.set_position(0, (janela.height - pad1.height)/2)
            pad2.set_position(janela.width - pad2.width, (janela.height - pad2.height)/2)
            pontos_direita += 1
            pause = True
            vel_y = 0
            gerar_posicoes_aleatorias()  

        # pad direita perde
        if ball.x - ball.width >= janela.width:
            ball.set_position((janela.width - ball.width) / 2, (janela.height - ball.height) / 2)
            pad1.set_position(0, (janela.height - pad1.height) / 2)
            pad2.set_position(janela.width - pad2.width, (janela.height - pad2.height) / 2)
            pontos_esquerda += 1
            pause = True
            vel_y = 0
            gerar_posicoes_aleatorias()

        if pause and teclado.key_pressed("SPACE"):
            pause = False
            vel_y = 200

        # controle dos pads
        if teclado.key_pressed("UP") and pad1.y >= 0:
            pad1.move_key_y(250 * janela.delta_time())
        if teclado.key_pressed("DOWN") and pad1.y + pad1.height <= janela.height:
            pad1.move_key_y(250 * janela.delta_time())

        # padbot
        if vel_y > 0:
            velpad = 85 * janela.delta_time()
        elif vel_y < 0:
            velpad = -85 * janela.delta_time()
        elif vel_y == 0:
            velpad = 0

        pad2.y += velpad  

        if pad2.y < 0:
            pad2.y = 0
        if pad2.y + pad2.height > janela.height:
            pad2.y = janela.height - pad2.height

        if ball.collided(pad1) and ball.x <= pad1.x + pad1.width: 
            ball.x = pad1.x + pad1.width  # evita deslizamento
            vel_x *= -1
        if ball.collided(pad2) and ball.x + ball.width >= pad2.x:
            ball.x = pad2.x - ball.width  # evita deslizamento
            vel_x *= -1

        # Verifica game over
        if pontos_direita == 3:
            game_over = True
            vencedor = "Jogador da Direita Venceu!"
        elif pontos_esquerda == 3:
            game_over = True
            vencedor = "Jogador da Esquerda Venceu!"

    # Placar
    janela.draw_text(str(pontos_esquerda), 200, 30, size=40, color=(0, 0, 0))
    janela.draw_text(str(pontos_direita), 600, 30, size=40, color=(0, 0, 0))

    # Game over
    if game_over:
        janela.set_background_color((200, 0, 0))
        janela.draw_text("GAME OVER", 250, 150, size=50, color=(255, 255, 255), bold=True)
        janela.draw_text(vencedor, 225, 200, size=30, color=(255, 255, 255))

    janela.update()
