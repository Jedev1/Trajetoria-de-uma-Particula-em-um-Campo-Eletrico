import pygame
import math

# Inicialização do Pygame
pygame.init()

# Constantes
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Simulação de Campo Elétrico")

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)
azul = (0, 0, 255)
amarelo = (255, 255, 0)
cinza_claro = (200, 200, 200)

# Fontes
font = pygame.font.Font(None, 36)
font_pequena = pygame.font.Font(None, 24)

# Função para entrada de dados do usuário
def entrada_usuario(texto, posicao):
    ativo = True
    input_texto = ""
    while ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    ativo = False
                elif evento.key == pygame.K_BACKSPACE:
                    input_texto = input_texto[:-1]
                else:
                    input_texto += evento.unicode

        # Atualizar tela
        tela.fill(branco)
        texto_render = font.render(texto, True, preto)
        input_render = font.render(input_texto, True, preto)
        tela.blit(texto_render, posicao)
        tela.blit(input_render, (posicao[0], posicao[1] + 40))
        pygame.display.flip()

    return input_texto

# Função para exibir o menu inicial e coletar parâmetros
def menu_inicial():
    q = float(entrada_usuario("Digite a carga da partícula (q):", (50, 50)))
    m = float(entrada_usuario("Digite a massa da partícula (m):", (50, 150)))
    E = float(entrada_usuario("Digite a intensidade do campo elétrico (E):", (50, 250)))
    direcao = float(entrada_usuario("Digite a direção do campo (graus):", (50, 350)))
    return q, m, E, direcao

# Inicialização dos parâmetros
q, m, E, direcao = menu_inicial()

# Parâmetros iniciais
x, y = largura / 2, altura / 2
vx, vy = 0, 0
raio = 20

dt = 0.1
clock = pygame.time.Clock()

# Função para desenhar o campo elétrico
def desenhar_campo_eletrico():
    for i in range(0, largura, 20):
        pygame.draw.line(tela, vermelho, (i, 0), (i, altura), 2)
    angulo_rad = math.radians(direcao)
    componente_x = E * math.cos(angulo_rad)
    componente_y = E * math.sin(angulo_rad)
    ponto_final_x = x + componente_x * 10
    ponto_final_y = y + componente_y * 10
    pygame.draw.line(tela, azul, (x, y), (ponto_final_x, ponto_final_y), 2)

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                # Voltar ao menu inicial
                q, m, E, direcao = menu_inicial()
                x, y = largura / 2, altura / 2
                vx, vy = 0, 0

    # Calcular a força e a aceleração
    fx = q * E * math.cos(math.radians(direcao))
    fy = q * E * math.sin(math.radians(direcao))
    ax = fx / m
    ay = fy / m

    # Atualizar a velocidade e a posição
    vx += ax * dt
    vy += ay * dt
    x += vx * dt
    y += vy * dt

    # Limitar a tela
    if x < 0:
        x = 0
        vx = -vx
    elif x > largura:
        x = largura
        vx = -vx
    if y < 0:
        y = 0
        vy = -vy
    elif y > altura:
        y = altura
        vy = -vy

    # Desenhar
    tela.fill(branco)
    desenhar_campo_eletrico()
    pygame.draw.circle(tela, preto, (int(x), int(y)), raio)

    # Mostrar informações
    surface_velocidade = pygame.Surface((200, 30))
    surface_velocidade.fill(amarelo)
    texto_velocidade = font_pequena.render(f"Velocidade: ({vx:.2f}, {vy:.2f})", True, preto)
    surface_velocidade.blit(texto_velocidade, (5, 5))
    tela.blit(surface_velocidade, (10, 10))

    # Texto explicativo
    surface_explicativo = pygame.Surface((400, 30))
    surface_explicativo.fill(amarelo)
    texto_explicativo = font.render("Simulação de Campo Elétrico", True, preto)
    surface_explicativo.blit(texto_explicativo, (10, 5))
    tela.blit(surface_explicativo, (largura // 2 - 200, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
