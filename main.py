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

# Constante gravitacional
g = 9.81

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
    q = float(entrada_usuario("Digite a carga da partícula (q em C):", (50, 50)))
    m = float(entrada_usuario("Digite a massa da partícula (m em kg):", (50, 150)))
    E = float(entrada_usuario("Digite a intensidade do campo elétrico (E em N/C):", (50, 250)))
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
        pygame.draw.line(tela, cinza_claro, (i, 0), (i, altura), 1)
    angulo_rad = math.radians(direcao)
    componente_x = E * math.cos(angulo_rad)
    componente_y = E * math.sin(angulo_rad)
    ponto_final_x = largura / 2 + componente_x * 10
    ponto_final_y = altura / 2 - componente_y * 10
    pygame.draw.line(tela, vermelho, (largura / 2, altura / 2), (ponto_final_x, ponto_final_y), 3)

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

    # Calcular forças
    angulo_rad = math.radians(direcao)
    fe_x = q * E * math.cos(angulo_rad)
    fe_y = q * E * math.sin(angulo_rad)
    peso = m * g

    # Força resultante
    fr_x = fe_x
    fr_y = fe_y - peso

    # Aceleração
    ax = fr_x / m
    ay = fr_y / m

    # Atualizar a velocidade e a posição
    vx += ax * dt
    vy += ay * dt
    x += vx * dt
    y += vy * dt

    # Limitar a tela
    if x < raio:
        x = raio
        vx = -vx
    elif x > largura - raio:
        x = largura - raio
        vx = -vx
    if y < raio:
        y = raio
        vy = -vy
    elif y > altura - raio:
        y = altura - raio
        vy = -vy

    # Desenhar
    tela.fill(branco)
    desenhar_campo_eletrico()
    pygame.draw.circle(tela, azul, (int(x), int(y)), raio)

    # Mostrar informações
    texto_velocidade = font_pequena.render(f"Vel: ({vx:.2f}, {vy:.2f})", True, preto)
    texto_forcas = font_pequena.render(f"Forças: Fx={fr_x:.2f} N, Fy={fr_y:.2f} N", True, preto)
    texto_aceleracao = font_pequena.render(f"Acel: ({ax:.2f}, {ay:.2f}) m/s^2", True, preto)

    tela.blit(texto_velocidade, (10, 10))
    tela.blit(texto_forcas, (10, 40))
    tela.blit(texto_aceleracao, (10, 70))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
