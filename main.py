import telebot
from telebot.types import *
from sqll import *
import requests

token = "Your_Token"

bot = telebot.TeleBot(token)

my_id = "Your_Id"

msg = "" # اتركها لا تخلي اي شي

mainCommandsText = "اهلا بك يا مطوري في لوحة الاوامر!" # رساله المطور تكدر تعدلها

WelcomeMember = "اهلا بك ياعزيزي المستخدم!"  # رساله العضو تكدر تغيرها



def MangeBot():
    mrk = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text= "تفعيل التواصل", callback_data= "on communication"),
                InlineKeyboardButton(text= "تعطيل التواصل", callback_data= "off communication"),
            ],
            [
                InlineKeyboardButton(text= "تفعيل اشعار الدخول", callback_data= "on access"),
                InlineKeyboardButton(text= "تعطيل اشعار الدخول", callback_data= "off access"),
            ],
            [
                InlineKeyboardButton(text= "الاحصائيات", callback_data= "statistics"),
            ],
            [
                InlineKeyboardButton(text= "مسح المحظورين", callback_data= "del blcs"),
                InlineKeyboardButton(text= "مسح محظور", callback_data= "del blc"),
                InlineKeyboardButton(text= "حظر", callback_data= "blc"),
            ],
            [
                InlineKeyboardButton(text= "مسح القنوات المحظورة", callback_data= "del channels"),
                InlineKeyboardButton(text= "مسح قناة محظورة", callback_data= "del channel"),
                InlineKeyboardButton(text= "حظر قناة", callback_data= "blc channel"),
            ],
            [
                InlineKeyboardButton(text= "قناة الاشتراك الاجباري", callback_data= "sub chn"),
                InlineKeyboardButton(text= "اضف قناة", callback_data= "add chn"),
                InlineKeyboardButton(text= "مسح قناة", callback_data= "del chn"),
            ],
            [
                InlineKeyboardButton(text= "اذاعة للكل", callback_data="brd all"),
            ],
            [
                InlineKeyboardButton(text= "اذاعة بالتثبيت للأعضاء", callback_data= "brdcast pin me"),
                InlineKeyboardButton(text= "اذاعة للأعضاء", callback_data= "brdcast me"),
                InlineKeyboardButton(text= "اذاعة بالتحويل للأعضاء", callback_data= "brdcast fod me"),
            ],
            [
                InlineKeyboardButton(text= "اذاعة بالتثبيت للقنوات", callback_data= "brdcast pin ch"),
                InlineKeyboardButton(text= "اذاعة للقنوات", callback_data= "brdcast ch"),
                InlineKeyboardButton(text= "اذاعة بالتحويل للقنوات", callback_data= "brdcast fod ch"),
            ],
        ]
    )
    return mrk

def back():
    mrk = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text= '. رجوع .',callback_data= "back")]
        ]
    )
    return mrk

def cans():
    mrk = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text= '. الغاء .',callback_data= "cans")]
        ]
    )
    return mrk

def getTitleAUrl():
    ch = get_compulsory_subscription()
    if ch not in [0, "0"]:
        all = bot.create_chat_invite_link(ch, name=__name__)
        return all.invite_link
    else:
        return None
    

def source():
    all = getTitleAUrl()
    if all:
        
        mrk = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text= "سورس البوت", url= all)
                ]
            ]
        )
        return mrk
    
    else:
        return None



def HandleMessageMember():
    mrk = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text= 'رد', callback_data= "reply"),
                InlineKeyboardButton(text= 'حظر', callback_data= "block"),
            ]
        ]
    )
    return mrk


# فنكشن تتحقق هل اليوزر مشترك بالقناه او لا
def IN_channel(user_id):
    url = f"https://api.telegram.org/bot{token}/getChatMember?chat_id={get_compulsory_subscription()}&user_id={user_id}"
    req = requests.get(url).json()
    if "result" in req:
        if req["result"]["status"] in ["member", "creator", "administrator"]:
            return True
        else:
            return False
    else:
        return False


# ستارت فقط للمطور
@bot.message_handler(func= lambda message: message.from_user.id in [my_id], commands=['start'])
def MainMenuDev(message:Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.send_message(chat_id=chat_id, text= mainCommandsText, reply_markup= MangeBot())


# ستارت لاي عضو
@bot.message_handler(func= lambda message: message.from_user.id not in [my_id], commands=['start'])
def MainMenuDev(message:Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    txt1 = WelcomeMember
    txt2 = "اشترك في قناة البوت لأستخدام الاوامر!"
    mrk = source()
    inf = get_user_info(user_id)
    if inf and inf[1] == "mms":
        if mrk:
            txt = txt2
            if not IN_channel(user_id):
                bot.send_message(chat_id=chat_id, text= txt, reply_to_message_id= message.id, reply_markup=source())

            else:
                txt = txt1
                bot.send_message(chat_id=chat_id, text= txt, reply_to_message_id= message.id, reply_markup=source())
        else:
            bot.send_message(chat_id=chat_id, text= txt1, reply_to_message_id= message.id)

    # اذا كان العضو جديد
    if not get_user_info(user_id):
        if get_notifications() not in [0, "0"]:
            txt = "تم دخول مستخدم جديد ال البوت" + f"\nالايدي = {user_id} " + f"\nالاسم = {message.from_user.first_name}" + f"\nالمعرف = {message.from_user.username} \n`"
            bot.send_message(my_id, txt)
    insert_user(user_id, "mms")
    

#  العضو اذا ارسل رساله غير ستارت
@bot.message_handler(func= lambda message: message.text)
def MainMenuDev(message:Message):
    global msg
    msg = message
    chat_id = message.chat.id
    user_id = message.from_user.id
    txt1 = "اهلا بك!"
    txt2 = "اشترك في قناة البوت لأستخدام الاوامر!"
    mrk = source()
    inf = get_user_info(user_id)
    if inf and inf[1] == "mms":
        if mrk:
            txt = txt2
            if not IN_channel(user_id):
                bot.send_message(chat_id=chat_id, text= txt, reply_to_message_id= message.id, reply_markup=mrk)
            else:
                txt = txt1
                bot.send_message(chat_id=chat_id, text= txt, reply_to_message_id= message.id, reply_markup=mrk)
                if get_login() not in [0, "0"]:
                    bot.send_message(my_id, f"الرسالة = {message.text}" + "\nمن = " + f"\nالاسم = {message.from_user.first_name}" + f"\nالمعرف = {message.from_user.username}", reply_markup=HandleMessageMember())
        else:
            bot.send_message(chat_id=chat_id, text= txt1, reply_to_message_id= message.id)
            if get_login() not in [0, "0"]:
                    bot.send_message(my_id, f"الرسالة = {message.text}" + "\nمن = " + f"\nالاسم = {message.from_user.first_name}" + f"\nالمعرف = {message.from_user.username}", reply_markup=HandleMessageMember())
    if not get_user_info(user_id):
        if get_notifications() not in [0, "0"]:
            txt = "تم دخول مستخدم جديد ال البوت" + f"\الايدي = {user_id} " + f"\nالاسم = {message.from_user.first_name}" + f"\nالمعرف = {message.from_user.username}"
            bot.send_message(my_id, txt)
    insert_user(user_id, "mms")
    





@bot.callback_query_handler(func= lambda call:True)
def MAinQury(call: CallbackQuery):
    data = call.data
    message = call.message
    chat_id = message.chat.id
    user_id = call.from_user.id
    if user_id in [my_id]:
        if data == "on communication":
            txt = "تم تقغيل التواصل"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=back())
            update_user_settings(login=1)

        elif data == "off communication":
            txt = "تم تعطيل التواصل"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=back())
            update_user_settings(login=0)

        elif data == "on access":
            txt = "تم تفعيل اشعارات الدخول"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=back())
            update_user_settings(notifications=0)

        elif data == "off access":
            txt = "تم تعطيل اشعارات الدخول"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=back())
            update_user_settings(notifications=0)


        elif data == "statistics":
            num_us, num_blcs, num_ch, num_gr = (get_total_mms(), get_total_bans(), get_total_ch(), get_total_gr())
            txt = "عزيزي المطور, اليك القائمة الخاصة باحصائيات البوت" + f"\nعدد مستخدمين البوت = {num_us}" + f"\nعدد المحظورين = {num_blcs}" + f"\nعدد القنوات = {num_ch}" + f"\nعدد الكروبات = {num_gr}"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=back())


        elif data == "del blcs":
            txt = "تم حذف جميع المستخدمين المحظورين"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=back())
            unban_uss()
            
        elif data == "del blc":
            txt = "ارسل ايدي المحظور"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=cans())
            bot.register_next_step_handler(message, unban)

        elif data == "blc":
            txt = "ارسل ايدي المستخدم"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=cans())
            bot.register_next_step_handler(message, ban)


        elif data == "del channels":
            txt = "تم حذف جميع القنوات المحظورة"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=back())
            unban_channels()
            
        elif data == "del channel":
            txt = "ارسل ايدي القناة المحظورة"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=cans())
            bot.register_next_step_handler(message, unblock)

        elif data == "blc channel":
            txt = "ارسل ايدي القناة لحظرها"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=cans())
            bot.register_next_step_handler(message, block)


        elif data == "sub chn":
            ch = get_compulsory_subscription()
            txt1 = "قناة الاشتراك الاجباري" + "\nاسم القناة: {name_ch}" + "\nمعرف القناة: {us_ch}" + "\nايدي القناة: {id_ch}"
            txt2 = "عذرا, ليس لديك قناة اشتارك اجباري!"
            if ch in [0, "0"]:
                txt = txt2
            else:
                all = bot.get_chat(ch)
                txt = txt1.format(name_ch = all.title, us_ch = all.username, id_ch = all.id)

            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=back())

        elif data == "add chn":
            txt = "لأضافه قناة اشتراك اجباري يجب اولا رفع البوت مشرفا في القناة" + "\nارسل ايدي او معرف القناة"
            bot.register_next_step_handler(message, addCh)
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=cans())

        elif data == "del chn":
            txt = "تم حذف قناة الاشتراك الاجباري!"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=back())
            update_user_settings(compulsory_subscription=0)


        elif data == "brd all":
            txt = "ارسل محتوى الاذاعة, انتبة يجب ان تكون نصية!"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=cans())
            bot.register_next_step_handler(message, brd_all)


        elif data == "brdcast me":
            txt = "ارسل محتوى الاذاعة, انتبة يجب ان تكون نصية!"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=cans())
            bot.register_next_step_handler(message, broadcast)

        elif data == "brdcast pin me":
            txt = "ارسل محتوى الاذاعة للتثبيت, انتبة يجب ان تكون نصية!"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=cans())
            bot.register_next_step_handler(message, broadcast_pin)

        elif data == "brdcast fod me":
            txt = "ارسل محتوى الاذاعة للتحويل, انتبة يجب ان تكون نصية!"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=cans())
            bot.register_next_step_handler(message, broadcast_fod)


        elif data == "brdcast ch":
            txt = "ارسل محتوى الاذاعة, انتبة يجب ان تكون نصية!"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=cans())
            bot.register_next_step_handler(message, brd)

        elif data == "brdcast pin ch":
            txt = "ارسل محتوى الاذاعة للتثبيت, انتبة يجب ان تكون نصية!"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=cans())
            bot.register_next_step_handler(message, brd_pin)

        elif data == "brdcast fod ch":
            txt = "ارسل محتوى الاذاعة للتحويل, انتبة يجب ان تكون نصية!"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=cans())
            bot.register_next_step_handler(message, brd_fod)


        elif data == "cans":
            bot.clear_step_handler(message)
            bot.edit_message_text(text= "تم الغاء المهمة بنجاح!", chat_id=chat_id, message_id=message.id, reply_markup=back())

        elif data == "back":
            bot.edit_message_text(text= mainCommandsText, chat_id=chat_id, message_id=message.id, reply_markup=MangeBot())


        elif data == "reply":
            bot.send_message(text= "ارسل الرد: ", chat_id=chat_id,  reply_markup=cans())
            bot.register_next_step_handler(message, rplt)

        elif data == "block":
            bot.send_message(text= "المستخدم تم حظرة!", chat_id=chat_id,  reply_markup=back())
            try:
                bot.send_message(text= "لقد تم حظرك من استخدام البوت!", chat_id=msg.chat.id)
            except:
                pass
            update_user(msg.from_user.id, "blc")








def ban(message:Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    txt = "تم حظر المستخدم بنجاح!"
    if message.text:
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
        try:
                bot.send_message(text= "لقد تم حظرك من استخدام البوت!", chat_id=message.text)
        except:
            pass
        update_user(user_id= message.text, type= "blc")
    else:
        txt = "يجب ان تكون الرسالة نصية!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())



def unban(message:Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    txt = "تم الغاء حظر المستخدم بنجاح!"
    if message.text:
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
        try:
                bot.send_message(text= "لقد تم الغاء الحظر عن حسابك!", chat_id=message.text)
        except:
            pass
        update_user(user_id= message.text, type= "mms")
    else:
        txt = "يجب ان تكون الرسالة نصية!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())



def block(message:Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    txt = "تم حظر القناة بنجاح!"
    if message.text:
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
        try:
            bot.leave_chat(message.text)
        except:
            pass
        update_channel(user_id= message.text, blc= "1")
    else:
        txt = "يجب ان تكون الرسالة نصية!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())



def unblock(message:Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    txt = "تم الغاء الحظر عن القناة بنجاح!"
    if message.text:
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
        update_channel(user_id= message.text, blc= "0")
    else:
        txt = "يجب ان تكون الرسالة نصية!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())


def addCh(message:Message):
    chat_id = message.chat.id
    if message.text:
        try:
            id = bot.get_chat(message.text).id
            txt = "تم اضافه قناة الاشتراك الاجباري بنجاح!"
            bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
            update_user_settings(compulsory_subscription=id)
        except:
            txt = "تحقق من وجود البوت في القناة"
            bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
    else:
        txt = "يجب ان تكون الرسالة نصية!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())

def brd_all(message:Message):
    chat_id = message.chat.id
    if message.text:
        for user_id in get_total_users():
            try:
                bot.send_message(user_id, message.text, disable_web_page_preview=True)
            except:
                pass
        for channel_id in get_total_channels():
            try:
                bot.send_message(channel_id, message.text, disable_web_page_preview=True)
            except:
                pass
        txt = "تم ارسال الاذاعة الى الكل!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
    else:
        txt = "يجب ان تكون الرسالة نصية!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())


def broadcast(message:Message):
    chat_id = message.chat.id
    if message.text:
        for user_id in get_total_users():
            try:
                bot.send_message(user_id, message.text, disable_web_page_preview=True)
            except:
                pass
        txt = "تم ارسال الاذاعة الى جميع المستخدمين!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
    else:
        txt = "يجب ان تكون الرسالة نصية!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())



def broadcast_pin(message:Message):
    chat_id = message.chat.id
    if message.text:
        for user_id in get_total_users():
            try:
                m = bot.send_message(user_id, message.text, disable_web_page_preview=True)
                bot.pin_chat_message(m.chat.id, m.id)
            except:
                pass
        txt = "تم ارسال الاذاعة الى جميع المستخدمين!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
    else:
        txt = "يجب ان تكون الرسالة نصية!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())


def broadcast_fod(message:Message):
    chat_id = message.chat.id
    if message.text:
        for user_id in get_total_users():
            try:
                bot.forward_message(user_id, chat_id, message.id)
            except:
                pass
        txt = "تم ارسال الاذاعة الى جميع المستخدمين!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
    else:
        txt = "يجب ان تكون الرسالة نصية!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())


def brd(message:Message):
    chat_id = message.chat.id
    if message.text:
        for channel_id in get_total_channels():
            try:
                bot.send_message(channel_id, message.text, disable_web_page_preview=True)
            except:
                pass
        txt = "تم ارسال الاذاعة الى جميع القنوات!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
    else:
        txt = "يجب ان تكون الرسالة نصية!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())



def brd_pin(message:Message):
    chat_id = message.chat.id
    if message.text:
        for channel_id in get_total_channels():
            try:
                bot.send_message(channel_id, message.text, disable_web_page_preview=True)
            except:
                pass
        txt = "تم ارسال الاذاعة الى جميع القنوات!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
    else:
        txt = "يجب ان تكون الرسالة نصية!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())


def brd_fod(message:Message):
    chat_id = message.chat.id
    if message.text:
        for channel_id in get_total_channels():
            try:
                bot.send_message(channel_id, message.text, disable_web_page_preview=True)
            except:
                pass
        txt = "تم ارسال الاذاعة الى جميع القنوات!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
    else:
        txt = "يجب ان تكون الرسالة نصية!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())




def rplt(message:Message):
    chat_id = message.chat.id
    if message.text:
        txt = f"الرد= {message.text}"
        bot.send_message(text= txt, chat_id=msg.chat.id)

    else:
        txt = "يجب ان تكون الرسالة نصية!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())






# فنشكن اذا البوت انظم لكروب او قناه
@bot.my_chat_member_handler(func= lambda chat:True)
def MyChatMember(message:ChatMemberUpdated):
    chat_id = message.chat.id
    user_id = message.from_user.id
    inf = get_channel_info(chat_id)

    if message.new_chat_member.status == "kicked":
        delete_channel(chat_id)


    if not inf and message.chat.type == "channel":
        try:
            link = bot.create_chat_invite_link(message.chat.id, name=message.chat.title).invite_link
            bot.send_message(my_id, f"تم تفعيل بوتك في قناة: الايدي = {chat_id} | المعرف = {link}")
            bot.send_message(user_id, "تم تفعيل البوت في قناتك, استمتع بالمميزات!")
        except:
            pass
        insert_channel(chat_id, "ch")
    elif  inf and message.chat.type == "channel":
        if not inf[2] in [0, "0"]:
            try:
                bot.leave_chat(chat_id)
            except:
                pass






print("Your Bot Running ...")


bot.infinity_polling(skip_pending=True, allowed_updates=telebot.util.update_types)