#!/bin/bash
supportversion=14
server_port=1194


init()
{	
	version=`lsb_release -a|grep -i "release"|awk -F ":" '{print $2}'|sed  's/^[ \t]//g'|sed 's/[ ]*$//g'|cut -d "." -f 1`
	if [ ${version} -lt ${supportversion} ];then
		echo "[ERROR]The application does support ubunut ${version},The earlist vesion is Ubuntu${supportversion} ."
		exit 1
	fi
	currentuser=`whoami`
	if [ "s${currentuser}" == "sroot" ];then
		echo "[INFO]Current user : ${currentuser}"
	else
		echo "The currentuser is ： ${currentuser} ,please change user to root to run this script . "
		exit 1
	fi	
}

addUser()
{
	username=$1
	password=$2
	cat /etc/group|awk -F ":" '{print $1}'|grep -w "admin"
	if [ $? -eq 1 ];then
		groupadd admin
	fi
	useradd -m -s /bin/bash -G admin,sudo ${username}
	echo ${username}:${password}|chpasswd
	if [ $? -ne 0 ];then
		echo "[ERROR]Add user account failed .."
		exit 1
	fi
}

isUserExist()
{
	user=$1
	cat /etc/passwd|awk -F ":" '{print $1}'|grep -w ${user}
	if [ $? -eq 0 ];then
		echo "[ERROR]${user} has already existed!"
		exit 1
	fi
}

installPip()
{
	apt-get update
	which pip
	if [ $? -eq 1 ];then
		ehco "[INFO]pip is not installed in this OS .."
		echo "[INFO]Install pip ,please wait ...."
		apt-get install python-pip -y -q
	fi
	pip -V
	if [ $? -eq 0 ];then
		echo "[INFO]Instaln pip successfully ! "
	else
		echo "[ERROR]Install pip failed ...."
		exit 1
	fi
}
installshadowsocks()
{
	pip list|grep "shadowsocks"
	if [ $? -eq 1 ];then
		echo "[INFO]Start to install shadowsocks ....."
		pip install shadowsocks -q
	fi
	pip list |grep shadowsocks
	if [ $? -eq 0 ];then 
		echo "[INFO]Install shadowsocks successfully !"
	else 
		echo "[ERROR]Install shadowsocks failed ..."
		exit 1
	fi
}
touchCfgFile()
{
	if [ ! -d /etc/shadowsocks ];then
		echo "[INFO]/etc/shadowsocks does existed .make it ..."
		mkdir /etc/shadowsocks -p
	fi
	if [ ! -f /etc/shadowsocks/config.json ];then
		echo "[INFO]/etc/shadowsocks/config.json does existed ,touch it ...."
		touch /etc/shadowsocks/config.json
	else
		echo ">/etc/shadowsocks/config.json"
	fi		
}
writeConfig()
{
	password=$1
	file="/etc/shadowsocks/config.json"
	echo "{">>${file}
	echo "  \"server\":\"0.0.0.0\", ">>${file}
	echo "  \"server_port\":${server_port},">>${file}
	echo "  \"local_address\":\"127.0.0.1\",">>${file}
	echo "  \"local_port\":1080,">>${file}
	echo "  \"password\":\"${shadowsocks_password}\", ">>${file}
	echo "  \"timeout\":300, ">>${file}
	echo "  \"method\":\"aes-256-cfb\",">>${file}
	echo "  \"fast_open\":false,">>${file}
	echo "  \"workers\": 1 ">>${file}
	echo "}">>${file}
}
startServer()
{
	ssserver -c /etc/shadowsocks/config.json -d start
}
main()
{
	init
	read -p "please input username:" username
	isUserExist ${username}
	read -p "please input password:" password
	addUser ${username} ${password}
	installPip
	installshadowsocks
	touchCfgFile
	read -p "Input shadowsocks password:" shadowsocks_password
	writeConfig ${shadowsocks_password}
	startServer
}
main $@
