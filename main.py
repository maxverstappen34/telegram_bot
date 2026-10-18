
from telegram import Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,MessageHandler,filters,CallbackQueryHandler,ContextTypes
from database import session_local,CartItem


TOKEN = "8833186570:AAEAUw6dcMxB7RLnxRJn4bHe2T2WtLmsXKw"

main_menu_keyboard=[
    [
        KeyboardButton("menu"),
        KeyboardButton("cart")
    ],
    [
        KeyboardButton("contact"),
        KeyboardButton("hours")
    ]
]

# start method
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup=ReplyKeyboardMarkup(
        main_menu_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )
    await update.message.reply_text("Hello! I'm your bot. How can I assist you today?\n",reply_markup=reply_markup)

# replying method

async def echo(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# help method
    
async def help_method(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(" I'M here to help you my friend.")

# menu method 
    
async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    key_button=[
        [
        InlineKeyboardButton("burger (10$)",callback_data="add burger"),
        InlineKeyboardButton("fries (5$)",callback_data="add fries"),
        ],
        [
            InlineKeyboardButton("Drinks (3)",callback_data="add drinks"),
        ]
    ]
    reply_markup=InlineKeyboardMarkup(key_button)
    await update.message.reply_text("Here is our menu :",reply_markup=reply_markup)
    
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You can contact us at 010-123456789 or email us at example@email.com")
    
async def handle_hours(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("We are open from 9 AM to 9 PM, Monday to Sunday.")


async def handel_click(update:Update,context:ContextTypes.DEFAULT_TYPE):
    query=update.callback_query
    await query.answer()
    if query.data=="add burger":
        db=session_local()
        user_id=update.effective_user.id
        new_item=CartItem(user_id=user_id,item_name="burger")
        db.add(new_item)
        db.commit()
        await query.edit_message_text("Burger saved to your cart : 🍔")
    elif query.data=="add fries":
        db=session_local()
        user_id=update.effective_user.id
        new_item=CartItem(user_id=user_id,item_name="fries")
        db.add(new_item)
        db.commit()
        await query.edit_message_text("Fries saved to your cart : 🍟")
    elif query.data=="add drinks":
        db=session_local()
        user_id=update.effective_user.id
        new_item=CartItem(user_id=user_id,item_name="drinks")
        db.add(new_item)
        db.commit()
        await query.edit_message_text("Drinks saved to your cart : 🥂")
async def cart_method(update:Update,context:ContextTypes.DEFAULT_TYPE):
    db=session_local()
    user_id=update.effective_user.id
    cart_items=db.query(CartItem).filter(CartItem.user_id==user_id).all()
    if not cart_items:
        await update.message.reply_text("your cart is empty : ")
    else:
        cart_text="your cart : \n"
        for item in cart_items:
            cart_text+=f"{item.item_name} (quantity: {item.quantity})\n"
        await update.message.reply_text(cart_text)
    db.close()
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("^menu$"),handle_menu))
    app.add_handler(MessageHandler(filters.Regex("^contact$"),handle_contact))
    app.add_handler(MessageHandler(filters.Regex("^hours$"),handle_hours))
    app.add_handler(CallbackQueryHandler(handel_click))
    app.add_handler(CommandHandler("cart",cart_method))
    app.add_handler(MessageHandler(filters.Regex("^cart$"),cart_method))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    app.add_handler(CommandHandler("help", help_method))

    print("Bot is running...")
    app.run_polling()