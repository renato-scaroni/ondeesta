#!/usr/bin/env python

""" mailtracker: script de rastreamento automatico de correspondencias """

########################################################################
# Console de gerenciamento de usuarios e encomendas                    #
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

# Import notification module
import mail

# Import shell module
import cmd

# Import getpassword
from getpass import *

# Import DB
from DB import *

welcome = "\nBem-vindo ao console de gerenciamento de usuarios do 'Onde esta - mailtracker' \n"
welcome += "Para mais informacoes de uso digite help\n"

helpmsg = "\nComandos validos:\n"
helpmsg += "addMail - adiciona correspondecia a um usuario logado\n"
helpmsg += "lsMail - lista todas as correspondecias de um usuario logado\n"
helpmsg += "rmMail - deleta correspondecia escolhida de um usuario logado\n"
helpmsg += "updateStatus (u) - atualiza o status de todas as correspondecias\n"
helpmsg += "addUser - adiciona usuarios\n"
helpmsg += "help (h) - lista comandos validos\n"
helpmsg += "quit (q) - encerra execucao\n"

session = None

class Session(object):
    """Session"""
    login = ""
    ms = []

    def __init__(self, lg, p):
        super(Session, self).__init__()
        self.login = lg
        self.p = p

class CMDParser(cmd.Cmd):
    """Simple command processor example."""
    prompt = ">> "

    def cmdloop(self, intro=welcome):
        return cmd.Cmd.cmdloop(self, intro)

    # um dia impolementar essa porcaria
    def specificHelp(cmd):
        pass

    def do_addMail(self, param):
        par = param.split(" ")
        if len(par) == 2:
            if len(par[1]) == 14 or len(par[1]) == 15 or len(par[1]) == 13:
                addMail(session.login, par[1], par[0])
                par.pop(0)
                par.pop(0)
            else:
                print "digite um trackcode valido, "+par[1]+" nao parece ser um trackcode"
        elif len(par) > 2:
            print "digite uma encomenda por vez"
        else:
            print "numero invalido de argumentos"

    def do_lsMail(self, param):
        if session.ms == []:
            ms = lsMailUser(session.login)
        else:
            i = 1
            for m in ms:
                print i, m.packName, m.trackCode, m.status 
                i += 1

    def do_rmMail(self, param):
        if session.ms == []:
            ms = lsMailUser(session.login)
        else:
            i = 1
            for m in ms:
                print i, m.packName, m.trackCode, m.status 
                i += 1
        d = int(raw_input("Qual enomenda deseja deletar? "))
        rmSingleMail(ms[d-1].trackCode)
        print "encomenda deletada"

        
    def do_u(self, param):
        mail.UpdateAndNotifyUser(session.login)


    def do_updateStatus(self, param):
        mail.UpdateAndNotifyUser(session.login)

    def help(self, param):
        if param:
            specificHelp(param.split(" "))
        else:
            print helpmsg

    def do_h(self, rest):
        self.help(rest)
                
    def do_help(self, rest):
        self.help(rest)        

    def do_quit(self, line):
        print "\nAte logo!\n"
        return True
    
    def do_EOF(self, line):
        print "\n\nAte logo!\n"
        return True
        
def main ():
    global session
    login = raw_input("Por favor, informe um usuario e senha validos\nLogin: ")
    p = getpass()
    while checkUser(login, p) == "NOK":
        login = raw_input("senha ou usuario incorretos, informe um usuario e senha validos\nLogin: ")
        p = getpass()

    session = Session(login, p)
    CMDParser().cmdloop()
    

if __name__ == '__main__':
    main()
