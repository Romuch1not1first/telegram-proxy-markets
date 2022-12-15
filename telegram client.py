import telebot
import config
from proxymarkets import scrap

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def request_handler(message):
    markup = telebot.types.ReplyKeyboardMarkup(True, True)

    bot.send_message(message.chat.id,'Multifunctional proxy search service in online stores and price comparison!!')

    menu(message)


@bot.message_handler(content_types=['text'])
def menu(message):
    TelebotInterface(message).menu_which_proxies(message)




class TelebotInterface:
    def __init__(self,message):
        self.message_handl = message

    def proxy_markets(self):
        self.markets =[
            {
                'name':'froxy',
                'link':'https://lnnk.in/d8gx',
                'characteristics':['1','Fast','Residential','Mobile']
            },
            {
                'name':'proxy6',
                'link':'https://lnnk.in/aPiH',
                'characteristics':['Fast','IPv6','IPv4','IPv4 shared']
            }

        ]

        return self.markets
        

    def menu_which_proxies(self,message):
        markup = telebot.types.ReplyKeyboardMarkup(True, True)
        self.characteristics = {
            'question':'Which proxies do you need?'
        }

        markup.row(('Fast'), ('Residential'), ('Mobile'))
        self.message_menu_info = self.characteristics['question']
        self.message_me = bot.send_message(message.chat.id, self.message_menu_info)
        
        self.into_message = bot.send_message(message.chat.id, 'Select the button',reply_markup=markup)

        bot.register_next_step_handler(message, self.menu_proxy_count)


    def menu_proxy_count(self,message):
        markup = telebot.types.ReplyKeyboardMarkup(True, True)
        bot.delete_message(message.chat.id, self.into_message.id)
        self.characteristics['cases'] = message.text

        markup.row(('IPv6'), ('IPv4'), ('IPv4 Shared'))
        self.message_menu_info += '\n-> ' + str(self.characteristics['cases'])
        bot.edit_message_text(text=str(self.message_menu_info), chat_id=message.chat.id, message_id=self.message_me.id)

        self.into_message = bot.send_message(message.chat.id, 'Select the button',reply_markup=markup)
        bot.register_next_step_handler(message, self.menu_ipv)


    def menu_ipv(self,message):
        markup = telebot.types.ReplyKeyboardMarkup(True, True)
        bot.delete_message(message.chat.id, self.into_message.id)
 
        self.characteristics['ipv'] = message.text

        self.message_menu_info += '\n-> ' + str(self.characteristics['ipv'])
        bot.edit_message_text(text=self.message_menu_info, chat_id=message.chat.id, message_id=self.message_me.id)
        
        self.into_message = bot.send_message(message.chat.id, 'Write proxy count:',reply_markup=markup)
        bot.register_next_step_handler(message, self.menu_count)

    def menu_count(self,message):
        markup = telebot.types.ReplyKeyboardMarkup(True, True)
        bot.delete_message(message.chat.id, self.into_message.id)

        self.characteristics['count'] = message.text

        self.message_menu_info += '\n-> ' + str(self.characteristics['count'])
        bot.edit_message_text(text=self.message_menu_info, chat_id=message.chat.id, message_id=self.message_me.id)
        
        markup.row(('Search for the best offer🔎'))
        self.message_ready = bot.send_message(message.chat.id, 'Are you ready to find the best offer?',reply_markup=markup)
        bot.register_next_step_handler(message, self.price_comparison)



    def price_comparison(self,message):
        # Loading
        bot.delete_message(message.chat.id, self.message_ready.id)
        self.loading_message = bot.send_message(message.chat.id, 'Loading[■□□□□□□□□□] 10%')
        bot.edit_message_text(text='[■■■■□□□□□□] 40%', chat_id=message.chat.id, message_id=self.loading_message.id)

        scraping = scrap()
        markup_inline = telebot.types.InlineKeyboardMarkup()
        hashtags_list = []
        best_hashtags_market = []

        """Save all hashtags"""
        for i, j in self.characteristics.items():
            if i != 'question':
                hashtags_list.append(j)

        # """We select offers from 1 proxy"""
        # if '1' not in hashtags_list:
        #     num = ['2','3','4','5','6','7','8','9','0']
        #     hashtags_list1 = []
        #     for i in hashtags_list:
        #         if i not in num:
        #             hashtags_list1.append(i)
        #     hashtags_list = hashtags_list1

        # Loading
        bot.edit_message_text(text='[■■■■■■■□□□] 70%', chat_id=message.chat.id, message_id=self.loading_message.id)

        """Save best proxy markets on hashtags"""
        crossing_count = 0
        for markets_info in self.proxy_markets():
            result_count = len(list(set(markets_info['characteristics']) & set(hashtags_list)))
            if crossing_count < result_count:
                crossing_count = result_count
        for markets_info in self.proxy_markets():
            result_count = len(list(set(markets_info['characteristics']) & set(hashtags_list)))
            if result_count == crossing_count:
                best_hashtags_market.append(markets_info['name'])

        price_dict = scraping.answer_price(markets=best_hashtags_market)

        # select needed product on hashtag
        price_markets = dict()

        for market, dicts in price_dict.items():
            for name, price in dicts.items():
                for i in hashtags_list: # if name in hashtags_list:
                    if name.lower() == i.lower():
                        price_markets[market] = price

        # Loading
        bot.edit_message_text(text='[■■■■■■■■□□] 80%', chat_id=message.chat.id, message_id=self.loading_message.id)

        """Change currency in usd"""
        # # select change currency
        # for market, price in price_markets.items():
        #     if market == 'proxy6':
        #         price_markets['proxy6'] = round(price / scrap.exchanger('rub'), 2)

        #select best price market
        for k, v in price_markets.items():
            price_markets[k] = float(v)
        min_vol = min(price_markets.values())
        for name, vol in price_markets.items():
            if vol == min_vol:
                best_market = name

        # Loading
        bot.edit_message_text(text='[■■■■■■■■■□] 90%', chat_id=message.chat.id, message_id=self.loading_message.id)

        """Send best deal"""
        for dicts in self.proxy_markets():
            if dicts['name'] == best_market:
                best_market = dicts['link']

        # Loading
        bot.edit_message_text(text='100% ᴄᴏᴍᴘʟᴇᴛᴇ ✅', chat_id=message.chat.id, message_id=self.loading_message.id)

        url_button = telebot.types.InlineKeyboardButton(text='Market', url=best_market)
        markup_inline.add(url_button)
        bot.send_message(message.chat.id, 'Cool, we found the best deal!',reply_markup=markup_inline)



# run
if __name__ == '__main__':
    bot.polling(non_stop=True)