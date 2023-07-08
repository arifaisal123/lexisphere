from __future__ import print_function
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from flask import Flask, redirect, render_template, request
from dotenv import load_dotenv
from PyMultiDictionary import MultiDictionary, DICT_WORDNET, DICT_THESAURUS
from googletrans import Translator
import requests
import json
import os
from gtts import gTTS
import gtts
from io import BytesIO
import pygame

# Configure application
app = Flask(__name__)

# load_dotenv("../.env")
api_key = os.environ.get("API_KEY")
owner_email = os.environ.get("OWNER_EMAIL")

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

        if not synonym:
            is_empty = True
        else:
            is_empty = False

        return render_template("synonym.html", word=word, synonym=synonym, is_empty=is_empty)
    else:
        return render_template("synonym.html")
    

@app.route("/antonym", methods=["GET", "POST"])
def antonym():
    if request.method == "POST":
        word = request.form["antonym"]
        antonym = dictionary.antonym('en', word)

        if not antonym:
            is_empty = True
        else:
            is_empty = False

        return render_template("antonym.html", word=word, antonym=antonym, is_empty=is_empty)
    else:
        return render_template("antonym.html")
    

@app.route("/translation", methods=["GET", "POST"])
def translation():
    if request.method == "POST":
        user_lang = request.form["language"][0:2]
        user_tld = request.form["language"][2:]
        if user_lang == "zh":
            user_lang = "zh-cn"
            user_tld = "cn"
        text = request.form["translation"]

        translator = Translator()
        translation = translator.translate(text, dest=user_lang)
        translated_text = translation.text

        try:
            tts = gTTS(translated_text, lang=user_lang, tld=user_tld)
        except:
            tts = gTTS(translated_text, lang="en", tld="us")

        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)

        pygame.mixer.init()
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        pygame.mixer.quit()
       
        return render_template("translation.html", translated_text=translated_text)
    else:
        return render_template("translation.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/credits")
def credits():
    return render_template("credits.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = api_key
        
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        subject = "Feedback from customer at lexisphere"
        sender = {"name":name,"email":email}
        html_content = f"<html><body>{message}</body></html>"
        to = [{"email": owner_email,"name":"Lexisphere"}]
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)

        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            print(api_response)
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
        
        return render_template("sendform.html")
    else:
        return render_template("contact.html")
  
@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html")
