import logging
from asyncio import sleep

import aiohttp
import instabot
from asgiref.sync import sync_to_async
from instagram_private_api import ClientThrottledError

from utils.cookies_work import update_cookie
from data.config import IG_USERNAME, IG_PASSWORD, BOT_HOST, CONTROLLER_HOST
from loader import inst, ssl_context
from utils.img_work import get_banana_num
from utils.status import update_status


async def check_stories():
    try:
        logging.info("~~~~~~~~~~~~~~~~~~START CHECK STORIES~~~~~~~~~~~~~~~~~~")
        success_threads_count = 0

        update_cookie()

        inst.login(username=IG_USERNAME, password=IG_PASSWORD, is_threaded=True)
        await sleep(1)

        pending_threads: list = await get_pending_threads(inst)
        await sleep(1)

        threads_count = len(pending_threads)

        for thread in pending_threads:
            item: dict = thread["last_permanent_item"]
            item_type = item["item_type"]
            thread_id = thread["thread_id"]

            user = thread["users"][0]
            ig_username = user["username"]
            ig_user_id = user["pk"]

            if thread["thread_type"] != "private":
                await hide_thread(thread_id, inst)
                await sleep(1)
                continue

            if item_type == "reel_share" and item["reel_share"]["mentioned_user_id"] == inst.user_id:
                stories_url = item["reel_share"]["media"]["image_versions2"]["candidates"][0]["url"]
                banana_num: int = await get_banana_num(stories_url)

                if banana_num:
                    await notify_succeeded_stories(ig_username, banana_num)
                    success_threads_count += 1
                else:
                    await notify_failed_stories(ig_username)

            else:
                user_image_stories, user_video_stories = await get_user_stories(ig_user_id, inst)
                await sleep(1)

                count_img_stories, count_video_stories = len(user_image_stories), len(user_video_stories)
                banana_num = await show_last_stories(user_image_stories, count=3) if count_img_stories > 0 else None
                if banana_num:
                    await notify_succeeded_stories(ig_username, banana_num)
                elif count_img_stories > 0 or count_video_stories > 0:
                    await notify_failed_stories(ig_username)

            await hide_thread(thread_id, inst)
            await sleep(1)

        inst.logout()
        await notify_reboot_aws(
            status="SUCCESS",
            threads_count=threads_count,
            success_threads_count=success_threads_count)
        logging.info("~~~~~~~~~~~~~~~~~~FINISH CHECK STORIES~~~~~~~~~~~~~~~~~~")
    except ClientThrottledError as exc:
        await notify_reboot_aws(
            status="ERROR: "+exc.__str__(),
            threads_count=threads_count,
            success_threads_count=success_threads_count
        )
    # except Exception as exc:
    #     await notify_reboot_aws(status="ERROR"+exc.__str__())


@sync_to_async
def get_pending_threads(inst_bot: instabot.Bot):
    logging.info(f"Get NEW pending_threads")
    return inst_bot.get_pending_thread_requests()


@sync_to_async
def hide_thread(thread_id: str, inst_bot: instabot.Bot):
    inst_bot.api.hide_pending_thread(thread_id)


@sync_to_async
def get_user_stories(ig_user_id: str, inst_bot: instabot.Bot):
    return inst_bot.get_user_stories(ig_user_id)


async def notify_reboot_aws(status: str, threads_count: int, success_threads_count: int):
    update_status(status)

    async with aiohttp.ClientSession() as session:
        logging.info(f"Restart aws-inst server with status {status}")
        url = CONTROLLER_HOST + "/restart_inst_bot"
        json = dict(
            status=status,
            threads_count=threads_count,
            success_threads_count=success_threads_count
        )
        await session.post(url, json=json, ssl_context=ssl_context)


async def show_last_stories(user_image_stories: list, count: int = 3) -> int:
    amount_stories = len(user_image_stories)
    count = count if amount_stories > count else amount_stories
    max_i = amount_stories - 1
    banana_num: int
    for i in range(max_i, max_i-count, -1):
        banana_num = await get_banana_num(user_image_stories[i])
        if banana_num:
            return banana_num


async def notify_succeeded_stories(ig_username: str, banana_num: int):
    async with aiohttp.ClientSession() as session:
        url = BOT_HOST + "/notify_succeeded_stories"
        await session.post(url, data=str(banana_num), ssl_context=ssl_context)
        logging.info(f"Notify succeeded stories for IG_User={ig_username} with banana_num={banana_num}")


async def notify_failed_stories(ig_username: str):
    async with aiohttp.ClientSession() as session:
        url = BOT_HOST + "/notify_failed_stories"
        await session.post(url, data=str(ig_username), ssl_context=ssl_context)
        logging.info(f"Notify failed stories for user with IG_User={ig_username}")