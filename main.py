import asyncio
import logging
import os
from contextlib import suppress
from tempfile import NamedTemporaryFile
from typing import Awaitable, Callable, Dict, List, Optional, TypedDict

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from pdf import PDFEditor, text_generator
from templates import gb_template, ie_template, ir_template

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN (или BOT_TOKEN) должен быть задан в .env")

TextGenerator = Callable[[str], List[dict]]


class ModeConfig(TypedDict):
    label: str
    required_lines: int
    template_path: str
    generator: TextGenerator
    template_hint: str
    result_name: str


MODE_CONFIG: Dict[str, ModeConfig] = {
    "israel": {
        "label": "Israel",
        "required_lines": 20,
        "template_path": "template_ir.pdf",
        "generator": text_generator.generate_text_data_ir,
        "template_hint": ir_template,
        "result_name": "israel_statement.pdf",
    },
    "ireland": {
        "label": "Ireland",
        "required_lines": 23,
        "template_path": "template_ie.pdf",
        "generator": text_generator.generate_text_data_ie,
        "template_hint": ie_template,
        "result_name": "ireland_statement.pdf",
    },
    "uk": {
        "label": "UK",
        "required_lines": 12,
        "template_path": "template_uk.pdf",
        "generator": text_generator.generate_text_data_uk,
        "template_hint": gb_template,
        "result_name": "uk_statement.pdf",
    },
}

user_modes: Dict[int, str] = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if not message:
        return
    await message.reply_text(
        "Привет! Я генерирую PDF по заранее подготовленным шаблонам.\n"
        "Выбери режим командой /israel, /ireland или /uk и отправь данные построчно.\n"
        "Команда /info покажет подробную справку."
    )


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if not message:
        return
    await message.reply_text(
        "Доступные режимы:\n"
        "• /israel — счёт Israel (20 строк)\n"
        "• /ireland — счёт Ireland (23 строки)\n"
        "• /uk — счёт Великобритания (12 строк)\n\n"
        "После активации режима просто пришли данные построчно. "
        "Если нужен новый документ — выбери режим заново. "
        "Команда /return отменяет текущий режим."
    )


async def activate_mode(update: Update, mode_key: str) -> None:
    message = update.message
    user = update.effective_user
    if not message or not user:
        return

    config = MODE_CONFIG[mode_key]
    user_modes[user.id] = mode_key
    await message.reply_text(
        f"📝 Режим {config['label']} активирован!\n"
        f"Отправь {config['required_lines']} строк данных в одном сообщении.\n"
        f"Пример:\n{config['template_hint']}",
        parse_mode=ParseMode.MARKDOWN,
    )


def build_mode_handler(mode_key: str) -> Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]:
    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await activate_mode(update, mode_key)

    return handler


async def reset_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    user = update.effective_user
    if not message or not user:
        return

    if user.id in user_modes:
        user_modes.pop(user.id, None)
        await message.reply_text("❌ Режим отменён")
    else:
        await message.reply_text("ℹ️ Нет активного режима")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    user = update.effective_user
    if not message or not message.text or not user:
        return

    mode_key = user_modes.get(user.id)
    if not mode_key:
        await message.reply_text("ℹ️ Сначала выбери режим: /israel, /ireland или /uk")
        return

    await process_pdf(update, context, mode_key, message.text)
    user_modes.pop(user.id, None)


async def process_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    mode_key: str,
    user_message: str,
) -> None:
    message = update.message
    if not message:
        return

    config = MODE_CONFIG[mode_key]
    required_lines = config["required_lines"]
    lines = user_message.strip().split("\n")

    if len(lines) < required_lines:
        await message.reply_text(
            f"❌ Недостаточно данных: получено {len(lines)}, нужно {required_lines} строк."
        )
        return

    await message.reply_text("⏳ Начинаю обработку PDF...")

    pdf_path: Optional[str] = None
    try:
        generator: TextGenerator = config["generator"]
        text_data = generator(user_message)
        template_path = config["template_path"]
        pdf_path = await asyncio.to_thread(build_pdf, template_path, text_data)
        await send_pdf(update, context, pdf_path, config["result_name"])
    except Exception as exc:  # noqa: BLE001
        logging.exception("Не удалось создать PDF для режима %s", mode_key)
        await message.reply_text(f"❌ Ошибка создания PDF: {exc}")
    finally:
        if pdf_path and os.path.exists(pdf_path):
            with suppress(OSError):
                os.remove(pdf_path)


def build_pdf(template_path: str, text_data: List[dict]) -> str:
    editor = PDFEditor(template_path)
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        output_path = tmp.name
    editor.add_text(output_path, text_data)
    return output_path


async def send_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    pdf_path: str,
    filename: str,
) -> None:
    chat = update.effective_chat
    if not chat:
        return
    with open(pdf_path, "rb") as pdf_file:
        await context.bot.send_document(
            chat_id=chat.id,
            document=pdf_file,
            filename=filename,
            caption="✅ Готово! Вот твой PDF файл.",
        )


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if message:
        await message.reply_text("⚠️ Неизвестная команда. Используй /info для справки.")


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start, block=True))
    application.add_handler(CommandHandler("info", info, block=True))
    application.add_handler(CommandHandler("return", reset_mode, block=True))
    application.add_handler(CommandHandler("israel", build_mode_handler("israel"), block=True))
    application.add_handler(CommandHandler("ireland", build_mode_handler("ireland"), block=True))
    application.add_handler(CommandHandler("uk", build_mode_handler("uk"), block=True))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    logging.info("Запуск Telegram PDF бота...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
