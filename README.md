# CCPBL2
Repositório destinado ao problema 2 da disciplina de Concorrência e Conectividade

## Requisitos

- PHP (pode ser instalado via xampp) para executar os dispositivos ou pode ser utilizado Docker, utilizando o arquivo ``Dockerfile`` na pasta raiz do projeto para criar a imagem, essa imagem irá executar os dispositivos.
- É necessário ter o Python 3.7+ instalado com a biblioteca <a link=https://pypi.org/project/paho-mqtt/>paho-mqtt</a>, o Framework Flask, a extensão flask_cors e flask_restful.

## Organização das pastas

- O projeto está divido em 3 pastas e em 3 arquivos na pasta raiz.
  - **api**
    - Essa pasta contém o arquivo do servidor, sendo recomendável criar um novo ambiente python para instalar as dependências da API, que incluem: o <a link=https://pypi.org/project/paho-mqtt/>paho-mqtt</a>, o Framework Flask, as extensões flask_cors e flask_restful.
  - **model**
    - Essa pasta possui o código em php do dispositivo e as suas duas dependências que são ``Sensor.php`` e ``Patient.php``.
  - **vendor**
    - Essa pasta contém as dependências php para executar o dispositivo, ela poderia ser instalada via composer utilizando ``composer install``, porém, como é apenas uma dependência (php-mqtt), ela pode ser utilizada do jeito como está.
  - **Fog.py**
    - Esse arquivo contém o código da classe que representa a Fog do sistema e a classe das threads que a Fog gera.
  - **quicksort.py**
    - Esse arquivo contém o código que faz a ordenação dos dados utilizando o algoritmo *Quicksort*.
  - **Dockerfile**
    - Esse arquivo contém as instruções para construção da imagem *Docker*, caso seja preferível executar os dispositivos em um container *Docker*.

## Como Executar

- Aqui será apresentado o passo a passo recomendável para executar o projeto.

  - Passo 1: Vá no arquivo de Servidor e altere na variável ``fogsAddr`` os enedereços dos *Broker's* que estão sendo utilizados e a porta utilizada, desse modo a API irá requisitar em todos eles os dados dos pacientes.

  - Passo 2: Abra o git bash e, no diretório raiz do projeto, digite:

    ``export FLASK_APP=api/Servidor``

    após isso, digite:

    ``flask run``

    Então a API estará já disponível.

    OBS.: Caso queria escolher em que endereço deseja executar a API, siga o modelo:

    ``flask run --host=0.0.0.0``

  - Passo 3: Vá ao arquivo ``Fog.py`` e altere as variáveis ``BROKER_ADDR0`` e ``BROKER_ADDR1`` para os endereços corretos e a ``PORT_BROKER`` para a porta correta dos *Broker's* utilizados.

  - Passo 4: Execute o arquivo ``Fog.py`` e, no terminal será solicitado um input, digite 0 e confirme para indicar que aquela *Fog* está conectada ao *Broker* 0, e, em outro terminal, faça a mesma coisa digitando 1, que indica o *Broker* 1. 

    A partir daí as *Fog's* estão prontas para receber os pacientes.

  **IMPORTANTE**: antes de seguir para o próximo passo, vá ao arquivo ``PatientClient.php`` e altere as informações de endereço e porta no construtor da classe ``PatientClient``

  - Passo 5: Se decidir utilizar *Docker* siga as instruções neste passo, se não pule para o passo 6.

    Para executar os pacientes na quantidade que desejar utilizando o *Docker* vá no terminal na pasta raiz do projeto e construa a imagem digitando:

    **IMPORTANTE**: antes de criar a imagem vá ao arquivo ``PatientClient.php`` e altere as informações de endereço e porta no construtor da classe ``PatientClient``

    ``docker build -t nome_da_imagem .``

    A imagem está criada, agora crie um swarm:

    ``docker swarm init``

    O swarm está criado, agora crie um serviço neste swarm:

    ``docker service create nome_da_imagem``

    Agora veja o o ID do serviço criado:

    ``docker service ls``

    Agora copie o ID do serviço e escolha a quantidade de réplicas que deseja criar desse serviço, que é quantos dispositivos você deseja executar:

    ``docker service scale id_do_serviço=quantidade``

    Desse modo, você já estará executando toda essa quantidade de dispositivos, conectados as suas *Fog's* e as requisições já podem ser feitas através da API.

  - Passo 6: Abra o terminal na pasta raiz do projeto e digite:

    *php model/PatientClient.php*

    Então o seu dispositivo do paciente estará executando e conectado a alguma das *Fog's*, podendo ser requisitado pela API.

  - Extra: Para encerrar o serviço criado no *Docker* e finalizar a swarm siga as instruções:

    ``docker service rm id_do_serviço``

    ``docker swarm leave --force``

### Sobre as rotas

- Existem duas rotas na API:
  - Rota 1: /patients/n
    - n é o número de pacientes que deseja recuperar da API, este número é decidido pelo usuário na interface do projeto
  - Rota 2: /patient/id
    - id é o ID do paciente que deseja recuperar da API, essa rota é utilizada internamente para recuperar apenas um paciente quando o mesmo é fixado pelo usuário.
