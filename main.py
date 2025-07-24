# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sala_leitura.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelos do banco
class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, default=1)

class Emprestimo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_aluno = db.Column(db.String(100), nullable=False)
    sala_aluno = db.Column(db.String(50), nullable=False)
    livro_id = db.Column(db.Integer, db.ForeignKey('livro.id'), nullable=False)
    data_devolucao = db.Column(db.String(50), nullable=False)

    livro = db.relationship('Livro')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'nome_aluno' in request.form:
            livro_id = int(request.form['livro_id'])
            livro = Livro.query.get(livro_id)

            if livro and livro.quantidade > 0:
                emprestimo = Emprestimo(
                    nome_aluno=request.form['nome_aluno'],
                    sala_aluno=request.form['sala_aluno'],
                    livro_id=livro_id,
                    data_devolucao=request.form['data_devolucao']
                )
                livro.quantidade -= 1
                db.session.add(emprestimo)
                db.session.commit()

        elif 'titulo_livro' in request.form:
            novo_livro = Livro(
                titulo=request.form['titulo_livro'],
                autor=request.form['autor_livro'],
                quantidade=int(request.form['quantidade_livro'])
            )
            db.session.add(novo_livro)
            db.session.commit()

        return redirect(url_for('index'))

    pesquisa = request.args.get('pesquisar')
    if pesquisa:
        livros = Livro.query.filter(Livro.titulo.ilike(f"%{pesquisa}%")).all()
    else:
        livros = Livro.query.all()

    emprestimos = Emprestimo.query.all()
    return render_template('index.html', livros=livros, emprestimos=emprestimos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
