import sqlite3
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

# ---------- FUNÇÃO PARA DEFINIR O CAMINHO DO BANCO NO ANDROID ----------
def get_db_path():
    # Esta função identifica se o app está no Android ou PC e define a pasta correta
    app = App.get_running_app()
    if app:
        # 'user_data_dir' é a pasta segura onde o Android permite salvar o banco
        path = app.user_data_dir
    else:
        path = "."
    return os.path.join(path, 'banco.db')

# ---------- BANCO ----------
def criar_banco():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT UNIQUE,
            senha TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS treinos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            nome TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------- TELA LOGIN ----------
class TelaLogin(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        self.add_widget(Label(text='Login', font_size=24))

        self.email = TextInput(hint_text='Email', multiline=False)
        self.senha = TextInput(hint_text='Senha', password=True, multiline=False)

        self.add_widget(self.email)
        self.add_widget(self.senha)

        btn_login = Button(text='Entrar', size_hint_y=None, height=50)
        btn_login.bind(on_press=self.login)
        self.add_widget(btn_login)

        btn_cadastro = Button(text='Criar usuário', size_hint_y=None, height=50)
        btn_cadastro.bind(on_press=self.ir_cadastro)
        self.add_widget(btn_cadastro)

        self.msg = Label(text='')
        self.add_widget(self.msg)

    def login(self, instance):
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, nome FROM usuarios WHERE email=? AND senha=?",
            (self.email.text, self.senha.text)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            app = App.get_running_app()
            app.root.clear_widgets()
            app.root.add_widget(TelaUsuario(user[0], user[1]))
        else:
            self.msg.text = 'Email ou senha inválidos'

    def ir_cadastro(self, instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(TelaCadastro())


# ---------- TELA CADASTRO ----------
class TelaCadastro(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        self.add_widget(Label(text='Criar Usuário', font_size=24))

        self.nome = TextInput(hint_text='Nome', multiline=False)
        self.email = TextInput(hint_text='Email', multiline=False)
        self.senha = TextInput(hint_text='Senha', password=True, multiline=False)

        self.add_widget(self.nome)
        self.add_widget(self.email)
        self.add_widget(self.senha)

        btn = Button(text='Cadastrar', size_hint_y=None, height=50)
        btn.bind(on_press=self.cadastrar)
        self.add_widget(btn)

        self.msg = Label(text='')
        self.add_widget(self.msg)

    def cadastrar(self, instance):
        try:
            conn = sqlite3.connect(get_db_path())
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                (self.nome.text, self.email.text, self.senha.text)
            )

            conn.commit()
            conn.close()

            app = App.get_running_app()
            app.root.clear_widgets()
            app.root.add_widget(TelaLogin())

        except sqlite3.IntegrityError:
            self.msg.text = 'Email já cadastrado'


# ---------- TELA USUÁRIO ----------
class TelaUsuario(BoxLayout):
    def __init__(self, usuario_id, nome_usuario, **kwargs):
        super().__init__(**kwargs)
        self.usuario_id = usuario_id
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        self.add_widget(Label(
            text=f'Bem-vindo, {nome_usuario}',
            font_size=22
        ))

        self.treino_nome = TextInput(
            hint_text='Nome do treino',
            multiline=False
        )
        self.add_widget(self.treino_nome)

        btn = Button(text='Cadastrar treino', size_hint_y=None, height=50)
        btn.bind(on_press=self.cadastrar_treino)
        self.add_widget(btn)

        scroll = ScrollView()
        self.lista = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None
        )
        self.lista.bind(minimum_height=self.lista.setter('height'))

        scroll.add_widget(self.lista)
        self.add_widget(scroll)

        self.carregar_treinos()

    def cadastrar_treino(self, instance):
        if self.treino_nome.text.strip() == '':
            return

        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO treinos (usuario_id, nome) VALUES (?, ?)",
            (self.usuario_id, self.treino_nome.text)
        )

        conn.commit()
        conn.close()

        self.treino_nome.text = ''
        self.carregar_treinos()

    def carregar_treinos(self):
        self.lista.clear_widgets()

        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()

        cursor.execute(
            "SELECT nome FROM treinos WHERE usuario_id=?",
            (self.usuario_id,)
        )
        treinos = cursor.fetchall()
        conn.close()

        if not treinos:
            self.lista.add_widget(Label(text='Nenhum treino cadastrado'))
            return

        for treino in treinos:
            self.lista.add_widget(Label(text=f'🏋️ {treino[0]}'))


# ---------- APP ----------
class MeuApp(App):
    def build(self):
        criar_banco()
        root = BoxLayout()
        root.add_widget(TelaLogin())
        return root


if __name__ == '__main__':
    MeuApp().run()







