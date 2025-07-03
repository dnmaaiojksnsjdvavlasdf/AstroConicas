from PyQt5 import QtWidgets, QtCore, QtMultimedia, QtMultimediaWidgets  #Instale a biblioteca PyQt5 corretamente, ela que faz a interface.
from PyQt5.QtGui import QIcon 
import sys
import os
from reconhece import simplificar
from animação import CenaConicaComMovimento 
from animação import CenaDegenerada
from manim import tempconfig

# Dicionário para mapear os tipos retornados por Reconhecer_conicas para textos explicativos:
MENSAGENS_CONICAS = {
    "Ponto Degenerado": "A órbita gerada é um Ponto! Uma órbita que seja apenas um ponto não existe, porque \n"
                        "qualquer objeto em movimento sob influência gravitacional sempre segue uma trajetória no espaço. \n"
                        "Um ponto representaria um corpo parado no tempo e no espaço, o que na prática não acontece. \n"
                        "Mesmo que a velocidade inicial seja zero, o objeto acabará sendo atraído e começará a se mover.",
    
    "Duas Retas que se Cruzam": "A órbita gerada é um caso de Reta! Órbitas perfeitamente retas não existem, porque sempre\n"
                                "há alguma força gravitacional agindo sobre o objeto. Mas, a grandes distâncias, uma órbita \n"
                                "parabólica pode parecer uma reta, já que a influência da gravidade fica tão pequena que a trajetória \n"
                                "segue quase em linha reta pelo espaço.",
    
    "Reta Dupla": "A órbita gerada é um caso de Reta! Órbitas perfeitamente retas não existem, porque sempre\n"
                  "há alguma força gravitacional agindo sobre o objeto. Mas, a grandes distâncias, uma órbita \n"
                  "parabólica pode parecer uma reta, já que a influência da gravidade fica tão pequena que a trajetória \n"
                  "segue quase em linha reta pelo espaço.",
    
    "Duas Retas Paralelas": "A órbita gerada é um caso de Reta! Órbitas perfeitamente retas não existem, porque sempre\n"
                            "há alguma força gravitacional agindo sobre o objeto. Mas, a grandes distâncias, uma órbita \n"
                            "parabólica pode parecer uma reta, já que a influência da gravidade fica tão pequena que a trajetória \n"
                            "segue quase em linha reta pelo espaço.",
    
    "Conjunto Vazio": "A órbita gerada é Vazia! O universo é grande o suficiente para \n"
                      "o vazio, e ainda é possível ver o vislumbre no nada. “Nada existe senão átomos e vazio.” — Demócrito",
    
    "Plano Inteiro (0=0)": "A equação representa o plano inteiro (0=0). Não é uma cônica específica.",
    
    "Caso Degenerado Indefinido": "A órbita gerada é um caso degenerado que não pôde ser classificado especificamente. \n"
                                  "Pode representar uma ou mais retas, ou um conjunto vazio, dependendo dos coeficientes exatos."
}

# Criando a janela da interface com todos as ferramentas presentes nela
class InterfaceUsuario(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AstroCônicas")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("planet-2.png"))

        self.layout = QtWidgets.QVBoxLayout() #Os widgets vão aparecer em um layout horizontal básico

        # Adicionar um QLabel para exibir a equação geral da cônica
        self.equation_label = QtWidgets.QLabel("Equação: Ax² + Bxy + Cy² + Dx + Ey + F = 0")
        self.equation_label.setAlignment(QtCore.Qt.AlignCenter)
        self.equation_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(self.equation_label)
        
        # Widget dos sliders
        self.a_slider = self.crie_slider("A", -50, 50, 1)
        self.b_slider = self.crie_slider("B", -50, 50, 0)
        self.c_slider = self.crie_slider("C", -50, 50, 4)
        self.d_slider = self.crie_slider("D", -50, 50, 0)
        self.e_slider = self.crie_slider("E", -50, 50, 0)
        self.f_slider = self.crie_slider("F", -50, 50, -16)

        self.layout.addWidget(self.a_slider)
        self.layout.addWidget(self.b_slider)
        self.layout.addWidget(self.c_slider)
        self.layout.addWidget(self.d_slider)
        self.layout.addWidget(self.e_slider)
        self.layout.addWidget(self.f_slider)

        # Widget do botão que aciona a animação da cônica
        self.animacao_botao = QtWidgets.QPushButton("Gerar Órbita")
        self.animacao_botao.clicked.connect(self.animacao_conica)
        self.layout.addWidget(self.animacao_botao)

        # Widget de vídeo
        self.video_widget = QtMultimediaWidgets.QVideoWidget()
        self.layout.addWidget(self.video_widget)
        self.media_player = QtMultimedia.QMediaPlayer(None, QtMultimedia.QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)

        self.setLayout(self.layout)

        # Conectar os sliders à função de atualização da equação
        self.a_slider.layout().itemAt(0).widget().valueChanged.connect(self.update_equation_display)
        self.b_slider.layout().itemAt(0).widget().valueChanged.connect(self.update_equation_display)
        self.c_slider.layout().itemAt(0).widget().valueChanged.connect(self.update_equation_display)
        self.d_slider.layout().itemAt(0).widget().valueChanged.connect(self.update_equation_display)
        self.e_slider.layout().itemAt(0).widget().valueChanged.connect(self.update_equation_display)
        self.f_slider.layout().itemAt(0).widget().valueChanged.connect(self.update_equation_display)

        # Chamar a atualização inicial para exibir a equação padrão
        self.update_equation_display()

    # Definindo os sliders e os parâmetros que armazenam
    def crie_slider(self, rotulo, min_valor, max_valor, valor_inicial):
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setRange(min_valor, max_valor)
        slider.setValue(valor_inicial)
        slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        slider.setTickInterval(1)

        slider_rotulo = QtWidgets.QLabel(f"{rotulo}: {valor_inicial}")
        slider.valueChanged.connect(lambda valor: slider_rotulo.setText(f"{rotulo}: {valor}"))

        slider_layout = QtWidgets.QHBoxLayout()
        slider_layout.addWidget(slider)
        slider_layout.addWidget(slider_rotulo)

        container = QtWidgets.QWidget()
        container.setLayout(slider_layout)
        return container

    # Definindo como irá ocorrer a atualização dos valores dos sliders para aparecer na interface
    def update_equation_display(self):
        # Pega os valores atuais dos sliders
        A = self.a_slider.layout().itemAt(0).widget().value()
        B = self.b_slider.layout().itemAt(0).widget().value()
        C = self.c_slider.layout().itemAt(0).widget().value()
        D = self.d_slider.layout().itemAt(0).widget().value()
        E = self.e_slider.layout().itemAt(0).widget().value()
        F = self.f_slider.layout().itemAt(0).widget().value()

        # Constrói a string da equação de forma legível
        equation_parts = []

        if A != 0:
            equation_parts.append(f"{A}x²" if A != 1 else "x²")
        if B != 0:
            equation_parts.append(f"{B}xy" if B != 1 else "xy")
        if C != 0:
            equation_parts.append(f"{C}y²" if C != 1 else "y²")
        if D != 0:
            equation_parts.append(f"{D}x" if D != 1 else "x")
        if E != 0:
            equation_parts.append(f"{E}y" if E != 1 else "y")
        if F != 0:
            equation_parts.append(f"{F}")
        
        # Concatena as partes com sinais
        equation_str = ""
        for i, part in enumerate(equation_parts):
            if i > 0 and (part[0] != '-' and part[0].isdigit() or part[0] == 'x' or part[0] == 'y'):
                equation_str += " + "
            elif i > 0 and part[0] == '-':
                equation_str += " " # Já tem o sinal de menos
            
            equation_str += part

        if not equation_str: # Se todos os coeficientes forem zero
            equation_str = "0"

        self.equation_label.setText(f"Equação: {equation_str} = 0")

    # Definindo como ocorre a geração dos vídeos: pegando os valores dos sliders enviando para os outros arquivos .py que irão reduzir e animar a cônica
    def animacao_conica(self):
        # Pega os valores dos sliders
        A = self.a_slider.layout().itemAt(0).widget().value()
        B = self.b_slider.layout().itemAt(0).widget().value()
        C = self.c_slider.layout().itemAt(0).widget().value()
        D = self.d_slider.layout().itemAt(0).widget().value()
        E = self.e_slider.layout().itemAt(0).widget().value()
        F = self.f_slider.layout().itemAt(0).widget().value()
        
        # Chama a função de simplificação
        resultado = simplificar(A, B, C, D, E, F)
        print(f"Resultado da simplificação: {resultado}")

        output_file = f"conica_A{A}_B{B}_C{C}_D{D}_E{E}_F{F}.mp4"
        output_dir = "media/videos/custom"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        video_path = os.path.join(output_dir, output_file)

        # Configurações do Manim para renderização
        with tempconfig({
            "media_dir": "media",
            "video_dir": output_dir,
            "output_file": output_file,
            "quality": "low_quality", 
            "preview": True # Abre a janela do Manim após renderizar
        }):
            tipo_identificado = resultado[0] if isinstance(resultado, list) and resultado else "Indefinido"

            mensagem_para_cena = MENSAGENS_CONICAS.get(tipo_identificado, tipo_identificado)

            if tipo_identificado in MENSAGENS_CONICAS:
                scene = CenaDegenerada(mensagem_para_cena)
                scene.render()
            elif tipo_identificado in ['Elipse', 'Circunferência', 'Hipérbole', 'Parábola']:
                scene = CenaConicaComMovimento(A, B, C, D, E, F, resultado)
                scene.render()
            else: 
                scene = CenaDegenerada("Tipo de Cônica Não Reconhecido ou Inesperado.")
                scene.render()
        
        if os.path.exists(video_path):
            url = QtCore.QUrl.fromLocalFile(os.path.abspath(video_path))
            self.media_player.setMedia(QtMultimedia.QMediaContent(url))
            self.media_player.play()
        else:
            QtWidgets.QMessageBox.warning(self, "Erro", f"Vídeo não encontrado em: {video_path}")

# Trivialidades para a biblioteca; estamos definindo o que irá ocorrer quando iniciar o programa
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = InterfaceUsuario()
    window.show()
    sys.exit(app.exec_())
