import os
from datetime import datetime
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()


#client = MongoClient(os.getenv('CONNECTION_STRING'))
client = MongoClient(os.getenv('CONNECTION_STRING'), tlsCAFile=certifi.where())
db = client[os.getenv('DB_NAME')]
collection_perm = db[os.getenv('COLLECTION_NAME_Permanent')]
collection_temp = db[os.getenv('COLLECTION_NAME_Temporary')]



def create_user_perm(user: dict) -> bool:
    '''
    Create a new user

    Parameters:
        - user(dict)

    Returns:
        - bool, 0 for failure and 1 for success
    '''

    result = collection_perm.find_one(
        {
            'participant_id': user['participant_id']
        }
    )

    if not result:
        result = collection_perm.insert_one(user)
        return result.acknowledged
    return False


def insert_message_perm(participant_id: int, message: dict) -> bool:
    '''
    Update messages for the user
    this is the function which stores messages

    Parameters:
        - participant_id(int): user telegram id
        - message(dict): mesage document to insert

    Returns:
        - bool, 0 for failure and 1 for success
    '''

    result = collection_perm.find_one_and_update(
        {
            'participant_id': participant_id
        },
        {
            '$push': {
                'messages': message
            }
        }
    )

    if not result:
        return False
    else:
        return True


def save_message_to_db_perm(prompt: str, response: str, participant_id: int, participant_mail:str) -> bool:


    message = {
        'user': prompt,
        'assistant': response,
        'created_at': datetime.now().strftime('%d/%m/%Y, %H:%M')
    }

    user = {
        'participant_mail': participant_mail,
        'participant_id': participant_id,
        'messages': [message]
    }

    result = create_user_perm(user) #this is unnecssary operation we can remove it by creating a user base already.
    #result true means new user created, false means user id already exists.

    if result:
        return True
    else:
        result = insert_message_perm(participant_id, message)
        return result


#For temproray collection
def create_user_temp(user: dict) -> bool:
    '''
    Create a new user

    Parameters:
        - user(dict)

    Returns:
        - bool, 0 for failure and 1 for success
    '''

    result = collection_temp.find_one(
        {
            'participant_id': user['participant_id']
        }
    )

    if not result:
        result = collection_temp.insert_one(user)
        return result.acknowledged
    return False


def insert_message_temp(participant_id: int, message: dict) -> bool:
    '''
    Update messages for the user

    Parameters:
        - telegram_id(int): user telegram id
        - message(dict): mesage document to insert

    Returns:
        - bool, 0 for failure and 1 for success
    '''

    result = collection_temp.find_one_and_update(
        {
            'participant_id': participant_id
        },
        {
            '$push': {
                'messages': message
            }
        }
    )

    if not result:
        return False
    else:
        return True


def save_message_to_db_temp(data: str, response: str,tokens_used:int, participant_id: int,participant_mail:str) -> bool:
    '''
    Process thewhole body and update the db

    Parameters:
        - data(dict): the incoming request from Telegram

    Returns:
        - bool, 0 for failure and 1 for success
    '''

    message = {
        'user': data,
        'assistant': response,
        'tokens_used_in_conv':tokens_used,#tokens used in this conversation
    }

    user = {
        'participant_mail': participant_mail,
        'participant_id': participant_id,
        'messages': [message]
    }

    result = create_user_temp(user)
    #result true means new user created, false means user id already exists.

    if result:
        return True
    else:
        result = insert_message_temp(participant_id, message)
        return result



#function to delete sat from temp memory

def del_previous_conversations_temp(participant_id:str):
    collection_temp.delete_one({"participant_id":participant_id}) # i need to change this we can retan at least first conversation, so that we donot need to create it back


def get_previous_messages_temp(participant_id:str):
    # takes participant id and retrieve previous conversation and send them in form of list of list suitable for merging with chatbot(gradio)
    # return a list of list for previous CHATGPT conversations [[user, ai response],[user, ai response]]
    previous_conversations= []
    results= collection_temp.find_one({"participant_id":participant_id})
    try:
        retrieved = (results['messages'])#retrieved is a list of dictionary 
    except:
        return previous_conversations
    for obj in retrieved:
        #obj will be a dictionary
        new_list= [str(obj["user"]),str(obj["assistant"])]
        previous_conversations.append(new_list)

    return previous_conversations

'''
This function provides output suitable for chatcompletion-open ai
def get_previous_messages_temp(participant_id:str):
    # takes telegram id and retrieve previous conversation and send them in form string
    #now i need to return a list of dictionary for CHATGPT conversations
    previous_conversations= [{"role": "system", "content":" You are an helpful, creative, and clever assistant"},]
    results= collection_temp.find_one({"participant_id":participant_id})
    try:
        retrieved = (results['messages'])#retrieved is a list of dictionary 
    except:
        return previous_conversations
    for obj in retrieved:
        #obj will be a dictionary
        new_dict_1={"role": "user", "content":str(obj["user"])}
        previous_conversations.append(new_dict_1)
        new_dict_2={"role": "assistant", "content":str(obj["assistant"])}
        previous_conversations.append(new_dict_2)

    return previous_conversations

'''
