from typing import List, Dict, AnyStr
import logging
import re

import asyncio
import time

from mastoBot.configManager import ConfigAccessor
from mastoBot.mastoBot import MastoBot, handleMastodonExceptions

class MyBot(MastoBot):
    @handleMastodonExceptions
    def processMention(self, mention: Dict):
        api_status = self.getStatus(mention.get("status"))
        api_account = self.getAccount(mention.get("account"))
        content = api_status.get("content")

        logging.info(f"📬 \t Mention processed: {mention.get('id')}")
        self.dismissNotification(mention.get("id"))

    @handleMastodonExceptions
    def processReblog(self, reblog: Dict):
        self.dismissNotification(reblog.get("id"))

    @handleMastodonExceptions
    def processFavourite(self, favourite: Dict):
        self.dismissNotification(favourite.get("id"))

    @handleMastodonExceptions
    def processFollow(self, follow: Dict):
        # Get latest account from the Mastodon API
        api_account = self.getAccount(follow.get("account"))
        account = api_account.get("acct")

        template_data = {"account": account}

        # Generate the welcoming message from the template
        try:
            output = self.getTemplate("new_follow.txt", template_data)
            self._api.status_post(status=output, visibility="direct")
        except Exception as e:
            logging.critical("❗ \t Error posting Status")
            raise e

        logging.info(f"📭 \t Follow processed: {follow.get('id')}")
        self.dismissNotification(follow.get("id"))

    @handleMastodonExceptions
    def processPoll(self, poll: Dict):
        self.dismissNotification(poll.get("id"))

    @handleMastodonExceptions
    def processFollowRequest(self, follow_request: Dict):
        self.dismissNotification(follow_request.get("id"))

    @handleMastodonExceptions
    def processUpdate(self, update: Dict) -> None:
        self.dismissNotification(update.get("id"))

if __name__ == "__main__":
    config = ConfigAccessor("config.yml")
    credentials = ConfigAccessor("credentials.yml")
    bot = MyBot(credentials=credentials, config=config)

    async def runBot():
        while True:
            logging.info("✅ \t Running bot")
            await bot.run()
            await asyncio.sleep(10)

    async def main():
        await asyncio.gather(runBot())

    while True:
        try:
            asyncio.run(main())
        except:
            time.sleep(10)
            pass
