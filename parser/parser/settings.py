import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

BOT_NAME = "parser"

SPIDER_MODULES = ["parser.spiders"]
NEWSPIDER_MODULE = "parser.spiders"

ADDONS = {}

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1

FEED_EXPORT_ENCODING = "utf-8"

ITEM_PIPELINES = {
    "parser.pipelines.DatabasePipeline": 300,
}

USER_AGENT = "currency-service/1.0 (+https://example.com)"
