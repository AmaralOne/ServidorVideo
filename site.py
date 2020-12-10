from flask import Flask
import random
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os


'''
  Base de dados "aleatoria" utilizada
'''
v_name = ["","Bailarina","Futebol","Estátua","Pintor","Frio","Bebê","Mímico","Escova de dentes","Lápis","Livro"]
v_descr = ["","Bailarina dancante","Futebol de rua","Estátua de papelão","Pintor de privada","Frio de morrer","Bebê do João","Mímico desastrado","Escova de dentes azul","Lápis de tabuada","Livro de nárnia"]
vds = []



'''
  Classe de armazenamento dos videos -> Comunicação com o frontend  
'''
class Video:
  url = None
  descr = None
  name = None

  def __init__(self):
    return

  def __init__(self, url, descr, name):
    self.url = url
    self.descr = descr
    self.name = name


'''
  Iniciando o servidor Flash
'''
app = Flask(__name__)


'''
  Rota inicial do site: Onde é gerado os 4 videos aleatorios. Além disso é feita verificada a autenticação do usuario, caso n esteja logado
  será redirecionado para a tela de login.
'''
@app.route('/')
def home(msg="Login"):
  global vds
  for idx in range(1,len(v_name)):
    print(v_name[idx])
    vds.append(Video(url_for('static', filename='videos/v' + str(idx) + '.mp4'),
                     v_descr[idx],
                     v_name[idx]
                     ))

  url = url_for('static', filename= 'videos/v' + str(random.randint(1,10))  + '.mp4')
  descr = "teste descricao"
  name = "teste nome"

  random.shuffle(vds)

  if not session.get('logged_in'):
    return render_template('login.html', msg = msg)
  else:
    return render_template('index.html', videos = [ vds[i] for i in range(4)] )



'''
  Validação de usuario e senha
'''
@app.route('/login', methods=['POST'])
def do_admin_login():
  login = request.form

  userName = login['username']
  password = login['password']

  msg = "Login"

  session['logged_in'] = False 
  if userName == "Teste" and password == "SenhaTeste":
    session['logged_in'] = True
  else:
    msg = "Usuário ou senha incorretos!"
    flash('wrong password!')
  return home(msg)


'''
  Logout do usuario
'''
@app.route('/logout')
def logout():
  session['logged_in'] = False
  return home()

'''
  Onde é inicializado o servidor flash e é consigurado:
  - host
  - porta
'''
if __name__ == "__main__":
  app.secret_key = os.urandom(12)
  app.run(debug=False,host='127.0.0.1', port=5000)