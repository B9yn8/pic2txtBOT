import os
import pytesseract
from PIL import Image
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

# Get the path to the Tesseract executable from the environment variable
tesseract_path = os.getenv("TESSERACT_CMD")

# تعيين التوكن الخاص بالبوت
TOKEN = "6806941124:AAEbsXEPS9824Mcnt4EcK1JZFuF6EkDZOtE"

# قائمة اللغات وروابط تنزيل الملفات
languages = {
    "eng": "https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata"
}

# تحميل ملفات اللغات
def download_language_files():
    os.system("mkdir -p tessdata")
    for lang_code, lang_url in languages.items():
        os.system(f"curl -L -o tessdata/{lang_code}.traineddata {lang_url}")

# إعداد Tesseract
def setup_tesseract():
    os.environ["TESSDATA_PREFIX"] = "./tessdata"
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
    else:
        print("Error: Tesseract path not found. Make sure to set the TESSERACT_CMD environment variable.")

# وظيفة لتحويل الصورة إلى نص
def image_to_text(update, context):
    # إرسال رسالة للمستخدم لتوضيح العملية
    msg = update.message.reply_text("جاري تحويل الصورة إلى نص...")

    try:
        # الحصول على الملف المرسل
        photo = update.message.photo[-1].get_file()
        # تحميل الصورة وتحويلها إلى نص
        img_file = photo.download()
        img = Image.open(img_file)
        # تحديد دقة الصورة
        img = img.convert('RGB')
        text = pytesseract.image_to_string(img)
        # تحديث الرسالة بالنص المستخرج
        msg.edit_text(text)
        # حذف الملف بعد الانتهاء
        os.remove(img_file)
    except Exception as e:
        # في حالة وجود أي خطأ، إرسال رسالة إلى المستخدم
        msg.edit_text("حدث خطأ أثناء معالجة الصورة. الرجاء المحاولة مرة أخرى.")
     
    # إرسال رسالة للمستخدم لتوضيح العملية
    update.message.reply_text("إذا كنت ترغب في دعمنا، يمكنك التبرع عبر /donate")
    os.remove(img_file)

    # يجب إغلاق الملف بعد الانتهاء من استخدامه
    img.close()

# وظيفة للترحيب
def start(update, context):
    update.message.reply_text("مرحبا بكم! يمكنك إرسال الصور لاستخراج النص منها.")

# وظيفة لعرض التعليمات
def help(update, context):
    update.message.reply_text("يمكنك ببساطة إرسال الصور إلى هذا البوت وسيقوم بإرجاع النص المستخرج.")

# وظيفة لطلب التبرع
def donate(update, context):
    update.message.reply_text("شكرا لاستخدام البوت! إذا كنت ترغب في دعم المطورين، يمكنك التبرع على الرابط التالي: [رابط التبرع]")

def main():
    # تنزيل ملفات اللغات عند تشغيل البرنامج
    download_language_files()

    # إعداد Tesseract
    setup_tesseract()

    # إعداد Updater والتوكن الخاص بالبوت
    updater = Updater(TOKEN, use_context=True)

    # الحصول على Dispatcher للبوت
    dp = updater.dispatcher

    # تعيين معالج الرسائل للبوت
    dp.add_handler(MessageHandler(Filters.photo, image_to_text))

    # تعيين وظيفة للأمر /start
    dp.add_handler(CommandHandler("start", start))

    # تعيين وظيفة للأمر /help
    dp.add_handler(CommandHandler("help", help))

    # تعيين وظيفة للأمر /donate
    dp.add_handler(CommandHandler("donate", donate))

    # بدء البوت
    updater.start_polling()

    # البقاء على البوت حتى يتم الضغط على Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
