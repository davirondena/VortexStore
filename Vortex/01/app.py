from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'chave-secreta-muito-secreta'

produtos_csgo = {
    1: {'id': 1, 'nome': 'AK-47 | Redline', 'preco': 100.00, 'imagem': 'ak_redline.jpg'},
    2: {'id': 2, 'nome': 'AWP | Dragon Lore', 'preco': 9500.00, 'imagem': 'awp_dragon_lore.jpg'},
    3: {'id': 3, 'nome': 'M4A4 | Howl', 'preco': 4500.00, 'imagem': 'm4a4_howl.jpg'},
    4: {'id': 4, 'nome': 'Glock-18 | Fade', 'preco': 1500.00, 'imagem': 'glock_fade.jpg'},
    5: {'id': 5, 'nome': 'Karambit | Doppler', 'preco': 12000.00, 'imagem': 'karambit_doppler.jpg'},
    6: {'id': 6, 'nome': 'Desert Eagle | Blaze', 'preco': 2100.00, 'imagem': 'deagle_blaze.jpg'},
    7: {'id': 7, 'nome': 'USP-S | Kill Confirmed', 'preco': 1600.00, 'imagem': 'usp_kill_confirmed.jpg'},
    8: {'id': 8, 'nome': 'Butterfly Knife | Marble Fade', 'preco': 13400.00, 'imagem': 'butterfly_marble.jpg'}
}

produtos_steam = {
    101: {'id': 101, 'nome': 'Steam Gift Card R$30', 'preco': 30.00, 'imagem': 'steamwallet.png'},
    102: {'id': 102, 'nome': 'Steam Gift Card R$50', 'preco': 50.00, 'imagem': 'steamwallet.png'},
    103: {'id': 103, 'nome': 'Steam Gift Card R$100', 'preco': 100.00, 'imagem': 'steamwallet.png'}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/steam')
def steam():
    return render_template('steam.html', produtos=produtos_steam)

@app.route('/cs2')
def cs2():
    return render_template('cs2.html', produtos=produtos_csgo)

@app.route('/dota2')
def dota2():
    return render_template('dota2.html')

@app.route('/add_carrinho/<int:produto_id>')
def add_carrinho(produto_id):
    if 'carrinho' not in session:
        session['carrinho'] = {}

    carrinho = session['carrinho']

    if str(produto_id) in carrinho:
        carrinho[str(produto_id)]['quantidade'] += 1
    else:
        # ✅ Agora busca em ambas as categorias
        produto = produtos_csgo.get(produto_id) or produtos_steam.get(produto_id)
        if produto:
            carrinho[str(produto_id)] = {
                'nome': produto['nome'],
                'preco': produto['preco'],
                'quantidade': 1
            }

    session.modified = True
    return redirect(request.referrer or url_for('index'))

@app.route('/carrinho')
def ver_carrinho():
    carrinho = session.get('carrinho', {})
    total = sum(item['preco'] * item['quantidade'] for item in carrinho.values())
    return render_template('carrinho.html', carrinho=carrinho, total=total)

@app.route('/remover/<item_id>', methods=['POST'])
def remover_item(item_id):
    carrinho = session.get('carrinho', {})

    if item_id in carrinho:
        del carrinho[item_id]
        session['carrinho'] = carrinho

    return redirect(url_for('ver_carrinho'))

if __name__ == '__main__':
    app.run(debug=True)
