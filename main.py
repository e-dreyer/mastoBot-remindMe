from typing import List, Dict, AnyStr
import logging
import re

import asyncio
import time
import datetime

from mastoBot.configManager import ConfigAccessor
from mastoBot.mastoBot import MastoBot, handleMastodonExceptions

class MyBot(MastoBot):
    @handleMastodonExceptions
    def processMention(self, mention: Dict):
        # Get the mention data
        api_status = self.getStatus(mention.get("status"))
        content = api_status.get("content")
        mention_created_at = api_status.get("created_at")
        
        # Get the account data
        api_account = self.getAccount(mention.get("account"))
        
        # Pattern for extracting time parameters
        pattern = r'(?i)<span class="h-card"><a href="https://techhub\.social/@remindMe" class="u-url mention">@<span>remindMe</span></a></span>\s*(?:(?:(\d+)\s*years?)?\s*)?(?:(\d+)\s*months?)?\s*(?:(\d+)\s*weeks?)?\s*(?:(\d+)\s*days?)?\s*(?:(\d+)\s*hours?)?\s*(?:(\d+)\s*minutes?)?'

        # Search for matches
        matches = re.search(pattern, content)
        
        # If matches are found
        if matches:
            # Extract data
            years, months, weeks, days, hours, minutes = map(lambda x: int(x) if x else 0, matches.groups())
            logging.info(f"Years: {years}, Months: {months}, Weeks: {weeks}, Days: {days}, Hours: {hours}, Minutes: {minutes}")
            
            # Calculate delta time
            delta = datetime.timedelta(
                days=days + weeks * 7 + months * 30 + years * 365,
                hours=hours,
                minutes=minutes
            )
            
            future_time = mention_created_at + delta
            logging.info(f"Current Time: {mention_created_at}")
            logging.info(f"Future Time: {future_time}")
            
            # Create scheduled message
            scheduled_reminder_message = bot.getTemplate(
                file_name='scheduled_reminder.txt',
                data={
                    'account': api_account.get('acct'),
                    'requested_post_url': api_status.get('url')
                })
            
            # Create reply message
            reply_message = bot.getTemplate(
                file_name='reply_to_request.txt',
                data={
                    'account': api_account.get('acct')
                }
            )
            
            try:
                # Post scheduled post
                scheduled_post = bot._api.status_post(
                    status=scheduled_reminder_message, 
                    scheduled_at=future_time,
                    visibility='direct'
                    )
                
                # Post reply and acknowledging message
                reply_post = bot._api.status_post(
                    status=reply_message,
                    in_reply_to_id=api_status.get('id'),
                    visibility='direct'
                )
                
                logging.info(f'new scheduled post: {scheduled_post}')
                logging.info(f'new reply post: {reply_post}')
                
                # Favourite their request message
                bot.favoriteStatus(api_status.get('id'))
        
                # Dismiss the notification
                logging.info(f"📬 \t Mention processed: {mention.get('id')}")
                self.dismissNotification(mention.get("id"))
            except:
                pass

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
