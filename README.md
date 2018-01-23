##Proyeto Enterprise 
================================

Frontend  @devtechmx
Backend   @xtornasol512


##Instrucciones
=====================


1. Instalar Dependencias
``
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install mysql-server mysql-client
$ mysql_secure_installation
$ sudo apt-get install libmysqlclient-dev python-dev
$ sudo pip install mysql-python

``
2. Crear Base de Datos y Usuario
``
echo "CREATE DATABASE DATABASENAME;" | mysql -u root -p
echo "CREATE USER 'DATABASEUSER'@'localhost' IDENTIFIED BY 'PASSWORD';" | mysql -u root -p
echo "GRANT ALL PRIVILEGES ON DATABASENAME.* TO 'DATABASEUSER'@'localhost';" | mysql -u root -p
echo "FLUSH PRIVILEGES;" | mysql -u root -p
``
