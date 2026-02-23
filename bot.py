import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# إعدادات الحساب (يفضل استخدام Environment Variables في Render)
api_id = int(os.environ.get("API_ID", 954313)) # استبدله برقمك
api_hash = os.environ.get("API_HASH", "b5eb232272556aeeef4a31902db0c7f3")
bot_token = os.environ.get("BOT_TOKEN", "8270945505:AAGBeMBqvEp2RhDLCTCAMurChwWimceCt84")
channel_id = "@Saadeem" # معرف قناتك العامة

app = Client("universal_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# دالة للتحقق إذا كان النص المرسل هو رابط فيديو
def is_video_url(url):
    video_extensions = ['.mp4', '.mkv', '.mov', '.avi']
    return any(ext in url.lower() for ext in video_extensions) or "od.lk" in url

@app.on_message(filters.private & filters.text)
async def process_video_link(client, message):
    url = message.text.strip()
    
    if is_video_url(url):
        waiting_msg = await message.reply("⏳ جاري إرسال الفيديو للقناة...")
        
        try:
            # إرسال الفيديو للقناة مع الرابط الذي أرسله المستخدم
            sent_video = await client.send_video(
                chat_id=channel_id,
                video=url,
                caption="سديم",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("استخراج النص 📝", callback_data=f"extract_{message.id}")]
                ])
            )
            
            await waiting_msg.edit(f"✅ تم النشر بنجاح في القناة: {channel_id}")
            
        except Exception as e:
            await waiting_msg.edit(f"❌ حدث خطأ أثناء الإرسال: {e}")
    else:
        await message.reply("⚠️ من فضلك أرسل رابط فيديو مباشر (ينتهي بـ .mp4 مثلاً)")

@app.on_callback_query(filters.regex("^extract_"))
async def handle_extraction(client, callback_query):
    # مصفوفة نصوص تجريبية للمحاكاة (بما أننا على الهاتف)
    # في النسخة المتقدمة هنا يتم استدعاء Whisper AI
    simulation_text = "جاري تحليل مقطع الفيديو.."
    words = simulation_text.split()
    
    current_text = ""
    for word in words:
        current_text += word + " "
        try:
            await callback_query.edit_message_reply_markup(
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(f"🩷 {current_text}", callback_data="none")]
                ])
            )
            await asyncio.sleep(0.5)
        except:
            continue

print("البوت يعمل الآن ومستعد لاستقبال الروابط...")
app.run()
