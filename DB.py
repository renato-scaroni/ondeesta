#!/usr/bin/python

""" mailtracker: script de rastreamento automatico de correspondencias """

########################################################################
# Modulo de consistencia de dados                                      #
# Escrito por Renato Scaroni <scaroni@linux.ime.usp.br>                #
########################################################################

########################################################################
# This program is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# This program is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.#
########################################################################


from peewee import *
from hashlib import sha256
from subprocess import call

mailTrackDB = SqliteDatabase('bd.db')

#########################################################
#                       BD Models                       #
#########################################################

class SqliteModel(Model):
    """A base model that will use our Sqlite database"""
    class Meta:
        database = mailTrackDB

class User(SqliteModel):
    username = CharField()
    password = CharField()
    email = CharField()

class Mails(SqliteModel):
    user = ForeignKeyField(User, related_name='mails')
    trackCode = CharField()
    status = CharField()
    packName = CharField()
    
#########################################################
#                  Auxiliary Methods                    #
#########################################################

def showAllMail ():
    for mail in Mails.select():
        print mail.user.username, mail.user.email, mail.packName, mail.trackCode

def encryptPass (p):
    return sha256(p).hexdigest()

def addUser (user, p, e):
    if User.filter(username = user).count() > 0:
        print "usuario ja existente"
    else:
        u = User(username = user, password = encryptPass(p), email = e)
        u.save()

def addMail (user, trackCode, packName):
    if User.filter(username = user).count() == 0:
        print "Usuario inexistente. Favor criar um usuario antes de cadastrar uma encomenda"
        return      
    for u in User.filter(username = user):
        if Mails.filter(trackCode = trackCode).count() > 0:
            print "encomenda ja cadastrada"
        else:
            m = Mails(user = u, trackCode = trackCode, status = "", packName=packName)
            m.save()


def sampleData ():
    addUser ("eu", "teste", "renato.scaroni@gmail.com")
    
    addMail("eu", "RC433652875CN", "R4")

def StartDB ():
    print "Avaliando necessidade de criacao de um banco de dados"
    try:
        User.create_table()
        Mails.create_table()
        print "BD Criado com sucesso"
    except Exception, e:
        print "BD ja criado"

def DeleteDB():
    call(["rm", "-f", "bd.db"])

def main ():
    StartDB()
    y = raw_input("Deseja adicionar ao Bd usuario e encomenda de teste? [y|n]")
    if y == "y":
        sampleData()    
    y = raw_input("Deseja executar query de teste? [y|n]")
    if y == "y":
        showAllMail()
    y = raw_input("Deseja deletar o bd criado de teste? [y|n]")
    if y == "y":
        DeleteDB()

if __name__ == '__main__':
    main()
