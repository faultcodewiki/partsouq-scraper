import asyncio
import re
from urllib.parse import quote_plus
from apify import Actor
from bs4 import BeautifulSoup
from curl_cffi import requests


def scrape_part(query: str, include_cross_ref: bool = True, proxy_url: str | None = None) -> list[dict]:
    clean_q = query.strip()
    if not clean_q:
        return []

    url = f"https://partsouq.com/en/search/all?q={quote_plus(clean_q)}"
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None

    res = requests.get(url, impersonate="chrome", proxies=proxies, timeout=30)
    if res.status_code != 200:
        Actor.log.warning(f"[{clean_q}] HTTP {res.status_code}")
        return []

    title_map = {}
    for chunk in res.text.split("view_item")[1:]:
        b = chunk[:500]
        pid_m = re.search(r"item_id:'([^']+)'", b)
        name_m = re.search(r"item_name:'([^']+)'", b)
        if pid_m and name_m:
            title_map[pid_m.group(1)] = name_m.group(1).replace(r"\/", "/")

    soup = BeautifulSoup(res.text, "html.parser")
    results = []
    norm_q = re.sub(r"[^A-Z0-9]", "", clean_q.upper())

    for price_el in soup.select(".search-product-price"):
        card = price_el
        for _ in range(8):
            card = card.parent
            if card and card.select_one(".search-product-card-info-item"):
                break
        if not card:
            continue

        info = {}
        for item in card.select(".search-product-card-info-item"):
            lbl = item.select_one(".search-product-card-info-label")
            val = item.select_one(".search-product-card-info-value")
            if lbl and val:
                info[lbl.get_text(strip=True)] = val.get_text(strip=True)

        pn = info.get("Part number", "")
        norm_pn = re.sub(r"[^A-Z0-9]", "", pn.upper())
        is_exact = norm_pn == norm_q
        if not include_cross_ref and not is_exact:
            continue

        price_num = re.findall(r"[0-9.]+", price_el.get_text(strip=True))
        form_el = card.select_one("form[data-product-id]")
        pid = form_el["data-product-id"] if form_el else ""

        avail_raw = info.get("Availability", "")
        avail_num = re.findall(r"\d+", avail_raw)

        results.append({
            "search_query": clean_q,
            "match_type": "Exact Match" if is_exact else "Replacement / Cross-Ref",
            "part_number": pn,
            "brand": info.get("Make", ""),
            "title": title_map.get(pid, ""),
            "price_usd": float(price_num[0]) if price_num else None,
            "in_stock_qty": int(avail_num[0]) if avail_num else 0,
            "availability_raw": avail_raw,
            "lead_time": info.get("Processing", ""),
            "made_in": info.get("Made in", ""),
            "product_id": pid,
            "search_url": url,
        })

    return results


async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        part_numbers = actor_input.get("partNumbers") or ["90915-YZZD1"]
        include_cross_ref = actor_input.get("includeCrossRef", True)

        proxy_url = None
        proxy_cfg = actor_input.get("proxyConfiguration")
        if proxy_cfg:
            proxy_info = await Actor.create_proxy_configuration(actor_proxy_input=proxy_cfg)
            if proxy_info:
                proxy_url = await proxy_info.new_url()

        total_saved = 0
        for idx, pn in enumerate(part_numbers, 1):
            Actor.log.info(f"[{idx}/{len(part_numbers)}] Searching: {pn}")
            try:
                items = await asyncio.to_thread(scrape_part, pn, include_cross_ref, proxy_url)
                if items:
                    await Actor.push_data(items)
                    total_saved += len(items)
                    Actor.log.info(f"  -> {len(items)} items saved")
                else:
                    Actor.log.info(f"  -> No results: {pn}")
            except Exception as e:
                Actor.log.error(f"[{pn}] Error: {e}")

            if idx < len(part_numbers):
                await asyncio.sleep(1.2)

        Actor.log.info(f"Done! Total {total_saved} parts extracted.")
