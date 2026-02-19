#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import uuid
import json
import difflib
import threading
import telebot
from telebot import types
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask

# ১. Firebase ডাটা সরাসরি এখানে
firebase_dict = {
  "type": "service_account",
  "project_id": "fojik-9e328",
  "private_key_id": "57407655d55a8859d38c192ac7bba3f0c7fc35c7",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDA3Z/3LeafkVed\nq7ahLcGh5wWiYCjEcAXWxxxZqsOWWLk8Yd4luGx+01RKfhIoOGQ0Np1Gjb9oiO2A\nWpsp0otxc4Z/44p2uiZxXIjZeuI36kpd3tD4zUNrcoFHd+j/7pECi2OuybLUKfGh\nhqij+dolMr1IK2s2T2KiLVMggw3PO6JT0feILvxaH1rqjHBUpK1b7/ecTimLoE2d\nz1peUPpGS1+siHPfskuDP4gwusz0YqAiM+TdiIRMQMjs0Yj7FjubUYzDJQpxyPmN\n8aXt4Qk3+FO9Xr2F0V5hCegg936T5YMIaipkJS1pMQ170p8pAQYhioGiYtUFDD31\nIHNi7CLrAgMBAAECggEAJaaeZejGDvyWuCcffhOqq2qoROy0yLR9z1ILjM2zZRRp\nBQquDXsVYyTqXaiC7usjVLYcuftOFKA2jUoi5GU/56P/69OF4muwuYyxApPkubm5\nTt4Cua+Iq98sscEM8XmnQXHoweSKTrTpgPkCzxAlsAFZxk8DnRSeUr66baxn875/\ng7hIsdeuXDIdgn2vSKol134WDqobCFBo1FTAHCl/y5KTzbXyoU6fd+JdTQRTbdo8\nuKJ6oFAKwsndulXxNoP4Ttbfn3L1FCLzetOMVtGLIC8+gjUIjnHB/sj+LxCqD89S\nBwTsDGdE68D+CgR6okMycI3XUifBK6+p09Zcmive0QKBgQDxLIMC4fCh/s+7GLQY\n48tNV5hEhrCNzCWgmm5kfV2z6PWvGztaGkfHzA++JQ/JABATJkqAq79RSK54AotS\nKJmFTGCYRXegdUIIKW5QwrZLjA9n8BZTzzmUXTyBQVNgfVB8AfekjtQUJiNbYjvZ\n6ogqvbYMTdUDOkeuFZdmAkQllwKBgQDMuNxVaYcQH9Vps8RgcCPhPqa+3/y9Mfvp\n3e36TXLvgJ+yZxYbqr0OxUbQ+zARoyGOaEIq86nX1ahQ6T2KAxYWas+HtqcKXBdg\n2W1hC/6kL10zpYNs4pt2SOUdE+26wI3eCgew/Ks8BIvCSY+iVTTFYnayZiQF/NrI\nOsY7bbFfzQKBgQC0CPFoBnhWxdwWpBNVfT835krx5MYJpDr2kDIWbAu2ERLOe/qr\ngXDSMoASBqKo/pYBZZU6RnuUVzh+uA9+7nXkLybwpPLvYnk/lIYYXbIt5Ule4rgY\nKlqmaY+QQc7W+dVKLUHLox+oRuwf/M4HF/A8T9CFkNiSB0CZMN8LNGfg0wJ/ZY9P\nvw+a8WTZepaz1SPMqPFrx0VXHISvdFWkuYeyfR5SGy8IyLDrGWjEuOfj8Nv8yajv\nKl+24lwcJAeRf+YIDxbt3WW/eGQ3NNSobnyE1u6oTfbOPDYu6X9AKiy4wuzDdGOF\nbUfrqtqWeswDdYTPqRwvxlDljhLidnKx5MmGNQKBgQC/vlj5gDyEspLUbUbFOPDN\niZj8pA7VJlP8kSqo/VJuUXdK2GNmQSNMguDrqWJX5CvJk7pyt0msr4LsWXAGB9Vr\ncZ89AvK6Pg1BExuPaQ830y0xTssk3xDeUNy3vp7uprJoditoPTm3oRChXBc/G9l3\nCX2EultqHS1CV6X7lo4d9A==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@fojik-9e328.iam.gserviceaccount.com",
  "client_id": "115386057281973540490",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40fojik-9e328.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# ২. Firebase Initialize (একবারই হবে)
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://fojik-9e328-default-rtdb.firebaseio.com/'
    })

# ----------------- CONFIG -----------------
TOKEN = "8559869299:AAEBtkcJ0H_4WwGkywzHwsJeTy_ciIYyedY"
OWNER_ID = 5880876410          
CHANNELS = ["fojikapp", "fojikapp"]

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Bot is Alive!"

# ------------------------------------------

def save_user(user_id):
    ref = db.reference('users')
    ref.child(str(user_id)).set(True)

def save_post(files_list, title, buttons=[]):
    uid = str(uuid.uuid4())[:8]
    ref = db.reference(f'posts/{uid}')
    data = {
        "title": title,
        "files": files_list,
        "buttons": buttons,
        "created_at": int(time.time())
    }
    ref.set(data)
    return uid

def load_post(code):
    ref = db.reference(f'posts/{code}')
    return ref.get()


def build_buttons_markup(buttons):
    if not buttons:
        return None
    markup = types.InlineKeyboardMarkup(row_width=1)
    for btn in buttons:
        markup.add(types.InlineKeyboardButton(btn["text"], url=btn["url"]))
    return markup

# ----------------- SEND GROUP -----------------
def send_group(chat_id, data):
    title = data.get("title", "")
    files = data.get("files", [])
    buttons = data.get("buttons", [])
    markup = build_buttons_markup(buttons)

    i = 0
    sent_first_caption = False

    while i < len(files):
        item = files[i]
        ftype = item.get("ftype")
        fid = item.get("file_id")

        # Photos album
        if ftype == "photo":
            photos = []
            j = i
            while j < len(files) and files[j].get("ftype") == "photo" and len(photos) < 10:
                photos.append(files[j]["file_id"])
                j += 1

            media = []
            for idx, pid in enumerate(photos):
                cap = title if (not sent_first_caption and idx == 0) else None
                media.append(types.InputMediaPhoto(pid, caption=cap))

            try:
                # Album can't have inline buttons, so attach to first photo
                if not sent_first_caption and markup:
                    bot.send_photo(chat_id, photos[0], caption=title, reply_markup=markup)
                    for pid in photos[1:]:
                        bot.send_photo(chat_id, pid)
                else:
                    bot.send_media_group(chat_id, media)
                sent_first_caption = True
            except Exception:
                for idx, pid in enumerate(photos):
                    cap = title if (not sent_first_caption and idx == 0) else None
                    try:
                        bot.send_photo(chat_id, pid, caption=cap)
                        sent_first_caption = True
                    except Exception as e2:
                        print("photo fallback error:", e2)
            i = j
            continue

        cap = title if not sent_first_caption else None
        try:
            if ftype == "video":
                if markup and not sent_first_caption:
                    bot.send_video(chat_id, fid, caption=cap, reply_markup=markup)
                else:
                    bot.send_video(chat_id, fid, caption=cap)
            elif ftype == "document":
                if markup and not sent_first_caption:
                    bot.send_document(chat_id, fid, caption=cap, reply_markup=markup)
                else:
                    bot.send_document(chat_id, fid, caption=cap)
            elif ftype == "text":
                msg = f"{title}\n\n{item.get('text','')}" if not sent_first_caption else item.get('text','')
                if markup and not sent_first_caption:
                    bot.send_message(chat_id, msg, reply_markup=markup)
                else:
                    bot.send_message(chat_id, msg)
            else:
                if markup and not sent_first_caption:
                    bot.send_document(chat_id, fid, caption=cap, reply_markup=markup)
                else:
                    bot.send_document(chat_id, fid, caption=cap)
        except Exception as e:
            print("send error:", e)

        sent_first_caption = True
        i += 1

# ----------------- USER CHECK -----------------
def is_user_member(user_id, channel_username):
    try:
        member = bot.get_chat_member(f"@{channel_username}", user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False

def send_join_message(user_id, firstname):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [
        types.InlineKeyboardButton("Join Channel 1", url=f"https://t.me/{CHANNELS[0]}"),
        types.InlineKeyboardButton("Join Channel 2", url=f"https://t.me/{CHANNELS[1]}"),
        types.InlineKeyboardButton("✅ Joined", callback_data="joined")
    ]
    markup.add(*btns)
    text = f"Hey {firstname}\n\nPlease join all update channels to use the bot!"
    bot.send_message(user_id, text, parse_mode="Markdown", reply_markup=markup)

# ---------------- COMMANDS ----------------
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id
    firstname = message.from_user.first_name or "friend"
    args = message.text.split()
    if len(args) > 1:
        code = args[1].strip()
        data = load_post(code)
        if data:
            if all(is_user_member(user_id, ch) for ch in CHANNELS):
                send_group(user_id, data)
                save_user(user_id)
            else:
                send_join_message(user_id, firstname)
            return
    if all(is_user_member(user_id, ch) for ch in CHANNELS):
        bot.send_message(user_id, f"✅ Welcome {firstname}!")
        save_user(user_id)
    else:
        send_join_message(user_id, firstname)

@bot.callback_query_handler(func=lambda call: call.data == "joined")
def check_joined(call):
    user_id = call.message.chat.id
    firstname = call.from_user.first_name or "friend"
    if all(is_user_member(user_id, ch) for ch in CHANNELS):
        bot.send_message(user_id, f"✅ Thank you {firstname}! You can now use the bot.")
    else:
        bot.send_message(user_id, "⚠️ Please join both channels first!")

# ---------------- UPLOAD ----------------
@bot.message_handler(commands=["upload"])
def upload_cmd(message):
    if message.chat.id != OWNER_ID:
        bot.reply_to(message, "❌ শুধুমাত্র মালিক এই কমান্ড ব্যবহার করতে পারবেন।")
        return
    bot.reply_to(message,
        "📤 এখন এক পোস্টের সব ফাইল পাঠান (ছবি/ভিডিও/ডকুমেন্ট/টেক্সট)।\n"
        "প্রতিটি ফাইলে ক্যাপশন লিখে দিলে সেটি পোস্টের টেকস্ট হিসেবে ধরা হবে (প্রথম ক্যাপশন হবে টাইটেল)।\n\n"
        "সব ফাইল পাঠানো শেষ হলে /done লিখুন।\n"
        "কোনো সময় /cancel লিখে ক্যানসেল করতে পারেন।")
    bot.register_next_step_handler(message, collect_post_files, [], [], None)

def collect_post_files(message, collected, buttons, title):
    if message.text and message.text.strip().lower() == "/cancel":
        bot.reply_to(message, "❌ আপলোড ক্যানসেল করা হয়েছে।")
        return
    if message.text and message.text.strip().lower() == "/done":
        if not collected:
            bot.reply_to(message, "⚠️ কোনো ফাইল পাওয়া যায়নি!")
            return
        if not title:
            title = "Untitled Post"
        code = save_post(collected, title, buttons)
        link = f"https://t.me/{bot.get_me().username}?start={code}"
        bot.send_message(message.chat.id,
                         f"✅ পোস্ট আপলোড সম্পন্ন!\n🎬 টাইটেল: {title}\n🔗 লিংক: {link}\n\nকোড: {code}")
        return

    text = (message.text or "").strip()
    if text.startswith("Button:"):
        try:
            _, rest = text.split("Button:", 1)
            name, url = rest.split("|", 1)
            buttons.append({"text": name.strip(), "url": url.strip()})
            bot.reply_to(message, f"✅ বাটন যোগ হয়েছে: {name.strip()}")
        except Exception:
            bot.reply_to(message, "❌ ভুল ফরম্যাট")
        bot.register_next_step_handler(message, collect_post_files, collected, buttons, title)
        return

    entry = None
    if message.content_type == "photo":
        fid = message.photo[-1].file_id
        entry = {"ftype": "photo", "file_id": fid}
        if not title and message.caption:
            title = message.caption
    elif message.content_type == "video":
        fid = message.video.file_id
        entry = {"ftype": "video", "file_id": fid}
        if not title and message.caption:
            title = message.caption
    elif message.content_type == "document":
        fid = message.document.file_id
        entry = {"ftype": "document", "file_id": fid, "file_name": message.document.file_name}
        if not title and message.caption:
            title = message.caption
    elif message.content_type == "text":
        if not title:
            title = text
            bot.reply_to(message, f"✔ টাইটেল সেট করা হলো: {title}\nএখন ফাইল পাঠান অথবা /done লিখুন।")
            bot.register_next_step_handler(message, collect_post_files, collected, buttons, title)
            return
        else:
            entry = {"ftype": "text", "text": text}

    if entry:
        collected.append(entry)
        bot.reply_to(message, "📥 ফাইল যোগ করা হয়েছে — আরও পাঠাতে পারেন, শেষ হলে /done লিখুন।")

    bot.register_next_step_handler(message, collect_post_files, collected, buttons, title)

# ---------------- BROADCAST ----------------
@bot.message_handler(commands=["broadcast"])
def broadcast_cmd(message):
    if message.chat.id != OWNER_ID:
        bot.reply_to(message, "❌ আপনি এই কমান্ড ব্যবহার করতে পারবেন না।")
        return
    bot.reply_to(message, "📢 যা পাঠাবেন, সেটা সবার কাছে পাঠানো হবে — এখন যা পাঠাবেনওই পাঠান:")
    bot.register_next_step_handler(message, do_broadcast)

def do_broadcast(message):
    ref = db.reference('users')
    users_data = ref.get()
    if not users_data:
        bot.reply_to(message, "❌ কোনো ইউজার পাওয়া যায়নি!")
        return
    users = list(users_data.keys())
    sent = 0
    failed = 0
    for uid in users:
        try:
            if message.content_type == "text":
                bot.send_message(uid, message.text)
            elif message.content_type == "photo":
                bot.send_photo(uid, message.photo[-1].file_id, caption=message.caption)
            elif message.content_type == "video":
                bot.send_video(uid, message.video.file_id, caption=message.caption)
            elif message.content_type == "document":
                bot.send_document(uid, message.document.file_id, caption=message.caption)
            sent += 1
        except Exception:
            failed += 1
    bot.send_message(OWNER_ID, f"📨 Broadcast সম্পন্ন!\n✔ সফল: {sent}\n❌ ব্যর্থ: {failed}")

# ---------------- DELETE POST ----------------
@bot.message_handler(commands=["delete"])
def delete_cmd(message):
    if message.chat.id != OWNER_ID:
        bot.reply_to(message, "❌ আপনি এই কমান্ড ব্যবহার করতে পারবেন না।")
        return
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "🗑️ ব্যবহার: /delete <code>")
        return
    code = parts[1].strip()
    ref = db.reference(f'posts/{code}')
    if ref.get():
        ref.delete()
        bot.reply_to(message, f"✅ পোস্ট {code} Firebase থেকে ডিলিট হয়েছে।")
    else:
        bot.reply_to(message, f"❌ পোস্ট {code} ডাটাবেসে পাওয়া যায়নি।")

# ---------------- SMART SEARCH ----------------
@bot.message_handler(func=lambda m: True)
def smart_search_handler(message):
    if message.text and message.text.startswith("/"):
        return

    query = (message.text or "").strip().lower()
    if not query:
        return

    best = None
    best_ratio = 0.0

    all_posts = db.reference('posts').get()
    if all_posts:
        for code, data in all_posts.items():
            title = (data.get("title") or "").lower()
            ratio = difflib.SequenceMatcher(None, query, title).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best = (code, data)

    firstname = message.from_user.first_name or "friend"

    if best_ratio >= 0.8:
        code, data = best
        if all(is_user_member(message.chat.id, ch) for ch in CHANNELS):
            send_group(message.chat.id, data)
            save_user(message.chat.id)
        else:
            # 80%+ মিল হলেও চ্যানেলে জয়েন না থাকলে join মেসেজ
            send_join_message(message.chat.id, firstname)
    else:
        # Warning message আগে
        bot.send_message(
            message.chat.id,
            "𝐘𝐨𝐮 𝐦𝐚𝐲 𝐛𝐞 𝐭𝐲𝐩𝐢𝐧𝐠 𝐢𝐭 𝐰𝐫𝐨𝐧𝐠, 𝐭𝐡𝐚𝐭'𝐬 𝐰𝐡𝐲 𝐈 𝐜𝐨𝐮𝐥𝐝𝐧'𝐭 𝐟𝐢𝐧𝐝 𝐢𝐭, 𝐩𝐥𝐞𝐚𝐬𝐞 𝐭𝐲𝐩𝐞 𝐢𝐭 𝐜𝐨𝐫𝐫𝐞𝐜𝐭𝐥𝐲."
        )
        # তারপর join চ্যানেল মেসেজ
        send_join_message(message.chat.id, firstname)
# ---------------- START POLLING ----------------
if __name__ == "__main__":
    print("🤖 Bot is starting successfully...")
    # Flask সার্ভার রান করা
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080))), daemon=True).start()
    
    # পোলিং শুরু (এটিই বটকে সচল রাখে)
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=60)
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(5)
