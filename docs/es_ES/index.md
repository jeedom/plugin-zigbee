# Complemento de Zigbee

El complemento Zigbee le permite comunicarse con la mayoría de los equipos Zigbee existentes. Se basa en el proyecto (super) Zigpy que es compatible con las siguientes teclas zigbee :

- Deconz. Probado y validado por el equipo de Jeedom. No es necesario tener instalado Deconz
- EZSP (clave basada en un chupset de Silicon Labs). Sometido a prueba por el equipo de Jeedom
- X-bee. No probado por el equipo de Jeedom
- Zigate. No probado por el equipo, marcado como experimental en Zigpy
- ZNP (instrumento de Texas, pila Z 3.X.X). No probado por el equipo, marcado como experimental en Zigpy
- CC (instrumento de Texas, pila Z 1.2.X). No probado por el equipo, marcado como experimental en Zigpy

# Configuración del plugin

Después de instalar el complemento, solo tiene que instalar las dependencias, seleccionar su tipo de clave, el puerto (tenga cuidado solo el tipo de clave deconz admite el puerto en automático) e iniciar el demonio. También puedes elegir el canal para el zigbee.

>**Importante**
>
>Cualquier cambio de canal requiere necesariamente un reinicio del demonio. Un cambio de canal también puede requerir la reincorporación de cierto módulo


# Inclusión del módulo

La inclusión es la parte más difícil en Zigbee. Aunque simple, la operación a menudo se realiza varias veces. En el lado del complemento, es fácil simplemente hacer clic en el botón "Incluir modo", una vez hecho esto, tiene 3 minutos para incluir su equipo.

Cambios de lado del equipo en función del módulo, es necesario consultar la documentación de este cada vez.

>**Importante**
>
>No olvide hacer un reset del módulo antes de cualquier inclusión

# Equipement

Una vez incluido, Jeedom debe reconocer automáticamente su módulo (si este no es el caso, consulte el siguiente capítulo) y por lo tanto crear los comandos que vayan bien. Tenga en cuenta que debido a un error en cierto firmware (Ikea, Sonoff ...) a veces es necesario elegir el tipo de módulo directamente en la lista "Equipo" y luego guardar para tener los comandos correctos.

Tienes en la pestaña de equipos los siguientes parámetros :

- **Nombre del equipo zigbee** : nombre de su equipo Zigbee
- **Identificación** : identificadores únicos del equipo, incluso durante una reincorporación (o incluso si cambia el tipo de llave zigbee)
- **Activar**
- **Visible**
- **Objeto padre**
- **Despacho**
- **Categoría**
- **No espere el regreso de ejecución de órdenes (más rápido pero menos confiable)** : no espere a que la validación de la clave diga que el comando se ha ejecutado. Hace que la mano sea más rápida pero no garantiza que todo haya ido bien

En la pestaña de comandos encontrarás los comandos de tu módulo (si ha sido reconocido)

## Pedido de expertos

Para los expertos, así es como funcionan los controles :

- ``attributes::ENDPOINT::CLUSTER_TYPE::CLUSTER::ATTRIBUT::VALUE``, le permite escribir el valor de un atributo (tenga cuidado de que no todos los atributos se pueden cambiar) con :
  - ``ENDPOINT`` : número de punto final
  - ``CLUSTER_TYPE`` : tipo de clúster (IN o OUT)
  - ``CLUSTER`` : número de grupo
  - ``ATTRIBUT`` : número de atributo
  - ``VALUE`` : valor para escribir
Ejemplo : ``attributes::1::in::513::18::#slider#*100``, aquí escribiremos el atributo en el punto final 1, clúster entrante (``in``) 513, atributo 18 con el valor de la ``slider*10``
- ``ENDPOINT::CLUSTER:COMMAND::PARAMS``, permite ejecutar un comando del servidor, con :
  - ``ENDPOINT`` : número de punto final
  - ``CLUSTER`` : nombre del clúster
  - ``COMMAND`` : Nombre de la orden
  - ``PARAMS`` parámetro en el orden correcto separado por ::
Ejemplo : ``1::on_off::on``, aquí ejecutamos el comando ``on`` en el punto final 1 del clúster ``on_off`` sin parámetros
Ejemplo : ``1::level::move_to_level::#slider#::0``, aquí ejecutamos el comando ``move_to_level`` en el punto final 1 del clúster ``level`` Con parámetros ``#slider#`` y ``0``

# Mi módulo no es reconocido

Si su módulo no es reconocido por jeedom (sin comando) pero está incluido, debe pedirle al equipo de Jeedom que lo agregue.

>**Importante**
>
>El equipo de Jeedom se reserva el derecho de rechazar cualquier solicitud de integración, siempre es mejor tomar un módulo ya compatible

Para ello, debe proporcionar los siguientes elementos (cualquier solicitud incompleta será rechazada sin una respuesta del equipo de Jeedom) :

- Proporcione el modelo exacto de su módulo (con un enlace a la página de ventas)
- En la página del equipo, haga clic en configuración, luego en la pestaña "Información sin procesar" y envíe el contenido al equipo de Jeedom
- Ponga el daemon en debug (y reinícielo), realice acciones en el equipo (si es un sensor de temperatura, varíe la temperatura por ejemplo, si es una válvula, varíe el setpoint ...) y envíe el registro de depuración de zigbee (tenga cuidado de tomar el zigbee y no el zigbeed)

# Touchlink

Touchlink o Lightlink es una parte especial del Zigbee que le permite enviar órdenes de gestión a un módulo si está muy cerca de él (50cm). Se usa por ejemplo para hacer un reset en las bombillas que no tienen botón.

Esto por lo tanto concierne a todo lo que sean bombillas Zigbee tipo Philips Hue, Ikea, Osram, Icasa ... etc. El principio es muy sencillo para poder asociar este tipo de módulo con una red zigbee, primero debes hacer un reset. Luego, al reiniciar, el módulo intentará asociarse automáticamente con la primera red Zigbee abierta que encuentre.

## Restablecer en Touchlink

Esta es la parte complicada (como siempre en Zigbee lo más difícil es el reinicio / asociación). Varios métodos :

- Haga el encendido / apagado 5 o 6 veces rápidamente, la bombilla normalmente parpadea rápidamente al final para indicar que está bien (rara vez funciona)
- Utilice un control remoto zigbee y
  - presione al mismo tiempo el botón de ENCENDIDO y APAGADO durante 5 a 10 segundos cerca de la bombilla encendida (tenga cuidado con ciertas bombillas, a veces tiene que apagar / encender la bombilla justo antes) para los controles remotos de Philips hue
  - presione el botón de reinicio (al lado de la batería) durante 5 a 10 segundos cerca de la bombilla encendida (tenga cuidado con ciertas bombillas, a veces tiene que apagar / encender la bombilla justo antes) para los controles remotos de Ikea
- Para las bombillas de tono, también puede incluirlas en el puente de tono y luego quitarlas de él

# FAQ

>**LQI o RSSI es N / A
>
>Normalmente es luego de un reinicio de las redes Zigbee los valores se vacían, es necesario esperar a que el módulo se vuelva a unir para que los valores regresen
