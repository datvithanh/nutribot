from flask import Flask, request
from pymessenger import Bot
import random
import ibm_watson
from utils import entity_to_nutri, get_nparr

app = Flask(__name__, static_folder='static')

app.config.from_pyfile('configs/constants.py')

bot = Bot(app.config['FACEBOOK_ACCESS_TOKEN'])

assistant = ibm_watson.AssistantV1(
    version='2019-02-28',
    iam_apikey=app.config['ASSISTANT_API_KEY'],
    url=app.config['ASSISTANT_URL']
)

nparr = get_nparr()
nparr = [tmp[0] for tmp in nparr]

@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    print(message['message'].get('text'))

                    response = assistant.message(
                        workspace_id=app.config['ASSISTANT_WORKSPACE_ID'],
                        input={
                            'text': message['message'].get('text')
                        }
                    ).get_result()

                    # response_sent_text = get_message()

                    entities = [tmp['entity'] for tmp in response['entities'] if tmp['entity'] in nparr]

                    if len(entities) > 0:
                        response_sent_text = entity_to_nutri(entities[0])
                    else:
                        response_sent_text = 'Xin lỗi, tôi không hiểu yêu cầu của bạn'
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == app.config['FACEBOOK_VERIFY_TOKEN']:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["message received"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=True)