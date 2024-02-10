from flask import Flask,render_template,request,redirect,send_from_directory,url_for
from pytube import YouTube
import os
import time
from datetime import datetime
import re


app = Flask(__name__)

Pasta = os.path.join('static', 'downloads')


def eh_link_youtube(url):
    padrao_youtube = re.compile(
        r'(https?://)?(www\.)?'
        r'(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/).+'
    )
    return bool(padrao_youtube.match(url))

def limpar_arquivos_antigos(diretorio, idade_maxima_em_minutos):
    tempo_atual = time.time()
    idade_maxima_em_segundos = idade_maxima_em_minutos * 60
    for arquivo in os.listdir(diretorio):
        caminho_arquivo = os.path.join(diretorio, arquivo)
        if os.path.isfile(caminho_arquivo):
            idade_arquivo = tempo_atual - os.path.getmtime(caminho_arquivo)
            if idade_arquivo > idade_maxima_em_segundos:
                try:
                    os.remove(caminho_arquivo)
                    print(f"Arquivo {arquivo} removido com sucesso.")
                except Exception as e:
                    print(f"Erro ao remover o arquivo {arquivo}: {e}")

@app.route('/')
def home():
    limpar_arquivos_antigos(Pasta, 1)
    return render_template("index.html")

@app.route('/verlink',methods=['GET','POST'])
def ver():
    if request.method == 'POST':
        link = request.form['link']
        Verifica = eh_link_youtube(link)
        if Verifica:
            yt = YouTube(link)
            video = yt.streams.get_highest_resolution()
            localdoDownload = video.download(output_path=Pasta)
            novo_nome_arquivo = datetime.now().strftime("%Y%m%d%H%M%S") + ".mp4"
            novo_caminho = os.path.join(Pasta, novo_nome_arquivo)
            os.rename(localdoDownload, novo_caminho)
            return redirect("/download/" + novo_nome_arquivo)
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/download/<nome>')
def download(nome):
    pastaPusuario = os.path.join(app.root_path, 'static', 'downloads')
    return  send_from_directory(pastaPusuario, nome, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
