#!/usr/bin/python3
#
#   Copyright (c) 2023, Monaco F. J. <monaco@usp.br>
#   Copyright 2024 The Authors of Coral
#
#   This file is part of Coral.
#
#   Coral is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Importação das bibliotecas necessárias para o jogo
import pygame
import random
import sys

##
## Customização do jogo.
##

# Modos de vídeo suportados (resoluções possíveis para a tela do jogo)
VIDEO_MODES = [
    (800, 800), (700, 700), (600, 600),
    (500, 500), (400, 400), (300, 300)
]

# Dimensões padrão da tela do jogo
WIDTH, HEIGHT = 800, 800     

# Cores definidas para diferentes elementos do jogo (cabeça da cobra, maçã, etc.)
HEAD_COLOR      = "#00aa00"  # Cor da cabeça da cobra.
DEAD_HEAD_COLOR = "#4b0082"  # Cor da cabeça da cobra quando está morta.
TAIL_COLOR      = "#00ff00"  # Cor da cauda da cobra.
APPLE_COLOR     = "#aa0000"  # Cor da maçã.
ARENA_COLOR     = "#202020"  # Cor do fundo.
CONFIG_COLOR    = "#D3D3D3"  # Cor da área de configurações.
GRID_COLOR      = "#3c3c3b"  # Cor das linhas de grade.
SCORE_COLOR     = "#ffffff"  # Cor da pontuação.
LINE_COLOR      = "#000000"  # Cor das linhas da pontuação.
MESSAGE_COLOR   = "#808080"  # Cor da mensagem de game over.

WINDOW_TITLE    = "Coral"  # Título da janela do jogo.

# Configurações iniciais de velocidade, tamanho e número de maçãs
velocity = [4, 7, 10, 15]
size = [60, 40, 20]  
n_apple = [1, 2, 3] 
configs = [1, 1, 0]  # Configurações do jogo: velocidade, tamanho e frequência de maçãs.

WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 153, 0)

ENERGY_BAR_WIDTH, ENERGY_BAR_HEIGHT = 200, 20
ENERGY_CONSUMPTION = 1  # Consumo de energia por ciclo.
MAX_ENERGY = 100  # Energia máxima.
APPLE_ENERGY = 50  # Energia recuperada por maçã.

# Definindo o modo "hard" como falso inicialmente.
hard_mode = False  
border_wrap = False  # Controla a opção de "borda envolvente", onde a cobra sai de um lado e aparece no outro.
is_muted = False  # Definido como falso, ou seja, não mudo inicialmente.

##
## Implementação do Jogo.
##

# Inicializando o pygame
pygame.init()

clock = pygame.time.Clock()

display_info = pygame.display.Info()

mon_w = display_info.current_w  # Largura da tela do monitor.
mon_h = display_info.current_h  # Altura da tela do monitor.

# Resolução da janela do jogo definida pela largura
win_res = WIDTH

# Se a resolução padrão não couber na tela do monitor, ajusta a resolução para a maior possível que caiba.
if (mon_w < WIDTH or mon_h < HEIGHT):
    min_dim = min(mon_w, mon_h)
    win_res = VIDEO_MODES[-1][0]  # O padrão é a resolução mais baixa.
    for mode in VIDEO_MODES:
        if mode[0] < mon_w and mode[1] < mon_h:
            win_res = mode[0]
            break

# Definindo a janela do jogo com a resolução ajustada
win = pygame.display.set_mode((win_res, win_res))

# Criando a superfície de jogo
arena = pygame.display.set_mode((WIDTH, HEIGHT))

# Tocar música de fundo e ajustar o volume
pygame.mixer.music.set_volume(0.4)
background_music = pygame.mixer.music.load('musics/CPU Talk - FMA - CC BY BoxCat Games.mp3')
pygame.mixer.music.play(-1)

# Definindo efeitos sonoros
got_apple_sound = pygame.mixer.Sound('musics/got_apple.ogg')
got_apple_sound.set_volume(0.6)

game_over_sound = pygame.mixer.Sound('musics/game_over.wav')
game_over_sound.set_volume(0.7)

# Definindo fontes para as mensagens
BIG_FONT = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(WIDTH / 8))
SMALL_FONT = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(WIDTH / 20))
IN_GAME_FONT = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(WIDTH / 48))

pygame.display.set_caption(WINDOW_TITLE)  # Definir o título da janela do jogo.

game_on = 1  # Variável que controla o estado do jogo.

##
## Função chamada quando a cobra morre.
##
def center_prompt(title, subtitle):
    global hard_mode, border_wrap, CLOCK_TICKS

    # Exibe título e subtítulo na tela centralizada
    center_title = BIG_FONT.render(title, True, MESSAGE_COLOR)
    center_title_rect = center_title.get_rect(center=(WIDTH/2, HEIGHT*(0.3)))
    arena.blit(center_title, center_title_rect)

    center_subtitle = SMALL_FONT.render(subtitle, True, MESSAGE_COLOR)
    center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.4)))
    arena.blit(center_subtitle, center_subtitle_rect)
    
    # Adiciona opções para reiniciar o jogo ou configurar o jogo
    center_subtitle = SMALL_FONT.render("Aperte C para configurar o jogo!", True, MESSAGE_COLOR)
    center_subtitle_rect = center_subtitle.get_rect(center=(WIDTH/2, HEIGHT*(0.5)))
    arena.blit(center_subtitle, center_subtitle_rect)

    # Adiciona opções para jogar em modo difícil ou fácil
    hard_mode_text = SMALL_FONT.render("Press H for Hard Mode", True, MESSAGE_COLOR)
    hard_mode_text_rect = hard_mode_text.get_rect(center=(WIDTH/2, HEIGHT*(0.7)))
    arena.blit(hard_mode_text, hard_mode_text_rect)

    easy_mode_text = SMALL_FONT.render("Press E for Easy Mode", True, MESSAGE_COLOR)
    easy_mode_text_rect = easy_mode_text.get_rect(center=(WIDTH/2, HEIGHT*(0.8)))
    arena.blit(easy_mode_text, easy_mode_text_rect)
    
    pygame.display.update()
        
    # Loop de espera até que uma tecla seja pressionada ou a janela seja fechada
    while ( event := pygame.event.wait() ):
        if event.type == pygame.KEYDOWN:
            break
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Reseta as configurações do jogo
    border_wrap = False

    if event.key == pygame.K_q:  # 'Q' fecha o jogo
        pygame.quit()
        sys.exit()
    if event.key == pygame.K_c:
        config_prompt()
    if event.key == pygame.K_h:
        hard_mode = True  # Ativa o modo difícil
        configs[0] = 2
    if event.key == pygame.K_e:
        border_wrap = True  # Ativa o modo com bordas envolventes

    if not hard_mode:  # Se não estiver no modo difícil, configura as configurações padrão
        configs[0] = 1

        # Draw stylized tail
def draw_tail(self, tail, direction):
    print(direction)
    # Define tail dimensions
    GRID_SIZE = size[configs[1]]  # Tamanho da célula na grade
    tail_radius = GRID_SIZE // 3  # Raio menor para a cauda
    big_tail_center = (tail[0] + tail_radius, tail[1] + tail_radius)  # Posição central da parte maior da cauda
    tail_center = (tail[0] + tail_radius, tail[1] + tail_radius)  # Posição central da parte arredondada da cauda

    # Determine tail shape and position based on the last segment's movement
    if direction[0] > 0:  # Moving right
        big_tail_center = (tail[0] + GRID_SIZE, tail[1] + GRID_SIZE // 2)  # A cauda é ajustada para a direita
        tail_center = (tail[0] + GRID_SIZE - tail_radius, tail[1] + GRID_SIZE // 2)  # Ajuste da parte arredondada
    elif direction[0] < 0:  # Moving left
        big_tail_center = (tail[0], tail[1] + GRID_SIZE // 2)  # A cauda é ajustada para a esquerda
        tail_center = (tail[0] + tail_radius, tail[1] + GRID_SIZE // 2)  # Ajuste da parte arredondada
    elif direction[1] > 0:  # Moving down
        big_tail_center = (tail[0] + GRID_SIZE // 2 , tail[1] + GRID_SIZE)  # A cauda é ajustada para baixo
        tail_center = (tail[0] + GRID_SIZE // 2, tail[1] + 2 * tail_radius)  # Ajuste da parte arredondada
    else:  # Moving up
        big_tail_center = (tail[0] + GRID_SIZE // 2 , tail[1])  # A cauda é ajustada para cima
        tail_center = (tail[0] + GRID_SIZE // 2, tail[1] + tail_radius)  # Ajuste da parte arredondada

    # Choose color based on alive status
    tail_color = HEAD_COLOR if self.alive else DEAD_HEAD_COLOR  # Define a cor da cauda dependendo do estado da cobra

    # Draw the main part of the tail (rounded edge)
    pygame.draw.circle(arena, tail_color, tail_center, tail_radius)  # Desenha a parte arredondada da cauda

    # Draw the rectangular part connecting to the next segment
    pygame.draw.circle(arena, tail_color, big_tail_center, 3 / 2 * tail_radius)  # Desenha a parte maior da cauda


##
## The apple class.
##

class Apple:
    def __init__(self):
        # Pick a random position within the game arena
        self.x = int(random.randint(0, WIDTH)/size[configs[1]]) * size[configs[1]]  # Posição aleatória na grade
        self.y = int(random.randint(0, HEIGHT)/size[configs[1]]) * size[configs[1]]  # Posição aleatória na grade

        # Create an apple at that location
        self.rect = pygame.Rect(self.x, self.y, size[configs[1]], size[configs[1]])  # Cria o retângulo da maçã na posição

    # This function is called each iteration of the game loop
    def update(self):
        # Drop the apple
        pygame.draw.rect(arena, APPLE_COLOR, self.rect)  # Desenha a maçã na tela


##
## Draw the arena
##

def draw_grid():
    # Desenha a grade no fundo da arena
    for x in range(0, WIDTH, size[configs[1]]):
        for y in range(0, HEIGHT, size[configs[1]]):
            rect = pygame.Rect(x, y, size[configs[1]], size[configs[1]])  # Define o retângulo de cada célula
            pygame.draw.rect(arena, GRID_COLOR, rect, 1)  # Desenha a célula da grade

score = BIG_FONT.render("1", True, MESSAGE_COLOR)  # Renderiza o texto da pontuação
score_rect = score.get_rect(center=(WIDTH/2, HEIGHT/20+HEIGHT/30))  # Posiciona a pontuação na tela

draw_grid()  # Chama a função para desenhar a grade

snake = Snake()  # Cria o objeto cobra
apple = Apple()  # Cria o objeto maçã

center_prompt(WINDOW_TITLE, "Press to start")  # Exibe uma mensagem inicial para o jogador

##
## Main loop
##

while True:
    for event in pygame.event.get():  # Aguarda eventos, como pressionamento de teclas e fechamento da janela
        if event.type == pygame.QUIT:  # Se o evento for o fechamento da janela
            pygame.quit()
            sys.exit()

        # Key pressed
        if event.type == pygame.KEYDOWN:  # Quando uma tecla for pressionada
            if event.key == pygame.K_q:  # Se a tecla for "Q", o jogo é fechado
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_p:  # Se a tecla for "P", o jogo é pausado
                game_on = not game_on
            elif event.key == pygame.K_m:  # Se a tecla for "M", o som é ativado/desativado
                is_muted = not is_muted
                pygame.mixer.music.set_volume(0 if is_muted else 0.4)

            # Allow movement only if the game is not paused
            if game_on:
                # Movimentos da cobra
                if event.key == pygame.K_DOWN and snake.ymov == 0:  # Se a tecla for seta para baixo
                    snake.ymov = 1
                    snake.xmov = 0
                elif event.key == pygame.K_UP and snake.ymov == 0:  # Se a tecla for seta para cima
                    snake.ymov = -1
                    snake.xmov = 0
                elif event.key == pygame.K_RIGHT and snake.xmov == 0:  # Se a tecla for seta para a direita
                    snake.ymov = 0
                    snake.xmov = 1
                elif event.key == pygame.K_LEFT and snake.xmov == 0:  # Se a tecla for seta para a esquerda
                    snake.ymov = 0
                    snake.xmov = -1

    ## Update the game

    # Show "Paused" and "Press P to continue" messages in the center of the grid if the game is paused
    if not game_on:
        pause_text = BIG_FONT.render("Paused", True, MESSAGE_COLOR)  # Mensagem de pausa
        pause_text_rect = pause_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))  # Posiciona a mensagem de pausa
        arena.blit(pause_text, pause_text_rect)  # Exibe a mensagem de pausa

        continue_text = SMALL_FONT.render("Press P to continue", True, MESSAGE_COLOR)  # Mensagem para retomar o jogo
        continue_text_rect = continue_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))  # Posiciona a mensagem
        arena.blit(continue_text, continue_text_rect)  # Exibe a mensagem

        pygame.display.update()  # Atualiza a tela
        continue  # Pula o resto do loop quando o jogo está pausado
    
    if game_on:
        snake.update()  # Atualiza o estado da cobra

        arena.fill(ARENA_COLOR)  # Limpa a tela
        draw_grid()  # Desenha a grade novamente

        apple.update()  # Atualiza a maçã na tela

        snake.energy.update()  # Atualiza a energia da cobra

    # Draw the tail
    for square in snake.tail:
        if square is snake.tail[-1]:
            if len(snake.tail) == 1:
                snake.draw_tail(square, (snake.xmov, snake.ymov))  # Desenha a cauda da cobra se for o último segmento
            else:
                snake.draw_tail(square, (snake.tail[-2][0] - square[0], snake.tail[-2][1] - square[1]))  # Desenha a cauda conectando ao segmento anterior
        else:
            pygame.draw.rect(arena, HEAD_COLOR, square)  # Desenha o segmento da cauda normalmente

    # Draw head
    snake.draw_head()  # Desenha a cabeça da cobra

    # Show score (snake length = head + tail)
    score = BIG_FONT.render(f"{len(snake.tail)}", True, SCORE_COLOR)  # Atualiza a pontuação
    arena.blit(score, score_rect)  # Exibe a pontuação na tela

    # If the head passes over an apple, lengthen the snake and drop another apple
    if snake.head.x == apple.x and snake.head.y == apple.y:  # Se a cabeça da cobra colidir com a maçã
        snake.got_apple = True  # A cobra pegou a maçã
        apple = Apple()  # Gera uma nova maçã
        got_apple_sound.play()  # Toca o som de maçã comida

    pygame.display.update()  # Atualiza a tela

    clock.tick(velocity[configs[0]])  # Controla a velocidade do jogo
