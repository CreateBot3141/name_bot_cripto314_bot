
def start_prog (user_id,namebot,message_in,status,message_id,name_file_picture,telefon_nome):
    import iz_telegram
    import requests
    import json  
    import iz_func  
    
    label_send = False


    if message_in.find ('Контакты_main') != -1:
        label = 'no send'  
        message_out,markup = iz_telegram.get_kontakt (user_id,namebot)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)


    if message_in == '/add_news':
        label_send = True
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,"Ввод новый данных через Excel",'S',0)
        iz_telegram.save_variable (user_id,namebot,"status",'Ввод новый данных через Excel')
        status = ""

    if status == 'Ввод новый данных через Excel':
        label_send = True
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,"Информация принята",'S',0)
        iz_telegram.save_variable (user_id,namebot,"status",'')
        iz_telegram.save_Excel(message_in,"","","","","","","","","","")
         
    if message_in == '/start':
        label_send = True
        iz_telegram.save_variable (user_id,namebot,"status",'')
        status = ''   

    if message_in == '/calendar':
        message_out,menu = iz_telegram.get_message (user_id,'Календарь',namebot)
        markup = ''
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 
        from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

        calendar, step = DetailedTelegramCalendar(locale = 'ru').build()
        #bot.send_message(m.chat.id,f"Select {LSTEP[step]}",reply_markup=calendar) 
        message_out = f"Select {LSTEP[step]}"
        markup = calendar
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 

    if message_in.find ('cbcal') != -1:
        from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
        result, key, step = DetailedTelegramCalendar().process(message_in)
        if not result and key:
            #bot.edit_message_text(f"Select {LSTEP[step]}",c.message.chat.id,message_id,reply_markup=key)
            message_out = f"Select {LSTEP[step]}"
            markup = key
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id) 
        elif result:
            #bot.edit_message_text(f"You selected {result}",c.message.chat.id,message_id)
            message_out = f"You selected {result}"
            markup =  ''
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id) 

    if status == 'Название задачи':
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,"Информация сохранена",'S',0) 
        iz_telegram.save_variable (user_id,namebot,"status",'')
        db,cursor = iz_func.connect ()
        sql = "INSERT INTO bot_task (name,about,namebot,status,user_id,сategory) VALUES ('{}','{}','{}','{}','{}','{}')".format (message_in,message_in,'','','','')
        cursor.execute(sql)
        db.commit()

    if message_in == '/new_task':
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,"Введите название задачи",'S',0) 
        iz_telegram.save_variable (user_id,namebot,"status",'Название задачи')

    if message_in == '/list_task':
        import datetime
        now = datetime.datetime.now()
        td = now.strftime("%d-%m-%Y %H:%M")
        db,cursor = iz_func.connect ()
        sql = "select id,name from bot_task where status = '' ORDER BY id DESC;"
        cursor.execute(sql)
        results = cursor.fetchall()    
        list_m =  ''
        refer  = 0
        for row in results:
            id,name = row.values()
            refer = refer + 1
            list_m = list_m +str(refer)+") "+str(name) +' /task_'+str(id)+'\n'
        message_out,menu = iz_telegram.get_message (user_id,'Список выполняемой работы',namebot)
        message_out = message_out.replace('%%Текущее время%%',str(td))  
        message_out = message_out.replace('%%Список задач%%',str(list_m))     
        markup = ''
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 
    
    
    if message_in.find ('add_end_task_') != -1:
        task = message_in.replace('add_end_task_',"")  
        db,cursor = iz_func.connect ()
        sql = "UPDATE bot_task SET status = 'Выполнен' WHERE id = "+str(task)+""
        print ('[+] sql:',sql)
        cursor.execute(sql)
        db.commit()
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,"Задача выполнена",'S',message_id) 

    if message_in.find ('/task_') != -1:
        task = message_in.replace('/task_',"")    
        db,cursor = iz_func.connect ()
        sql = "select id,name,about from bot_task where id = "+str(task)+";"
        id = 0
        try:
            cursor.execute(sql)
            results = cursor.fetchall()                
            for row in results:
                id,name,about = row.values()
        except:
            id = 0
        

        if id != 0:
            message_out,menu = iz_telegram.get_message (user_id,'Подробная информация про задачу',namebot)
            message_out = message_out.replace('%%Номер задачи%%',str(id)) 
            message_out = message_out.replace('%%Название задачи%%',str(name))  
            message_out = message_out.replace('%%Описание задачи%%',str(about))         
            #message_out = message_out.replace('%%Список задач%%',str(list_m))  
            list = [['rename_task_'+str(id),'Исправить'],['end_task_'+str(id),'Выполнить']]            
            markup = iz_telegram.simple_menu (user_id,namebot,list)
            print ('[+] message_out:',message_out)
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 


    if message_in == '/test05':
        label_send = True
        iz_telegram.save_variable (user_id,namebot,"status",'')
        status = ''
        message_out,menu = iz_telegram.get_message (user_id,'Настроки системы',namebot)
        import telebot    
        from telebot import types
        token = iz_telegram.get_token (namebot)
        markup = types.InlineKeyboardMarkup(row_width=6)
        bot     = telebot.TeleBot(token)
        menu11  = iz_telegram.get_namekey (user_id,namebot,'Настройка_01')
        comad11 = 'Настройка_01'
        mn11    = types.InlineKeyboardButton(text=menu11,callback_data=comad11)
        menu11  = iz_telegram.get_namekey (user_id,namebot,'Настройка_02')
        comad11 = 'Настройка_02'
        mn12    = types.InlineKeyboardButton(text=menu11,callback_data=comad11)
        menu11  = iz_telegram.get_namekey (user_id,namebot,'Настройка_03')
        comad11 = 'Настройка_03'
        mn13    = types.InlineKeyboardButton(text=menu11,callback_data=comad11)
        menu11  = iz_telegram.get_namekey (user_id,namebot,'Настройка_04')
        comad11 = 'Настройка_04'
        mn14    = types.InlineKeyboardButton(text=menu11,callback_data=comad11)
        menu11  = iz_telegram.get_namekey (user_id,namebot,'Настройка_05')
        comad11 = 'Настройка_05'
        mn15    = types.InlineKeyboardButton(text=menu11,callback_data=comad11)
        menu11  = iz_telegram.get_namekey (user_id,namebot,'Настройка_06')
        comad11 = 'Настройка_06'
        mn16    = types.InlineKeyboardButton(text=menu11,callback_data=comad11)
        markup.add(mn11,mn12,mn13,mn14,mn15,mn16)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 

    if message_in == 'Создать телеграмм бота':
        import iz_telegram
        import requests
        import json
        label_send = True
        iz_telegram.save_variable (user_id,namebot,"status",'Ввод токена')

    if status     == 'Ввод токена':
        import iz_telegram
        label_send = True
        iz_telegram.save_variable (user_id,namebot,"status",'')
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,"Проверка работы токена",'S',0) 
        token = '1855654570:AAGJGcW6bAljpmxYFrw4uAnrYXs3DaV2lG8'
        url = 'https://api.telegram.org/bot'+str(token)+'/getMe'
        answer = requests.get(url)    
        print ('    [+] Информация',answer.text)
        username   = ''
        first_name = ''
        parsed_string = json.loads(answer.text)
        username_test   =  (parsed_string['result']['username'])
        username_test   =  "@"+username_test
        first_name_test =  (parsed_string['result']['first_name'])        
        message_out,menu = iz_telegram.get_message (user_id,'Результат проверки',namebot)
        message_out = message_out.replace('%%Имя бота%%',str(username_test))   
        message_out = message_out.replace('%%Описание бота%%',str(first_name_test))
        markup = ''
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 
        db,cursor = iz_func.connect ()
        sql = "INSERT INTO bots (about,name,token,user_id,webhook,status) VALUES ('{}','{}','{}','{}','{}','')".format (first_name_test,username_test,token,user_id,"Да")
        cursor.execute(sql)
        db.commit()
        nerok = 'https://a7da4ed75223.ngrok.io'
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,"Настройка работы бота",'S',0) 
        url = 'https://api.telegram.org/bot'+str(token)+'/setWebhook?url='+nerok+'/telegram/3141/'+username_test+'/'
        print ('    [+] url',url)
        answer = requests.get(url)                                
        print ('    [+] Постановка ',answer.text)
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,"Установка бота закончина",'S',0) 

    if message_in == 'Ваш ID код':
        label_send = True
        import iz_telegram
        message_out,menu = iz_telegram.get_message (user_id,'Ваш ID код вывод',namebot)
        message_out = message_out.replace('%%user_id%%',str(user_id))
        markup = ""
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)  




    if message_in == 'Получить пароль в админку':
        label_send = True
        import iz_func
        import iz_telegram
        new_pass  = iz_func.get_pass ()
        db,cursor = iz_func.connect ()
        sql = "UPDATE bot_user SET pass = '"+new_pass+"' WHERE `user_id` = '"+str(user_id)+"' and namebot = '"+namebot+"' "
        cursor.execute(sql)
        db.commit()
        message_in              = "Ваш пароль для входа в Админку"
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,message_in,'S',0) 
        iz_telegram.save_variable (user_id,namebot,"Пароль в админку",str(new_pass))
        message_in = "Пароль в админку"        
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,message_in,'S',0) 
        iz_telegram.save_variable (user_id,namebot,"status",'')

    if message_in == 'Отключить пароль в админку':
        label_send = True
        import iz_func    
        import iz_telegram
        db,cursor = iz_func.connect ()
        sql = "UPDATE bot_user SET pass = '' WHERE `user_id` = '"+str(user_id)+"' and namebot = '"+namebot+"' "
        cursor.execute(sql)
        db.commit()    
        message_in = "Пароль в админку отключен"
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,message_in,'S',0) 

    if message_in == 'Настройка':
        label_send = True
        sql_request = "select * from bots where user_id = '"+str(user_id)+"';"
        list = iz_telegram.get_data_list (user_id,namebot,sql_request,'name','select_bot')
        markup = iz_telegram.list_menu (user_id,namebot,list)
        message_out = 'TEST'
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 

    if message_in == 'Coin Farmer':
        label_send = True
        import iz_game
        iz_game.game_farmer (user_id,namebot,"start",message_id,'')

    if message_in.find ('game_farmer_') != -1:
        label_send = True
        import iz_game
        iz_game.game_farmer (user_id,namebot,message_in,message_id,'')

    if label_send == False:
        #import iz_telegram
        #import iz_func
        #import time
        #message_out,menu,answer = iz_telegram.send_message (user_id,namebot,"Поиск в базе данных",'S',0) 
        #import pymysql
        #db = pymysql.connect(host='localhost',
        #                        user='izofen',
        #                        password='Podkjf3141!',
        #                        database='site_rus',
        #                        charset='utf8mb4',
        #                        cursorclass=pymysql.cursors.DictCursor)
        #cursor = db.cursor()      
        #sql = "select id,name,title from site where title like '%"+str(message_in)+"%' linmit 10"
        #cursor.execute(sql)
        #data = cursor.fetchall()
        #id = 0
        #for rec in data: 
        #    id,name,title = rec.values()
        #    #message_out,menu,answer = iz_telegram.send_message (user_id,namebot,"Ответ в базе",'S',0)
        #    message_out,menu = iz_telegram.get_message (user_id,'Ответ в базе',namebot)  
        #   message_out = message_out.replace('%%title%%',str(title))
        #    message_out = message_out.replace('%%name%%',str(name))
        #    markup = ''
        #    answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 
        #    time.sleep (2)    
        #db.close    
        #message_out,menu,answer = iz_telegram.send_message (user_id,namebot,"Поиск закончина",'S',0) 
        pass
 


