#Salve este arquivo com o nome 'animação.py' para funcionar corretamente com os outros dois.
from manim import *   #Você deve ter o manim instalado corretamente, é uma biblioteca complicada de se instalar, boa sorte!
import numpy as np   #Você deve ter o numpy instalado corretamente.
import sympy as sp  #Você deve ter o sympy instalado corretamente.

class CenaConicaComMovimento(ThreeDScene):                                                     #Cria uma classe para executar a animação
    def __init__(self, A, B, C, D, E, F, resultado, desloc_x=0.0, desloc_y=-0.5, **kwargs):
        super().__init__(**kwargs)
        self.A, self.B, self.C, self.D, self.E, self.F = A, B, C, D, E, F
        self.resultado = resultado 
        self.tipo = resultado[0] if resultado else 'Indefinido'
        self.desloc_x = desloc_x
        self.desloc_y = desloc_y

    def construct(self):
        print("Tipo de cônica para animação:", self.tipo)
        titulo = Tex(f"Tipo de cônica: {self.tipo}", font_size=36)
        titulo.to_edge(UP)
        self.play(Write(titulo), run_time=2, rate_func=smooth)

        if self.tipo == "Elipse":  #Caso o 'tipo' (resultado[0]) for elipse, definimos as especifiações visuais da animação para elipse aqui, como o texto, duração e a própria animação (definida na função animar_elipse)
            if len(self.resultado) >= 3:  #Garante que a lista 'resultado' tenha pelo menos 3 elementos para poder animar (isso é apenas para evitar possíveis erros).
                self.animar_elipse(float(self.resultado[1]), float(self.resultado[2]), self.desloc_x, self.desloc_y)  #Resultado[1] se refere ao 'a'.
            else:
                self.play(FadeOut(titulo))
                self.play(Write(Text("Erro: Parâmetros insuficientes para Elipse.", font_size=30, color=RED)))
                self.wait(2)

        elif self.tipo == "Circunferência": #Análogo ao que fizemos na elipse
            # O resultado para circunferência pode ser apenas o raio, ou o a e b (que são iguais).
            if len(self.resultado) >= 2: # Espera pelo menos o raio
                raio = float(self.resultado[1])
                self.animar_circunferencia(raio, self.desloc_x, self.desloc_y)
            else:
                self.play(FadeOut(titulo))
                self.play(Write(Text("Erro: Parâmetros insuficientes para Circunferência.", font_size=30, color=RED)))
                self.wait(2)

        elif self.tipo == "Hipérbole": #Análogo ao que fizemos na elipse
            if len(self.resultado) >= 3:
                self.animar_hiperbole(float(self.resultado[1]), float(self.resultado[2]), self.desloc_x, self.desloc_y)
            else:
                self.play(FadeOut(titulo))
                self.play(Write(Text("Erro: Parâmetros insuficientes para Hipérbole.", font_size=30, color=RED)))
                self.wait(2)
                
        elif self.tipo == "Parábola": #Análogo ao que fizemos na elipse
            if len(self.resultado) >= 2:
                p = float(self.resultado[1])
                # A parábola padrão no Manim é x=y^2, ajustaremos para a forma 4py = x^2 no lambda.
                # A função animar_parabola deve usar o 'p' para ajustar a curva e o foco.
                self.animar_parabola(self.desloc_x, self.desloc_y, p)
            else:
                self.play(FadeOut(titulo))
                self.play(Write(Text("Erro: Parâmetro 'p' da Parábola ausente.", font_size=30, color=RED)))
                self.wait(2)
        else: # Para qualquer outro caso (o que não deve acontecer se tiver tudo certo)
            self.wait(2)


    def animar_circunferencia(self, raio, desloc_x, desloc_y):  #Parâmetros, valores, e equações matemáticas que guiam a animação da circunferência.
        mu = 1.0 #Esse mu é uma constante que definimos para adequar os movimentos celestes à animação do computador, mudando ele poder mudar a maneira com que a animação é renderizada
        foco = np.array([desloc_x, desloc_y, 0]) # O foco é o centro para uma órbita circular 

        curva = ParametricFunction(                         #Parametrizando para fazer a animação do planeta descrevendo a cônica.
            lambda t: np.array([desloc_x + raio * np.cos(t), desloc_y + raio * np.sin(t), 0]),
            t_range=[0, 2 * np.pi],
            color=BLUE
        )
        
        t_tracker = ValueTracker(0)
        planeta = Dot(color=RED).move_to(curva.point_from_proportion(0))

        def pos_vel_circ(t):
            x = desloc_x + raio * np.cos(t)
            y = desloc_y + raio * np.sin(t)
            pos = np.array([x, y, 0])

            # Velocidade orbital para órbita circular
            v_mod = np.sqrt(mu / raio)

            dx = -raio * np.sin(t)
            dy = raio * np.cos(t)
            tang = np.array([dx, dy, 0])
            tang_norm = np.linalg.norm(tang)
            if tang_norm != 0:
                tang /= tang_norm
            else:
                tang = np.array([0, 0, 0]) # Evita divisão por zero

            vel = v_mod * tang
            return pos, vel
        
        planeta.add_updater(lambda m: m.move_to(pos_vel_circ(t_tracker.get_value())[0]))

        vel_arrow = always_redraw(lambda: Arrow(                              #Vetor que representa a velocidade do planeta
            start=planeta.get_center(),
            end=planeta.get_center() + 0.5 * pos_vel_circ(t_tracker.get_value())[1],
            color=ORANGE,
            buff=0
        ))
        
        foco_dot = Dot(point=foco, color=YELLOW).set_opacity(1) # Foco visível amarelo

        self.play(Create(curva), run_time=2)
        self.add(planeta, vel_arrow, foco_dot)

        def update_t(dt):               #Fica atualizando a função em tempo real
            current_t = t_tracker.get_value()
            _, v = pos_vel_circ(current_t)
            v_scalar = np.linalg.norm(v)
            # Ajusta a velocidade de atualização para manter a velocidade orbital constante na animação
            t_tracker.set_value((current_t + (v_scalar / raio) * dt) % (2 * np.pi))
        
        self.add_updater(update_t)
        self.wait(20) # Tempo da animação
        self.remove_updater(update_t)

    def animar_elipse(self, a, b, desloc_x, desloc_y):
        mu = 1.0  
        # Foco da elipse. assumes foco em (c,0) onde c = sqrt(a^2-b^2)
        c_foco = np.sqrt(max(0, a**2 - b**2)) # Garante que c_foco não seja complexo
        foco = np.array([desloc_x - c_foco, desloc_y, 0]) # Assumindo foco à esquerda do centro para órbita

        curva = ParametricFunction(
            lambda t: np.array([desloc_x + a * np.cos(t), b * np.sin(t) + desloc_y, 0]),
            t_range=[0, 2 * np.pi],
            color=BLUE
        )

        t_tracker = ValueTracker(0)
        planeta = Dot(color=RED).move_to(curva.point_from_proportion(0))

        def pos_vel_elipse(t):
            x = desloc_x + a * np.cos(t)
            y = b * np.sin(t) + desloc_y
            pos = np.array([x, y, 0])
            r = np.linalg.norm(pos - foco)
            
            # Velocidade orbital para elipse (Lei de Vis-viva)
            v_mod = np.sqrt(mu * (2 / r - 1 / a)) # 'a' aqui é o semi-eixo maior

            dx = -a * np.sin(t)
            dy = b * np.cos(t)
            tang = np.array([dx, dy, 0])
            tang_norm = np.linalg.norm(tang)
            if tang_norm != 0:
                tang /= tang_norm
            else:
                tang = np.array([0, 0, 0])

            vel = v_mod * tang
            return pos, vel

        planeta.add_updater(lambda m: m.move_to(pos_vel_elipse(t_tracker.get_value())[0]))

        vel_arrow = always_redraw(lambda: Arrow(
            start=planeta.get_center(),
            end=planeta.get_center() + 0.5 * pos_vel_elipse(t_tracker.get_value())[1],
            color=ORANGE,
            buff=0
        ))

        foco_dot = Dot(point=foco, color=YELLOW).set_opacity(1)

        self.play(Create(curva), run_time=3)
        self.add(planeta, vel_arrow, foco_dot)

        def update_t(dt):
            t = t_tracker.get_value()
            pos, vel = pos_vel_elipse(t)
            # A taxa de mudança do ângulo não é constante em elipses (2a Lei de Kepler)
            # Para simulação aproximada, ajustamos a velocidade de 't' com base na velocidade escalar
            # Isso é uma simplificação, a forma mais precisa envolveria resolver a Equação de Kepler
            v_scalar = np.linalg.norm(vel)
            
            # Estimativa de dt para o ângulo excêntrico
            # d_t = (r * v_scalar / (a*b)) * dt, mas r varia, então usamos uma aproximação.
            # Uma forma simples é variar a taxa de 't' para que o planeta acelere perto do foco
            # e desacelere longe. Quanto menor r, maior a velocidade.
            
            # Aproximação de velocidade angular
            angular_vel = v_scalar / np.linalg.norm(pos - np.array([desloc_x, desloc_y, 0])) # Distância do centro
            if np.linalg.norm(pos - np.array([desloc_x, desloc_y, 0])) < 0.1: # Evita divisão por zero perto do centro
                angular_vel = v_scalar / 0.1
            
            # Multiplicador para tornar a animação mais suave e visível
            speed_multiplier = 1.5 # Ajuste este valor se a animação estiver muito rápida/lenta

            t_tracker.set_value((t + angular_vel * dt * speed_multiplier) % (2 * np.pi))

        self.add_updater(update_t)
        self.wait(20) # Tempo da animação
        self.remove_updater(update_t)

    def animar_hiperbole(self, a, b, desloc_x, desloc_y):
        mu = 1.0
        # Foco da hipérbole. c = sqrt(a^2+b^2)
        c_foco = np.sqrt(a**2 + b**2)
        foco = np.array([desloc_x + c_foco, desloc_y, 0]) # Assumindo foco à direita do centro

        t_range_lower = -2.0 # Ajuste conforme necessário para ver uma boa parte da curva
        t_range_upper = 2.0
        time = ValueTracker(t_range_lower)

        # Usamos cosh e sinh para a parte positiva da hipérbole (um ramo da hipérbole)
        curva_direita = ParametricFunction(
            lambda t: np.array([desloc_x + a * np.cosh(t), b * np.sinh(t) + desloc_y, 0]),
            t_range=[t_range_lower, t_range_upper],
            color=BLUE
        )
        # REMOVA OU COMENTE ESTE TRECHO PARA EXCLUIR O RAMO ESQUERDO
        # curva_esquerda = ParametricFunction(
        #     lambda t: np.array([desloc_x - a * np.cosh(t), -b * np.sinh(t) + desloc_y, 0]), # ajuste de sinal para simetria
        #     t_range=[t_range_lower, t_range_upper],
        #     color=BLUE
        # )
        
        planeta = Dot(color=RED)

        e = c_foco / a # Excentricidade

        def kepler_hiperbolica(M, e, tol=1e-9, itmax=20):
            # Resolve a equação de Kepler hiperbólica M = e sinh(H) - H
            H = np.arcsinh(M / e) if e != 0 else M # Chute inicial
            for _ in range(itmax):
                f = e * np.sinh(H) - H - M
                fp = e * np.cosh(H) - 1
                if fp == 0: # Evita divisão por zero
                    break
                H_new = H - f / fp
                if abs(H_new - H) < tol:
                    break
                H = H_new
            return H

        def pos_vel_hiperbole(t_param):
            # t_param aqui é como o M na Equação de Kepler Hiperbólica
            M = t_param 
            H = kepler_hiperbolica(M, e)

            # Posição na hipérbole direita
            x = desloc_x + a * np.cosh(H)
            y = b * np.sinh(H) + desloc_y
            pos = np.array([x, y, 0])
            r = np.linalg.norm(pos - foco)
            
            # Velocidade orbital para hipérbole
            v_mod = np.sqrt(mu * (2 / r + 1 / abs(a))) # 'a' aqui é o semi-eixo real

            dx = a * np.sinh(H)
            dy = b * np.cosh(H)
            tang = np.array([dx, dy, 0])
            tang_norm = np.linalg.norm(tang)
            if tang_norm != 0:
                tang /= tang_norm
            else:
                tang = np.array([0, 0, 0])

            vel = v_mod * tang
            return pos, vel

        planeta.add_updater(lambda m: m.move_to(pos_vel_hiperbole(time.get_value())[0]))

        vel_arrow = always_redraw(lambda: Arrow(
            start=planeta.get_center(),
            end=planeta.get_center() + 0.4 * pos_vel_hiperbole(time.get_value())[1],
            color=ORANGE,
            buff=0
        ))

        foco_dot = Dot(point=foco, color=YELLOW).set_opacity(1)

        # Altere esta linha caso tenha colocado o ramo esquerdo da hipérbole:
        self.play(Create(curva_direita), run_time=3) # REMOVA 'Create(curva_direita) e coloque 'Create(curva_esquerda)' caso tenha colocado o ramo esquerdo da hipérbole.
        
        self.add(planeta, vel_arrow, foco_dot)

        def update_time(dt):
            t_current = time.get_value()
            pos, vel = pos_vel_hiperbole(t_current)
            v_scalar = np.linalg.norm(vel)
            
            # Ajusta a velocidade de 't' baseada na velocidade escalar para simular movimento
            # O fator 0.2 é um ajuste de velocidade da animação, pode mudá-lo para melhor visualização.
            novo_t = t_current + 0.2 * v_scalar * dt 
            
            # Reinicia a animação ao atingir o limite
            if novo_t > t_range_upper:
                novo_t = t_range_lower
            time.set_value(novo_t)

        self.add_updater(update_time)
        self.wait(20) # Tempo da animação
        self.remove_updater(update_time)
    
    def animar_parabola(self, desloc_x, desloc_y, p):
        mu = 1.0 
        
        # O foco de uma parábola x^2 = 4py é (0, p). Se a equação é x^2 = 4py, o vértice é (0,0).
        # Ajustamos para o deslocamento.
        foco = np.array([desloc_x, desloc_y + p, 0]) # Foco para x^2 = 4py

        # Para x^2 = 4py, t_range é o valor de x. y = x^2 / (4p)
        # A curva será definida por: x = t, y = t^2 / (4p)
        # Cuidado com p=0, mas a lógica da interface já deveria tratar isso como degenerado.
        curva = ParametricFunction(
            lambda t: np.array([desloc_x + t, desloc_y + (t**2) / (4 * p), 0]),
            t_range=[-6, 6], # Ajuste a amplitude da parábola visualizada
            color=BLUE
        )

        s_tracker = ValueTracker(-6) # O tracker para o 't' da função paramétrica
        planeta = Dot(color=RED).move_to(curva.point_from_proportion(0))

        foco_dot = Dot(point=foco, color=YELLOW).set_opacity(1)

        def parabola_pos_vel(s):
            # s é o parâmetro 'x' na nossa função paramétrica
            s_clipped = np.clip(s, -6, 6) # Garante que 's' esteja dentro do t_range
            
            pos = np.array([desloc_x + s_clipped, desloc_y + (s_clipped**2) / (4 * p), 0])
            r = np.linalg.norm(pos - foco)
            
            # Velocidade orbital para parábola (v^2 = 2mu/r)
            v_mod = np.sqrt(2 * mu / r)

            # Vetor tangente (derivadas de x e y em relação a s)
            dx_ds = 1
            dy_ds = (2 * s_clipped) / (4 * p) # Derivada de t^2/(4p) é 2t/(4p) = t/(2p)
            
            tang = np.array([dx_ds, dy_ds, 0])
            tang_norm = np.linalg.norm(tang)
            if tang_norm != 0:
                tang /= tang_norm # Normaliza o vetor tangente
            else:
                tang = np.array([0,0,0])

            vel = v_mod * tang
            return pos, vel

        planeta.add_updater(lambda m: m.move_to(parabola_pos_vel(s_tracker.get_value())[0]))

        vel_arrow = always_redraw(lambda: Arrow(
            start=planeta.get_center(),
            end=planeta.get_center() + 0.5 * parabola_pos_vel(s_tracker.get_value())[1],
            color=ORANGE,
            buff=0
        ))

        self.play(Create(curva), run_time=3)
        self.add(planeta, foco_dot, vel_arrow)

        def update_s(dt):
            s = s_tracker.get_value()
            _, v = parabola_pos_vel(s)
            v_scalar = np.linalg.norm(v)
            
            # A taxa de mudança de 's' é proporcional à velocidade escalar
            # Ajustamos o fator para controlar a velocidade da animação
            speed_multiplier = 1.0 # Ajuste este valor conforme necessário
            novo_s = s + speed_multiplier * v_scalar * dt 
            
            # Reinicia a animação ao atingir o limite
            if novo_s > 6:
                novo_s = -6
            s_tracker.set_value(novo_s)

        self.add_updater(update_s)
        self.wait(30) # Tempo da animação
        self.remove_updater(update_s)


class CenaDegenerada(Scene):   #Aqui, fizemos uma nova classe somente para animar as cônicas degeneradas.
    def __init__(self, tipo_degenerado, **kwargs):
        self.tipo_degenerado = tipo_degenerado   #Caso o tipo seja degenerado
        super().__init__(**kwargs)

    def construct(self):
        texto = Text(self.tipo_degenerado, font_size=20, color=RED)
        self.play(Write(texto))
        self.wait(30)
