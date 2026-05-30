#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Настройка FunPay Cardinal${NC}"
echo -e "${BLUE}========================================${NC}"

# Запрос username
read -p "Введите username для рабочей директории: " username

if [ -z "$username" ]; then
    echo -e "${RED}Ошибка: username не может быть пустым!${NC}"
    exit 1
fi

WORK_DIR="/home/$username/FunPayCardinal"

# Проверка существования директории
if [ ! -d "$WORK_DIR" ]; then
    echo -e "${RED}Ошибка: Директория $WORK_DIR не найдена!${NC}"
    echo -e "${RED}Убедитесь, что FunPayCardinal установлен в /home/$username/${NC}"
    exit 1
fi

cd "$WORK_DIR"

echo -e "${GREEN}[1/11] Удаление ненужных файлов...${NC}"
rm -f announcements.py Setup.bat Start.bat .gitignore README.md delete.json
rm -rf .github
echo -e "${GREEN}✓ Ненужные файлы удалены${NC}"

echo -e "${GREEN}[2/11] Обработка cardinal.py...${NC}"
sed -i '/import announcements/d' cardinal.py
sed -i '/self\.add_handlers_from_plugin(announcements)/d' cardinal.py
echo -e "${GREEN}✓ cardinal.py обработан${NC}"

echo -e "${GREEN}[3/11] Обработка tg_bot/bot.py...${NC}"
sed -i 's/sh_text = "🛠️ github\.com\/sidor0912\/FunPayCardinal 💰 @sidor_donate 👨‍💻 @sidor0912 🧩 @fpc_plugins 🔄 @fpc_updates 💬 @funpay_cardinal"/sh_text = "👨‍💻 Владелец @mynameisvyach"/' tg_bot/bot.py
echo -e "${GREEN}✓ tg_bot/bot.py обработан${NC}"

echo -e "${GREEN}[4/11] Обработка locales/ru.py...${NC}"
python3 << EOF
import re

with open('locales/ru.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Замена fpc_init
fpc_init_start = content.find('fpc_init = """')
if fpc_init_start != -1:
    fpc_init_end = content.find('"""', fpc_init_start + 13)
    new_fpc_init = '''fpc_init = """✅ <b><u>FunPay Cardinal инициализирован!</u></b>\n
ℹ️ <b><i>Версия:</i></b> <code>{}</code>
👑 <b><i>Аккаунт:</i></b>  <code>{}</code> | <code>{}</code>
💰 <b><i>Баланс:</i></b> <code>{}₽, {}$, {}€</code>
📊 <b><i>Активные заказы:</i></b>  <code>{}</code>"""'''
    content = content[:fpc_init_start] + new_fpc_init + content[fpc_init_end+3:]

# Замена about
about_start = content.find('about = """')
if about_start != -1:
    about_end = content.find('"""', about_start + 9)
    new_about = 'about = "<b>🐦 FunPay Cardinal 🐦 v{}</b>"'
    content = content[:about_start] + new_about + content[about_end+3:]

# Замена adv_description
adv_start = content.find('adv_description = """')
if adv_start != -1:
    adv_end = content.find('"""', adv_start + 22)
    new_adv = 'adv_description = "🐦 𝑭𝒖𝒏𝑷𝒂𝒚 𝑪𝒂𝒓𝒅𝒊𝒏𝒂𝒍 v{}🐦"'
    content = content[:adv_start] + new_adv + content[adv_end+3:]

with open('locales/ru.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("✓ locales/ru.py обновлен")
EOF

echo -e "${GREEN}[5/11] Создание storage/cache/answer_templates.json...${NC}"
mkdir -p storage/cache
cat > storage/cache/answer_templates.json << 'EOF'
["\u041f\u0420\u0410\u0412\u0418\u041b\u041e \u041f\u041e\u041a\u0423\u041f\u041a\u0418:\n1\ufe0f\u20e3 - \u041f\u0440\u0438 \u043f\u043e\u043a\u0443\u043f\u043a\u0435 \u0443 \u0432\u0430\u0441 \u0434\u043e\u043b\u0436\u043d\u0430 \u0431\u044b\u0442\u044c \u0432\u043a\u043b\u044e\u0447\u0435\u043d\u0430 \u0437\u0430\u043f\u0438\u0441\u044c \u044d\u043a\u0440\u0430\u043d\u0430, \u0447\u0442\u043e\u0431\u044b \u0432 \u0441\u043b\u0443\u0447\u0430\u0435 \u043d\u0435\u0432\u0435\u0440\u043d\u044b\u0445 \u0434\u0430\u043d\u043d\u044b\u0445, \u044f \u043f\u043e\u043c\u0435\u043d\u044f\u043b \u0432\u0430\u043c \u0442\u043e\u0432\u0430\u0440/\u0441\u0434\u0435\u043b\u0430\u043b \u0432\u043e\u0437\u0432\u0440\u0430\u0442. \u041d\u0430 \u0444\u0440\u0430\u043f\u0441\u0435 \u0434\u043e\u043b\u0436\u043d\u043e \u0431\u044b\u0442\u044c \u0432\u0438\u0434\u043d\u043e, \u043a\u0430\u043a \u0432\u044b \u0432\u043e\u0441\u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435 \u043e\u043f\u043b\u0430\u0442\u0443 \u0438 \u043a\u0430\u043a \u043f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0435\u0442\u0435 lvl \u0438 \u043f\u0440\u0438\u0432\u044f\u0437\u043a\u0438 \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430.\n2\ufe0f\u20e3 - \u041f\u0440\u043e\u0434\u0430\u0432\u0435\u0446 \u043d\u0435 \u043d\u0435\u0441\u0435\u0442 \u043e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0441\u0442\u0438 \u0437\u0430 \u0432\u0430\u0448 \u0431\u0430\u043d, \u0442\u0430\u043a \u043a\u0430\u043a \u043f\u043e\u043a\u0443\u043f\u043a\u0430 \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u043e\u0432 \u043d\u0430 \u043f\u0440\u043e\u0435\u043a\u0442\u0435 \u0437\u0430\u043f\u0440\u0435\u0449\u0435\u043d\u0430.\n3\ufe0f\u20e3 - \u041d\u0435 \u0441\u0442\u043e\u0438\u0442 \u0441\u043f\u0430\u043c\u0438\u0442\u044c \u0438 \u043f\u0438\u0441\u0430\u0442\u044c \u043d\u0430\u0437\u043e\u0439\u043b\u0438\u0432\u044b\u0435 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f \u043f\u0440\u043e\u0434\u0430\u0432\u0446\u0443, \u0435\u0441\u043b\u0438 \u043d\u0430\u0440\u0443\u0448\u0438\u043b\u0438 \u043f\u0440\u0430\u0432\u0438\u043b\u043e \u0438 \u0442\u0440\u0435\u0431\u0443\u0435\u0442\u0435 \u0432\u043e\u0437\u0432\u0440\u0430\u0442.", "\u041f\u0440\u0435\u0434\u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u043a\u0430\u043a\u043e\u0439-\u043b\u0438\u0431\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u0438 \u043f\u043e \u0438\u043c\u0443\u0449\u0435\u0441\u0442\u0432\u0443: \u0434\u043e\u043c, \u043c\u0430\u0448\u0438\u043d\u044b, \u043d\u043e\u043c\u0435\u0440\u0430, \u0441\u0438\u043c-\u043a\u0430\u0440\u0442\u044b \u0438 \u0442.\u0434. - \u044f\u0432\u043b\u044f\u0435\u0442\u0441\u044f \u043d\u0435\u0431\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u044b\u043c \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0435\u043c \u0434\u043b\u044f \u043f\u0440\u043e\u0434\u0430\u0432\u0446\u0430, \u043f\u043e \u044d\u0442\u0438\u043c \u0434\u0430\u043d\u043d\u044b\u043c \u043c\u043e\u0436\u043d\u043e \u043b\u0435\u0433\u043a\u043e \u0435\u0433\u043e \u043e\u0442\u0441\u043b\u0435\u0434\u0438\u0442\u044c."]
EOF
echo -e "${GREEN}✓ answer_templates.json создан${NC}"

echo -e "${GREEN}[6/11] Создание storage/cache/notifications.json...${NC}"
cat > storage/cache/notifications.json << 'EOF'
{"8235458801": {"12": 1, "11": 1, "13": 1, "2": true, "4": true, "3": true, "8": true, "5r": true, "10": true, "5": true}}
EOF
echo -e "${GREEN}✓ notifications.json создан${NC}"

echo -e "${GREEN}[7/11] Создание storage/cache/tg_authorized_users.json...${NC}"
cat > storage/cache/tg_authorized_users.json << 'EOF'
{"8235458801": {}}
EOF
echo -e "${GREEN}✓ tg_authorized_users.json создан${NC}"

echo -e "${GREEN}[8/11] Создание configs/auto_response.cfg...${NC}"
mkdir -p configs
cat > configs/auto_response.cfg << 'EOF'
[!инструкция]
response : Инструкция для отправки отзыва:
	1) Открываете раздел 'Покупки' или переходите по ссылке https://funpay.com/orders/;
	2) Нажимаете на заказ;
	3) Внизу ставите оценку по 5-бальной системе и добавляете комментарий.
telegramNotification : 0

[!help]
response : ✅ Продавец вызван, ожидайте.
telegramNotification : 1
notificationText : Пользователь $username позвал Вас!
EOF
echo -e "${GREEN}✓ auto_response.cfg создан${NC}"

echo -e "${GREEN}[9/11] Обновление configs/_main.cfg...${NC}"
# Создаем бэкап оригинального файла
cp configs/_main.cfg configs/_main.cfg.bak

# Обновляем только нужные строки с помощью sed
# autoRaise : 0 -> 1
sed -i 's/autoRaise : 0/autoRaise : 1/' configs/_main.cfg

# autoResponse : 0 -> 1
sed -i 's/autoResponse : 0/autoResponse : 1/' configs/_main.cfg

# ignoreSystemMessages : 0 -> 1
sed -i 's/ignoreSystemMessages : 0/ignoreSystemMessages : 1/' configs/_main.cfg

# sendGreetings : 0 -> 1
sed -i 's/sendGreetings : 0/sendGreetings : 1/' configs/_main.cfg

# Замена greetingsText (многострочный)
sed -i '/greetingsText : /c\greetingsText : 🤖 𝙧𝙮𝙥𝙧𝙤𝙙𝙪𝙘𝙩𝙨 𝙗𝙤𝙩 🤖 Позвать продавца - команда !help.\n\t👋 Здравствуйте, $username. Скоро отвечу вам!\n\t━━━━━━━━━━━━━━━━━━━━━━' configs/_main.cfg

# watermark : 1 -> 0 (в секции OrderConfirm)
sed -i '/\[OrderConfirm\]/,/\[/ s/watermark : 1/watermark : 0/' configs/_main.cfg

# sendReply : 0 -> 1
sed -i 's/sendReply : 0/sendReply : 1/' configs/_main.cfg

# Замена replyText
sed -i '/replyText : /c\replyText : ❤️ $username, спасибо за подтверждение заказа $order_id!\n\t💞 Буду благодарен вашему отзыву. Как оставить отзыв !инструкция 💖' configs/_main.cfg

# Обновление star1-5Reply : 0 -> 1
sed -i 's/star1Reply : 0/star1Reply : 1/' configs/_main.cfg
sed -i 's/star2Reply : 0/star2Reply : 1/' configs/_main.cfg
sed -i 's/star3Reply : 0/star3Reply : 1/' configs/_main.cfg
sed -i 's/star4Reply : 0/star4Reply : 1/' configs/_main.cfg
sed -i 's/star5Reply : 0/star5Reply : 1/' configs/_main.cfg

# Замена текстов ответов на отзывы
sed -i '/star1ReplyText : /c\star1ReplyText : 🤖Нам очень жаль, что мы не смогли оказать нужный сервис для вас. Заказ оценен $date в $full_time.' configs/_main.cfg
sed -i '/star2ReplyText : /c\star2ReplyText : 🤖Нам очень жаль, что мы не смогли оказать нужный сервис для вас. Заказ оценен $date в $full_time.' configs/_main.cfg
sed -i '/star3ReplyText : /c\star3ReplyText : 🤖Нам очень жаль, что мы не смогли оказать нужный сервис для вас. Заказ оценен $date в $full_time.' configs/_main.cfg
sed -i '/star4ReplyText : /c\star4ReplyText : 🤖Спасибо за покупку! Заказ оценен $date в $full_time.' configs/_main.cfg
sed -i '/star5ReplyText : /c\star5ReplyText : 🤖Спасибо за покупку! Заказ оценен $date в $full_time.' configs/_main.cfg

# watermark : 🐦 -> (пусто) в секции Other
sed -i '/\[Other\]/,/^\[/ s/watermark : 🐦/watermark : /' configs/_main.cfg

echo -e "${GREEN}✓ _main.cfg обновлен${NC}"

echo -e "${GREEN}[10/11] Проверка изменений...${NC}"
if [ ! -f "announcements.py" ] && [ ! -d ".github" ]; then
    echo -e "${GREEN}✓ Ненужные файлы успешно удалены${NC}"
else
    echo -e "${YELLOW}⚠ Некоторые файлы могли не удалиться${NC}"
fi

if [ -f "configs/auto_response.cfg" ] && [ -f "storage/cache/answer_templates.json" ]; then
    echo -e "${GREEN}✓ Новые файлы конфигурации созданы${NC}"
fi

echo -e "${GREEN}[11/11] Завершение настройки...${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ Настройка FunPay Cardinal завершена!${NC}"
echo -e "${GREEN}📁 Рабочая директория: $WORK_DIR${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${PURPLE}${BOLD}═══════════════════════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}${BOLD}                        ⚠️  ВАЖНО! НЕ ЗАБУДЬТЕ! ⚠️${NC}"
echo -e "${PURPLE}${BOLD}═══════════════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}${BOLD}🎯 Установите плагины для FunPay Cardinal!${NC}"
echo ""

cd ..
