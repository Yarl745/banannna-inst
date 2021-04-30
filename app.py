import logging

from aiohttp import web

from jobs import check_stories
from loader import scheduler


async def schedule_jobs():
    scheduler.add_job(check_stories, "interval", hours=1)
    pass


async def on_startup():
    await schedule_jobs()

    app = web.Application()

    logging.info(f"Start banannna-inst")

    return app


if __name__ == "__main__":
    scheduler.start()
    web.run_app(on_startup())