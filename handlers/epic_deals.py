import os
import json
import html
import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import httpx

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────
# SETTINGS
# ─────────────────────────────────────────
TZ = ZoneInfo("Europe/Oslo")
COUNTRY = "NO"
LOCALE = "nb-NO"          # prices come back as "184,50 kr"
STORE_LANG = "nb"         # store.epicgames.com/nb/p/<slug>
CACHE_PATH = os.getenv("EPIC_CACHE_PATH", "data/epic_deals.json")
GRAPHQL_URL = "https://store.epicgames.com/graphql"
MIN_DISCOUNT = 30         # skip deals below this %
DEALS_PER_WEEK = 7        # one per day
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

QUERY = """
query searchStoreQuery($country: String!, $locale: String, $count: Int, $start: Int,
                       $onSale: Boolean, $category: String) {
  Catalog {
    searchStore(country: $country, locale: $locale, count: $count, start: $start,
                onSale: $onSale, category: $category) {
      elements {
        title
        productSlug
        urlSlug
        keyImages { type url }
        catalogNs { mappings(pageType: "productHome") { pageSlug } }
        offerMappings { pageSlug pageType }
        price(country: $country) {
          totalPrice {
            originalPrice
            discountPrice
            fmtPrice(locale: $locale) { originalPrice discountPrice }
          }
        }
      }
    }
  }
}
"""


# ─────────────────────────────────────────
# PARSER
# ─────────────────────────────────────────
def _slug(el):
    for m in el.get("offerMappings") or []:
        if m.get("pageType") == "productHome" and m.get("pageSlug"):
            return m["pageSlug"]
    for m in (el.get("catalogNs") or {}).get("mappings") or []:
        if m.get("pageSlug"):
            return m["pageSlug"]
    raw = el.get("productSlug") or el.get("urlSlug")
    return raw.split("/")[0] if raw else None


def _image(el):
    imgs = {i["type"]: i["url"] for i in el.get("keyImages") or [] if i.get("url")}
    for t in ("OfferImageWide", "DieselStoreFrontWide", "Thumbnail", "OfferImageTall"):
        if t in imgs:
            return imgs[t]
    return next(iter(imgs.values()), None)


def _parse(el):
    total = (el.get("price") or {}).get("totalPrice") or {}
    orig = total.get("originalPrice") or 0
    disc = total.get("discountPrice") or 0
    slug = _slug(el)
    if not orig or disc >= orig or not slug:
        return None

    percent = round((orig - disc) / orig * 100)
    if percent < MIN_DISCOUNT:
        return None

    fmt = total.get("fmtPrice") or {}
    return {
        "title": el.get("title", "Unknown"),
        "percent": percent,
        "original_price": fmt.get("originalPrice", ""),
        "discount_price": fmt.get("discountPrice", ""),
        "image": _image(el),
        "url": f"https://store.epicgames.com/{STORE_LANG}/p/{slug}",
    }


async def fetch_deals():
    payload = {
        "query": QUERY,
        "variables": {
            "country": COUNTRY,
            "locale": LOCALE,
            "count": 100,
            "start": 0,
            "onSale": True,
            "category": "games/edition/base",  # base games only, no DLC
        },
    }
    headers = {"User-Agent": USER_AGENT, "Content-Type": "application/json"}

    async with httpx.AsyncClient(timeout=20, headers=headers, follow_redirects=True) as client:
        resp = await client.post(GRAPHQL_URL, json=payload)
        resp.raise_for_status()
        elements = resp.json()["data"]["Catalog"]["searchStore"]["elements"]

    deals, seen = [], set()
    for el in elements:
        deal = _parse(el)
        if deal and deal["title"] not in seen:
            seen.add(deal["title"])
            deals.append(deal)

    deals.sort(key=lambda d: d["percent"], reverse=True)
    return deals[:DEALS_PER_WEEK]


# ─────────────────────────────────────────
# WEEKLY CACHE
# ─────────────────────────────────────────
def load_cache():
    try:
        with open(CACHE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_cache(deals):
    os.makedirs(os.path.dirname(CACHE_PATH) or ".", exist_ok=True)
    tmp = CACHE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(
            {"fetched_at": datetime.now(TZ).isoformat(), "deals": deals},
            f, ensure_ascii=False, indent=2,
        )
    os.replace(tmp, CACHE_PATH)


def _last_monday_8(now):
    monday = (now - timedelta(days=now.weekday())).replace(
        hour=8, minute=0, second=0, microsecond=0
    )
    return monday if monday <= now else monday - timedelta(days=7)


def _is_stale(cache):
    """Cache is stale if it is empty or was fetched before the latest Monday 08:00."""
    if not cache or not cache.get("deals"):
        return True
    fetched = datetime.fromisoformat(cache["fetched_at"])
    return fetched < _last_monday_8(datetime.now(TZ))


async def refresh_epic_deals(context=None):
    """Monday 08:00 job. On failure the old cache is kept."""
    try:
        deals = await fetch_deals()
        if not deals:
            logger.warning("Epic: parser returned 0 deals, keeping old cache.")
            return None
        save_cache(deals)
        logger.info(f"Epic: cache refreshed, {len(deals)} deals.")
        return deals
    except Exception as e:
        logger.error(f"Epic refresh error: {e}")
        return None


# ─────────────────────────────────────────
# DAILY POST (09:00)
# ─────────────────────────────────────────
async def send_epic_deal(context):
    cache = load_cache()
    if _is_stale(cache):  # first run / redeploy wiped the file / missed Monday
        await refresh_epic_deals()
        cache = load_cache()

    if not cache or not cache.get("deals"):
        logger.warning("Epic: no deals to post.")
        return

    deals = cache["deals"]
    deal = deals[datetime.now(TZ).weekday() % len(deals)]  # Mon=0 ... Sun=6

    title = html.escape(deal["title"])
    url = html.escape(deal["url"], quote=True)
    caption = (
        "<b>🎮 Epic Games Deal of the Day</b>\n\n"
        f"<b>{title}</b>\n"
        f"🔥 <b>-{deal['percent']}%</b>\n"
        f"<s>{html.escape(deal['original_price'])}</s> → "
        f"<b>{html.escape(deal['discount_price'])}</b>\n\n"
        f'<a href="{url}">Open in Epic Games Store</a>'
    )

    try:
        if deal.get("image"):
            await context.bot.send_photo(
                chat_id=CHANNEL_ID, photo=deal["image"],
                caption=caption, parse_mode="HTML",
            )
        else:
            await context.bot.send_message(
                chat_id=CHANNEL_ID, text=caption, parse_mode="HTML"
            )
        logger.info(f"Epic deal sent: {deal['title']}")
    except Exception as e:
        logger.error(f"Epic send error: {e}")
