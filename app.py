from flask import Flask, render_template, request, jsonify, redirect, url_for

from models.auth import Auth
from models.users import Users
from models.words import Words

app = Flask(__name__)


@app.route('/')
def home():
    [signed, _, _] = Auth.check(request)

    if signed:
        return redirect(url_for("my_words"))

    return render_template("index.html")


@app.route('/mywords')
def my_words():
    [signed, _, _] = Auth.check(request)

    if not signed:
        return redirect(url_for("home"))

    return render_template("mywords.html")


@app.route('/quiz')
def quiz():
    [signed, _, _] = Auth.check(request)

    if not signed:
        return redirect(url_for("home"))

    return render_template("quiz.html")


@app.route('/api/login', methods=['POST'])
def login():
    user_id = request.form['user_id']
    user_passwd = request.form['user_passwd']

    [signed, token, message] = Auth.sign(user_id, user_passwd)
    return jsonify({"ok": signed, "token": token, "message": message})


@app.route('/api/signup', methods=['POST'])
def sign_up():
    user_id = request.form['user_id']
    user_name = request.form['user_name']
    user_passwd = request.form['user_passwd']

    [success, message] = Users.create(user_id, user_name, user_passwd)

    if not success:
        return jsonify({"ok": False, "message": message})

    [ok, message] = Words.dummy(user_id)
    return jsonify({"ok": ok, "message": message})


@app.route('/api/words', methods=["GET"])
def word_find():
    [signed, user_id, _] = Auth.check(request)

    if not signed:
        return redirect(url_for("home"))

    query = request.args.to_dict()
    [ok, words, message] = Words.find(user_id, query)

    return jsonify({"ok": ok, "words": words, "message": message})


@app.route('/api/words/new', methods=["POST"])
def word_insert():
    [signed, user_id, _] = Auth.check(request)

    if not signed:
        return redirect(url_for("home"))

    doc = request.form
    [ok, message] = Words.add(user_id, doc)

    return jsonify({"ok": ok, message: message})


@app.route('/api/words/<string:word_id>', methods=["PUT"])
def word_modify(word_id):
    [signed, user_id, _] = Auth.check(request)

    if not signed:
        return redirect(url_for("home"))

    doc = request.form
    [ok, message] = Words.update(user_id, word_id, doc)

    return jsonify({"ok": ok, message: message})


@app.route('/api/words/<string:word_id>', methods=["DELETE"])
def word_delete(word_id):
    [signed, user_id, _] = Auth.check(request)

    if not signed:
        return redirect(url_for("home"))

    [ok, message] = Words.delete(user_id, word_id)
    return jsonify({"ok": ok, message: message})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
