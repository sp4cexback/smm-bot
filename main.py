import logging
from telegram import LabeledPrice, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    PreCheckoutQueryHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# 1. /start Komutu (Rusça Ana Menü)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🛒 Каталог услуг (Все сервисы)", callback_data="all_services")],
        [InlineKeyboardButton("👤 Профиль / Баланс", callback_data="profile")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Привет, {user.first_name}! 🚀 Добро пожаловать в SMM бот.\n\n"
        "Выберите нужный раздел в меню ниже:",
        reply_markup=reply_markup
    )

# 2. Tüm Hizmetlerin Ayrı Ayrı Listelendiği Menü
async def all_services_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("⭐ TikTok Подписчики (1.000) - 300 Stars", callback_data="buy_tt_sub")],
        [InlineKeyboardButton("👁️ TikTok Просмотры (10.000) - 150 Stars", callback_data="buy_tt_view")],
        [InlineKeyboardButton("❤️ TikTok Лайки (1.000) - 150 Stars", callback_data="buy_tt_like")],
        [InlineKeyboardButton("📢 Telegram Канал Подписчики (1.000) - 300 Stars", callback_data="buy_tg_channel")],
        [InlineKeyboardButton("👥 Telegram Группа Участники (1.000) - 300 Stars", callback_data="buy_tg_group")],
        [InlineKeyboardButton("👁️ Telegram Просмотры постов (10K) - 100 Stars", callback_data="buy_tg_posts")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="📋 **Выберите нужную услугу:**",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# 3. Seçilen Butona Göre Fatura (Ödeme) Oluşturma
async def create_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    chat_id = query.message.chat_id
    
    if data == "buy_tt_sub":
        title = "TikTok Подписчики 1.000"
        description = "Пакет из 1.000 подписчиков для вашего TikTok аккаунта."
        price = 300
        payload = "order_tt_sub"
    elif data == "buy_tt_view":
        title = "TikTok Просмотры 10.000"
        description = "10.000 просмотров для вашего видео в TikTok."
        price = 150
        payload = "order_tt_view"
    elif data == "buy_tt_like":
        title = "TikTok Лайки 1.000"
        description = "1.000 лайков для вашего контента в TikTok."
        price = 150
        payload = "order_tt_like"
    elif data == "buy_tg_channel":
        title = "Telegram Канал Подписчики 1.000"
        description = "1.000 подписчиков для вашего публичного Telegram канала."
        price = 300
        payload = "order_tg_channel"
    elif data == "buy_tg_group":
        title = "Telegram Группа Участники 1.000"
        description = "1.000 участников для вашей публичной Telegram группы."
        price = 300
        payload = "order_tg_group"
    elif data == "buy_tg_posts":
        title = "Telegram Просмотры постов 10K"
        description = "10.000 просмотров для ваших постов в Telegram."
        price = 100
        payload = "order_tg_posts"
    else:
        return

    # Telegram Stars faturası gönderiliyor
    await context.bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=payload,
        provider_token="", # Telegram Stars için boş kalmalı!
        currency="XTR",
        prices=[LabeledPrice(title, price)],
    )

# 4. Ana Menüye Dönüş
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🛒 Каталог услуг (Все сервисы)", callback_data="all_services")],
        [InlineKeyboardButton("👤 Профиль / Баланс", callback_data="profile")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text="Главное меню:", reply_markup=reply_markup)

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="👤 **Информация профиля:**\n\nВы можете безопасно совершать покупки с помощью Telegram Stars.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]]),
        parse_mode="Markdown"
    )

# 5. Ön Ödeme Onayı
async def pre_checkout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)

# 6. Başarılı Ödeme Sonrası Mesajı
async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payment = update.message.successful_payment
    await update.message.reply_text(
        f"✅ Оплата успешно получена! ({payment.total_amount} Telegram Stars)\n\n"
        "🚀 Ваш заказ принят и передан в обработку."
    )

if __name__ == "__main__":
    TOKEN = "9013439428:AAHen0G_v3Mav4bAoYy0FBE_h7VlnQENyoQ"
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(main_menu, pattern="^main_menu$"))
    app.add_handler(CallbackQueryHandler(all_services_menu, pattern="^all_services$"))
    app.add_handler(CallbackQueryHandler(profile_handler, pattern="^profile$"))
    
    # Buton tetikleyicileri
    app.add_handler(CallbackQueryHandler(create_invoice, pattern="^buy_"))
    
    # Ödeme İşleyicileri
    app.add_handler(PreCheckoutQueryHandler(pre_checkout_callback))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))

    print("Русский SMM бот запущен...")
    app.run_polling()
