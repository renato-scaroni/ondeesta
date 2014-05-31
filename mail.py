#!/usr/bin/env python

""" mailtracker: script de rastreamento automatico de correspondencias """

########################################################################
# Modulo de consulta e notificacao                                     #
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

########################################################################
# Agradecimentos a Leandro T. de Souza por escrever a API de           #
# rastreamento de encomendas para o correio brasileiro em python e     #
# torna-la disponivel a comunidade como software livre                 #
########################################################################

# Import smtplib for the mail sending function
import smtplib

# Import tracking library
from correios import Correios

# Import the email modules we'll need
from email.mime.text import MIMEText

# Import Database module
from DB import *

def CheckStatusUpdate(encomenda, status):
    print "obtendo status atual"
    newstatus = encomenda.status[-1].situacao

    newstatus = newstatus.decode("windows-1252")
    newstatus = newstatus.encode("utf-8")
    status = status.decode("windows-1252")
    status = status.encode("utf-8")

    print "comparando status"
    if(status == newstatus):
        print "status inalterado"
        return None
    return newstatus

def NotifyStatusUpdate(encomenda, newstatus, mail):
    print "atualizando status"

    s = "Encomenda: {0} \nData da atualizacao: {1} ".format (encomenda.identificador, encomenda.status[-1].atualizacao.date())
    s += "\nHora da atualizacao: {0}".format(encomenda.status[-1].atualizacao.time ())
    s += "\nPais: {0} \nSituacao: {1}".format(encomenda.status[-1].pais, newstatus) 
    s += "\nPais: {0}".format(encomenda.status[-1].observacao)
    print s

    print "salvando novo status"

    mail.status = newstatus
    mail.save()

    print"gerando e-mail de notificacao"

    msg = MIMEText(s)
    msg['Subject'] = "Onde esta o " + mail.packName + "?"

    print "iniciando conexao"

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("", "")
    s.sendmail("", mail.user.email, msg.as_string())
    s.quit()

    print "e-mail enviado!"

def UpdateAndNotify(mail):
    print mail.user.username, mail.packName, mail.trackCode
    print "buscando encomenda"
    encomenda = Correios.get_encomenda (mail.trackCode)
    print "obtendo status anterior"
    newstatus = CheckStatusUpdate(encomenda, mail.status)
    if newstatus != None:
        NotifyStatusUpdate(encomenda, newstatus, mail)

def UpdateAndNotifyAll():
    mailTrackDB = SqliteDatabase('bd.db')
    mailTrackDB.connect()
    for mail in Mails.select():
        UpdateAndNotify(mail)
        
def main ():
    UpdateAndNotifyAll()

if __name__ == '__main__':
    main()