#! /usr/bin/python3
from flask import Flask, render_template, request,redirect, url_for
from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
import random
import smtplib
#from chatterbot.trainers import ChatterBotCorpusTrainer
from botConfig import myBotName, chatBG, botAvatar, useGoogle, confidenceLevel



import logging
logging.basicConfig(level=logging.INFO)

application = Flask(__name__)

chatbotName = myBotName
print("Bot Name set to: " + chatbotName)
print("Confidence level set to " + str(confidenceLevel))


bot = ChatBot(
    "ChatBot",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': confidenceLevel,
            'default_response': 'IDKresponse'
        }
    ],
    response_selection_method=get_random_response, #Comment this out if you want best response
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database="botData.sqlite3"
)

bot.read_only=True #Comment this out if you want the bot to learn based on experience
print("Bot Learn Read Only:" + str(bot.read_only))

#You can comment these out for production later since you won't be training everytime:
#bot.set_trainer(ChatterBotCorpusTrainer)
#bot.train("data/trainingdata.yml")

def tryGoogle(myQuery):
	#print("<br>Try this from my friend Google: <a target='_blank' href='" + j + "'>" + query + "</a>")
	return "<br><br>You can try this from my friend Google: <a target='_blank' href='https://www.google.com/search?q=" + myQuery + "'>" + myQuery + "</a>"
def link(myQuery):
    #print("<br>Try this from my friend Google: <a target='_blank' href='" + j + "'>" + query + "</a>")
    return "Please visit this link: <a target='_blank' href='" +myQuery+"'>" + myQuery + "</a>"


def tryMail():
    print("in function")
    #print("<br>Try this from my friend Google: <a target='_blank' href='" + j + "'>" + query + "</a>")
    #return "<form method='post' action='/trial'><input type='text' name='rd'></form>"
    return "<form method='get' action='/trial'>Query:<input type='text' name='query'><br>" \
           " Email-ID:<input type='email' name='rmail'> <br>" \
           "<button type=submit>send</button> </form>"

@application.route("/")
def home():
    return render_template("index.html", botName = chatbotName, chatBG = chatBG, botAvatar = botAvatar)

@application.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    botReply = str(bot.get_response(userText))
    if botReply is "IDKresponse":
        botReply = str(bot.get_response('IDKnull')) ##Send the i don't know code back to the DB
        if useGoogle == "yes":
            botReply = botReply + tryGoogle(userText)
    elif botReply == "getTIME":
        botReply = getTime()
        print(getTime())
    elif botReply == "getDATE":
        botReply = getDate()
        print(getDate())
    elif botReply == "getMail":
        botReply = tryMail()
        print("gettttmaillll")
    elif botReply.find("http") != -1:
        print("done")
        print(botReply.find("http"))
        endstring = botReply[botReply.find("http"):]
        print(endstring)
        botReply = link(endstring)
    return botReply

@application.route("/trial")
def tryy():
    print(request.args.get('query'))
    msg=request.args.get('query')
    reciever_mail=request.args.get('rmail')
    email = smtplib.SMTP('smtp.gmail.com', 587) 
  
# TLS for security 
    email.starttls() 
  
# authentication
# compiler gives an error for wrong credential. 
    email.login("email", "password") 
  
# message to be sent 
   
  
# sending the mail 
    email.sendmail("email", reciever_mail, msg) 
  
# terminating the session 
    email.quit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    application.run()
    #application.run(host='0.0.0.0', port=5000)
