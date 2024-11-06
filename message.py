import smtplib
from dotenv import load_dotenv
import os
load_dotenv('secret.env')

user_login = os.getenv('USER')
password = os.getenv('PASSWORD')

from_mail = 'vladProgrammer97@yandex.ru'
to_mail = 'vladProgrammer97@yandex.ru'
subject = 'Приглашение!'

letter = f"""From: {from_mail}
To: {to_mail}
Subject: {subject}
Content-Type: text/plain; charset="UTF-8";

Привет, %friend_name%! %my_name% приглашает тебя на сайт %website%!

%website% — это новая версия онлайн-курса по программированию. 
Изучаем Python и не только. Решаем задачи. Получаем ревью от преподавателя. 

Как будет проходить ваше обучение на %website%? 

→ Попрактикуешься на реальных кейсах. 
Задачи от тимлидов со стажем от 10 лет в программировании.
→ Будешь учиться без стресса и бессонных ночей. 
Задачи не «сгорят» и не уйдут к другому. Занимайся в удобное время и ровно столько, сколько можешь.
→ Подготовишь крепкое резюме.
Все проекты — они же решение наших задачек — можно разместить на твоём GitHub. Работодатели такое оценят. 

Регистрируйся → %website%  
На курсы, которые еще не вышли, можно подписаться и получить уведомление о релизе сразу на имейл.""". format(from_mail = from_mail, to_mail = to_mail, subject = subject)

letter = letter.replace("%website%", "https://dvmn.org/profession-ref-program/vladushakov89/eWTNo/")
letter = letter.replace("%friend_name%", "Alex")
letter = letter.replace("%my_name%", "Vlad")

server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
server.login(user_login, password)
server.sendmail(from_mail, to_mail, letter.encode("UTF-8")) 
letter = letter.encode("UTF-8")
print(letter)





