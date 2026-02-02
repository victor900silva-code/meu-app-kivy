[app]
# (str) Título do seu aplicativo
title = Meu App Python

# (str) Nome do pacote (sem espaços)
package.name = meuapp

# (str) Domínio do pacote (ex: org.test)
package.domain = org.seuusuario

# (str) Nome do arquivo principal
source.include_exts = py,png,jpg,kv,atlas

# (list) Versão do seu app
version = 0.1

# (list) Requisitos (adicione bibliotecas aqui, ex: kivy, requests)
requirements = python3,kivy

# (str) Orientação (landscape, portrait ou all)
orientation = portrait

# (bool) Indicar se o app deve rodar em tela cheia
fullscreen = 0

# (list) Permissões do Android
android.permissions = INTERNET

# (int) Nível do API Android (33 é o padrão atual para Play Store)
android.api = 33
android.minapi = 21

[buildozer]
# (int) Log level (1 = error, 2 = info, 4 = debug)
log_level = 2
