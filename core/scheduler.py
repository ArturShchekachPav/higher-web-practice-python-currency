import asyncio
from datetime import datetime, timezone
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def run_spider() -> None:
    """Запускает Scrapy spider в отдельном процессе."""
    logger.info("Starting CBR spider...")
    try:
        process = await asyncio.create_subprocess_exec(
            "scrapy", "crawl", "cbr", "-a", "days=30",
            cwd="/app/parser",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        logger.info("Spider stdout: %s", stdout.decode(errors="replace"))
        if process.returncode != 0:
            logger.error("Spider stderr: %s", stderr.decode(errors="replace"))
        else:
            logger.info("Spider finished successfully")
    except Exception:
        logger.exception("Failed to run spider")


def start_scheduler() -> None:
    scheduler.add_job(
        run_spider,
        trigger=IntervalTrigger(hours=24),
        id="cbr_parser",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started: CBR spider will run every 24 hours")


def stop_scheduler() -> None:
    scheduler.shutdown(wait=False)