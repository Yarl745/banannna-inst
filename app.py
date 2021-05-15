from datetime import datetime, timedelta
from random import randint

from aiohttp import web

from jobs import check_stories
from loader import scheduler
from utils.logging import logging
from utils.status import read_status


async def schedule_checking(minutes=45):
    check_stories_date = datetime.now() + timedelta(minutes=minutes)
    scheduler.add_job(check_stories, "date", run_date=check_stories_date)
    pass


async def on_startup():
    last_status = read_status()
    minutes = randint(47, 59) if last_status == "SUCCESS" else 1
    await schedule_checking(minutes=minutes)

    app = web.Application()

    logging.info(f"Start banannna-inst")

    return app


if __name__ == "__main__":
    scheduler.start()
    web.run_app(on_startup())