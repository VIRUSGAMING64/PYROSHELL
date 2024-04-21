
import pyrogram
import Gvar

def CreateNewUser(message:pyrogram.types.Message):
    TEMP_USER = [
            message.from_user.id,  # USER_ID  0
            message.id,  # LAST_MESSAGE_ID 1
            0,  # CHDIR 2
            0,  # MKDIR 3
            0,  # SEND 4
            0,  # GETURL 5
            Gvar.ROOT+ "/" + str(message.from_user.id) + "-" + str(message.from_user.first_name),  # PATH 6
            0,  # ASKING 7
            0,  # WRITING 8
            0,  # GETING_NOTEPAD_NAME 9
            0,  # WRITING_FILEPATH 10
            0,  # BOT_LAST_MESSAGE_ID 11
            0,  # CATING 12
            0,  # LAST_MESSAGE_DOWNLOAD_ID 13
            message.chat.id,  # chat_id 14
            0,  # other vars 15
            0,  # other vars 16
            0,  # other vars 17
            0,  # other vars 18
            0,  # other vars 19
            0,  # other vars 20
        ]
    return TEMP_USER