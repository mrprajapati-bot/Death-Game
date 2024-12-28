#  GNU nano 8.2                                                                      daethgameonly.py
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Define initial player stats
player_stats = {
    "coins": 500000,  # Initial coins
    "gems": 5000,     # Initial gems
    "tokens": 200,    # Initial tokens
}

# Define the deck of cards
deck = [
    "Death Card", "Death Card",
    "Coins Card", "Gems Card", "Gems Card",
    "Masks Card", "Tokens Card",
    "Empty Card", "Empty Card"
]

# Shuffle the deck
def shuffle_deck():
    return random.sample(deck, len(deck))

# Card outcomes
def card_outcome(card, stats):
    if card == "Death Card":
        stats["coins"] = max(0, stats["coins"] - 50000)
        stats["gems"] = max(0, stats["gems"] - 500)
        stats["tokens"] = max(0, stats["tokens"] - 20)
        return f"💀 You drew a Death Card! You lost 50,000 coins, 500 gems, and 20 tokens."
    elif card == "Coins Card":
        stats["coins"] += 150000
        return f"💰 You drew a Coins Card! You won 150,000 coins."
    elif card == "Gems Card":
        stats["gems"] += 2000
        return f"💎 You drew a Gems Card! You won 2,000 gems."
    elif card == "Masks Card":
        return f"🎭 You drew a Masks Card! You won 150 masks. (Masks are collectible but don't affect stats.)"
    elif card == "Tokens Card":
        stats["tokens"] += 150
        return f"🎟️ You drew a Tokens Card! You won 150 tokens."
    elif card == "Empty Card":
        return f"🃏 You drew an Empty Card. Nothing happens."
    return "❌ Unknown card."

# Start and Play command combined
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Shuffle the deck
    shuffled_deck = shuffle_deck()
    context.user_data["shuffled_deck"] = shuffled_deck
    context.user_data["game_active"] = True  # Game is active

    # Create a 3x3 grid of card backs
    keyboard = [
        [InlineKeyboardButton("🃏 Card", callback_data=str(i)) for i in range(3)],
        [InlineKeyboardButton("🃏 Card", callback_data=str(i)) for i in range(3, 6)],
        [InlineKeyboardButton("🃏 Card", callback_data=str(i)) for i in range(6, 9)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎲 Welcome to 'Choose a Card'! Tap a card to reveal it.\n"
        f"Your starting stats:\nCoins: {player_stats['coins']}\n"
        f"Gems: {player_stats['gems']}\nTokens: {player_stats['tokens']}",
        reply_markup=reply_markup
    )

# Handle card selection
async def reveal_card(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Check if the game is still active
    if not context.user_data.get("game_active", False):
        await query.answer("Game over! Restart the game with /start.", show_alert=True)
        return

    # Retrieve the shuffled deck
    shuffled_deck = context.user_data.get("shuffled_deck")

    if not shuffled_deck:
        await query.edit_message_text("Type '/start' to start a new game.")
        return

    # Reveal the selected card and disable further actions
    card_index = int(query.data)
    selected_card = shuffled_deck[card_index]
    result = card_outcome(selected_card, player_stats)
    context.user_data["game_active"] = False  # Disable further selections

    # Create a 3x3 grid with all cards revealed
    keyboard = []
    for row in range(3):
        keyboard_row = [
            InlineKeyboardButton(shuffled_deck[row * 3 + col], callback_data="disabled")
            for col in range(3)
        ]
        keyboard.append(keyboard_row)

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Edit the message with the selected card and reveal all
    stats = (
        f"\nYour current stats:\nCoins: {player_stats['coins']}\n"
        f"Gems: {player_stats['gems']}\nTokens: {player_stats['tokens']}"
    )
    await query.edit_message_text(
        f"You revealed card {card_index + 1}: {result}\n"
        f"All cards are now revealed.\n{stats}\n\n"
        "Type /start to start a new game.",
        reply_markup=reply_markup
    )

# Main function
def main():
    TOKEN = "7996841554:AAGefNt0UsOuqh1gGkUbVBnUYnefQNY6kLc"

    # Create the application
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(reveal_card))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
