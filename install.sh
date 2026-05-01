#!/bin/bash
#################### x-ui-pro v2.4.3 ##############################################
[[ $EUID -ne 0 ]] && echo "not root! Please run as root" && exit 1

##############################INFO######################################################################
msg_ok() { echo -e "\e[1;42m $1 \e[0m";}
msg_err() { echo -e "\e[1;41m $1 \e[0m";}
msg_inf() { echo -e "\e[1;34m$1\e[0m";}
echo
msg_inf '           ___    _   _   _  '
msg_inf ' \/ __ | |  | __ |_) |_) / \ '
msg_inf ' /\    |_| _|_   |   | \ \_/ '
echo

##################################Variables#############################################################
XUIDB="/etc/x-ui/x-ui.db"
domain=""
UNINSTALL="n"
INSTALL="n"
PNLNUM=1
CFALLOW="n"
CLASH=0
CUSTOMWEBSUB=0
Pak=$(type apt &>/dev/null && echo "apt" || echo "yum")
AUTODOMAIN="n"

# Останавливаем сервисы если они есть
systemctl stop x-ui 2>/dev/null
systemctl stop nginx 2>/dev/null

# Очистка старых конфигов
rm -rf /etc/systemd/system/x-ui.service 2>/dev/null
rm -rf /usr/local/x-ui 2>/dev/null
rm -rf /etc/x-ui 2>/dev/null
rm -rf /etc/nginx/sites-enabled/* 2>/dev/null
rm -rf /etc/nginx/sites-available/* 2>/dev/null
rm -rf /etc/nginx/stream-enabled/* 2>/dev/null

##################################generate ports and paths#############################################################
get_port() {
    echo $(( ((RANDOM<<15)|RANDOM) % 49152 + 10000 ))
}

gen_random_string() {
    local length="$1"
    tr -dc 'a-zA-Z0-9' < /dev/urandom 2>/dev/null | head -c "$length"
    echo
}

make_port() {
    while true; do
        PORT=$(get_port)
        if ! ss -tlnp | grep -q ":$PORT "; then
            echo $PORT
            break
        fi
    done
}

sub_port=$(make_port)
panel_port=$(make_port)
web_path=$(gen_random_string 10)
sub_path=$(gen_random_string 10)
json_path=$(gen_random_string 10)
panel_path=$(gen_random_string 10)
ws_port=$(make_port)
ws_path=$(gen_random_string 10)
xhttp_path=$(gen_random_string 10)
config_username=$(gen_random_string 10)
config_password=$(gen_random_string 10)

################################Get arguments###########################################################
while [ "$#" -gt 0 ]; do
    case "$1" in
        -auto_domain) AUTODOMAIN="$2"; shift 2 ;;
        -install) INSTALL="$2"; shift 2 ;;
        -panel) PNLNUM="$2"; shift 2 ;;
        -subdomain) domain="$2"; shift 2 ;;
        -reality_domain) reality_domain="$2"; shift 2 ;;
        -uninstall) UNINSTALL="$2"; shift 2 ;;
        *) shift 1 ;;
    esac
done

##############################Uninstall#################################################################
UNINSTALL_XUI() {
    printf 'y\n' | x-ui uninstall 2>/dev/null
    rm -rf /etc/x-ui/ /usr/local/x-ui/ /usr/bin/x-ui/
    $Pak -y remove nginx nginx-common nginx-core nginx-full python3-certbot-nginx 2>/dev/null
    $Pak -y autoremove 2>/dev/null
    rm -rf /var/www/html/ /etc/nginx/ /usr/share/nginx/
    clear && msg_ok "Completely Uninstalled!" && exit 0
}

if [[ ${UNINSTALL} == "y" ]]; then
    UNINSTALL_XUI
fi

# Получаем IP адрес
IP4_REGEX="^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"
IP4=$(ip route get 8.8.8.8 2>/dev/null | grep -Po -- 'src \K\S*')
[[ $IP4 =~ $IP4_REGEX ]] || IP4=$(curl -s --max-time 5 ipv4.icanhazip.com 2>/dev/null | tr -d '[:space:]')

if [[ ${AUTODOMAIN} == "y" ]]; then
    domain="${IP4}.cdn-one.org"
    reality_domain="${IP4//./-}.cdn-one.org"
fi

##############################Domain Validations########################################################
while [[ -z "$domain" ]]; do
    echo -en "Enter available subdomain (sub.domain.tld): " && read domain
done
domain=$(echo "$domain" | tr -d '[:space:]')

while [[ -z "$reality_domain" ]]; do
    echo -en "Enter available subdomain for REALITY (sub.domain.tld): " && read reality_domain
done
reality_domain=$(echo "$reality_domain" | tr -d '[:space:]')

###############################Install Packages#########################################################
# Отключаем другие фаерволы
systemctl stop firewalld 2>/dev/null && systemctl disable firewalld 2>/dev/null
systemctl stop nftables 2>/dev/null && systemctl disable nftables 2>/dev/null

# Отключаем IPv6
cat > /etc/sysctl.d/99-disable-ipv6.conf << EOF
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
EOF
sysctl -p /etc/sysctl.d/99-disable-ipv6.conf 2>/dev/null

# Отключаем ufw
ufw disable 2>/dev/null
sed -i 's/IPV6=yes/IPV6=no/g' /etc/default/ufw 2>/dev/null

# Установка пакетов
NEED_INSTALL=0
if [[ ${INSTALL} == "y" ]] || ! command -v certbot &>/dev/null || ! command -v nginx &>/dev/null; then
    NEED_INSTALL=1
fi

if [[ $NEED_INSTALL -eq 1 ]]; then
    msg_inf "Installing required packages..."
    $Pak update -y
    $Pak install -y curl wget jq sudo nginx certbot python3-certbot-nginx sqlite3 ufw openssl socat net-tools
fi

# Очистка портов
fuser -k 80/tcp 443/tcp 2>/dev/null

##################################GET SERVER IPv4#####################################################
IP4=$(curl -s --max-time 5 ipv4.icanhazip.com 2>/dev/null | tr -d '[:space:]')
[[ ! $IP4 =~ $IP4_REGEX ]] && IP4=$(ip route get 8.8.8.8 2>/dev/null | grep -Po -- 'src \K\S*')

##############################Install SSL###############################################################
resolve_to_ip() {
    local host="$1"
    local a=$(getent ahostsv4 "$host" 2>/dev/null | awk 'NR==1{print $1}')
    [[ -n "$a" ]] && [[ "$a" == "$IP4" ]]
}

if [[ ${AUTODOMAIN} == "y" ]]; then
    if ! resolve_to_ip "$domain"; then
        msg_err "Auto-domain $domain does not resolve to this server IP ($IP4)"
        exit 1
    fi
    if ! resolve_to_ip "$reality_domain"; then
        msg_err "Auto-domain $reality_domain does not resolve to this server IP ($IP4)"
        exit 1
    fi
fi

# Получаем SSL сертификаты
msg_inf "Getting SSL certificate for $domain..."
certbot certonly --standalone --non-interactive --agree-tos --register-unsafely-without-email -d "$domain" 2>&1
if [[ ! -d "/etc/letsencrypt/live/${domain}/" ]]; then
    msg_err "$domain SSL could not be generated!"
    exit 1
fi

msg_inf "Getting SSL certificate for $reality_domain..."
certbot certonly --standalone --non-interactive --agree-tos --register-unsafely-without-email -d "$reality_domain" 2>&1
if [[ ! -d "/etc/letsencrypt/live/${reality_domain}/" ]]; then
    msg_err "$reality_domain SSL could not be generated!"
    exit 1
fi

###################################Get Installed XUI Port/Path##########################################
if [[ -f $XUIDB ]]; then
    XUIPORT=$(sqlite3 -list $XUIDB 'SELECT "value" FROM settings WHERE "key"="webPort" LIMIT 1;' 2>/dev/null)
    XUIPATH=$(sqlite3 -list $XUIDB 'SELECT "value" FROM settings WHERE "key"="webBasePath" LIMIT 1;' 2>/dev/null)
    if [[ $XUIPORT -gt 0 && $XUIPORT != "54321" && $XUIPORT != "2053" ]] && [[ ${#XUIPORT} -gt 4 ]]; then
        sqlite3 $XUIDB <<EOF
        DELETE FROM "settings" WHERE "key" IN ("webCertFile", "webKeyFile");
        INSERT INTO "settings" ("key", "value") VALUES ("webCertFile", "");
        INSERT INTO "settings" ("key", "value") VALUES ("webKeyFile", "");
EOF
    fi
fi

#################################Nginx Config###########################################################
mkdir -p /root/cert/${domain}
chmod 755 /root/cert 2>/dev/null

ln -sf /etc/letsencrypt/live/${domain}/fullchain.pem /root/cert/${domain}/fullchain.pem
ln -sf /etc/letsencrypt/live/${domain}/privkey.pem /root/cert/${domain}/privkey.pem

# Создаем основную конфигурацию nginx
cat > /etc/nginx/nginx.conf << 'EOF'
user www-data;
worker_processes auto;
pid /run/nginx.pid;
worker_rlimit_nofile 65535;

events {
    worker_connections 4096;
    multi_accept on;
    use epoll;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 100M;
    
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
    
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss application/rss+xml text/js image/svg+xml;
    
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
EOF

# Создаем конфигурацию для stream модуля
mkdir -p /etc/nginx/stream-enabled
cat > /etc/nginx/stream-enabled/stream.conf << EOF
stream {
    upstream xray {
        server 127.0.0.1:8443;
    }
    
    upstream www {
        server 127.0.0.1:7443;
    }
    
    server {
        listen 443 reuseport;
        proxy_pass www;
        proxy_protocol on;
    }
}
EOF

# Создаем конфиг для HTTP->HTTPS редиректа
cat > /etc/nginx/sites-available/80.conf << EOF
server {
    listen 80;
    listen [::]:80;
    server_name ${domain} ${reality_domain};
    return 301 https://\$server_name\$request_uri;
}
EOF

# Создаем сниппет для includes
mkdir -p /etc/nginx/snippets
cat > /etc/nginx/snippets/includes.conf << EOF
location /${xhttp_path} {
    grpc_pass grpc://unix:/dev/shm/uds2023.sock;
    grpc_read_timeout 1h;
    grpc_send_timeout 1h;
}

location ~ ^/(?<fwdport>\d+)/(?<fwdpath>.+)$ {
    proxy_http_version 1.1;
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
    
    proxy_pass http://127.0.0.1:\$fwdport\$is_args\$args;
    
    proxy_buffering off;
    proxy_request_buffering off;
}
EOF

# Создаем основной конфиг для домена
cat > "/etc/nginx/sites-available/${domain}" << EOF
server {
    server_tokens off;
    server_name ${domain};
    listen 7443 ssl http2 proxy_protocol;
    listen [::]:7443 ssl http2 proxy_protocol;
    
    root /var/www/html;
    index index.html;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!eNULL:!MD5:!RC4;
    ssl_certificate /etc/letsencrypt/live/${domain}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${domain}/privkey.pem;
    
    location /${panel_path} {
        proxy_pass https://127.0.0.1:${panel_port};
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    include /etc/nginx/snippets/includes.conf;
}
EOF

# Создаем конфиг для reality домена
cat > "/etc/nginx/sites-available/${reality_domain}" << EOF
server {
    server_tokens off;
    server_name ${reality_domain};
    listen 9443 ssl http2;
    listen [::]:9443 ssl http2;
    
    root /var/www/html;
    index index.html;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!eNULL:!MD5:!RC4;
    ssl_certificate /etc/letsencrypt/live/${reality_domain}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${reality_domain}/privkey.pem;
    
    location /${panel_path} {
        proxy_pass http://127.0.0.1:${panel_port};
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
    
    include /etc/nginx/snippets/includes.conf;
}
EOF

# Активируем конфиги
ln -sf /etc/nginx/sites-available/80.conf /etc/nginx/sites-enabled/
ln -sf "/etc/nginx/sites-available/${domain}" /etc/nginx/sites-enabled/
ln -sf "/etc/nginx/sites-available/${reality_domain}" /etc/nginx/sites-enabled/

# Создаем тестовую HTML страницу
mkdir -p /var/www/html
cat > /var/www/html/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>Working</title></head>
<body><h1>Server is working!</h1></body>
</html>
EOF

# Проверяем и запускаем nginx
msg_inf "Testing Nginx configuration..."
if nginx -t 2>&1 | grep -q "successful"; then
    msg_ok "Nginx configuration is OK!"
    systemctl start nginx
    systemctl enable nginx
else
    msg_err "Nginx configuration error!"
    nginx -t
    exit 1
fi

if ! systemctl is-active --quiet nginx; then
    msg_err "Nginx failed to start!"
    journalctl -u nginx -n 20 --no-pager
    exit 1
fi

msg_ok "Nginx is running!"

##############################generate uri's###########################################################
sub_uri="https://${domain}/${sub_path}/"
json_uri="https://${domain}/${web_path}?name="

##############################generate keys###########################################################
shor=($(openssl rand -hex 8) $(openssl rand -hex 8) $(openssl rand -hex 8) $(openssl rand -hex 8))

########################################Install X-UI####################################################
install_xui() {
    msg_inf "Installing X-UI panel..."
    
    cd /usr/local/
    
    # Получаем последнюю версию
    tag_version=$(curl -s "https://api.github.com/repos/MHSanaei/3x-ui/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
    if [[ -z "$tag_version" ]]; then
        tag_version=$(curl -4 -s "https://api.github.com/repos/MHSanaei/3x-ui/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
    fi
    
    if [[ -z "$tag_version" ]]; then
        msg_err "Failed to fetch x-ui version"
        exit 1
    fi
    
    arch=$(uname -m)
    case "$arch" in
        x86_64|amd64) arch="amd64" ;;
        aarch64|arm64) arch="arm64" ;;
        armv7l) arch="armv7" ;;
        *) msg_err "Unsupported architecture: $arch"; exit 1 ;;
    esac
    
    wget -q -O /usr/local/x-ui-linux-${arch}.tar.gz "https://github.com/MHSanaei/3x-ui/releases/download/${tag_version}/x-ui-linux-${arch}.tar.gz"
    if [[ $? -ne 0 ]]; then
        msg_err "Failed to download x-ui"
        exit 1
    fi
    
    tar zxvf x-ui-linux-${arch}.tar.gz >/dev/null 2>&1
    rm x-ui-linux-${arch}.tar.gz -f
    
    cd x-ui
    chmod +x x-ui bin/xray-linux-${arch}
    
    cp -f x-ui.service.debian /etc/systemd/system/x-ui.service
    systemctl daemon-reload
    systemctl enable x-ui
    
    msg_ok "X-UI installed successfully!"
}

##############################Update X-UI Database#######################################################
update_xuidb() {
    if [[ ! -f $XUIDB ]]; then
        msg_err "x-ui.db not found!"
        exit 1
    fi
    
    x-ui stop 2>/dev/null
    
    # Генерируем ключи
    output=$(/usr/local/x-ui/bin/xray-linux-amd64 x25519 2>/dev/null)
    private_key=$(echo "$output" | grep "PrivateKey:" | awk '{print $2}')
    public_key=$(echo "$output" | grep "PublicKey:" | awk '{print $2}')
    
    client_id=$(/usr/local/x-ui/bin/xray-linux-amd64 uuid)
    client_id2=$(/usr/local/x-ui/bin/xray-linux-amd64 uuid)
    client_id3=$(/usr/local/x-ui/bin/xray-linux-amd64 uuid)
    
    # Настройка Telegram бота
    echo ""
    msg_inf "Enable Telegram Bot? (y/n): "
    read -r tg_enable_choice
    TG_BOT_ENABLE="false"
    TG_BOT_TOKEN=""
    TG_BOT_CHAT_ID=""
    
    if [[ "$tg_enable_choice" == "y" ]]; then
        TG_BOT_ENABLE="true"
        echo -n "Telegram Bot Token: " && read -r TG_BOT_TOKEN
        echo -n "Telegram Chat ID: " && read -r TG_BOT_CHAT_ID
    fi
    
    # Настройка базы данных
    sqlite3 $XUIDB <<EOF
    INSERT OR REPLACE INTO "settings" ("key", "value") VALUES 
        ("subPort", '${sub_port}'),
        ("subPath", '/${sub_path}/'),
        ("subURI", '${sub_uri}'),
        ("subEnable", 'true'),
        ("webListen", ''),
        ("webDomain", ''),
        ("tgBotEnable", '${TG_BOT_ENABLE}'),
        ("tgBotToken", '${TG_BOT_TOKEN}'),
        ("tgBotChatId", '${TG_BOT_CHAT_ID}'),
        ("timeLocation", 'Europe/Moscow');
    
    DELETE FROM "inbounds";
    DELETE FROM "client_traffics";
    
    INSERT INTO "inbounds" ("user_id","up","down","total","remark","enable","expiry_time","listen","port","protocol","settings","stream_settings","tag","sniffing") VALUES 
    (1,0,0,0,'Reality',1,0,'',8443,'vless',
     '{"clients":[{"id":"${client_id}","flow":"xtls-rprx-vision","email":"first"}],"decryption":"none","fallbacks":[]}',
     '{"network":"tcp","security":"reality","realitySettings":{"serverNames":["${reality_domain}"],"privateKey":"${private_key}","shortIds":["${shor[0]}","${shor[1]}","${shor[2]}","${shor[3]}"],"settings":{"publicKey":"${public_key}","fingerprint":"chrome"}},"tcpSettings":{"acceptProxyProtocol":true}}',
     'inbound-8443','{"enabled":false}');
    
    INSERT INTO "inbounds" ("user_id","up","down","total","remark","enable","expiry_time","listen","port","protocol","settings","stream_settings","tag","sniffing") VALUES 
    (1,0,0,0,'WebSocket',1,0,'',${ws_port},'vless',
     '{"clients":[{"id":"${client_id2}","email":"first_1"}],"decryption":"none","fallbacks":[]}',
     '{"network":"ws","security":"none","wsSettings":{"path":"/${ws_port}/${ws_path}","host":"${domain}"}}',
     'inbound-${ws_port}','{"enabled":false}');
EOF
    
    # Настройка панели
    /usr/local/x-ui/x-ui setting -username "${config_username}" -password "${config_password}" -port "${panel_port}" -webBasePath "${panel_path}"
    /usr/local/x-ui/x-ui cert -webCert "/root/cert/${domain}/fullchain.pem" -webCertKey "/root/cert/${domain}/privkey.pem"
    
    x-ui start
    msg_ok "X-UI configured successfully!"
}

# Установка X-UI
if systemctl is-active --quiet x-ui; then
    x-ui restart
else
    install_xui
    sleep 2
    update_xuidb
fi

######################enable bbr and tune system########################################################
cat >> /etc/sysctl.conf << EOF
net.core.default_qdisc=fq
net.ipv4.tcp_congestion_control=bbr
fs.file-max=2097152
net.core.rmem_max=16777216
net.core.wmem_max=16777216
EOF
sysctl -p 2>/dev/null

######################cronjob for ssl/reload service####################################################
(crontab -l 2>/dev/null | grep -v "certbot\|x-ui" | crontab - 2>/dev/null)
(crontab -l 2>/dev/null; echo '@daily x-ui restart > /dev/null 2>&1 && systemctl reload nginx') | crontab - 2>/dev/null
(crontab -l 2>/dev/null; echo '@monthly certbot renew --quiet --nginx --post-hook "systemctl reload nginx"') | crontab - 2>/dev/null

##################################Configure UFW##########################################################
ufw --force reset 2>/dev/null
ufw default deny incoming 2>/dev/null
ufw default allow outgoing 2>/dev/null
ufw allow 22/tcp 2>/dev/null
ufw allow 80/tcp 2>/dev/null
ufw allow 443/tcp 2>/dev/null
ufw allow ${panel_port}/tcp 2>/dev/null
ufw --force enable 2>/dev/null

##################################Show Details##########################################################
clear
echo ""
msg_ok "==================== INSTALLATION COMPLETED ===================="
echo ""
msg_inf "X-UI Panel Access:"
echo -e "  URL:      \e[1;33mhttps://${domain}/${panel_path}/\e[0m"
echo -e "  Username: \e[1;33m${config_username}\e[0m"
echo -e "  Password: \e[1;33m${config_password}\e[0m"
echo ""
msg_inf "Subscription URL:"
echo -e "  \e[1;33m${sub_uri}\e[0m"
echo ""
msg_inf "Configuration Files:"
echo -e "  Nginx:    /etc/nginx/"
echo -e "  SSL:      /etc/letsencrypt/live/${domain}/"
echo -e "  X-UI DB:  ${XUIDB}"
echo ""
msg_inf "Useful Commands:"
echo -e "  x-ui menu          - Open X-UI control panel"
echo -e "  x-ui restart       - Restart X-UI"
echo -e "  nginx -t           - Test Nginx config"
echo -e "  certbot renew      - Renew SSL certificates"
echo ""
msg_ok "================================================================"
echo ""

# Проверка статуса
systemctl is-active --quiet x-ui && msg_ok "✓ X-UI is running" || msg_err "✗ X-UI is not running"
systemctl is-active --quiet nginx && msg_ok "✓ Nginx is running" || msg_err "✗ Nginx is not running"
systemctl is-active --quiet certbot && msg_ok "✓ Certbot is running" || msg_inf "⚠ Certbot is not running (normal if no renewals)"

echo ""
msg_ok "Installation completed successfully!"
