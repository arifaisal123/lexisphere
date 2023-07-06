from flask import Flask, redirect, render_template, request
from translate import Translator
from PyMultiDictionary import MultiDictionary, DICT_WORDNET, DICT_THESAURUS
import requests
import json

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configures dictionary
dictionary = MultiDictionary()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/word_meaning", methods=["GET", "POST"])
def word_meaning():
    if request.method == "POST":
        word = request.form["word_meaning"]
        word_meaning = dictionary.meaning('en', word, dictionary=DICT_WORDNET)

        try:
            if not word_meaning[0]:
                is_empty = True
        except:
            is_empty = False

        return render_template("word_meaning.html", word_meaning=word_meaning, is_empty=is_empty)
    else:
        return render_template("word_meaning.html")


@app.route("/synonym", methods=["GET", "POST"])
def synonym():
    if request.method == "POST":
        word = request.form["synonym"]
        synonym = dictionary.synonym("en", word)
        return render_template("synonym.html", synonym=synonym)
    else:
        return render_template("synonym.html")
    

@app.route("/antonym", methods=["GET", "POST"])
def antonym():
    if request.method == "POST":
        word = request.form["antonym"]
        antonym = dictionary.antonym('en', word)
        return render_template("antonym.html", antonym=antonym)
    else:
        return render_template("antonym.html")
    

@app.route("/translation", methods=["GET", "POST"])
def translation():
    if request.method == "POST":
        lang = request.form["language"]
        text = request.form["translation"]

        translator= Translator(to_lang=lang)
        translation = translator.translate(text)
        return render_template("translation.html", translation=translation)
    else:
        return render_template("translation.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/credits")
def credits():
    return render_template("credits.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/sendform", methods=["GET", "POST"])
def sendform():
    return render_template("sendform.html")

@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html")