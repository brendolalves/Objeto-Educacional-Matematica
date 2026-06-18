import tkinter as tk
import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuração inicial do CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppInequacoes(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Analisador de Inequações do 2º Grau")
        self.geometry("1100x700")

        # Cores padrão do gráfico
        self.cor_linha = "blue"
        self.cor_area = "green"

        self.criar_interface()

    def criar_interface(self):
        # Frame Lateral Esquerdo - Controles
        self.frame_controle = ctk.CTkFrame(self, width=300, corner_radius=10)
        self.frame_controle.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Entradas dos coeficientes (ax² + bx + c)
        ctk.CTkLabel(self.frame_controle, text="Coeficientes", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.txt_a = self.criar_campo_entrada("Coeficiente a:", "1")
        self.txt_b = self.criar_campo_entrada("Coeficiente b:", "-5")
        self.txt_c = self.criar_campo_entrada("Coeficiente c:", "6")

        # Seleção do sinal da inequação
        ctk.CTkLabel(self.frame_controle, text="Sinal da Inequação:", font=("Arial", 12)).pack(pady=5)
        self.sinal_var = ctk.StringVar(value=">")
        self.cb_sinal = ctk.CTkComboBox(self.frame_controle, values=[">", ">=", "<", "<="], variable=self.sinal_var)
        self.cb_sinal.pack(pady=5)

        # Customização de Cores
        ctk.CTkLabel(self.frame_controle, text="Personalizar Gráfico", font=("Arial", 14, "bold")).pack(pady=15)
        
        ctk.CTkLabel(self.frame_controle, text="Cor da Função:").pack()
        self.cb_cor_linha = ctk.CTkComboBox(self.frame_controle, values=["blue", "red", "purple", "black"], command=self.mudar_cor_linha)
        self.cb_cor_linha.pack(pady=5)

        ctk.CTkLabel(self.frame_controle, text="Cor da Área Solução:").pack()
        self.cb_cor_area = ctk.CTkComboBox(self.frame_controle, values=["green", "yellow", "orange", "cyan"], command=self.mudar_cor_area)
        self.cb_cor_area.pack(pady=5)

        # Botão Calcular
        self.btn_calcular = ctk.CTkButton(self.frame_controle, text="Calcular e Plotar", command=self.processar_inequacao, fg_color="green", hover_color="darkgreen")
        self.btn_calcular.pack(pady=20)

        # Frame Direito - Resultados e Gráfico
        self.frame_resultado = ctk.CTkFrame(self, corner_radius=10)
        self.frame_resultado.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Área de Texto do Resultado
        self.txt_explicacao = ctk.CTkTextbox(self.frame_resultado, height=120, font=("Arial", 13))
        self.txt_explicacao.pack(fill=tk.X, padx=10, pady=10)
        self.txt_explicacao.insert("0.0", "Insira os valores e clique em Calcular.")

        # Container para o gráfico do Matplotlib
        self.frame_grafico = ctk.CTkFrame(self.frame_resultado)
        self.frame_grafico.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Inicializa a figura do Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def criar_campo_entrada(self, texto, valor_padrao):
        ctk.CTkLabel(self.frame_controle, text=texto).pack(anchor="w", padx=20)
        entrada = ctk.CTkEntry(self.frame_controle)
        entrada.insert(0, valor_padrao)
        entrada.pack(pady=2, padx=20, fill=tk.X)
        return entrada

    def mudar_cor_linha(self, escolha):
        self.cor_linha = escolha

    def mudar_cor_area(self, escolha):
        self.cor_area = escolha

    def processar_inequacao(self):
        try:
            a = float(self.txt_a.get())
            b = float(self.txt_b.get())
            c = float(self.txt_c.get())
            sinal = self.sinal_var.get()
        except ValueError:
            self.atualizar_texto("Erro: Certifique-se de preencher os coeficientes com números válidos.")
            return

        if a == 0:
            self.atualizar_texto("Erro: O coeficiente 'a' não pode ser zero em uma função do 2º grau.")
            return

        # Cálculo das Raízes (Fórmula de Bhaskara)
        delta = b**2 - 4*a*c
        raizes = []
        
        if delta > 0:
            x1 = (-b - np.sqrt(delta)) / (2*a)
            x2 = (-b + np.sqrt(delta)) / (2*a)
            raizes = sorted([x1, x2])
            texto_raizes = f"As raízes reais são: x1 = {raizes[0]:.2f} e x2 = {raizes[1]:.2f}"
        elif delta == 0:
            x1 = -b / (2*a)
            raizes = [x1]
            texto_raizes = f"A equação possui uma única raiz real dupla: x = {raizes[0]:.2f}"
        else:
            texto_raizes = "A equação não possui raízes reais."

        # Determinação do Conjunto Solução em formato de texto
        conjunto_solucao = ""
        if delta > 0:
            x1, x2 = raizes[0], raizes[1]
            if (sinal == ">" and a > 0) or (sinal == "<" and a < 0):
                conjunto_solucao = f"S = {{x ∈ ℝ | x < {x1:.2f} ou x > {x2:.2f}}}"
            elif (sinal == ">=" and a > 0) or (sinal == "<=" and a < 0):
                conjunto_solucao = f"S = {{x ∈ ℝ | x ≤ {x1:.2f} ou x ≥ {x2:.2f}}}"
            elif (sinal == "<" and a > 0) or (sinal == ">" and a < 0):
                conjunto_solucao = f"S = {{x ∈ ℝ | {x1:.2f} < x < {x2:.2f}}}"
            elif (sinal == "<=" and a > 0) or (sinal == ">=" and a < 0):
                conjunto_solucao = f"S = {{x ∈ ℝ | {x1:.2f} ≤ x ≤ {x2:.2f}}}"
        elif delta == 0:
            x1 = raizes[0]
            if (sinal == ">" and a > 0) or (sinal == "<" and a < 0):
                conjunto_solucao = f"S = {{x ∈ ℝ | x ≠ {x1:.2f}}}"
            elif (sinal == ">=" and a > 0) or (sinal == "<=" and a < 0):
                conjunto_solucao = "S = ℝ (Toda a reta real)"
            elif (sinal == "<" and a > 0) or (sinal == ">" and a < 0):
                conjunto_solucao = "S = ∅ (Não há solução real)"
            elif (sinal == "<=" and a > 0) or (sinal == ">=" and a < 0):
                conjunto_solucao = f"S = {{{x1:.2f}}}"
        else: # delta < 0
            if (sinal in [">", ">="] and a > 0) or (sinal in ["<", "<="] and a < 0):
                conjunto_solucao = "S = ℝ (Toda a reta real)"
            else:
                conjunto_solucao = "S = ∅ (Não há solução real)"

        # Montagem do texto explicativo final
        texto_final = f"{texto_raizes}\n\nPara a inequação: {a}x² + ({b})x + ({c}) {sinal} 0\n\nConjunto Solução: {conjunto_solucao}"
        self.atualizar_texto(texto_final)

        # Plotagem do Gráfico
        self.plotar_grafico(a, b, c, raizes, sinal)

    def atualizar_texto(self, texto):
        self.txt_explicacao.delete("0.0", tk.END)
        self.txt_explicacao.insert("0.0", texto)

    def plotar_grafico(self, a, b, c, raizes, sinal):
        self.ax.clear()

        # Definição do intervalo do eixo X dinamicamente baseado nas raízes
        if len(raizes) == 2:
            margem = (raizes[1] - raizes[0]) * 0.5 or 1.0
            x = np.linspace(raizes[0] - margem, raizes[1] + margem, 500)
        elif len(raizes) == 1:
            x = np.linspace(raizes[0] - 5, raizes[0] + 5, 500)
        else:
            x_vertice = -b / (2*a)
            x = np.linspace(x_vertice - 5, x_vertice + 5, 500)

        y = a*x**2 + b*x + c

        # Desenhar a curva da função
        self.ax.plot(x, y, color=self.cor_linha, linewidth=2.5, label=f"f(x) = {a}x² + {b}x + {c}")

        # Identificação da máscara lógica para preencher as áreas que resolvem a inequação
        if sinal == ">":
            condicao = y > 0
        elif sinal == ">=":
            condicao = y >= 0
        elif sinal == "<":
            condicao = y < 0
        elif sinal == "<=":
            condicao = y <= 0

        # Pintar as áreas que satisfazem a condição
        self.ax.fill_between(x, y, where=condicao, color=self.cor_area, alpha=0.3, label="Área Solução")

        # Linhas de referência (eixos x e y)
        self.ax.axhline(0, color='black', linewidth=1.2, linestyle='--')
        self.ax.axvline(0, color='black', linewidth=1.2, linestyle='--')

        # Destacar raízes com pontos vermelhos no gráfico se existirem
        for r in raizes:
            self.ax.plot(r, 0, marker="o", color="red", markersize=6)
            self.ax.text(r, 0.5, f" {r:.2f}", color="black", weight="bold")

        self.ax.set_title("Análise Visual da Inequação", fontsize=12, pad=10)
        self.ax.grid(True, linestyle=':', alpha=0.6)
        self.ax.legend()
        
        # Atualiza o canvas no Tkinter
        self.canvas.draw()

if __name__ == "__main__":
    app = AppInequacoes()
    app.mainloop()