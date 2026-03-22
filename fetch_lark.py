import json
import os
import urllib.request

APP_ID     = os.environ.get("LARK_APP_ID",     "cli_a9351d9c2578de15")
APP_SECRET = os.environ.get("LARK_APP_SECRET",  "ip3E3PgnLxq5lLKRbfjcabLSRCt21Box")
APP_TOKEN  = os.environ.get("LARK_APP_TOKEN",   "K4tEbmzwyah8XMs0lxljj7j8pJf")
TABLE_ID   = os.environ.get("LARK_TABLE_ID",    "tbljjIum2ML02FEG")


def get_access_token():
    url  = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    body = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req  = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read())
    if data.get("code") != 0:
        raise Exception("Auth gagal: " + data.get("msg", ""))
    return data["tenant_access_token"]


def fetch_all_records(token):
    all_items  = []
    page_token = ""

    while True:
        url = (
            f"https://open.larksuite.com/open-apis/bitable/v1/apps/{APP_TOKEN}"
            f"/tables/{TABLE_ID}/records?page_size=100"
        )
        if page_token:
            url += f"&page_token={page_token}"

        req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token})
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read())

        if data.get("code") != 0:
            raise Exception("Fetch gagal: " + data.get("msg", ""))

        all_items.extend(data["data"].get("items", []))

        if data["data"].get("has_more"):
            page_token = data["data"]["page_token"]
        else:
            break

    return all_items


if __name__ == "__main__":
    print("Mengambil token...")
    token = get_access_token()

    print("Mengambil data dari Lark Base...")
    items = fetch_all_records(token)

    print(f"Berhasil: {len(items)} record ditemukan")

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({"ok": True, "items": items}, f, ensure_ascii=False, indent=2)

    print("data.json berhasil disimpan.")
