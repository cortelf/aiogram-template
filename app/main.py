import asyncio
import sys
 import uvicorn
from aiogram import Bot
from aiogram import Dispatcher, Router
from aiogram.types import Update, FSInputFile

from services.auth import AuthService
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from services.unit_of_work import BotUnitOfWork
from bot.middlewares.services import ServicesMiddleware
from bot.middlewares.user import UserMiddleware
from bot.middlewares.i18n import I18nMiddleware
from internationalization import Internationalization
from internationalization.loaders import YAMLLoader
from config import Config, WebhookConfig

from bot.handlers.main import register_main_routes
from blacksheep import Application, FromJSON


async def webhook_handler(dp: Dispatcher, bot: Bot, update: FromJSON[Update]):
    await dp.feed_update(bot, update.value)


def configure_webhook(bot: Bot, dp: Dispatcher, config: WebhookConfig) -> Application:
    app = Application()
    app.services.add_instance(dp)
    app.services.add_instance(bot)

    app.router.add("POST", config.app_options.path, webhook_handler)

    @app.after_start
    async def after_start(application: Application) -> None:
        await bot.set_webhook(
            url=config.arguments.url,
            ip_address=config.arguments.ip_address,
            secret_token=config.arguments.secret_token,
            allowed_updates=config.arguments.allowed_updates,
            max_connections=config.arguments.max_connections,
            drop_pending_updates=config.arguments.drop_pending_updates,
            certificate=config.arguments.certificate and FSInputFile(config.arguments.certificate)
        )

    return app


def main(config: Config):
    i18n = Internationalization()
    i18n.initialize(YAMLLoader("locales"))
    bot_engine = create_async_engine(config.bot_connection_string)
    bot_service_factory = async_sessionmaker(bot_engine, expire_on_commit=False)

    auth = AuthService(
        bot_uow=lambda: BotUnitOfWork(bot_service_factory),
    )

    bot = Bot(config.bot_token)
    dp = Dispatcher()

    middlewares = [
        ServicesMiddleware(auth, bot),
        UserMiddleware(),
        I18nMiddleware()
    ]

    root_router = Router()
    for middleware in middlewares:
        root_router.message.outer_middleware.register(middleware)

    register_main_routes(root_router)

    dp.include_router(root_router)

    if config.webhook is not None:
        app = configure_webhook(bot, dp, config.webhook)
        uvicorn.run(app,
                    port=config.webhook.app_options.port,
                    host=config.webhook.app_options.host,
                    workers=config.webhook.app_options.workers,
                    ssl_keyfile=config.webhook.app_options.ssl_keyfile,
                    ssl_certfile=config.webhook.app_options.ssl_certfile,
                    ssl_keyfile_password=config.webhook.app_options.ssl_keyfile_password
                    )
    else:
        dp.run_polling(bot)


app_config = Config.parse_file("config.json")
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
main(app_config)
