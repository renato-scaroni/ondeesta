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

welcome = "\nBem-vindo ao console de gerenciamento de usuarios do 'Onde esta - mailtracker' \n"
welcome += "Para mais informacoes de uso digite help\n"

helpmsg = "Comandos validos:"
helpmsg += ""
helpmsg += "addUser - adiciona usuarios"
helpmsg += "help - lista comandos validos"
helpmsg += "quit - encerra execucao"


class CMDParser(cmd.Cmd):
    """Simple command processor example."""
    prompt = ">> "

    def cmdloop(self, intro=welcome):
        return cmd.Cmd.cmdloop(self, intro)

    def specificHelp(cmd):

    def do_help(self, rest):
        if rest:
            specificHelp(rest.split(" "))
    
    def quit():
        print "Ate logo!\n"
        return True

    def do_quit(self, line):
        quit()

    def do_EOF(self, line):
        quit()

def main ():
    CMDParser().cmdloop()

if __name__ == '__main__':
    main()