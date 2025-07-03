# 🪐 AstroCônicas - Simulador de "Órbitas" Cônicas

![Banner](imagens/logo_boa.png) <!-- O banner é pra estar aqui -->

> **Transforme equações gerais de cônicas em jornadas cósmicas visuais**

## ✨ Recursos
- 🎚️ Controle interativo de parâmetros
- 🪐 Visualização 2D de órbitas cônicas
- 📚 Explicações físicas para casos degenerados
- ⚡ Renderização com Manim

## 🚀 Instalação Rápida
Para uma instalação simples, digite cada um dos comandos abaixo em seu terminal de escolha. 
```bash
# Clone o repositório
git clone https://github.com/dnmaaiojksnsjdvavlasdf/astroconicas.git

# Instale as dependências
pip install -r requerimentos.txt
```
Caso essa opção de errado, você pode clicar no botão na direita do respositório, em verde, escrito "<> Code" e clicar em "Download ZIP" e extrair o arquivo baixado.

## ✏️ Descrição
O programa do Astrocônicas simula órbitas planetárias a partir da equação geral de uma cônica. Na interface, o usuário fornece os coeficientes da equação geral, que será reduzida e animada como uma órbita. O principal foco do programa é mostrar os casos possíveis de órbitas que de fato acontecem na mecânica celeste: Órbita elíptica, órbita hiperbólica e órbita parabólica. Entretanto, o programa também reconhece os casos degenerados, informando ao usuário algumas informações em um breve texto. 

## 🔍 Ensaio sobre o método
Quanto ao método utilizado para elaboração e estruturação do projeto, a maneira como o código foi construído reflete a forma como o grupo foi dividido. Dessa forma, as três partes componentes (interação, redução e animação) foram divididas como frentes independentes, num primeiro momento. Posteriormente, emergiram como três arquivos que interagiram entre si sob a seguinte rede de importação: os coeficientes obtidos pela parte interativa é enviada para a redução e identificação da cônica, que, por sua vez, é enviada para a animação. 
