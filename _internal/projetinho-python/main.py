import customtkinter as ctk
import tkinter as tk
from tkinter import PhotoImage,filedialog,messagebox
from tkinter import ttk
import shutil
import sqlite3
import xml.etree.ElementTree as ET

class documnets:
    documento_de_autorizacao = '''
Documento de Autorização para Cultivo de Planta

[Nome do Proprietário/Responsável pela Propriedade]

[Endereço da Propriedade]

[Cidade, Estado, CEP]

[Data]

Eu, [Seu Nome], doravante referido como "Autorizador", concedo autorização a [Nome do Autorizado], doravante referido como "Autorizado", 
para cultivar a planta identificada como:

Nome da Planta: [Nome da Planta]

Descrição: [Descrição da Planta]

A autorização é concedida sob as seguintes condições:

Local de Cultivo: O Autorizado está autorizado a cultivar a planta apenas no seguinte local: [Descrição do Local].

Finalidade: A autorização é concedida estritamente para fins [uso específico, por exemplo, ornamental, pesquisa, etc.].

Conformidade Legal: O Autorizado concorda em cumprir todas as leis locais, estaduais e federais relacionadas ao cultivo da planta, 
incluindo a obtenção de licenças e permissões necessárias.

Responsabilidades: O Autorizado assume total responsabilidade pelo cuidado, manutenção e custos associados ao cultivo da planta.

Duração da Autorização: A presente autorização é válida a partir de [Data de Início] até [Data de Término], 
a menos que seja revogada anteriormente por escrito pelo Autorizador.

Revogação da Autorização: O Autorizador reserva o direito de revogar esta autorização a qualquer momento, 
por qualquer motivo, mediante aviso por escrito ao Autorizado.

Este documento é uma declaração de autorização voluntária 
e não exime o Autorizado de qualquer responsabilidade legal ou penal que possa surgir do cultivo da planta.

Assinatura do Autorizador: ____________________________

Nome Impresso do Autorizador: ____________________________

Assinatura do Autorizado: ____________________________

Nome Impresso do Autorizado: ____________________________
'''

    documento_resposabilidade = '''
        Documento de Responsabilidade para Cultivo de Planta

[Nome do Responsável]

[Endereço do Responsável]

[Cidade, Estado, CEP]

[Data]

Eu, [Seu Nome], doravante referido como "Responsável", concordo em assumir total responsabilidade pelo cultivo da planta identificada como:

Nome da Planta: [Nome da Planta]

Descrição: [Descrição da Planta]

Declaro que compreendo e concordo com as seguintes responsabilidades:

Cuidado Adequado: Comprometo-me a fornecer os cuidados necessários para garantir o crescimento saudável da planta, 
incluindo água, luz solar adequada, solo apropriado, e qualquer outra necessidade específica da planta.

Manutenção: Assumo a responsabilidade pela manutenção regular da planta, incluindo poda, 
fertilização e quaisquer outras práticas culturais necessárias.

Conformidade Legal: Garanto que o cultivo da planta está em conformidade com todas as leis locais, 
estaduais e federais aplicáveis. Isso inclui a obtenção de todas as licenças necessárias para o cultivo da planta, se aplicável.

Impacto Ambiental: Comprometo-me a minimizar qualquer impacto ambiental negativo associado ao cultivo da planta, 
incluindo o descarte adequado de resíduos.

Responsabilidade Civil: Reconheço que sou o único responsável por quaisquer danos causados por minha negligência no cultivo 
da planta a terceiros ou à propriedade de terceiros.

Este documento é uma declaração de responsabilidade voluntária e não exime o Responsável de qualquer responsabilidade 
legal ou penal que possa surgir do cultivo da planta.

Assinatura: ____________________________

Nome Impresso: _________________________

'''

class Main:
    def __init__(self):
        self.window =ctk.CTk()
        self.window.title('ECOFY - SOFTWARE')
        self.configuracoes(self.window,1200,580)
        self.dados = ET.Element('Dados')
        self.nav()
        self.container()
        self.window.mainloop()    

    def configuracoes(self,window,width,height):
        self.window.config(bg = '#081C15')
        self.window.resizable(False,False)
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calcula as coordenadas para centralizar a janela
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Define a geometria da janela
        window.geometry(f'{width}x{height}+{x}+{y}')

    # funtions auxiliares

    def deleteW(self,window):
        for widget in window.winfo_children():
            widget.destroy()

    def downloadAutorizacao(self):
        self.caminho_do_arquivo = 'Archive/Autorizacao.pdf'
        self.local_de_destino = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Arquivos PDF", "*.pdf")])
        if self.local_de_destino:
            shutil.copy(self.caminho_do_arquivo, self.local_de_destino)
    def downloadResponsabilidade(self):
        self.caminho_do_arquivo = 'Archive/Termo_responsabilidade.pdf'
        self.local_de_destino = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Arquivos PDF", "*.pdf")])
        if self.local_de_destino:
            shutil.copy(self.caminho_do_arquivo, self.local_de_destino)

    def crud(self):
        if self.entry_nome.get() and self.entry_endereco.get() and self.entry_telefone.get() and self.variavel_controle_de_contemplado.get():
            name = self.entry_nome.get()
            endereco = self.entry_endereco.get()
            telefone = self.entry_telefone.get()
            classificacao = float(self.variavel_controle_de_contemplado.get())

            con = sqlite3.connect('dll.db')
            cursor = con.cursor()

            try:

                cursor.execute("INSERT INTO dados_dll VALUES(?,?,?,?)",(name,endereco,telefone,classificacao))
                self.entry_nome.delete(0,tk.END)
                self.entry_endereco.delete(0,tk.END)
                self.entry_telefone.delete(0,tk.END)

            except:
                messagebox.showerror(title='ERROR',message='Ocorreu um erro ao cadastrar o usuario')
            con.commit()
        else:
            messagebox.showwarning(title='Campos Vazios ',message='Há algum Campo faltando preecha-os e tente novamente')

    def xml_action_start(self):
        nome = self.nome_dados_item.get()
        emissor = self.nome_dados_emissor.get()
        quantidade = self.nome_dados_Quantidade.get()
        contemplado = self.nome_dados_contemplado.get()

        self.informacoes = ET.SubElement(self.dados,'informacoes')

        ET.SubElement(self.informacoes,'titulo').text = 'EMISSOR'
        ET.SubElement(self.informacoes,'emissor').text = emissor
        ET.SubElement(self.informacoes,'titulo').text = 'QUANTIDADE'
        ET.SubElement(self.informacoes,'quantidade').text = str(quantidade)
        ET.SubElement(self.informacoes,'titulo').text = 'CONTENPLADO'
        ET.SubElement(self.informacoes,'contemplado').text = contemplado
        ET.SubElement(self.informacoes,'titulo').text = 'PLANTA/ESPECIE'
        ET.SubElement(self.informacoes,'especie').text = nome

        tree = ET.ElementTree(self.dados)

        file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("Arquivos XML", "*.xml")])
        if file_path:
            # Salvar a nota fiscal no arquivo XML
            tree.write(file_path)

            # Informar ao usuário que a nota fiscal foi gerada e salva
            tk.messagebox.showinfo("Nota Fiscal Gerada", "Nota fiscal gerada e salva com sucesso!")





    def xml_auto(self,event):
        if self.nome_dados_item.get() and self.nome_dados_emissor.get() and self.nome_dados_Quantidade.get() and self.nome_dados_contemplado.get():
                self.imprimir_nota = ctk.CTkButton(self.container_root,text='IMPRIMIR NOTA',fg_color='#2d6a4f',font=('Inria Sans',14,'bold'),text_color='#FFFFFF',width=230,height=40,command=self.xml_action_start)
                self.imprimir_nota.place(x=570,y=500)

    # componentes

    def nav(self):
        try:
            self.nav_menu = PhotoImage(file='path/backgroud-bar.png')
            self.frame_nav = tk.Frame(self.window,background='#081C15',width=245)
            self.frame_nav.place(x=0,relheight=1)
            self.imagem_nav = tk.Label(self.frame_nav,image=self.nav_menu,background='#081c15')
            self.imagem_nav.place(x=0,y=318)
        except:
            self.frame_nav = tk.Frame(self.window,background='#081C15',width=245)
            self.frame_nav.place(x=0,relheight=1)

        self.button_requeriment0_nav = ctk.CTkButton(self.frame_nav,text='REQUERIMENTO',fg_color='#081C15',font=('Inria Sans',20,'bold','italic'),text_color='#FFFFFF',command=self.container)
        self.button_relatorio_nav = ctk.CTkButton(self.frame_nav,text='RELATÓRIOS',fg_color='#081C15',font=('Inria Sans',20,'bold','italic'),text_color='#FFFFFF',command=self.relatorios)
        self.button_requeriment0_nav.place(x=35,y=100)
        self.button_relatorio_nav.place(x=50,y=150)

    def container(self):
        self.container_root = tk.Frame(self.window,bg='#FFFFFF',width=955)
        self.container_root.place(x=246,relheight=1,relwidth=1)
        self.title_page_requerimento = ctk.CTkLabel(self.container_root,text='REQUERIMENTO',font=('Inria Sans',24,'bold'))
        self.title_page_requerimento.place(x=70,y=24)

        self.imageDecorator = PhotoImage(file='path/path-icons/line-bar.png')
        self.decorator = tk.Label(self.container_root,image=self.imageDecorator,background='#FFFFFF')
        self.decorator.place(x=10,y=74)

        self.title_dados_pessoais = ctk.CTkLabel(self.container_root,text='DADOS PESSOAIS',font=('Inria Sans',20,'bold', 'italic'))
        self.title_dados_pessoais.place(x=70,y=123)
        self.entry_nome = ctk.CTkEntry(self.container_root,placeholder_text='NOME',width=422,height=40)
        self.entry_endereco = ctk.CTkEntry(self.container_root,placeholder_text='ENDEREÇO',width=446,height=40)
        self.entry_telefone = ctk.CTkEntry(self.container_root,placeholder_text='TEL',width=265,height=40)

        self.entry_nome.place(x=70,y=177)
        self.entry_endereco.place(x=70,y=234)
        self.entry_telefone.place(x=70,y=297)

        self.variavel_controle_de_contemplado = tk.IntVar(value=0)
        self.opOne = ctk.CTkRadioButton(self.container_root,text='CONTEMPLADO ATIVO',variable=self.variavel_controle_de_contemplado,value=1)
        self.opTwo = ctk.CTkRadioButton(self.container_root,text='CONTEMPLADO PARCIAL',variable=self.variavel_controle_de_contemplado,value=2)

        self.opOne.place(x=70,y=370)
        self.opTwo.place(x=70,y=401)

        self.button_g_requerimento = ctk.CTkButton(self.container_root,text='GERAR REQUERIMENTO',font=('Inria Sans',14,'bold'),text_color='#FFFFFF',width=252,height=38,fg_color='#2d6a4f',command=self.crud)
        self.button_g_requerimento.place(x=70,y=500)

        self.label_dados_impressao = ctk.CTkLabel(self.container_root,text='DADOS IMPRESSÃO',font=('Inria Sans',20,'italic','bold'))
        self.nome_dados_item = ctk.CTkEntry(self.container_root,placeholder_text='NOME DA ESPÉCIE',width=281,height=40)
        self.nome_dados_Quantidade = ctk.CTkEntry(self.container_root,placeholder_text='QUANTIDADE',width=167,height=40)
        self.nome_dados_contemplado = ctk.CTkEntry(self.container_root,placeholder_text='CONTEMPLADO',width=281,height=40)
        self.nome_dados_emissor = ctk.CTkEntry(self.container_root,placeholder_text='EMISSOR',width=281,height=40)
        self.label_dados_impressao.place(x=570,y=123)
        self.nome_dados_item.place(x=570,y=168)
        self.nome_dados_Quantidade.place(x=570,y=220)
        self.nome_dados_contemplado.place(x=570,y=270)
        self.nome_dados_emissor.place(x=570,y=326)

        self.window.bind("<KeyRelease>",self.xml_auto)

    def item_selecionado(self,event):
        titulo = None
        dados = None
        nivel = None
        item_selecionado = self.arvore.focus()
        if item_selecionado == 'item2':
            titulo = self.dados_autorizacao['titulo']
            dados = self.dados_autorizacao['dados']
            nivel = self.dados_autorizacao['nivel']
            self.label_text_document.configure(text=f'{documnets.documento_de_autorizacao}',font=('Inria Sans',4),fg='#000000')
            self.label_text_document.place(x=0)
            self.titulo_value.config(text=f'{titulo}')
            self.dados_value.config(text=f'{dados}')
            self.nivel_value.config(text=f'{nivel}')
            self.caminho_do_arquivo = 'Archive/Autorizacao.pdf'
            self.button_gerar_relatorio = ctk.CTkButton(self.container_root,text='DOWNLOAD',width=269,height=40,fg_color='#2D6A4F',command=self.downloadAutorizacao)
            self.button_gerar_relatorio.place(x=600,y=500)

        elif item_selecionado == 'item3':
            titulo = self.dados_responsabilidade['titulo']
            dados = self.dados_responsabilidade['dados']
            nivel = self.dados_responsabilidade['nivel']

            self.label_text_document.configure(text=f'{documnets.documento_resposabilidade}',font=('Inria Sans',4),fg='#000000')
            self.label_text_document.place(x=0)

            self.titulo_value.config(text=f'{titulo}')
            self.dados_value.config(text=f'{dados}')
            self.nivel_value.config(text=f'{nivel}')

            self.button_gerar_relatorio = ctk.CTkButton(self.container_root,text='DOWNLOAD',width=269,height=40,fg_color='#2D6A4F',command=self.downloadResponsabilidade)
            self.button_gerar_relatorio.place(x=600,y=500)
        else:
            self.label_text_document.configure(text='(Vazio)',font=('Inria Sans',14),fg='#778da9')
            self.label_text_document.place(x=100)

            self.titulo_value.config(text=f'...')
            self.dados_value.config(text=f'...')
            self.nivel_value.config(text=f'...')
            self.caminho_do_arquivo = 'Archive/Termo_responsabilidade.pdf'

        if self.caminho_do_arquivo == '':
            messagebox.showerror(title='ERROR',message='Selecione um documento para download')

    def relatorios(self):
        self.deleteW(self.container_root)

        self.title_page_relatoriosD = ctk.CTkLabel(self.container_root,text='RELATÓRIOS',font=('Inria Sans',24,'bold'))
        self.title_page_relatoriosD.place(x=70,y=24)
        self.imageDecoratorD = PhotoImage(file='path/path-icons/line-bar.png')
        self.decoratorD = tk.Label(self.container_root,image=self.imageDecorator,background='#FFFFFF')
        self.decoratorD.place(x=10,y=74)

        self.arvore = ttk.Treeview(self.container_root)

        self.arvore.place(x=20,y=120,height=385,width=205)


        self.arvore.insert('','0','item1',text='Documentos')
        self.arvore.insert('','1','item5',text='Publicos')

        self.arvore.insert('','end','item3',text='Responsabilidade')
        self.arvore.insert('','end','item2',text='Autorização')
        self.arvore.insert('','end','item6',text='(vazio)')


        self.arvore.move('item2','item1','end')
        self.arvore.move('item3','item1','end')
        self.arvore.move('item6','item5','end')

        self.arvore.bind('<<TreeviewSelect>>',self.item_selecionado)

        self.titulo_documento = ctk.CTkLabel(self.container_root,text='TITULO:',font=('Inria Sans',14,'bold'))
        self.titulo_dados = ctk.CTkLabel(self.container_root,text='DADOS:',font=('Inria Sans',14,'bold'))
        self.titulo_nivel = ctk.CTkLabel(self.container_root,text='NÍVEL:',font=('Inria Sans',14,'bold'))
        self.titulo_documento.place(x=235,y=120)
        self.titulo_dados.place(x=235,y=150)
        self.titulo_nivel.place(x=235,y=300)

        self.frame_documento = ctk.CTkFrame(self.container_root,width=267,height=357)
        self.frame_documento.place(x=600,y=120)



        self.label_text_document = tk.Label(self.frame_documento,text='',font=('Inria Sans',4),justify='left',background='#D9D9D9')
        self.label_text_document.place(y=180,anchor='w')

        self.titulo_deapresentacao = ctk.CTkLabel(self.frame_documento,text='DOCUMENTO DE APRESENTAÇÃO', font=('Inria Sans',10,'bold'))
        self.titulo_deapresentacao.place(anchor='center',y=20,x=134)

        self.dados_autorizacao = {'titulo': 'Documento de Autorização','dados':'Um documento de autorização geralmente \ncontém informações como a identificação das partes envolvidas,\n a descrição clara da autorização concedida, \ncondições e restrições,\n a finalidade da autorização, data e duração,\n assinaturas das partes e cláusulas legais pertinentes.','nivel':'Categórico'}
        self.dados_responsabilidade = {'titulo': 'Documento de Responsabilidade','dados':'Um termo de responsabilidade é um documento que\n estabelece e esclarece as responsabilidades e obrigações \nde uma pessoa ou entidade em relação a uma atividade, \nsituação ou propriedade específica.','nivel':'Comprometimento'}

        self.titulo_value = tk.Label(self.container_root,text='...',font=('Inria Sans',9,'bold'),bg='#FFFFFF')
        self.dados_value = tk.Label(self.container_root,text='...',font=('Inria Sans',9),bg='#FFFFFF',justify='left')
        self.nivel_value = tk.Label(self.container_root,text='...',font=('Inria Sans',9,'bold'),bg='#FFFFFF',)

        self.titulo_value.place(x=300,y=123)
        self.dados_value.place(x=235,y=180)
        self.nivel_value.place(x=300,y=303)







if __name__ == '__main__':
 Main()




