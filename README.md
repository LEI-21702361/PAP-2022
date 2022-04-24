# PAP-2022

## Instruções de instalação
Ambiente de desenvolvimento - [Ubuntu 20.04](https://releases.ubuntu.com/20.04/)  
  
Para instalar o simulador de ndn é necessário seguir as instruções oficiais que se encontram no link [https://ndnsim.net/2.1/getting-started.html](https://ndnsim.net/2.1/getting-started.html).  
Apesar da simulação ser executada dentro do ns3-gym e não no ndnSIM, o visualizador de simulações (PyViz) só funciona corretamente dentro do ndnSIM
e portanto é aconcelhada a instalação do ndnSIM para se visualizar a simulação em modo gráfico.
  
Para instalar a framework de inteligência artificial, basta seguir as instruções oficiais que se encontram no link [https://apps.nsnam.org/app/ns3-gym/](https://apps.nsnam.org/app/ns3-gym/)  
## Correr a simulação e o agente
Para correr o projeto, basta colocar os 2 ficheiros que acompanham este relatório na pasta **“scratch” do ns3-gym**, um será um ficheiro com a extensão **“.cc”** 
que será o da simulação VANET, e outro será outro ficheiro terá a extensão **“.py”** que será o agente que irá receber os dados da simulação.  
Depois será necessário correr dois terminais, um para iniciar a simulação e outro para correr o agente conforme indicado 
na secção 7 do guia de instalação do ns3-gym.
