"""
Telegram Group Forwarder
Automatically forwards messages from one group/channel to another using your account.
Required: pip install telethon
"""

import asyncio
import json
import os
import sys
from telethon import TelegramClient, events
from telethon.tl.types import Channel, Chat
from telethon.errors import SessionPasswordNeededError

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)

async def get_all_groups(client):
    groups = []
    async for dialog in client.iter_dialogs():
        if isinstance(dialog.entity, (Channel, Chat)):
            groups.append({
                "id": dialog.entity.id,
                "title": dialog.name,
                "username": getattr(dialog.entity, "username", None)
            })
    return groups

async def authorize(client):
    """Authorization with 2FA support"""
    phone = input("\n📱 Enter your phone number (with country code, e.g. +1...): ").strip()
    await client.send_code_request(phone)

    code = input("📨 Enter the code from Telegram: ").strip()

    try:
        await client.sign_in(phone, code)
    except SessionPasswordNeededError:
        password = input("🔐 Enter your 2FA password: ").strip()
        await client.sign_in(password=password)

    return await client.is_user_authorized()

async def get_client_authorized(api_id, api_hash):
    """Returns a connected and authorized client"""
    client = TelegramClient("forwarder_session", api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        print("🔑 Authorization required...")
        ok = await authorize(client)
        if not ok:
            print("❌ Authorization failed")
            await client.disconnect()
            return None

    me = await client.get_me()
    print(f"✅ Authorized as: {me.first_name} (@{me.username})")
    return client

async def run_forwarder(api_id, api_hash, source_id, target_id, source_title, target_title):
    client = await get_client_authorized(api_id, api_hash)
    if not client:
        return

    try:
        source_entity = await client.get_entity(source_id)
        target_entity = await client.get_entity(target_id)
    except Exception as e:
        print(f"❌ Could not find group: {e}")
        await client.disconnect()
        return

    print(f"\n🚀 Forwarder is running!")
    print(f"📥 Source: {getattr(source_entity, 'title', source_title)}")
    print(f"📤 Target: {getattr(target_entity, 'title', target_title)}")
    print("─" * 40)
    print("Waiting for messages... (Ctrl+C to stop)\n")

    @client.on(events.NewMessage(chats=source_id))
    async def handler(event):
        msg = event.message
        try:
            if msg.media:
                await client.send_file(
                    target_entity,
                    file=msg.media,
                    caption=msg.text or "",
                )
            else:
                await client.send_message(target_entity, msg.text)
            preview = (msg.text or "[media]")[:60]
            print(f"✉️  Forwarded: {preview}")
        except Exception as e:
            print(f"❌ Forwarding error: {e}")

    await client.run_until_disconnected()

async def setup_groups(api_id, api_hash):
    """Select groups from the list"""
    client = await get_client_authorized(api_id, api_hash)
    if not client:
        return None, None

    print("\n⏳ Loading list of groups and channels...")
    groups = await get_all_groups(client)
    await client.disconnect()

    print(f"\n📋 Found {len(groups)} groups/channels:\n")
    for i, g in enumerate(groups):
        uname = f" @{g['username']}" if g['username'] else ""
        print(f"  [{i+1:3}] {g['title']}{uname}")

    print()
    src_idx = int(input("Select NUMBER of source group (from): ").strip()) - 1
    tgt_idx = int(input("Select NUMBER of target group (to): ").strip()) - 1

    return groups[src_idx], groups[tgt_idx]

async def main():
    print("=" * 50)
    print("   TELEGRAM GROUP FORWARDER")
    print("=" * 50)

    config = load_config()

    # API credentials
    if not config.get("api_id"):
        print("\n📌 Get your API keys at: https://my.telegram.org/apps")
        config["api_id"] = int(input("  Enter API ID: ").strip())
        config["api_hash"] = input("  Enter API Hash: ").strip()
        save_config(config)

    api_id = config["api_id"]
    api_hash = config["api_hash"]

    # Group selection
    if not config.get("source_id") or "--reset" in sys.argv:
        source, target = await setup_groups(api_id, api_hash)
        if not source:
            return
        config["source_id"] = source["id"]
        config["target_id"] = target["id"]
        config["source_title"] = source["title"]
        config["target_title"] = target["title"]
        save_config(config)
        print(f"\n✅ Settings saved!")
        print(f"   📥 Source → {source['title']}")
        print(f"   📤 Target → {target['title']}\n")
    else:
        print(f"\n📥 Source: {config.get('source_title', config['source_id'])}")
        print(f"📤 Target: {config.get('target_title', config['target_id'])}")
        print("(run with --reset to change groups)\n")

    await run_forwarder(
        api_id, api_hash,
        config["source_id"], config["target_id"],
        config.get("source_title", ""), config.get("target_title", "")
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Forwarder stopped.")
