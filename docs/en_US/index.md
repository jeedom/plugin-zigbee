# Zigbee plugin

The Zigbee plugin allows you to communicate with most existing Zigbee equipment. It is based on the (super) Zigpy project which is compatible with the following zigbee keys :

- Deconz. Tested and validated by the Jeedom team. There is no need to have Deconz installed
- EZSP (key based on a Silicon Labs chupset). Under test by the Jeedom team
- X-bee. Not tested by the Jeedom team
- Zigate. Not tested by the team, marked in experimental at Zigpy
- ZNP (Texas Instrument, Z-stack 3.X.X). Not tested by the team, marked in experimental at Zigpy
- CC (Texas Instrument, Z-stack 1.2.X). Not tested by the team, marked in experimental at Zigpy

# Plugin configuration

After installing the plugin, you just have to install the dependencies, select your type of key, the port (be careful only the type of deconz key supports the port in auto) and start the daemon. You can also choose the channel for the zigbee.

>**Important**
>
>Any change of channel necessarily requires a restart of the daemon. A change of channel may also require reinclusion of certain modulus


# Module inclusion

Inclusion is the hardest part in Zigbee. Although simple, the operation is often done several times. On the plugin side, it's easy, just click on the "Include mode" button, once done you have 3 minutes to include your equipment.

Equipment side changes depending on the module, it is necessary to refer to the documentation of this one each time.

>**Important**
>
>Do not forget to do a reset of the module before any inclusion

# Equipement

Once included Jeedom must automatically recognize your module (if this is not the case see next chapter) and therefore create the commands that go well. Note that due to a bug in certain firmware (Ikea, Sonoff ...) it is sometimes necessary to choose the type of module directly in the "Equipment" list then to save to have the correct commands.

You have in the equipment tab the following parameters :

- **Zigbee equipment name** : name of your Zigbee equipment
- **ID** : unique identifiers of the equipment, even during a reinclusion (or even if you change the type of zigbee key)
- **Activate**
- **Visible**
- **Parent object**
- **Office**
- **Category**
- **Do not wait for the return of execution of orders (faster but less reliable)** : do not wait for the key validation to say that the command has been executed. It makes the hand faster but does not guarantee that everything went well

In the command tab you will find the commands of your module (if it has been recognized)

## Order for experts

For the experts here is how the controls work :

- ``attributes::ENDPOINT::CLUSTER_TYPE::CLUSTER::ATTRIBUT::VALUE``, allows you to write the value of an attribute (be careful not all attributes can be changed) with :
  - ``ENDPOINT`` : endpoint number
  - ``CLUSTER_TYPE`` : cluster type (IN or OUT)
  - ``CLUSTER`` : cluster number
  - ``ATTRIBUT`` : attribute number
  - ``VALUE`` : value to write
Example : ``attributes::1::in::513::18::#slider#*100``, here we will write the attribute in endpoint 1, incoming cluster (``in``) 513, attribute 18 with the value of the ``slider*10``
- ``ENDPOINT::CLUSTER:COMMAND::PARAMS``, allows to execute a server command, with :
  - ``ENDPOINT`` : endpoint number
  - ``CLUSTER`` : cluster name
  - ``COMMAND`` : Name of the command
  - ``PARAMS`` parameter in the correct order separated by ::
Example : ``1::on_off::on``, here we execute the command ``on`` on endpoint 1 of the cluster ``on_off`` without parameters
Example : ``1::level::move_to_level::#slider#::0``, here we execute the command ``move_to_level`` on endpoint 1 of the cluster ``level`` With parameters ``#slider#`` and ``0``

# My module is not recognized

If your module is not recognized by jeedom (no command) but included then you must ask the Jeedom team to add it.

>**Important**
>
>The Jeedom team reserves the right to refuse any integration request it is always better to take an already compatible module

For this, you must provide the following elements (any incomplete request will be refused without a response from the Jeedom team) :

- Give the exact model of your module (with a link to the sales page)
- On the equipment page, click on configuration then tab "Raw information" and send the content to the Jeedom team
- Put the daemon in debug (and restart it), make actions on the equipment (if it is a temperature sensor, vary the temperature for example, if it is a valve, vary the setpoint ...) and send the zigbee debug log (be careful to take the zigbee and not the zigbeed)

# Touchlink

Touchlink or Lightlink is a special part of the Zigbee which allows you to send management orders to a module if you are very close to it (50cm). It is used for example to make a reset on the bulbs that do not have a button.

This therefore concerns all that is Zigbee bulbs type Philips Hue, Ikea, Osram, Icasa ... and so on. The principle is very simple to be able to associate this type of module with a zigbee network, you must first do a reset. Then when restarting the module will automatically try to associate with the first open Zigbee network it finds.

## Reset in Touchlink

This is the complicated part (as always in Zigbee the hardest is the reset / association). Several methods :

- Do the on / off 5 or 6 times quickly, the bulb normally flashes quickly at the end to signal that it is good (rarely works)
- Use a zigbee remote control and
  - press at the same time the ON and OFF button for 5 to 10 seconds near the powered bulb (beware of certain bulbs, you sometimes have to turn off / on the bulb just before) for Philips hue remote controls
  - press the reset button (next to the battery) for 5 to 10 seconds near the powered bulb (beware of certain bulbs, you sometimes have to turn the bulb off / on just before) for Ikea remote controls
- For the hue bulbs you can also include them on the hue bridge then remove them from it

# FAQ

>**LQI or RSSI is N / A
>
>It is normally following a restart of the Zigbee networks the values are emptied, it is necessary to wait for the module to recomunique so that the values return
