#!/bin/bash

red='\033[0;31m'
green='\033[0;32m'
blue='\033[0;34m'
yellow='\033[0;33m'
plain='\033[0m'

cur_dir=$(pwd)

xui_folder="${XUI_MAIN_FOLDER:=/usr/local/x-ui}"
xui_service="${XUI_SERVICE:=/etc/systemd/system}"
aghome_folder="/opt/AdGuardHome"

# check root
[[ $EUID -ne 0 ]] && echo -e "${red}Fatal error: ${plain} Please run this script with root privilege \n " && exit 1

# Check OS and set release variable
if [[ -f /etc/os-release ]]; then
    source /etc/os-release
    release=$ID
elif [[ -f /usr/lib/os-release ]]; then
    source /usr/lib/os-release
    release=$ID
else
    echo "Failed to check the system OS, please contact the author!" >&2
    exit 1
fi
echo "The OS release is: $release"

# Disable IPv6
disable_ipv6() {
    echo -e "${green}Disabling IPv6...${plain}"
    
    # Disable IPv6 via sysctl
    cat >> /etc/sysctl.conf << EOF

# IPv6 disabled by 3x-ui+AdGuard installer
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
EOF
    
    # Apply sysctl settings
    sysctl -p
    
    # Also disable for current session
    echo 1 > /proc/sys/net/ipv6/conf/all/disable_ipv6
    echo 1 > /proc/sys/net/ipv6/conf/default/disable_ipv6
    echo 1 > /proc/sys/net/ipv6/conf/lo/disable_ipv6
    
    echo -e "${green}IPv6 disabled successfully.${plain}"
}

arch() {
    case "$(uname -m)" in
        x86_64 | x64 | amd64) echo 'amd64' ;;
        i*86 | x86) echo '386' ;;
        armv8* | armv8 | arm64 | aarch64) echo 'arm64' ;;
        armv7* | armv7 | arm) echo 'armv7' ;;
        armv6* | armv6) echo 'armv6' ;;
        armv5* | armv5) echo 'armv5' ;;
        s390x) echo 's390x' ;;
        *) echo -e "${green}Unsupported CPU architecture! ${plain}" && rm -f install.sh && exit 1 ;;
    esac
}

echo "Arch: $(arch)"

# Simple helpers
is_ipv4() {
    [[ "$1" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]] && return 0 || return 1
}
is_ipv6() {
    [[ "$1" =~ : ]] && return 0 || return 1
}
is_ip() {
    is_ipv4 "$1" || is_ipv6 "$1"
}
is_domain() {
    [[ "$1" =~ ^([A-Za-z0-9](-*[A-Za-z0-9])*\.)+(xn--[a-z0-9]{2,}|[A-Za-z]{2,})$ ]] && return 0 || return 1
}

# Port helpers
is_port_in_use() {
    local port="$1"
    if command -v ss >/dev/null 2>&1; then
        ss -ltn 2>/dev/null | awk -v p=":${port}$" '$4 ~ p {exit 0} END {exit 1}'
        return
    fi
    if command -v netstat >/dev/null 2>&1; then
        netstat -lnt 2>/dev/null | awk -v p=":${port} " '$4 ~ p {exit 0} END {exit 1}'
        return
    fi
    if command -v lsof >/dev/null 2>&1; then
        lsof -nP -iTCP:${port} -sTCP:LISTEN >/dev/null 2>&1 && return 0
    fi
    return 1
}

get_port() {
    echo $(( ((RANDOM<<15)|RANDOM) % 49152 + 10000 ))
}

gen_random_string() {
    local length="$1"
    openssl rand -base64 $(( length * 2 )) | tr -dc 'a-zA-Z0-9' | head -c "$length"
}

install_base() {
    case "${release}" in
        ubuntu | debian | armbian)
            apt-get update && apt-get install -y -q cron curl tar tzdata socat ca-certificates openssl ufw dnsutils
        ;;
        fedora | amzn | virtuozzo | rhel | almalinux | rocky | ol)
            dnf -y update && dnf install -y -q cronie curl tar tzdata socat ca-certificates openssl ufw bind-utils
        ;;
        centos)
            if [[ "${VERSION_ID}" =~ ^7 ]]; then
                yum -y update && yum install -y cronie curl tar tzdata socat ca-certificates openssl ufw bind-utils
            else
                dnf -y update && dnf install -y -q cronie curl tar tzdata socat ca-certificates openssl ufw bind-utils
            fi
        ;;
        arch | manjaro | parch)
            pacman -Syu && pacman -Syu --noconfirm cronie curl tar tzdata socat ca-certificates openssl ufw bind-tools
        ;;
        opensuse-tumbleweed | opensuse-leap)
            zypper refresh && zypper -q install -y cron curl tar timezone socat ca-certificates openssl ufw bind-utils
        ;;
        alpine)
            apk update && apk add dcron curl tar tzdata socat ca-certificates openssl ufw bind-tools
        ;;
        *)
            apt-get update && apt-get install -y -q cron curl tar tzdata socat ca-certificates openssl ufw dnsutils
        ;;
    esac
}

install_acme() {
    echo -e "${green}Installing acme.sh for SSL certificate management...${plain}"
    cd ~ || return 1
    curl -s https://get.acme.sh | sh >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo -e "${red}Failed to install acme.sh${plain}"
        return 1
    else
        echo -e "${green}acme.sh installed successfully${plain}"
    fi
    return 0
}

setup_ssl_certificate() {
    local domain="$1"
    local server_ip="$2"
    local existing_port="$3"
    local existing_webBasePath="$4"
    
    echo -e "${green}Setting up SSL certificate...${plain}"
    
    if ! command -v ~/.acme.sh/acme.sh &>/dev/null; then
        install_acme
        if [ $? -ne 0 ]; then
            echo -e "${yellow}Failed to install acme.sh, skipping SSL setup${plain}"
            return 1
        fi
    fi
    
    local certPath="/root/cert/${domain}"
    mkdir -p "$certPath"
    
    echo -e "${green}Issuing SSL certificate for ${domain}...${plain}"
    echo -e "${yellow}Note: Port 80 must be open and accessible from the internet${plain}"
    
    ~/.acme.sh/acme.sh --set-default-ca --server letsencrypt --force >/dev/null 2>&1
    ~/.acme.sh/acme.sh --issue -d ${domain} --listen-v6 --standalone --httpport 80 --force
    
    if [ $? -ne 0 ]; then
        echo -e "${yellow}Failed to issue certificate for ${domain}${plain}"
        echo -e "${yellow}Please ensure port 80 is open and try again later with: x-ui${plain}"
        rm -rf ~/.acme.sh/${domain} 2>/dev/null
        rm -rf "$certPath" 2>/dev/null
        return 1
    fi
    
    ~/.acme.sh/acme.sh --installcert -d ${domain} \
        --key-file /root/cert/${domain}/privkey.pem \
        --fullchain-file /root/cert/${domain}/fullchain.pem \
        --reloadcmd "systemctl restart x-ui" >/dev/null 2>&1
    
    if [ $? -ne 0 ]; then
        echo -e "${yellow}Failed to install certificate${plain}"
        return 1
    fi
    
    ~/.acme.sh/acme.sh --upgrade --auto-upgrade >/dev/null 2>&1
    chmod 600 $certPath/privkey.pem 2>/dev/null
    chmod 644 $certPath/fullchain.pem 2>/dev/null
    
    local webCertFile="/root/cert/${domain}/fullchain.pem"
    local webKeyFile="/root/cert/${domain}/privkey.pem"
    
    if [[ -f "$webCertFile" && -f "$webKeyFile" ]]; then
        ${xui_folder}/x-ui cert -webCert "$webCertFile" -webCertKey "$webKeyFile" >/dev/null 2>&1
        echo -e "${green}SSL certificate installed and configured successfully!${plain}"
        return 0
    else
        echo -e "${yellow}Certificate files not found${plain}"
        return 1
    fi
}

setup_ip_certificate() {
    local ipv4="$1"
    local ipv6="$2"

    echo -e "${green}Setting up Let's Encrypt IP certificate (shortlived profile)...${plain}"
    echo -e "${yellow}Note: IP certificates are valid for ~6 days and will auto-renew.${plain}"

    if ! command -v ~/.acme.sh/acme.sh &>/dev/null; then
        install_acme
        if [ $? -ne 0 ]; then
            echo -e "${red}Failed to install acme.sh${plain}"
            return 1
        fi
    fi

    if [[ -z "$ipv4" ]]; then
        echo -e "${red}IPv4 address is required${plain}"
        return 1
    fi

    if ! is_ipv4 "$ipv4"; then
        echo -e "${red}Invalid IPv4 address: $ipv4${plain}"
        return 1
    fi

    local certDir="/root/cert/ip"
    mkdir -p "$certDir"

    local domain_args="-d ${ipv4}"
    if [[ -n "$ipv6" ]] && is_ipv6 "$ipv6"; then
        domain_args="${domain_args} -d ${ipv6}"
        echo -e "${green}Including IPv6 address: ${ipv6}${plain}"
    fi

    local reloadCmd="systemctl restart x-ui 2>/dev/null || rc-service x-ui restart 2>/dev/null || true"

    local WebPort=""
    read -rp "Port to use for ACME HTTP-01 listener (default 80): " WebPort
    WebPort="${WebPort:-80}"
    if ! [[ "${WebPort}" =~ ^[0-9]+$ ]] || ((WebPort < 1 || WebPort > 65535)); then
        echo -e "${red}Invalid port provided. Falling back to 80.${plain}"
        WebPort=80
    fi

    while true; do
        if is_port_in_use "${WebPort}"; then
            echo -e "${yellow}Port ${WebPort} is in use.${plain}"
            local alt_port=""
            read -rp "Enter another port (empty to abort): " alt_port
            alt_port="${alt_port// /}"
            if [[ -z "${alt_port}" ]]; then
                echo -e "${red}Port ${WebPort} is busy; cannot proceed.${plain}"
                return 1
            fi
            if ! [[ "${alt_port}" =~ ^[0-9]+$ ]] || ((alt_port < 1 || alt_port > 65535)); then
                echo -e "${red}Invalid port provided.${plain}"
                return 1
            fi
            WebPort="${alt_port}"
            continue
        else
            echo -e "${green}Port ${WebPort} is free.${plain}"
            break
        fi
    done

    echo -e "${green}Issuing IP certificate for ${ipv4}...${plain}"
    ~/.acme.sh/acme.sh --set-default-ca --server letsencrypt --force >/dev/null 2>&1
    
    ~/.acme.sh/acme.sh --issue \
        ${domain_args} \
        --standalone \
        --server letsencrypt \
        --certificate-profile shortlived \
        --days 6 \
        --httpport ${WebPort} \
        --force

    if [ $? -ne 0 ]; then
        echo -e "${red}Failed to issue IP certificate${plain}"
        rm -rf ~/.acme.sh/${ipv4} 2>/dev/null
        [[ -n "$ipv6" ]] && rm -rf ~/.acme.sh/${ipv6} 2>/dev/null
        rm -rf ${certDir} 2>/dev/null
        return 1
    fi

    ~/.acme.sh/acme.sh --installcert -d ${ipv4} \
        --key-file "${certDir}/privkey.pem" \
        --fullchain-file "${certDir}/fullchain.pem" \
        --reloadcmd "${reloadCmd}" 2>&1 || true

    if [[ ! -f "${certDir}/fullchain.pem" || ! -f "${certDir}/privkey.pem" ]]; then
        echo -e "${red}Certificate files not found after installation${plain}"
        rm -rf ~/.acme.sh/${ipv4} 2>/dev/null
        [[ -n "$ipv6" ]] && rm -rf ~/.acme.sh/${ipv6} 2>/dev/null
        rm -rf ${certDir} 2>/dev/null
        return 1
    fi

    ~/.acme.sh/acme.sh --upgrade --auto-upgrade >/dev/null 2>&1
    chmod 600 ${certDir}/privkey.pem 2>/dev/null
    chmod 644 ${certDir}/fullchain.pem 2>/dev/null

    ${xui_folder}/x-ui cert -webCert "${certDir}/fullchain.pem" -webCertKey "${certDir}/privkey.pem"
    
    if [ $? -ne 0 ]; then
        echo -e "${yellow}Warning: Could not set certificate paths automatically${plain}"
        echo -e "${yellow}Certificate files are at:${plain}"
        echo -e "  Cert: ${certDir}/fullchain.pem"
        echo -e "  Key:  ${certDir}/privkey.pem"
    else
        echo -e "${green}Certificate paths configured successfully${plain}"
    fi

    echo -e "${green}IP certificate installed and configured successfully!${plain}"
    return 0
}

ssl_cert_issue() {
    local existing_webBasePath=$(${xui_folder}/x-ui setting -show true | grep 'webBasePath:' | awk -F': ' '{print $2}' | tr -d '[:space:]' | sed 's#^/##')
    local existing_port=$(${xui_folder}/x-ui setting -show true | grep 'port:' | awk -F': ' '{print $2}' | tr -d '[:space:]')
    
    if ! command -v ~/.acme.sh/acme.sh &>/dev/null; then
        echo "acme.sh could not be found. Installing now..."
        cd ~ || return 1
        curl -s https://get.acme.sh | sh
        if [ $? -ne 0 ]; then
            echo -e "${red}Failed to install acme.sh${plain}"
            return 1
        else
            echo -e "${green}acme.sh installed successfully${plain}"
        fi
    fi

    local domain=""
    while true; do
        read -rp "Please enter your domain name: " domain
        domain="${domain// /}"
        
        if [[ -z "$domain" ]]; then
            echo -e "${red}Domain name cannot be empty. Please try again.${plain}"
            continue
        fi
        
        if ! is_domain "$domain"; then
            echo -e "${red}Invalid domain format: ${domain}. Please enter a valid domain name.${plain}"
            continue
        fi
        
        break
    done
    echo -e "${green}Your domain is: ${domain}, checking it...${plain}"
    SSL_ISSUED_DOMAIN="${domain}"

    local cert_exists=0
    if ~/.acme.sh/acme.sh --list 2>/dev/null | awk '{print $1}' | grep -Fxq "${domain}"; then
        cert_exists=1
        local certInfo=$(~/.acme.sh/acme.sh --list 2>/dev/null | grep -F "${domain}")
        echo -e "${yellow}Existing certificate found for ${domain}, will reuse it.${plain}"
        [[ -n "${certInfo}" ]] && echo "$certInfo"
    else
        echo -e "${green}Your domain is ready for issuing certificates now...${plain}"
    fi

    certPath="/root/cert/${domain}"
    if [ ! -d "$certPath" ]; then
        mkdir -p "$certPath"
    else
        rm -rf "$certPath"
        mkdir -p "$certPath"
    fi

    local WebPort=80
    read -rp "Please choose which port to use (default is 80): " WebPort
    if [[ ${WebPort} -gt 65535 || ${WebPort} -lt 1 ]]; then
        echo -e "${yellow}Your input ${WebPort} is invalid, will use default port 80.${plain}"
        WebPort=80
    fi

    systemctl stop x-ui 2>/dev/null || rc-service x-ui stop 2>/dev/null

    if [[ ${cert_exists} -eq 0 ]]; then
        ~/.acme.sh/acme.sh --set-default-ca --server letsencrypt --force
        ~/.acme.sh/acme.sh --issue -d ${domain} --listen-v6 --standalone --httpport ${WebPort} --force
        if [ $? -ne 0 ]; then
            echo -e "${red}Issuing certificate failed, please check logs.${plain}"
            rm -rf ~/.acme.sh/${domain}
            systemctl start x-ui 2>/dev/null || rc-service x-ui start 2>/dev/null
            return 1
        else
            echo -e "${green}Issuing certificate succeeded, installing certificates...${plain}"
        fi
    else
        echo -e "${green}Using existing certificate, installing certificates...${plain}"
    fi

    reloadCmd="systemctl restart x-ui || rc-service x-ui restart"
    ~/.acme.sh/acme.sh --installcert -d ${domain} \
        --key-file /root/cert/${domain}/privkey.pem \
        --fullchain-file /root/cert/${domain}/fullchain.pem --reloadcmd "${reloadCmd}" 2>&1

    if [[ -f "/root/cert/${domain}/privkey.pem" && -f "/root/cert/${domain}/fullchain.pem" ]]; then
        echo -e "${green}Installing certificate succeeded, enabling auto renew...${plain}"
    else
        echo -e "${red}Installing certificate failed, exiting.${plain}"
        if [[ ${cert_exists} -eq 0 ]]; then
            rm -rf ~/.acme.sh/${domain}
        fi
        systemctl start x-ui 2>/dev/null || rc-service x-ui start 2>/dev/null
        return 1
    fi

    ~/.acme.sh/acme.sh --upgrade --auto-upgrade
    chmod 600 $certPath/privkey.pem 2>/dev/null
    chmod 644 $certPath/fullchain.pem 2>/dev/null

    systemctl start x-ui 2>/dev/null || rc-service x-ui start 2>/dev/null

    read -rp "Would you like to set this certificate for the panel? (y/n): " setPanel
    if [[ "$setPanel" == "y" || "$setPanel" == "Y" ]]; then
        local webCertFile="/root/cert/${domain}/fullchain.pem"
        local webKeyFile="/root/cert/${domain}/privkey.pem"

        if [[ -f "$webCertFile" && -f "$webKeyFile" ]]; then
            ${xui_folder}/x-ui cert -webCert "$webCertFile" -webCertKey "$webKeyFile"
            echo -e "${green}Certificate paths set for the panel${plain}"
            systemctl restart x-ui 2>/dev/null || rc-service x-ui restart 2>/dev/null
        else
            echo -e "${red}Error: Certificate or private key file not found for domain: $domain.${plain}"
        fi
    fi
    
    return 0
}

prompt_and_setup_ssl() {
    local panel_port="$1"
    local web_base_path="$2"
    local server_ip="$3"

    local ssl_choice=""

    echo -e "${yellow}Choose SSL certificate setup method:${plain}"
    echo -e "${green}1.${plain} Let's Encrypt for Domain (90-day validity, auto-renews)"
    echo -e "${green}2.${plain} Let's Encrypt for IP Address (6-day validity, auto-renews)"
    echo -e "${green}3.${plain} Custom SSL Certificate (Path to existing files)"
    read -rp "Choose an option (default 2 for IP): " ssl_choice
    ssl_choice="${ssl_choice// /}"
    
    if [[ "$ssl_choice" != "1" && "$ssl_choice" != "3" ]]; then
        ssl_choice="2"
    fi

    case "$ssl_choice" in
    1)
        echo -e "${green}Using Let's Encrypt for domain certificate...${plain}"
        if ssl_cert_issue; then
            local cert_domain="${SSL_ISSUED_DOMAIN}"
            if [[ -z "${cert_domain}" ]]; then
                cert_domain=$(~/.acme.sh/acme.sh --list 2>/dev/null | tail -1 | awk '{print $1}')
            fi
            if [[ -n "${cert_domain}" ]]; then
                SSL_HOST="${cert_domain}"
                echo -e "${green}✓ SSL certificate configured successfully with domain: ${cert_domain}${plain}"
            else
                echo -e "${yellow}SSL setup may have completed, but domain extraction failed${plain}"
                SSL_HOST="${server_ip}"
            fi
        else
            echo -e "${red}SSL certificate setup failed for domain mode.${plain}"
            SSL_HOST="${server_ip}"
        fi
        ;;
    2)
        echo -e "${green}Using Let's Encrypt for IP certificate (shortlived profile)...${plain}"
        local ipv6_addr=""
        read -rp "Do you have an IPv6 address to include? (IPv6 is disabled, press Enter to skip): " ipv6_addr
        
        if [[ $release == "alpine" ]]; then
            rc-service x-ui stop >/dev/null 2>&1
        else
            systemctl stop x-ui >/dev/null 2>&1
        fi
        
        setup_ip_certificate "${server_ip}" ""
        if [ $? -eq 0 ]; then
            SSL_HOST="${server_ip}"
            echo -e "${green}✓ Let's Encrypt IP certificate configured successfully${plain}"
        else
            echo -e "${red}✗ IP certificate setup failed. Please check port 80 is open.${plain}"
            SSL_HOST="${server_ip}"
        fi
        ;;
    3)
        echo -e "${green}Using custom existing certificate...${plain}"
        local custom_cert=""
        local custom_key=""
        local custom_domain=""

        read -rp "Please enter domain name certificate issued for: " custom_domain
        custom_domain="${custom_domain// /}"

        while true; do
            read -rp "Input certificate path (keywords: .crt / fullchain): " custom_cert
            custom_cert=$(echo "$custom_cert" | tr -d '"' | tr -d "'")
            if [[ -f "$custom_cert" && -r "$custom_cert" && -s "$custom_cert" ]]; then
                break
            else
                echo -e "${red}Error: File does not exist or is not readable! Try again.${plain}"
            fi
        done

        while true; do
            read -rp "Input private key path (keywords: .key / privatekey): " custom_key
            custom_key=$(echo "$custom_key" | tr -d '"' | tr -d "'")
            if [[ -f "$custom_key" && -r "$custom_key" && -s "$custom_key" ]]; then
                break
            else
                echo -e "${red}Error: File does not exist or is not readable! Try again.${plain}"
            fi
        done

        ${xui_folder}/x-ui cert -webCert "$custom_cert" -webCertKey "$custom_key" >/dev/null 2>&1
        
        if [[ -n "$custom_domain" ]]; then
            SSL_HOST="$custom_domain"
        else
            SSL_HOST="${server_ip}"
        fi

        echo -e "${green}✓ Custom certificate paths applied.${plain}"
        systemctl restart x-ui >/dev/null 2>&1 || rc-service x-ui restart >/dev/null 2>&1
        ;;
    esac
}

config_after_install() {
    local existing_hasDefaultCredential=$(${xui_folder}/x-ui setting -show true | grep -Eo 'hasDefaultCredential: .+' | awk '{print $2}')
    local existing_webBasePath=$(${xui_folder}/x-ui setting -show true | grep -Eo 'webBasePath: .+' | awk '{print $2}' | sed 's#^/##')
    local existing_port=$(${xui_folder}/x-ui setting -show true | grep -Eo 'port: .+' | awk '{print $2}')
    local existing_cert=$(${xui_folder}/x-ui setting -getCert true | grep 'cert:' | awk -F': ' '{print $2}' | tr -d '[:space:]')
    
    local URL_lists=(
        "https://api4.ipify.org"
        "https://ipv4.icanhazip.com"
        "https://v4.api.info.io/ip"
        "https://ipv4.myexternalip.com/raw"
        "https://4.ident.me"
        "https://check-host.net/ip"
    )
    local server_ip=""
    for ip_address in "${URL_lists[@]}"; do
        local response=$(curl -s -w "\n%{http_code}" --max-time 3 "${ip_address}" 2>/dev/null)
        local http_code=$(echo "$response" | tail -n1)
        local ip_result=$(echo "$response" | head -n-1 | tr -d '[:space:]')
        if [[ "${http_code}" == "200" && -n "${ip_result}" ]]; then
            server_ip="${ip_result}"
            break
        fi
    done
    
    if [[ ${#existing_webBasePath} -lt 4 ]]; then
        if [[ "$existing_hasDefaultCredential" == "true" ]]; then
            local config_webBasePath=$(gen_random_string 18)
            local config_username=$(gen_random_string 10)
            local config_password=$(gen_random_string 10)
            
            read -rp "Would you like to customize the Panel Port settings? (y/n): " config_confirm
            if [[ "${config_confirm}" == "y" || "${config_confirm}" == "Y" ]]; then
                read -rp "Please set up the panel port: " config_port
                echo -e "${yellow}Your Panel Port is: ${config_port}${plain}"
            else
                local config_port=$(shuf -i 1024-62000 -n 1)
                echo -e "${yellow}Generated random port: ${config_port}${plain}"
            fi
            
            ${xui_folder}/x-ui setting -username "${config_username}" -password "${config_password}" -port "${config_port}" -webBasePath "${config_webBasePath}"
            
            echo ""
            echo -e "${green}═══════════════════════════════════════════${plain}"
            echo -e "${green}     SSL Certificate Setup (MANDATORY)     ${plain}"
            echo -e "${green}═══════════════════════════════════════════${plain}"
            echo -e "${yellow}For security, SSL certificate is required for all panels.${plain}"

            prompt_and_setup_ssl "${config_port}" "${config_webBasePath}" "${server_ip}"
            
            echo ""
            echo -e "${green}═══════════════════════════════════════════${plain}"
            echo -e "${green}     Panel Installation Complete!         ${plain}"
            echo -e "${green}═══════════════════════════════════════════${plain}"
            echo -e "${green}Username:    ${config_username}${plain}"
            echo -e "${green}Password:    ${config_password}${plain}"
            echo -e "${green}Port:        ${config_port}${plain}"
            echo -e "${green}WebBasePath: ${config_webBasePath}${plain}"
            echo -e "${green}Access URL:  https://${SSL_HOST}:${config_port}/${config_webBasePath}${plain}"
        else
            local config_webBasePath=$(gen_random_string 18)
            echo -e "${yellow}WebBasePath is missing or too short. Generating a new one...${plain}"
            ${xui_folder}/x-ui setting -webBasePath "${config_webBasePath}"
            echo -e "${green}New WebBasePath: ${config_webBasePath}${plain}"

            if [[ -z "${existing_cert}" ]]; then
                echo ""
                echo -e "${green}═══════════════════════════════════════════${plain}"
                echo -e "${green}     SSL Certificate Setup (RECOMMENDED)   ${plain}"
                prompt_and_setup_ssl "${existing_port}" "${config_webBasePath}" "${server_ip}"
                echo -e "${green}Access URL:  https://${SSL_HOST}:${existing_port}/${config_webBasePath}${plain}"
            fi
        fi
    else
        if [[ "$existing_hasDefaultCredential" == "true" ]]; then
            local config_username=$(gen_random_string 10)
            local config_password=$(gen_random_string 10)
            
            echo -e "${yellow}Default credentials detected. Security update required...${plain}"
            ${xui_folder}/x-ui setting -username "${config_username}" -password "${config_password}"
            echo -e "###############################################"
            echo -e "${green}Username: ${config_username}${plain}"
            echo -e "${green}Password: ${config_password}${plain}"
            echo -e "###############################################"
        fi

        existing_cert=$(${xui_folder}/x-ui setting -getCert true | grep 'cert:' | awk -F': ' '{print $2}' | tr -d '[:space:]')
        if [[ -z "$existing_cert" ]]; then
            echo ""
            echo -e "${green}═══════════════════════════════════════════${plain}"
            echo -e "${green}     SSL Certificate Setup (RECOMMENDED)   ${plain}"
            prompt_and_setup_ssl "${existing_port}" "${existing_webBasePath}" "${server_ip}"
            echo -e "${green}Access URL:  https://${SSL_HOST}:${existing_port}/${config_webBasePath}${plain}"
        fi
    fi
    
    ${xui_folder}/x-ui migrate
}

install_x-ui() {
    cd ${xui_folder%/x-ui}/
    
    if [ $# == 0 ]; then
        tag_version=$(curl -Ls "https://api.github.com/repos/MHSanaei/3x-ui/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
        if [[ ! -n "$tag_version" ]]; then
            echo -e "${yellow}Trying to fetch version with IPv4...${plain}"
            tag_version=$(curl -4 -Ls "https://api.github.com/repos/MHSanaei/3x-ui/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
            if [[ ! -n "$tag_version" ]]; then
                echo -e "${red}Failed to fetch x-ui version, it may be due to GitHub API restrictions, please try it later${plain}"
                exit 1
            fi
        fi
        echo -e "Got x-ui latest version: ${tag_version}, beginning the installation..."
        curl -4fLRo ${xui_folder}-linux-$(arch).tar.gz https://github.com/MHSanaei/3x-ui/releases/download/${tag_version}/x-ui-linux-$(arch).tar.gz
        if [[ $? -ne 0 ]]; then
            echo -e "${red}Downloading x-ui failed, please be sure that your server can access GitHub ${plain}"
            exit 1
        fi
    else
        tag_version=$1
        tag_version_numeric=${tag_version#v}
        min_version="2.3.5"
        
        if [[ "$(printf '%s\n' "$min_version" "$tag_version_numeric" | sort -V | head -n1)" != "$min_version" ]]; then
            echo -e "${red}Please use a newer version (at least v2.3.5). Exiting installation.${plain}"
            exit 1
        fi
        
        url="https://github.com/MHSanaei/3x-ui/releases/download/${tag_version}/x-ui-linux-$(arch).tar.gz"
        echo -e "Beginning to install x-ui $1"
        curl -4fLRo ${xui_folder}-linux-$(arch).tar.gz ${url}
        if [[ $? -ne 0 ]]; then
            echo -e "${red}Download x-ui $1 failed, please check if the version exists ${plain}"
            exit 1
        fi
    fi
    curl -4fLRo /usr/bin/x-ui-temp https://raw.githubusercontent.com/MHSanaei/3x-ui/main/x-ui.sh
    if [[ $? -ne 0 ]]; then
        echo -e "${red}Failed to download x-ui.sh${plain}"
        exit 1
    fi
    
    if [[ -e ${xui_folder}/ ]]; then
        if [[ $release == "alpine" ]]; then
            rc-service x-ui stop
        else
            systemctl stop x-ui
        fi
        rm ${xui_folder}/ -rf
    fi
    
    tar zxvf x-ui-linux-$(arch).tar.gz
    rm x-ui-linux-$(arch).tar.gz -f
    
    cd x-ui
    chmod +x x-ui
    chmod +x x-ui.sh
    
    if [[ $(arch) == "armv5" || $(arch) == "armv6" || $(arch) == "armv7" ]]; then
        mv bin/xray-linux-$(arch) bin/xray-linux-arm
        chmod +x bin/xray-linux-arm
    fi
    chmod +x x-ui bin/xray-linux-$(arch)
    
    mv -f /usr/bin/x-ui-temp /usr/bin/x-ui
    chmod +x /usr/bin/x-ui
    mkdir -p /var/log/x-ui
    config_after_install

    if [ -d "/etc/.git" ]; then
        if [ -f "/etc/.gitignore" ]; then
            if ! grep -q "x-ui/x-ui.db" "/etc/.gitignore"; then
                echo "" >> "/etc/.gitignore"
                echo "x-ui/x-ui.db" >> "/etc/.gitignore"
            fi
        else
            echo "x-ui/x-ui.db" > "/etc/.gitignore"
        fi
    fi
    
    if [[ $release == "alpine" ]]; then
        curl -4fLRo /etc/init.d/x-ui https://raw.githubusercontent.com/MHSanaei/3x-ui/main/x-ui.rc
        if [[ $? -ne 0 ]]; then
            echo -e "${red}Failed to download x-ui.rc${plain}"
            exit 1
        fi
        chmod +x /etc/init.d/x-ui
        rc-update add x-ui
        rc-service x-ui start
    else
        service_installed=false
        
        if [ -f "x-ui.service" ]; then
            cp -f x-ui.service ${xui_service}/ >/dev/null 2>&1
            if [[ $? -eq 0 ]]; then
                service_installed=true
            fi
        fi
        
        if [ "$service_installed" = false ]; then
            case "${release}" in
                ubuntu | debian | armbian)
                    if [ -f "x-ui.service.debian" ]; then
                        cp -f x-ui.service.debian ${xui_service}/x-ui.service >/dev/null 2>&1
                        if [[ $? -eq 0 ]]; then
                            service_installed=true
                        fi
                    fi
                ;;
                arch | manjaro | parch)
                    if [ -f "x-ui.service.arch" ]; then
                        cp -f x-ui.service.arch ${xui_service}/x-ui.service >/dev/null 2>&1
                        if [[ $? -eq 0 ]]; then
                            service_installed=true
                        fi
                    fi
                ;;
                *)
                    if [ -f "x-ui.service.rhel" ]; then
                        cp -f x-ui.service.rhel ${xui_service}/x-ui.service >/dev/null 2>&1
                        if [[ $? -eq 0 ]]; then
                            service_installed=true
                        fi
                    fi
                ;;
            esac
        fi
        
        if [ "$service_installed" = false ]; then
            case "${release}" in
                ubuntu | debian | armbian)
                    curl -4fLRo ${xui_service}/x-ui.service https://raw.githubusercontent.com/MHSanaei/3x-ui/main/x-ui.service.debian >/dev/null 2>&1
                ;;
                arch | manjaro | parch)
                    curl -4fLRo ${xui_service}/x-ui.service https://raw.githubusercontent.com/MHSanaei/3x-ui/main/x-ui.service.arch >/dev/null 2>&1
                ;;
                *)
                    curl -4fLRo ${xui_service}/x-ui.service https://raw.githubusercontent.com/MHSanaei/3x-ui/main/x-ui.service.rhel >/dev/null 2>&1
                ;;
            esac
            
            if [[ $? -ne 0 ]]; then
                echo -e "${red}Failed to install x-ui.service from GitHub${plain}"
                exit 1
            fi
            service_installed=true
        fi
        
        if [ "$service_installed" = true ]; then
            chown root:root ${xui_service}/x-ui.service >/dev/null 2>&1
            chmod 644 ${xui_service}/x-ui.service >/dev/null 2>&1
            systemctl daemon-reload
            systemctl enable x-ui
            systemctl start x-ui
        else
            echo -e "${red}Failed to install x-ui.service file${plain}"
            exit 1
        fi
    fi
}

# Check and free port 53 for AdGuard
prepare_port53() {
    echo -e "${green}Checking port 53 availability for AdGuard DNS...${plain}"
    
    # Check what's using port 53
    echo -e "${yellow}Checking processes using port 53:${plain}"
    if command -v lsof &>/dev/null; then
        lsof -i :53 2>/dev/null || echo "Nothing found on port 53"
    fi
    
    if command -v ss &>/dev/null; then
        ss -tlnp | grep ":53" || echo "Port 53 is free"
    fi
    
    # Handle systemd-resolved (common on Ubuntu/Debian)
    if systemctl list-units --type=service | grep -q "systemd-resolved.service"; then
        echo -e "${yellow}Detected systemd-resolved, stopping and disabling it...${plain}"
        systemctl stop systemd-resolved 2>/dev/null
        systemctl disable systemd-resolved 2>/dev/null
        
        # Remove stale resolv.conf link
        if [ -L /etc/resolv.conf ]; then
            rm -f /etc/resolv.conf
        fi
    fi
    
    # Kill any other process using port 53
    if command -v lsof &>/dev/null; then
        local pids=$(lsof -ti :53 2>/dev/null)
        if [[ -n "$pids" ]]; then
            echo -e "${yellow}Killing processes using port 53: $pids${plain}"
            kill -9 $pids 2>/dev/null
        fi
    fi
    
    # Set temporary DNS to ensure network works
    echo -e "${green}Setting temporary DNS...${plain}"
    echo "nameserver 1.1.1.1" > /etc/resolv.conf
    
    # Test DNS resolution
    echo -e "${green}Testing DNS resolution...${plain}"
    if ping -c 2 raw.githubusercontent.com &>/dev/null; then
        echo -e "${green}DNS resolution working!${plain}"
    else
        echo -e "${yellow}Warning: DNS resolution might have issues${plain}"
    fi
    
    # Verify port 53 is free
    if command -v ss &>/dev/null; then
        if ss -tlnp | grep -q ":53"; then
            echo -e "${red}Port 53 is still occupied! AdGuard DNS may not work correctly.${plain}"
            return 1
        else
            echo -e "${green}Port 53 is free for AdGuard DNS!${plain}"
            return 0
        fi
    fi
    return 0
}

# Install AdGuard Home using official script
install_adguard() {
    echo -e "${green}Installing AdGuard Home using official script...${plain}"
    
    # Prepare port 53
    prepare_port53
    if [ $? -ne 0 ]; then
        echo -e "${yellow}Warning: Port 53 is occupied. AdGuard DNS may not start correctly.${plain}"
        read -rp "Continue anyway? (y/n): " continue_anyway
        if [[ "$continue_anyway" != "y" && "$continue_anyway" != "Y" ]]; then
            echo -e "${red}AdGuard installation aborted.${plain}"
            return 1
        fi
    fi
    
    # Download and run official install script
    echo -e "${green}Downloading official AdGuard Home installer...${plain}"
    curl -s -S -L https://raw.githubusercontent.com/AdguardTeam/AdGuardHome/master/scripts/install.sh | sh -s -- -v
    
    if [ $? -ne 0 ]; then
        echo -e "${red}Official AdGuard Home installation failed!${plain}"
        echo -e "${yellow}Trying manual installation...${plain}"
        
        # Manual installation fallback
        mkdir -p ${aghome_folder}
        cd ${aghome_folder}
        
        case "$(arch)" in
            amd64) AG_ARCH="linux_amd64" ;;
            arm64) AG_ARCH="linux_arm64" ;;
            armv7) AG_ARCH="linux_armv7" ;;
            armv6) AG_ARCH="linux_armv6" ;;
            *) AG_ARCH="linux_amd64" ;;
        esac
        
        AG_VERSION=$(curl -s "https://api.github.com/repos/AdguardTeam/AdGuardHome/releases/latest" | grep -Po '"tag_name": "\K.*?(?=")')
        AG_VERSION="${AG_VERSION:-v0.107.54}"
        
        curl -L "https://github.com/AdguardTeam/AdGuardHome/releases/download/${AG_VERSION}/AdGuardHome_${AG_ARCH}.tar.gz" -o AdGuardHome.tar.gz
        tar -xzf AdGuardHome.tar.gz
        rm AdGuardHome.tar.gz
        
        cd AdGuardHome
        ./AdGuardHome -s install
    fi
    
    # Wait for service to start
    sleep 3
    
    # Get server IP for display
    local server_ip=$(curl -s ipv4.icanhazip.com)
    
    echo -e "${green}AdGuard Home installed successfully!${plain}"
    
    # Display AdGuard info
    echo ""
    echo -e "${green}═══════════════════════════════════════════${plain}"
    echo -e "${green}     AdGuard Home Setup Complete!         ${plain}"
    echo -e "${green}═══════════════════════════════════════════${plain}"
    echo -e "${green}AdGuard Home Web Interface:${plain}"
    echo -e "  http://${server_ip}:3000 (Initial Setup)"
    echo -e "  https://${server_ip}:3000 (After SSL setup)"
    echo -e "${green}DNS Servers:${plain}"
    echo -e "  ${server_ip}:53 (Standard DNS)"
    echo -e "  ${server_ip}:853 (DNS-over-TLS)"
    echo -e "  ${server_ip}:443 (DNS-over-HTTPS with path /dns-query)"
    echo -e "${green}Default ports - Web: 3000, DNS: 53, 853, 443${plain}"
}

# Configure AdGuard DNS after installation
configure_adguard_dns() {
    local server_ip="$1"
    
    echo -e "${green}Configuring system to use AdGuard DNS...${plain}"
    
    # Wait for AdGuard to be ready
    sleep 5
    
    # Set DNS to local AdGuard
    echo "nameserver 127.0.0.1" > /etc/resolv.conf
    
    # Make resolv.conf immutable to prevent changes
    chattr +i /etc/resolv.conf 2>/dev/null
    
    # Test DNS through AdGuard
    echo -e "${green}Testing DNS through AdGuard...${plain}"
    if command -v dig &>/dev/null; then
        dig @${server_ip} google.com +short
    else
        nslookup google.com 127.0.0.1
    fi
    
    echo -e "${green}System DNS configured to use AdGuard Home${plain}"
}

# Final firewall setup - disable other firewalls, keep only ufw
setup_firewall() {
    echo -e "${green}Configuring firewall...${plain}"
    
    # Detect and disable other firewalls
    echo -e "${yellow}Checking for other firewall services...${plain}"
    
    # Stop and disable firewalld if present
    if systemctl list-units --type=service | grep -q "firewalld.service"; then
        echo -e "${yellow}Disabling firewalld...${plain}"
        systemctl stop firewalld 2>/dev/null
        systemctl disable firewalld 2>/dev/null
    fi
    
    # Stop and disable nftables if present
    if systemctl list-units --type=service | grep -q "nftables.service"; then
        echo -e "${yellow}Disabling nftables...${plain}"
        systemctl stop nftables 2>/dev/null
        systemctl disable nftables 2>/dev/null
    fi
    
    # Stop and disable iptables service if present
    if systemctl list-units --type=service | grep -q "iptables.service"; then
        echo -e "${yellow}Disabling iptables service...${plain}"
        systemctl stop iptables 2>/dev/null
        systemctl disable iptables 2>/dev/null
    fi
    
    # Ensure ufw is installed
    if ! command -v ufw &>/dev/null; then
        echo -e "${yellow}Installing ufw...${plain}"
        if command -v apt &>/dev/null; then
            apt-get install -y ufw
        elif command -v dnf &>/dev/null; then
            dnf install -y ufw
        elif command -v yum &>/dev/null; then
            yum install -y ufw
        fi
    fi
    
    # Reset ufw to default
    echo -e "${yellow}Resetting UFW to default rules...${plain}"
    ufw --force disable
    ufw --force reset
    
    # Set default policies
    ufw default deny incoming
    ufw default allow outgoing
    
    # Allow essential ports
    echo -e "${green}Opening required ports...${plain}"
    ufw allow 22/tcp comment 'SSH'
    ufw allow 80/tcp comment 'HTTP'
    ufw allow 443/tcp comment 'HTTPS'
    ufw allow 8443/tcp comment 'X-UI Alternative'
    ufw allow 1080/tcp comment 'Proxy/SOCKS'
    ufw allow 8080/tcp comment 'HTTP Alt/Proxy'
    ufw allow 3000/tcp comment 'AdGuard Web'
    ufw allow 8888/tcp comment 'AdGuard Alt Web'
    
    # AdGuard DNS ports
    ufw allow 53/tcp comment 'AdGuard DNS TCP'
    ufw allow 53/udp comment 'AdGuard DNS UDP'
    ufw allow 853/tcp comment 'AdGuard DNS-TLS'
    
    # Enable ufw
    echo -e "${yellow}Enabling UFW...${plain}"
    ufw --force enable
    
    # Show status
    ufw status verbose
    
    echo -e "${green}Firewall configuration complete!${plain}"
}

# Create helper script for AdGuard setup
create_adguard_helper() {
    cat > /usr/local/bin/adguardhome-setup << 'EOF'
#!/bin/bash
red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
plain='\033[0m'

echo -e "${green}AdGuard Home Setup Helper${plain}"
echo -e "${yellow}================================${plain}"
echo ""
echo -e "1. Start AdGuard Home: ${green}systemctl start AdGuardHome${plain}"
echo -e "2. Stop AdGuard Home: ${red}systemctl stop AdGuardHome${plain}"
echo -e "3. Restart AdGuard Home: ${yellow}systemctl restart AdGuardHome${plain}"
echo -e "4. Check Status: ${green}systemctl status AdGuardHome${plain}"
echo -e "5. View Logs: ${green}journalctl -u AdGuardHome -f${plain}"
echo -e "6. Reset resolv.conf (if DNS issues): ${green}chattr -i /etc/resolv.conf && echo 'nameserver 1.1.1.1' > /etc/resolv.conf${plain}"
echo ""
echo -e "${green}Access Web Interface:${plain}"
SERVER_IP=$(curl -s ipv4.icanhazip.com)
echo -e "  http://${SERVER_IP}:3000"
echo ""
echo -e "${yellow}Initial Setup Steps:${plain}"
echo -e "1. Open http://${SERVER_IP}:3000 in browser"
echo -e "2. Complete the setup wizard"
echo -e "3. Set DNS upstream servers (e.g., 8.8.8.8, 1.1.1.1)"
echo -e "4. Configure HTTPS if you have a domain"
echo -e "5. Blocklists can be added in 'Filters' -> 'DNS blocklists'"
echo -e "6. After setup, run ${green}adguardhome-finalize${plain}"
EOF
    chmod +x /usr/local/bin/adguardhome-setup
}

# Create finalize script for AdGuard
create_adguard_finalize() {
    cat > /usr/local/bin/adguardhome-finalize << 'EOF'
#!/bin/bash
red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
plain='\033[0m'

echo -e "${green}Finalizing AdGuard Home configuration...${plain}"

# Get server IP
SERVER_IP=$(curl -s ipv4.icanhazip.com)

# Set DNS to local AdGuard
echo "nameserver 127.0.0.1" > /etc/resolv.conf
chattr +i /etc/resolv.conf 2>/dev/null

# Test DNS
echo -e "${green}Testing DNS resolution through AdGuard...${plain}"
if dig @${SERVER_IP} google.com +short 2>/dev/null | head -1; then
    echo -e "${green}✓ DNS is working through AdGuard Home${plain}"
else
    echo -e "${yellow}✗ DNS test failed. Please check AdGuard configuration.${plain}"
fi

echo -e "${green}AdGuard Home is now the system DNS resolver!${plain}"
echo -e "${yellow}Note: If you experience DNS issues, run:${plain}"
echo -e "  chattr -i /etc/resolv.conf && echo 'nameserver 1.1.1.1' > /etc/resolv.conf"
EOF
    chmod +x /usr/local/bin/adguardhome-finalize
}

# Enable BBR and tune system
tune_system() {
    echo -e "${green}Tuning system settings (BBR, file limits, etc.)...${plain}"
    
    # Check if BBR is already configured
    if ! grep -q "net.core.default_qdisc=fq" /etc/sysctl.conf; then
        echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
    fi
    if ! grep -q "net.ipv4.tcp_congestion_control=bbr" /etc/sysctl.conf; then
        echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
    fi
    if ! grep -q "fs.file-max=2097152" /etc/sysctl.conf; then
        echo "fs.file-max=2097152" >> /etc/sysctl.conf
    fi
    if ! grep -q "net.ipv4.tcp_timestamps = 1" /etc/sysctl.conf; then
        echo "net.ipv4.tcp_timestamps = 1" >> /etc/sysctl.conf
    fi
    if ! grep -q "net.ipv4.tcp_sack = 1" /etc/sysctl.conf; then
        echo "net.ipv4.tcp_sack = 1" >> /etc/sysctl.conf
    fi
    if ! grep -q "net.ipv4.tcp_window_scaling = 1" /etc/sysctl.conf; then
        echo "net.ipv4.tcp_window_scaling = 1" >> /etc/sysctl.conf
    fi
    if ! grep -q "net.core.rmem_max = 16777216" /etc/sysctl.conf; then
        echo "net.core.rmem_max = 16777216" >> /etc/sysctl.conf
    fi
    if ! grep -q "net.core.wmem_max = 16777216" /etc/sysctl.conf; then
        echo "net.core.wmem_max = 16777216" >> /etc/sysctl.conf
    fi
    if ! grep -q "net.ipv4.tcp_rmem = 4096 87380 16777216" /etc/sysctl.conf; then
        echo "net.ipv4.tcp_rmem = 4096 87380 16777216" >> /etc/sysctl.conf
    fi
    if ! grep -q "net.ipv4.tcp_wmem = 4096 65536 16777216" /etc/sysctl.conf; then
        echo "net.ipv4.tcp_wmem = 4096 65536 16777216" >> /etc/sysctl.conf
    fi
    
    # Apply settings
    sysctl -p
    
    # Check BBR status
    if [[ $(sysctl net.ipv4.tcp_congestion_control | awk '{print $3}') == "bbr" ]]; then
        echo -e "${green}BBR is enabled!${plain}"
    else
        echo -e "${yellow}BBR may need a reboot to take effect.${plain}"
    fi
}

# Setup cron jobs
setup_cron() {
    echo -e "${green}Setting up cron jobs...${plain}"
    
    # Remove existing entries and add new ones
    crontab -l | grep -v "certbot\|x-ui\|AdGuardHome" | crontab - 2>/dev/null
    
    # Daily x-ui restart (if needed)
    (crontab -l 2>/dev/null; echo '@daily x-ui restart > /dev/null 2>&1') | crontab -
    
    # Monthly certbot renewal (if certbot is installed)
    if command -v certbot &>/dev/null; then
        (crontab -l 2>/dev/null; echo '@monthly certbot renew --nginx --non-interactive --post-hook "nginx -s reload" > /dev/null 2>&1') | crontab -
    fi
    
    # Weekly AdGuard log cleanup
    (crontab -l 2>/dev/null; echo '@weekly find /var/log/adguardhome -name "*.log" -mtime +30 -delete 2>/dev/null') | crontab -
    
    echo -e "${green}Cron jobs configured!${plain}"
}

# Main installation function
main_install() {
    echo -e "${green}Starting 3x-ui + AdGuard Home installation...${plain}"
    
    # Step 1: Disable IPv6
    disable_ipv6
    
    # Step 2: Install base packages
    install_base
    
    # Step 3: Install 3x-ui
    install_x-ui $1
    
    # Step 4: Install AdGuard Home (optional)
    echo ""
    read -rp "Would you like to install AdGuard Home? (y/n): " install_ag
    if [[ "$install_ag" == "y" || "$install_ag" == "Y" ]]; then
        install_adguard
        create_adguard_helper
        create_adguard_finalize
        
        # Ask if user wants to configure DNS now
        echo ""
        read -rp "Would you like to configure system DNS to use AdGuard Home now? (y/n): " config_dns
        if [[ "$config_dns" == "y" || "$config_dns" == "Y" ]]; then
            local server_ip=$(curl -s ipv4.icanhazip.com)
            configure_adguard_dns "${server_ip}"
        else
            echo -e "${yellow}You can run 'adguardhome-finalize' later to configure DNS.${plain}"
        fi
    else
        echo -e "${yellow}Skipping AdGuard Home installation...${plain}"
    fi
    
    # Step 5: Tune system (BBR, etc.)
    tune_system
    
    # Step 6: Setup cron jobs
    setup_cron
    
    # Step 7: Configure firewall (last step to avoid interruptions)
    setup_firewall
    
    # Show installation summary
    echo ""
    echo -e "${green}═══════════════════════════════════════════════════════════════${plain}"
    echo -e "${green}                    Installation Complete!                      ${plain}"
    echo -e "${green}═══════════════════════════════════════════════════════════════${plain}"
    
    # Show panel info
    echo -e "${green}3x-ui Panel:${plain}"
    echo -e "  Run ${yellow}x-ui${plain} for management menu"
    
    # Show AdGuard info if installed
    if [[ "$install_ag" == "y" || "$install_ag" == "Y" ]]; then
        local server_ip=$(curl -s ipv4.icanhazip.com)
        echo -e "${green}AdGuard Home:${plain}"
        echo -e "  Service: ${yellow}AdGuardHome${plain}"
        echo -e "  Web Interface: ${yellow}http://${server_ip}:3000${plain}"
        echo -e "  DNS Server: ${yellow}${server_ip}:53${plain}"
        echo -e "  Helper Script: ${yellow}adguardhome-setup${plain}"
        echo -e "  Finalize Script: ${yellow}adguardhome-finalize${plain}"
    fi
    
    echo -e "${green}Firewall:${plain}"
    ufw status | head -8
    
    echo -e "${yellow}Note: You may need to reboot for all changes to take effect.${plain}"
}

# Run main installation
echo -e "${green}Running...${plain}"
main_install $1
