#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Начало установки и настройки сервера${NC}"
echo -e "${GREEN}========================================${NC}"

# 1) Обновление пакетов
echo -e "${YELLOW}[1/8] Обновление пакетов...${NC}"
sudo apt update && sudo apt upgrade -y

# Установка net-tools
echo -e "${YELLOW}Установка net-tools...${NC}"
sudo apt install net-tools -y

# Установка Docker
echo -e "${YELLOW}[2/8] Установка Docker...${NC}"
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce -y
sudo systemctl enable docker --now
sudo usermod -aG docker $USER
echo -e "${GREEN}Docker установлен успешно!${NC}"

# Установка Python
echo -e "${YELLOW}[3/8] Установка Python и venv...${NC}"
sudo apt install python3 python3-pip python3-venv -y
echo -e "${GREEN}Python установлен успешно!${NC}"

# Проверка и установка SSH сервера
echo -e "${YELLOW}[4/8] Проверка и установка SSH сервера...${NC}"
if ! systemctl list-unit-files | grep -q "ssh.service"; then
    echo -e "${YELLOW}SSH сервер не найден. Устанавливаю...${NC}"
    sudo apt install openssh-server -y
fi
sudo systemctl enable ssh --now
echo -e "${GREEN}SSH сервер установлен и запущен!${NC}"

# Вопрос про перенос ботов
echo -e "${YELLOW}[5/8] Вопрос пользователю...${NC}"
while true; do
    read -p "Вы перенесли ботов в папку /home/TelegramBots? (yes/no): " answer
    case $answer in
        [Yy]*|"yes"|"YES")
            echo -e "${GREEN}Отлично! Продолжаем...${NC}"
            break
            ;;
        [Nn]*|"no"|"NO")
            echo -e "${RED}Пожалуйста, перенесите ботов в /home/TelegramBots и запустите скрипт снова.${NC}"
            exit 1
            ;;
        *)
            echo "Пожалуйста, ответьте yes или no"
            ;;
    esac
done

# Переход в папку с ботами и настройка виртуального окружения
echo -e "${YELLOW}[6/8] Настройка виртуального окружения Python...${NC}"
cd /home/TelegramBots || { echo -e "${RED}Папка /home/TelegramBots не найдена!${NC}"; exit 1; }

python3 -m venv venv
source venv/bin/activate
pip3 install --upgrade pip
pip3 install -r https://raw.githubusercontent.com/mynameisvyach/install/refs/heads/main/requirements.txt
deactivate
echo -e "${GREEN}Виртуальное окружение настроено!${NC}"

# Настройка SSH (PubkeyAuthentication)
echo -e "${YELLOW}[7/8] Настройка SSH (PubkeyAuthentication)...${NC}"
sudo sed -i "s/#PubkeyAuthentication yes/PubkeyAuthentication yes/g" /etc/ssh/sshd_config
sudo sed -i "s/PubkeyAuthentication no/PubkeyAuthentication yes/g" /etc/ssh/sshd_config
sudo systemctl restart ssh
echo -e "${GREEN}SSH настроен!${NC}"

# Установка Fail2Ban
echo -e "${YELLOW}[8/9] Установка Fail2Ban...${NC}"
sudo apt install fail2ban -y
sudo systemctl enable fail2ban --now
echo -e "${GREEN}Fail2Ban установлен и запущен!${NC}"
sudo systemctl status fail2ban --no-pager

# Настройка Fail2Ban (опционально)
echo -e "${YELLOW}[9/9] Настройка Fail2Ban...${NC}"

# Небольшая задержка, чтобы fail2ban полностью инициализировался
sleep 2

read -p "Хотите добавить IP в ignorelist Fail2Ban? (yes/no): " add_ip
if [[ $add_ip == "yes" || $add_ip == "YES" || $add_ip == "y" ]]; then
    read -p "Введите IP адрес для добавления в ignorelist: " ip_address
    # ИСПРАВЛЕНО: используем sshd вместо DEFAULT
    sudo fail2ban-client set sshd addignoreip $ip_address
    echo -e "${GREEN}IP $ip_address добавлен в ignorelist для тюрьмы sshd${NC}"
fi

read -p "Хотите разбанить какой-либо IP? (yes/no): " unban_ip
if [[ $unban_ip == "yes" || $unban_ip == "YES" || $unban_ip == "y" ]]; then
    read -p "Введите IP адрес для разбана: " ip_to_unban
    # ИСПРАВЛЕНО: разбан для конкретной тюрьмы
    sudo fail2ban-client set sshd unbanip $ip_to_unban
    echo -e "${GREEN}IP $ip_to_unban разбанен в тюрьме sshd${NC}"
fi

# Перезагрузка
echo -e "${YELLOW}========================================${NC}"
echo -e "${GREEN}Все настройки выполнены успешно!${NC}"
echo -e "${YELLOW}Сервер будет перезагружен через 10 секунд...${NC}"
echo -e "${YELLOW}Нажмите Ctrl+C для отмены перезагрузки${NC}"
sleep 10
sudo reboot
