import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Configuração de Logs
logging.basicConfig(level=logging.INFO)

# ======================================================
# PREENCHA ABAIXO COM SEUS DADOS:
TOKEN = 8911054574:AAHwEmuDVuVon-f2JZ-qQr8o8A7b-n2-OCo
CHAT_ID_SUPORTE = -1004474645352  # COLOQUE O SEU ID DO GRUPO AQUI
# ======================================================


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        f"👋 **Olá, {update.effective_user.first_name}!**\n\n"
        "Seja bem-vindo ao nosso suporte pelo Telegram.\n"
        "Envie sua dúvida, comprovante ou mensagem abaixo e nossa equipe responderá em breve!"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")


async def receber_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Evita encaminhar mensagens enviadas dentro do próprio grupo de suporte
    if update.effective_chat.id == CHAT_ID_SUPORTE:
        return

    user = update.effective_user
    username = f"@{user.username}" if user.username else "Sem username"

    info_cliente = (
        f"📩 **NOVA MENSAGEM DE ATENDIMENTO**\n"
        f"👤 **Cliente:** {user.first_name} ({username})\n"
        f"🆔 **ID do Cliente:** `{user.id}`\n"
        f"-----------------------------------"
    )

    # 1. Envia ficha informativa do cliente para o seu grupo
    await context.bot.send_message(
        chat_id=CHAT_ID_SUPORTE, text=info_cliente, parse_mode="Markdown"
    )

    # 2. Encaminha a mensagem (texto, imagem, áudio ou documento) para o grupo
    await context.bot.forward_message(
        chat_id=CHAT_ID_SUPORTE,
        from_chat_id=update.effective_chat.id,
        message_id=update.message.message_id,
    )

    # 3. Responde o cliente confirmando o recebimento
    await update.message.reply_text(
        "✅ **Mensagem recebida!**\nNossa equipe já foi notificada e vai te responder aqui em breve."
    )


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.ALL & ~filters.COMMAND, receber_mensagem)
    )

    print("🚀 Bot ativo e aguardando mensagens...")
    app.run_polling()


if __name__ == "__main__":
    main()
