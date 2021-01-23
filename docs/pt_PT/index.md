# Plugin Zigbee

O plugin Zigbee permite que você se comunique com a maioria dos equipamentos Zigbee existentes. É baseado no (super) projeto Zigpy, que é compatível com as seguintes chaves zigbee :

- Deconz. Testado e validado pela equipe Jeedom. Não é necessário ter o Deconz instalado
- EZSP (chave baseada em um chupset da Silicon Labs). Em teste pela equipe Jeedom
- X-bee. Não testado pela equipe Jeedom
- Zigate. Não testado pela equipe, marcado em experimental no Zigpy
- ZNP (Texas Instrument, Z-stack 3.X.X). Não testado pela equipe, marcado em experimental no Zigpy
- CC (Texas Instrument, Z-stack 1.2.X). Não testado pela equipe, marcado em experimental no Zigpy

>**IMPORTANTE**
>
>O plugin não é compatível com as lâmpadas antigas que usam o Zigbee Lightlink digite o primeiro PhilipsHue. Para ter certeza da compatibilidade não esqueça de consultar o site da [Compatibilidade Jeedom](https://compatibility.jeedom.com)

# Configuração do plugin

Depois de instalar o plugin, você só precisa instalar as dependências, selecionar seu tipo de chave, a porta (cuidado apenas o tipo de chave deconz suporta a porta em auto) e iniciar o daemon. Você também pode escolher o canal para o zigbee.

>**IMPORTANTE**
>
>Qualquer mudança de canal requer necessariamente a reinicialização do daemon. Uma mudança de canal também pode exigir a reinclusão de certo módulo


# Inclusão de Módulo

Inclusão é a parte mais difícil no Zigbee. Embora simples, a operação costuma ser feita várias vezes. Do lado do plugin é fácil, basta clicar no botão "Modo de inclusão", uma vez feito você tem 3 minutos para incluir seu equipamento.

Mudanças de lado do equipamento dependendo do módulo, é necessário consultar a documentação deste cada vez.

>**IMPORTANTE**
>
>Não se esqueça de fazer um reset do módulo antes de qualquer inclusão

# Equipement

Uma vez incluído, o Jeedom deve reconhecer automaticamente o seu módulo (se este não for o caso, consulte o próximo capítulo) e, portanto, criar os comandos que funcionam bem. Observe que devido a um bug em certo firmware (Ikea, Sonoff ...) às vezes é necessário escolher o tipo de módulo diretamente na lista "Equipamentos" e salvar para ter os comandos corretos.

Você tem na guia de equipamentos os seguintes parâmetros :

- **Nome do equipamento Zigbee** : nome do seu equipamento Zigbee
- **ID** : identificadores únicos do equipamento, mesmo durante uma reinclusão (ou mesmo se você alterar o tipo de chave zigbee)
- **Ativar**
- **Visivél**
- **Objeto pai**
- **Escritório**
- **Categoria**
- **Não espere o retorno da execução dos pedidos (mais rápido, mas menos confiável)** : não espere pela validação da chave para dizer que o comando foi executado. Torna a mão mais rápida, mas não garante que tudo correu bem

Na página de comandos iráencontrar os comandos do seu módulo (se tiver sido reconhecido)

## Pedido para especialistas

Para os especialistas, aqui está como funcionam os controles :

- ``attributes::ENDPOINT::CLUSTER_TYPE::CLUSTER::ATTRIBUT::VALUE``, permite que você escreva o valor de um atributo (tenha cuidado, nem todos os atributos podem ser alterados) com :
  - ``ENDPOINT`` : número do endpoint
  - ``CLUSTER_TYPE`` : tipo de cluster (IN ou OUT)
  - ``CLUSTER`` : número do cluster
  - ``ATTRIBUT`` : número do atributo
  - ``VALUE`` : valor para escrever
Exemplo : ``attributes::1::in::513::18::#slider#*100``, aqui vamos escrever o atributo no ponto de extremidade 1, cluster de entrada (``in``) 513, atributo 18 com o valor do ``slider*10``
- ``ENDPOINT::CLUSTER:COMMAND::PARAMS``, permite executar um comando de servidor, com :
  - ``ENDPOINT`` : número do endpoint
  - ``CLUSTER`` : nome do cluster
  - ``COMMAND`` : nome do comando
  - ``PARAMS`` parâmetro na ordem correta, separado por ::
Exemplo : ``1::on_off::on``, aqui nós executamos o comando ``on`` no ponto final 1 do cluster ``on_off`` sem parâmetros
Exemplo : ``1::level::move_to_level::#slider#::0``, aqui nós executamos o comando ``move_to_level`` no ponto final 1 do cluster ``level`` com os parâmetros ``#slider#`` e ``0``

# Meu módulo não é reconhecido

Se o seu módulo não for reconhecido pelo jeedom (sem comando), mas incluído, você deve pedir à equipe do Jeedom para adicioná-lo.

>**IMPORTANTE**
>
>A equipa Jeedom reserva-se o direito de recusar qualquer pedido de integração, é sempre melhor levar um módulo já compatível

Para isso, você deve fornecer os seguintes elementos (qualquer solicitação incompleta será recusada sem uma resposta da equipe Jeedom) :

- Forneça o modelo exato do seu módulo (com um link para a página de vendas)
- Na página do equipamento, clique em configuração a seguir na aba "Informação bruta" e envie o conteúdo para a equipe Jeedom
- Coloque o daemon em debug (e reinicie), faça ações no equipamento (se for um sensor de temperatura, varie a temperatura por exemplo, se for uma válvula, varie o setpoint ...) e envie o registro de depuração do zigbee (tome cuidado para pegar o zigbee e não o zigbeed)

# Touchlink

Touchlink ou Lightlink é uma parte especial do Zigbee que permite enviar ordens de gerenciamento para um módulo se você estiver muito perto dele (50cm). É usado, por exemplo, para fazer um reset nas lâmpadas que não têm botão.

Portanto, isso diz respeito a tudo o que é lâmpadas Zigbee do tipo Philips Hue, Ikea, Osram, Icasa ... e assim por diante. O princípio é muito simples para poder associar este tipo de módulo a uma rede zigbee, você deve primeiro fazer um reset. Então, ao reiniciar, o módulo tentará automaticamente se associar à primeira rede Zigbee aberta que encontrar.

## Redefinir no Touchlink

Esta é a parte complicada (como sempre no Zigbee o mais difícil é o reset / associação). Vários métodos :

- Ligue / desligue 5 ou 6 vezes rapidamente, a lâmpada normalmente pisca rapidamente no final para sinalizar que está boa (raramente funciona)
- Use um controle remoto zigbee e
  - pressione ao mesmo tempo o botão LIGAR e DESLIGAR por 5 a 10 segundos perto da lâmpada elétrica (cuidado com algumas lâmpadas, às vezes você precisa desligar / ligar a lâmpada imediatamente antes) para os controles remotos Philips hue
  - pressione o botão de reinicialização (ao lado da bateria) por 5 a 10 segundos próximo à lâmpada elétrica (cuidado com certas lâmpadas, às vezes você precisa ligar / desligar a lâmpada um pouco antes) para os controles remotos Ikea
- Para os bulbos de matiz, você também pode incluí-los na ponte matiz e removê-los

# FAQ

>**LQI ou RSSI é N / A
>
>Normalmente é após um reinício das redes Zigbee que os valores são esvaziados, é necessário aguardar que o módulo recomunique para que os valores retornem

>**Tenho problemas de inclusão ou erros nos registros de tipo ``TXStatus.MAC_CHANNEL_ACCESS_FAILURE``**
>
>Tente remover a extensão USB se você tiver uma ou altere-a ou coloque uma se você não tiver