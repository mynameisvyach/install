#!/bin/bash
commands='22'

RED='\033[1;91m'
CYAN='\033[1;96m'
PURPLE_LIGHT='\033[5;35m'
RESET='\033[0m'

start_process_line="${PURPLE_LIGHT}################################################################################"
end_process_line="################################################################################${RESET}"

logo="\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m'\e[0m\e[38;5;0m\"\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;52m,\e[0m\e[38;5;52mi\e[0m\e[38;5;88m>\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;52m,\e[0m\e[38;5;88m>\e[0m\e[38;5;9m1\e[0m\e[38;5;160m[\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m'\e[0m\e[38;5;0m^\e[0m\e[38;5;52m:\e[0m\e[38;5;124m?\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;0m^\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;52mI\e[0m\e[38;5;160m{\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m)\e[0m\e[38;5;9m(\e[0m\e[38;5;52m:\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;52m,\e[0m\e[38;5;160m[\e[0m\e[38;5;9m(\e[0m\e[38;5;9m)\e[0m\e[38;5;9m(\e[0m\e[38;5;9m)\e[0m\e[38;5;9m(\e[0m\e[38;5;52mi\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;0ml\e[0m\e[38;5;60mt\e[0m\e[38;5;60m/\e[0m\e[38;5;60mt\e[0m\e[38;5;60m/\e[0m\e[38;5;59m/\e[0m\e[38;5;59m/\e[0m\e[38;5;59m/\e[0m\e[38;5;59m/\e[0m\e[38;5;59m/\e[0m\e[38;5;59m/\e[0m\e[38;5;17m!\e[0m\e[38;5;0m \e[0m\e[38;5;59m-\e[0m\e[38;5;60mt\e[0m\e[38;5;60m/\e[0m\e[38;5;60mt\e[0m\e[38;5;59m/\e[0m\e[38;5;59m/\e[0m\e[38;5;59m/\e[0m\e[38;5;59m|\e[0m\e[38;5;59m[\e[0m\e[38;5;17mi\e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0ml\e[0m\e[38;5;59m}\e[0m\e[38;5;60mf\e[0m\e[38;5;102mn\e[0m\e[38;5;102mn\e[0m\e[38;5;60mt\e[0m\e[38;5;59m}\e[0m\e[38;5;17m!\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;52mI\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m)\e[0m\e[38;5;160m]\e[0m\e[38;5;0m'\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m'\e[0m\e[38;5;0m \e[0m\e[38;5;59m1\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;59m/\e[0m\e[38;5;0m \e[0m\e[38;5;145mL\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;188ma\e[0m\e[38;5;59m|\e[0m\e[38;5;0m \e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;59m{\e[0m\e[38;5;146mq\e[0m\e[38;5;15m@\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m@\e[0m\e[38;5;59m-\e[0m\e[38;5;0m \e[0m\e[38;5;0m\`\e[0m\e[38;5;9m1\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m1\e[0m\e[38;5;9m)\e[0m\e[38;5;9m)\e[0m\e[38;5;160m[\e[0m\e[38;5;167m(\e[0m\e[38;5;168mc\e[0m\e[38;5;0m\"\e[0m\e[38;5;0m \e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m'\e[0m\e[38;5;0m \e[0m\e[38;5;59m}\e[0m\e[38;5;15m@\e[0m\e[38;5;15mB\e[0m\e[38;5;15m@\e[0m\e[38;5;188mM\e[0m\e[38;5;145mq\e[0m\e[38;5;146mp\e[0m\e[38;5;146mq\e[0m\e[38;5;146mq\e[0m\e[38;5;145mq\e[0m\e[38;5;146mq\e[0m\e[38;5;59m]\e[0m\e[38;5;0m \e[0m\e[38;5;102mY\e[0m\e[38;5;15m@\e[0m\e[38;5;15mB\e[0m\e[38;5;15m@\e[0m\e[38;5;188mb\e[0m\e[38;5;145mO\e[0m\e[38;5;145mZ\e[0m\e[38;5;188md\e[0m\e[38;5;15m@\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;59m)\e[0m\e[38;5;0m \e[0m\e[38;5;0m.\e[0m\e[38;5;103mY\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;188m#\e[0m\e[38;5;188ma\e[0m\e[38;5;188m*\e[0m\e[38;5;15m%\e[0m\e[38;5;15m$\e[0m\e[38;5;59m{\e[0m\e[38;5;0m \e[0m\e[38;5;52ml\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;160m[\e[0m\e[38;5;95m{\e[0m\e[38;5;124m]\e[0m\e[38;5;132mu\e[0m\e[38;5;188ma\e[0m\e[38;5;195m&\e[0m\e[38;5;182mb\e[0m\e[38;5;0m,\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m'\e[0m\e[38;5;0m \e[0m\e[38;5;59m}\e[0m\e[38;5;15m$\e[0m\e[38;5;15m@\e[0m\e[38;5;15m$\e[0m\e[38;5;102mX\e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;102mX\e[0m\e[38;5;15m$\e[0m\e[38;5;15m@\e[0m\e[38;5;15m$\e[0m\e[38;5;59m?\e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;59m/\e[0m\e[38;5;15m$\e[0m\e[38;5;15mB\e[0m\e[38;5;15m@\e[0m\e[38;5;145mm\e[0m\e[38;5;0m \e[0m\e[38;5;60mt\e[0m\e[38;5;15m$\e[0m\e[38;5;15m@\e[0m\e[38;5;15m@\e[0m\e[38;5;15m$\e[0m\e[38;5;109mU\e[0m\e[38;5;17mi\e[0m\e[38;5;0m\`\e[0m\e[38;5;0m.\e[0m\e[38;5;0m'\e[0m\e[38;5;0mI\e[0m\e[38;5;59m\\e[0m\e[38;5;17m!\e[0m\e[38;5;0m \e[0m\e[38;5;124m-\e[0m\e[38;5;9m(\e[0m\e[38;5;9m)\e[0m\e[38;5;9m1\e[0m\e[38;5;125m}\e[0m\e[38;5;95mt\e[0m\e[38;5;188mo\e[0m\e[38;5;224mW\e[0m\e[38;5;203mu\e[0m\e[38;5;9m1\e[0m\e[38;5;160m{\e[0m\e[38;5;124m-\e[0m\e[38;5;52mi\e[0m\e[38;5;0m\"\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m'\e[0m\e[38;5;0m \e[0m\e[38;5;59m}\e[0m\e[38;5;15m$\e[0m\e[38;5;15m@\e[0m\e[38;5;15m$\e[0m\e[38;5;188m*\e[0m\e[38;5;145mC\e[0m\e[38;5;145mL\e[0m\e[38;5;145mC\e[0m\e[38;5;145mC\e[0m\e[38;5;145mC\e[0m\e[38;5;102mj\e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;102mY\e[0m\e[38;5;15m$\e[0m\e[38;5;15m@\e[0m\e[38;5;15m$\e[0m\e[38;5;102mx\e[0m\e[38;5;59m~\e[0m\e[38;5;59m_\e[0m\e[38;5;59m]\e[0m\e[38;5;145mZ\e[0m\e[38;5;15m@\e[0m\e[38;5;15mB\e[0m\e[38;5;15m$\e[0m\e[38;5;103mY\e[0m\e[38;5;0m \e[0m\e[38;5;188mh\e[0m\e[38;5;15m$\e[0m\e[38;5;15m@\e[0m\e[38;5;15m$\e[0m\e[38;5;145mQ\e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;52m,\e[0m\e[38;5;9m)\e[0m\e[38;5;9m(\e[0m\e[38;5;9m)\e[0m\e[38;5;9m(\e[0m\e[38;5;160m[\e[0m\e[38;5;188ma\e[0m\e[38;5;15m$\e[0m\e[38;5;210mJ\e[0m\e[38;5;9m]\e[0m\e[38;5;9m)\e[0m\e[38;5;9m)\e[0m\e[38;5;160m[\e[0m\e[38;5;124m-\e[0m\e[38;5;52m!\e[0m\e[38;5;0m'\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m'\e[0m\e[38;5;0m \e[0m\e[38;5;59m}\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;188ma\e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;102mY\e[0m\e[38;5;15m$\e[0m\e[38;5;15m@\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;188mh\e[0m\e[38;5;0m:\e[0m\e[38;5;0m.\e[0m\e[38;5;188m*\e[0m\e[38;5;15m$\e[0m\e[38;5;15m@\e[0m\e[38;5;15m$\e[0m\e[38;5;66mf\e[0m\e[38;5;0m \e[0m\e[38;5;0m\`\e[0m\e[38;5;0m'\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m^\e[0m\e[38;5;160m}\e[0m\e[38;5;9m(\e[0m\e[38;5;9m)\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;160m]\e[0m\e[38;5;145mO\e[0m\e[38;5;15m$\e[0m\e[38;5;188mk\e[0m\e[38;5;210mC\e[0m\e[38;5;131m(\e[0m\e[38;5;88m>\e[0m\e[38;5;52ml\e[0m\e[38;5;52m,\e[0m\e[38;5;0m'\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m'\e[0m\e[38;5;0m \e[0m\e[38;5;59m}\e[0m\e[38;5;15m$\e[0m\e[38;5;15m@\e[0m\e[38;5;15m$\e[0m\e[38;5;188mh\e[0m\e[38;5;102mv\e[0m\e[38;5;102mc\e[0m\e[38;5;102mc\e[0m\e[38;5;102mv\e[0m\e[38;5;102mc\e[0m\e[38;5;59m\\e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;102mY\e[0m\e[38;5;15m$\e[0m\e[38;5;15m@\e[0m\e[38;5;15m$\e[0m\e[38;5;15m&\e[0m\e[38;5;188mM\e[0m\e[38;5;188mM\e[0m\e[38;5;188mo\e[0m\e[38;5;188md\e[0m\e[38;5;145mC\e[0m\e[38;5;59m(\e[0m\e[38;5;0m\`\e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;145mm\e[0m\e[38;5;15m$\e[0m\e[38;5;15m@\e[0m\e[38;5;15m$\e[0m\e[38;5;188mo\e[0m\e[38;5;0mI\e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m.\e[0m\e[38;5;0m^\e[0m\e[38;5;88m>\e[0m\e[38;5;160m}\e[0m\e[38;5;9m1\e[0m\e[38;5;160m{\e[0m\e[38;5;160m{\e[0m\e[38;5;9m1\e[0m\e[38;5;9m)\e[0m\e[38;5;124m]\e[0m\e[38;5;152mp\e[0m\e[38;5;15m@\e[0m\e[38;5;195m&\e[0m\e[38;5;195mB\e[0m\e[38;5;66mu\e[0m\e[38;5;0m \e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m'\e[0m\e[38;5;0m \e[0m\e[38;5;59m}\e[0m\e[38;5;15m$\e[0m\e[38;5;15mB\e[0m\e[38;5;15m$\e[0m\e[38;5;102mX\e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m'\e[0m\e[38;5;0m \e[0m\e[38;5;102mX\e[0m\e[38;5;15m$\e[0m\e[38;5;15mB\e[0m\e[38;5;15m$\e[0m\e[38;5;59m)\e[0m\e[38;5;0m'\e[0m\e[38;5;0m^\e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m'\e[0m\e[38;5;0m \e[0m\e[38;5;59m~\e[0m\e[38;5;15mB\e[0m\e[38;5;15m$\e[0m\e[38;5;15m@\e[0m\e[38;5;15m$\e[0m\e[38;5;15m%\e[0m\e[38;5;145m0\e[0m\e[38;5;102mx\e[0m\e[38;5;59m_\e[0m\e[38;5;88m~\e[0m\e[38;5;160m{\e[0m\e[38;5;9m)\e[0m\e[38;5;160m1\e[0m\e[38;5;160m{\e[0m\e[38;5;160m{\e[0m\e[38;5;160m{\e[0m\e[38;5;9m1\e[0m\e[38;5;9m(\e[0m\e[38;5;160m1\e[0m\e[38;5;167m)\e[0m\e[38;5;131m|\e[0m\e[38;5;131mf\e[0m\e[38;5;167mx\e[0m\e[38;5;52m<\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m'\e[0m\e[38;5;0m \e[0m\e[38;5;59m{\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;145mL\e[0m\e[38;5;0m \e[0m\e[38;5;0m\`\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m'\e[0m\e[38;5;0m.\e[0m\e[38;5;0m'\e[0m\e[38;5;0m \e[0m\e[38;5;109mU\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;59m1\e[0m\e[38;5;0m \e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m'\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;59m+\e[0m\e[38;5;188mk\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;15m$\e[0m\e[38;5;224m*\e[0m\e[38;5;203mX\e[0m\e[38;5;9m(\e[0m\e[38;5;9m1\e[0m\e[38;5;160m{\e[0m\e[38;5;160m{\e[0m\e[38;5;160m{\e[0m\e[38;5;160m{\e[0m\e[38;5;160m}\e[0m\e[38;5;160m{\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m1\e[0m\e[38;5;9m1\e[0m\e[38;5;9m{\e[0m\e[38;5;9m}\e[0m\e[38;5;52m:\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;59m-\e[0m\e[38;5;188mh\e[0m\e[38;5;188mb\e[0m\e[38;5;188mh\e[0m\e[38;5;102mn\e[0m\e[38;5;0m \e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;102mr\e[0m\e[38;5;188mh\e[0m\e[38;5;188mb\e[0m\e[38;5;188mh\e[0m\e[38;5;59m]\e[0m\e[38;5;0m \e[0m\e[38;5;0m'\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;0m.\e[0m\e[38;5;59m]\e[0m\e[38;5;174mL\e[0m\e[38;5;203mv\e[0m\e[38;5;160m]\e[0m\e[38;5;160m]\e[0m\e[38;5;160m{\e[0m\e[38;5;160m{\e[0m\e[38;5;160m{\e[0m\e[38;5;160m1\e[0m\e[38;5;160m{\e[0m\e[38;5;160m[\e[0m\e[38;5;160m{\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m)\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m)\e[0m\e[38;5;88m<\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m \e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m^\e[0m\e[38;5;88mi\e[0m\e[38;5;160m?\e[0m\e[38;5;160m[\e[0m\e[38;5;160m1\e[0m\e[38;5;160m1\e[0m\e[38;5;160m{\e[0m\e[38;5;160m1\e[0m\e[38;5;160m{\e[0m\e[38;5;160m[\e[0m\e[38;5;160m}\e[0m\e[38;5;9m)\e[0m\e[38;5;9m(\e[0m\e[38;5;9m)\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;160m]\e[0m\e[38;5;52ml\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;52mi\e[0m\e[38;5;160m{\e[0m\e[38;5;9m(\e[0m\e[38;5;160m1\e[0m\e[38;5;160m1\e[0m\e[38;5;160m{\e[0m\e[38;5;160m1\e[0m\e[38;5;160m{\e[0m\e[38;5;160m[\e[0m\e[38;5;160m[\e[0m\e[38;5;160m{\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;160m}\e[0m\e[38;5;88m~\e[0m\e[38;5;52m;\e[0m\e[38;5;0m'\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;52m,\e[0m\e[38;5;124m]\e[0m\e[38;5;9m)\e[0m\e[38;5;160m{\e[0m\e[38;5;160m{\e[0m\e[38;5;160m{\e[0m\e[38;5;160m1\e[0m\e[38;5;160m{\e[0m\e[38;5;160m[\e[0m\e[38;5;160m]\e[0m\e[38;5;160m{\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;160m}\e[0m\e[38;5;88m+\e[0m\e[38;5;52m;\e[0m\e[38;5;0m'\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;88m>\e[0m\e[38;5;160m1\e[0m\e[38;5;160m1\e[0m\e[38;5;160m{\e[0m\e[38;5;160m{\e[0m\e[38;5;160m1\e[0m\e[38;5;160m}\e[0m\e[38;5;124m]\e[0m\e[38;5;124m]\e[0m\e[38;5;160m{\e[0m\e[38;5;9m(\e[0m\e[38;5;9m(\e[0m\e[38;5;9m1\e[0m\e[38;5;124m]\e[0m\e[38;5;88m<\e[0m\e[38;5;52m,\e[0m\e[38;5;0m\`\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;0m^\e[0m\e[38;5;124m?\e[0m\e[38;5;9m)\e[0m\e[38;5;160m1\e[0m\e[38;5;160m{\e[0m\e[38;5;160m{\e[0m\e[38;5;160m[\e[0m\e[38;5;160m]\e[0m\e[38;5;160m[\e[0m\e[38;5;9m1\e[0m\e[38;5;9m(\e[0m\e[38;5;160m{\e[0m\e[38;5;124m+\e[0m\e[38;5;52mI\e[0m\e[38;5;0m\`\e[0m\e[38;5;0m.\e[0m\e[38;5;0m^\e[0m\e[38;5;0m \e[0m\e[38;5;0m\`\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;52ml\e[0m\e[38;5;160m1\e[0m\e[38;5;9m(\e[0m\e[38;5;160m}\e[0m\e[38;5;160m[\e[0m\e[38;5;160m[\e[0m\e[38;5;160m]\e[0m\e[38;5;160m]\e[0m\e[38;5;160m]\e[0m\e[38;5;124m-\e[0m\e[38;5;52mi\e[0m\e[38;5;52m,\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;0m\`\e[0m\e[38;5;0mI\e[0m\e[38;5;0m'\e[0m\e[38;5;0m^\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m'\e[0m\e[38;5;88m<\e[0m\e[38;5;160m{\e[0m\e[38;5;124m_\e[0m\e[38;5;52mi\e[0m\e[38;5;88m<\e[0m\e[38;5;124m+\e[0m\e[38;5;88m<\e[0m\e[38;5;52m!\e[0m\e[38;5;52m:\e[0m\e[38;5;0m'\e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m'\e[0m\e[38;5;0m^\e[0m\e[38;5;0m\"\e[0m\e[38;5;0m\"\e[0m\e[38;5;0m\`\e[0m\e[38;5;0m'\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m'\e[0m\e[38;5;52m,\e[0m\e[38;5;0m'\e[0m\e[38;5;0m.\e[0m\e[38;5;0m\"\e[0m\e[38;5;52m,\e[0m\e[38;5;0m\`\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m \e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\n\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m\e[38;5;0m.\e[0m"

clear
echo -e $logo


echo -e "\n\n${RED} * GitHub ${CYAN}github.com/sidor0912/FunPayCardinal${RESET}"
echo -e "${RED} * Telegram ${CYAN}t.me/funpay_cardinal${RESET}"
echo -e "\n\n\n"


echo -ne "${CYAN}Введите имя пользователя, от имени которого будет запускаться бот (например, 'fpc' или 'cardinal'): ${RESET}"
while true; do
  read username

  if [[ "$username" =~ ^[a-zA-Z][a-zA-Z0-9_-]+$ ]]; then
    if id "$username" &>/dev/null; then
      echo -ne "\n${RED}Пользователь уже существует.${RESET} Использовать его? (y/n): "
      read use_existing

      if [[ "$use_existing" =~ ^[Yy]$ ]]; then
        echo -e "${CYAN}Будет использован существующий пользователь: $username${RESET}"
        break
      else
        echo -ne "${CYAN}Введите другое имя пользователя: ${RESET}"
      fi
    else
      break
    fi
  else
    echo -ne "\n${RED}Имя пользователя содержит недопустимые символы. ${CYAN}Имя должно начинаться с буквы и может включать только буквы, цифры, '_', или '-'. Пожалуйста, введите другое имя пользователя: ${RESET}"
  fi
done

WORK_DIR="/home/$username/FunPayCardinal"
distro_version=$(lsb_release -rs)


clear
echo -e "${start_process_line}\nДобавляю репозитории...\n${end_process_line}"


# 1
if ! sudo apt update ; then
  echo -e "${start_process_line}\nПроизошла ошибка при обновлении списка пакетов. (1/${commands})\n${end_process_line}"
  exit 2
fi

#2
if ! sudo apt install -y software-properties-common ; then
  echo -e "${start_process_line}\nПроизошла ошибка при установке software-properties-common. (2/${commands})\n${end_process_line}"
  exit 2
fi

#3
case $distro_version in
  "22.04" | "22.10" | "23.04" | "23.10" | "24.04" | "24.10") # Ubuntu 22.04 (Jammy Jellyfish), 22.10 (Kinetic Kudu), 23.04 (Lunar Lobster), 23.10 (Mantic Minotaur), 24.04 (Noble Numbat), 24.10 (Oracular Oriole)
    ;;
  "12") # Debian 12 (Bookworm)
    ;;
  "11") # Debian 11 (Bullseye)
    # TODO: Ошибка проверки ключа репозитория на некоторых машинах, хз почему, проще использовать костыль ввиде убунтовских deadsnakes
    # #3.1
    # if ! sudo curl -O https://people.debian.org/~paravoid/python-all/unofficial-python-all.asc ; then
    #   echo -e "${start_process_line}\nПроизошла ошибка при загрузке ключа репозитория. (3.1/${commands})\n${end_process_line}"
    #   exit 2
    # fi

    # #3.2
    # if ! sudo mv unofficial-python-all.asc /etc/apt/trusted.gpg.d/ ; then
    #   echo -e "${start_process_line}\nПроизошла ошибка при перемещении ключа репозитория. (3.2/${commands})\n${end_process_line}"
    #   exit 2
    # fi

    # #3.3
    # if ! echo "deb http://people.debian.org/~paravoid/python-all $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/python-all.list ; then
    #   echo -e "${start_process_line}\nПроизошла ошибка при добавлении репозитория. (3.3/${commands})\n${end_process_line}"
    #   exit 2
    # fi

    #3.1
    if ! sudo apt install -y gnupg ; then
      echo -e "${start_process_line}\nПроизошла ошибка при установке gnupg. (3.1/${commands})\n${end_process_line}"
      exit 2
    fi

    #3.2
    if ! sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys BA6932366A755776 ; then
      echo -e "${start_process_line}\nПроизошла ошибка при добавлении ключа репозитория. (3.2/${commands})\n${end_process_line}"
      exit 2
    fi

    #3.3
    if ! sudo add-apt-repository -s "deb https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu focal main" ; then
      echo -e "${start_process_line}\nПроизошла ошибка при добавлении репозитория. (3.3/${commands})\n${end_process_line}"
      exit 2
    fi

    #3.4
    sudo tee /etc/apt/preferences.d/10deadsnakes-ppa >/dev/null <<EOF
Package: *
Pin: release o=LP-PPA-deadsnakes
Pin-Priority: 100
EOF
    if $? -ne 0 ; then
      echo -e "${start_process_line}\nПроизошла ошибка при добавлении приоритета репозитория. (3.4/${commands})\n${end_process_line}"
      exit 2
    fi
    ;;
  *)
    #3
    if ! sudo add-apt-repository -y ppa:deadsnakes/ppa ; then
      echo -e "${start_process_line}\nПроизошла ошибка при добавлении репозитория. (3/${commands})\n${end_process_line}"
      exit 2
    fi
    ;;
esac

#4
if ! sudo apt update ; then
  echo -e "${start_process_line}\nПроизошла ошибка при обновлении списка пакетов. (4/${commands})\n${end_process_line}"
  exit 2
fi


clear
echo -e "$start_process_line\nУстанавливаю необходимые пакеты...\n$end_process_line"


#5
if ! sudo apt install -y curl ; then
  echo -e "${start_process_line}\nПроизошла ошибка при установке Curl. (5/${commands})\n${end_process_line}"
  exit 2
fi

#6
if ! sudo apt install -y unzip ; then
  echo -e "${start_process_line}\nПроизошла ошибка при установке Unzip. (6/${commands})\n${end_process_line}"
  exit 2
fi


clear
echo -e "$start_process_line\nУстанавливаю Python...\n$end_process_line"


#7
case $distro_version in
  "24.04" | "24.10")
    if ! sudo apt install -y python3.12 python3.12-dev python3.12-gdbm python3.12-venv ; then
      echo -e "${start_process_line}\nПроизошла ошибка при установке Python. (7/${commands})\n${end_process_line}"
      exit 2
    fi
    ;;
  *)
    if ! sudo apt install -y python3.11 python3.11-dev python3.11-gdbm python3.11-venv ; then
      echo -e "${start_process_line}\nПроизошла ошибка при установке Python. (7/${commands})\n${end_process_line}"
      exit 2
    fi
    ;;
esac

clear
echo -e "$start_process_line\nСоздаю пользователя и устанавливаю/обновляю Pip...\n$end_process_line"

#8
if id "$username" &>/dev/null; then
    echo -e "${CYAN}Пользователь $username уже существует, пропускаем создание.${RESET}"
else
    if ! sudo useradd -m "$username"; then
        echo -e "${start_process_line}\nПроизошла ошибка при создании пользователя. (8/${commands})\n${end_process_line}"
        exit 2
    fi
fi

#9
case $distro_version in
  "24.04" | "24.10")
    if ! sudo -u $username python3.12 -m venv /home/$username/pyvenv ; then
      echo -e "${start_process_line}\nПроизошла ошибка при создании виртуального окружения. (9/${commands})\n${end_process_line}"
      exit 2
    fi
    ;;
  *)
    if ! sudo -u $username python3.11 -m venv /home/$username/pyvenv ; then
      echo -e "${start_process_line}\nПроизошла ошибка при создании виртуального окружения. (9/${commands})\n${end_process_line}"
      exit 2
    fi
    ;;
esac

#10
# Важно: eunsurepip стоить запускать от root, иначе будет ошибка на некоторых версиях ОС (например, Debian 11, Debian 12, Ubuntu 20.04, Ubuntu 24.04)
if ! sudo /home/$username/pyvenv/bin/python -m ensurepip --upgrade ; then
  echo -e "${start_process_line}\nПроизошла ошибка при установке Pip. (10/${commands})\n${end_process_line}"
  exit 2
fi

#11
if ! sudo -u $username /home/$username/pyvenv/bin/python -m pip install --upgrade pip ; then
  echo -e "${start_process_line}\nПроизошла ошибка при обновлении Pip. (11/${commands})\n${end_process_line}"
  exit 2
fi

#12
if ! sudo chown -hR $username:$username /home/$username/pyvenv ; then
  echo -e "${start_process_line}\nПроизошла ошибка при изменении владельца виртуального окружения. (12/${commands})\n${end_process_line}"
  exit 2
fi


clear
echo -e "$start_process_line\nУстанавливаю FunPayCardinal...\n$end_process_line"


#13
if ! sudo mkdir -p "/home/$username/fpc-install"; then
  echo -e "${start_process_line}\nПроизошла ошибка при создании директории для установки. (13/${commands})\n${end_process_line}"
  exit 2
fi

gh_repo="sidor0912/FunPayCardinal"
LOCATION=$(curl -sS https://api.github.com/repos/$gh_repo/releases/latest | grep "zipball_url" | awk '{ print $2 }' | sed 's/,$//' | sed 's/"//g' )

#14
if ! sudo curl -L $LOCATION -o /home/$username/fpc-install/fpc.zip ; then
  echo -e "${start_process_line}\nПроизошла ошибка при загрузке архива. (14/${commands})\n${end_process_line}"
  exit 2
fi

#15
if ! sudo unzip -o -q "/home/$username/fpc-install/fpc.zip" -d "/home/$username/fpc-install"; then
  echo -e "${start_process_line}\nПроизошла ошибка при распаковке архива. (15/${commands})\n${end_process_line}"
  exit 2
fi

#16
if ! sudo mkdir -p "/home/$username/FunPayCardinal"; then
  echo -e "${start_process_line}\nПроизошла ошибка при создании директории для бота. (16/${commands})\n${end_process_line}"
  exit 2
fi

#17
if ! sudo cp -r /home/$username/fpc-install/*/* /home/$username/FunPayCardinal/; then
    echo -e "${start_process_line}\nПроизошла ошибка при копировании файлов. (17/${commands})\n${end_process_line}"
    exit 2
fi

#18
if ! sudo rm -rf /home/$username/fpc-install ; then
  echo -e "${start_process_line}\nПроизошла ошибка при удалении директории для установки. (18/${commands})\n${end_process_line}"
  exit 2
fi

#19
if ! sudo chown -hR $username:$username /home/$username/FunPayCardinal ; then
  echo -e "${start_process_line}\nПроизошла ошибка при изменении владельца файлов. (19/${commands})\n${end_process_line}"
  exit 2
fi

#20
if ! sudo -u $username /home/$username/pyvenv/bin/pip install -U -r /home/$username/FunPayCardinal/requirements.txt ; then
  echo -e "${start_process_line}\nПроизошла ошибка при установке необходимых Py-пакетов. (20/${commands})\n${end_process_line}"
  exit 2
fi


clear
echo -e "$start_process_line\nСоздаю ссылку на файл фонового процесса...\n$end_process_line"


#21
if ! sudo ln -sf /home/$username/FunPayCardinal/FunPayCardinal@.service /etc/systemd/system/FunPayCardinal@.service ; then
  echo -e "${start_process_line}\nПроизошла ошибка при создании ссылки на файл фонового процесса. (21/${commands})\n${end_process_line}"
  exit 2
fi


clear
echo -e "$start_process_line\nНастраиваю кодировку сервера...\n$end_process_line"


#22
case $distro_version in
  "11" | "12")
    if ! sudo apt install -y locales locales-all ; then
      echo -e "${start_process_line}\nПроизошла ошибка при установке локализаций. (22/${commands})\n${end_process_line}"
      exit 2
    fi
    ;;
  *)
    if ! sudo apt install -y language-pack-en ; then
      echo -e "${start_process_line}\nПроизошла ошибка при установке языковых пакетов. (22/${commands})\n${end_process_line}"
      exit 2
    fi
    ;;
esac

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Настройка FunPay Cardinal${NC}"
echo -e "${BLUE}========================================${NC}"

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
echo -e "${BLUE}========================================${NC}"
cd ..

clear
echo -e $logo
echo -e '\n\n\e[1;91m * GitHub \e[1;96mgithub.com/sidor0912/FunPayCardinal\e[0m'
echo -e '\e[1;91m * Telegram \e[1;96mt.me/funpay_cardinal\e[0m'

echo -e "\n\n\e[1;92m################################################################################"
echo -e "Установка завершена."
echo -e "Запускаю первичную настройку..."
echo -e "################################################################################\e[0m"
sleep 3
clear

CONFIG_FILE="/home/$username/FunPayCardinal/configs/_main.cfg"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Файл конфигурации не найден. Запускаем первичную настройку..."
    sudo -u $username LANG=en_US.utf8 /home/$username/pyvenv/bin/python /home/$username/FunPayCardinal/main.py <&1
else
    echo -ne "\n${RED}Файл конфигурации найден.${RESET} Хотите добавить Telegram прокси? [y/n]:  "
    read edit_config
    case "$edit_config" in
        [yY]|[yY][eE][sS])
            echo -ne "${CYAN}Запускаем редактирование Telegram прокси...${RESET}\n\n"
            sudo -u $username LANG=en_US.utf8 /home/$username/pyvenv/bin/python -W ignore::SyntaxWarning /home/$username/FunPayCardinal/setup_telegram_proxy.py <&1
            ;;
        *)
            echo -ne "${CYAN}Редактирование пропущено.${RESET}"
            ;;
    esac

fi

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Настройка FunPay Cardinal${NC}"
echo -e "${BLUE}========================================${NC}"

cd "$WORK_DIR"

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

# watermark : 🐦 -> (пусто) в секции Other
sed -i '/\[Other\]/,/^\[/ s/watermark : 🐦/watermark : /' configs/_main.cfg

echo -e "${GREEN}✓ _main.cfg обновлен${NC}"

echo -e "${BLUE}========================================${NC}"
sleep 2
cd ..

sudo systemctl restart "FunPayCardinal@$username.service"

clear
echo -e $logo
echo -e '\n\n\e[1;91m * GitHub \e[1;96mgithub.com/sidor0912/FunPayCardinal\e[0m'
echo -e '\e[1;91m * Telegram \e[1;96mt.me/funpay_cardinal\e[0m'

echo -e "\n\n\e[1;92m################################################################################"
echo -e "${RED}!СДЕЛАЙ СКРИНШОТ!${CYAN}!СДЕЛАЙ СКРИНШОТ!${RED}!СДЕЛАЙ СКРИНШОТ!${CYAN}!СДЕЛАЙ СКРИНШОТ!"
echo -e "\nГотово!"
echo -e "FPC запущен как фоновый процесс!"
echo -e "Теперь напиши своему Telegram-боту."
echo -e "${YELLOW}${BOLD}🎯 Установите плагины для FunPay Cardinal!${NC}"
echo -e "\n\e[1;92mДля остановки FPC используй команду \e[93msudo systemctl stop FunPayCardinal@${username}\e[1;92m"
echo -e "Для запуска FPC используй команду \e[93msudo systemctl start FunPayCardinal@${username}\e[1;92m"
echo -e "Для перезапуска FPC используй команду \e[93msudo systemctl restart FunPayCardinal@${username}\e[1;92m"
echo -e "Для просмотра логов используй команду \e[93msudo systemctl status FunPayCardinal@${username} -n100\e[1;92m"
echo -e "Для добавления FPC в автозагрузку используй команду \e[93msudo systemctl enable FunPayCardinal@${username}\e[1;92m"
echo -e "${RED}* Перед добавлением FPC в автозагрузку убедись, что твой бот работает корректно.\e[1;92m"
echo -e "################################################################################\e[0m"

echo -ne "\n\n${CYAN}Сделал скриншот? ${PURPLE_LIGHT}Тогда нажми Enter, чтобы продолжить.${RESET}"
read
clear
