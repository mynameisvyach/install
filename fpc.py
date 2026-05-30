#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Настройка FunPay Cardinal${NC}"
echo -e "${BLUE}========================================${NC}"

# Проверка, что скрипт запущен из директории с установленным проектом
if [ ! -d "FunPayCardinal" ]; then
    echo -e "${RED}Ошибка: Директория FunPayCardinal не найдена!${NC}"
    echo -e "${RED}Убедитесь, что вы запускаете скрипт из папки, где находится установленный проект${NC}"
    exit 1
fi

cd FunPayCardinal

echo -e "${GREEN}[1/8] Удаление ненужных файлов...${NC}"
# Удаляем ненужные файлы и папки
rm -f announcements.py
rm -f Setup.bat
rm -f Start.bat
rm -f .gitignore
rm -f README.md
rm -f delete.json
rm -rf .github
echo -e "${GREEN}✓ Ненужные файлы удалены${NC}"

echo -e "${GREEN}[2/8] Обработка cardinal.py...${NC}"
# Удаляем import announcements и self.add_handlers_from_plugin(announcements) из cardinal.py
sed -i '/import announcements/d' cardinal.py
sed -i '/self\.add_handlers_from_plugin(announcements)/d' cardinal.py
echo -e "${GREEN}✓ cardinal.py обработан${NC}"

echo -e "${GREEN}[3/8] Обработка tg_bot/bot.py...${NC}"
# Заменяем строку в bot.py
sed -i 's/sh_text = "🛠️ github\.com\/sidor0912\/FunPayCardinal 💰 @sidor_donate 👨‍💻 @sidor0912 🧩 @fpc_plugins 🔄 @fpc_updates 💬 @funpay_cardinal"/sh_text = "👨‍💻 Владелец @mynameisvyach"/' tg_bot/bot.py
echo -e "${GREEN}✓ tg_bot/bot.py обработан${NC}"

echo -e "${GREEN}[4/8] Обработка locales/ru.py (fpc_init)...${NC}"
# Заменяем fpc_init в ru.py
sed -i '/fpc_init = """✅ <b><u>FunPay Cardinal инициализирован!<\/u><\/b>\\n/,/🤑 <b><i>Донат:<\/i><\/b> @sidor_donate"""/c\    fpc_init = """✅ <b><u>FunPay Cardinal инициализирован!<\/u><\/b>\\n\nℹ️ <b><i>Версия:<\/i><\/b> <code>{}<\/code>\n👑 <b><i>Аккаунт:<\/i><\/b>  <code>{}<\/code> | <code>{}<\/code>\n💰 <b><i>Баланс:<\/i><\/b> <code>{}₽, {}$, {}€<\/code>\n📊 <b><i>Активные заказы:<\/i><\/b>  <code>{}<\/code>"""' locales/ru.py
echo -e "${GREEN}✓ locales/ru.py (fpc_init) обработан${NC}"

echo -e "${GREEN}[5/8] Обработка locales/ru.py (about)...${NC}"
# Заменяем about в ru.py
sed -i '/about = """<b>🐦 FunPay Cardinal 🐦 v{}<\/b>\\n/,/🤑 <b><i>Донат:<\/i><\/b> @sidor_donate"""/c\    about = "<b>🐦 FunPay Cardinal 🐦 v{}</b>"' locales/ru.py
echo -e "${GREEN}✓ locales/ru.py (about) обработан${NC}"

echo -e "${GREEN}[6/8] Обработка locales/ru.py (adv_description)...${NC}"
# Заменяем adv_description в ru.py
sed -i '/adv_description = """🐦 𝑭𝒖𝒏𝑷𝒂𝒚 𝑪𝒂𝒓𝒅𝒊𝒏𝒂𝒍 v{}🐦\\n/,/💬 Чат: @funpay_cardinal"""/c\    adv_description = "🐦 𝑭𝒖𝒏𝑷𝒂𝒚 𝑪𝒂𝒓𝒅𝒊𝒏𝒂𝒍 v{}🐦"' locales/ru.py
echo -e "${GREEN}✓ locales/ru.py (adv_description) обработан${NC}"

echo -e "${GREEN}[7/8] Проверка изменений...${NC}"
# Проверяем, что изменения применились
if [ ! -f "announcements.py" ] && [ ! -d ".github" ]; then
    echo -e "${GREEN}✓ Ненужные файлы успешно удалены${NC}"
else
    echo -e "${RED}⚠ Некоторые файлы могли не удалиться${NC}"
fi

echo -e "${GREEN}[8/8] Завершение настройки...${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ Настройка FunPay Cardinal завершена!${NC}"
echo -e "${BLUE}========================================${NC}"

cd ..
