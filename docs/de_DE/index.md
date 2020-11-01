# ZigBee Plugin

Mit dem ZigBee-Plugin können Sie mit den meisten vorhandenen ZigBee-Geräten kommunizieren. Es basiert auf dem (Super-) Zigpy-Projekt, das mit den folgenden ZigBee-Schlüsseln kompatibel ist :

- Deconz. Vom Jeedom-Team getestet und validiert. Deconz muss nicht installiert sein
- EZSP (Schlüssel basierend auf einem Silicon Labs-Chupset). Wird vom Jeedom-Team getestet
- X-bee. Nicht vom Jeedom-Team getestet
- Zigate. Nicht vom Team getestet, experimentell bei Zigpy markiert
- ZNP (Texas Instrument, Z-Stapel 3.X.X). Nicht vom Team getestet, experimentell bei Zigpy markiert
- CC (Texas Instrument, Z-Stapel 1.2.X). Nicht vom Team getestet, experimentell bei Zigpy markiert

>**Wichtig**
>
>Das Plugin ist nicht kompatibel mit den alten Lampen, die den Zigbee Lightlink-Typ 1st PhilipsHue verwenden. Um die Kompatibilität zu gewährleisten, vergessen Sie nicht, die Website von zu konsultieren [Jeedom-Kompatibilität](https://compatibility.jeedom.com)

# Plugin Konfiguration

Nach der Installation des Plugins müssen Sie nur die Abhängigkeiten installieren, Ihren Schlüsseltyp und den Port auswählen (achten Sie darauf, dass nur der Deconz-Schlüsseltyp den Port in Auto unterstützt) und den Daemon starten. Sie können auch den Kanal für den Zickzack auswählen.

>**Wichtig**
>
>Jeder Kanalwechsel erfordert zwangsläufig einen Neustart des Daemons. Ein Kanalwechsel kann auch die Wiedereinschaltung eines bestimmten Moduls erfordern


# Moduleinschluss

Inklusion ist der schwierigste Teil in ZigBee. Obwohl einfach, wird die Operation oft mehrmals durchgeführt. Auf der Plugin-Seite ist es einfach, klicken Sie einfach auf die Schaltfläche "Einschlussmodus". Sobald Sie fertig sind, haben Sie 3 Minuten Zeit, um Ihre Ausrüstung einzuschließen.

Die Ausrüstungsseite ändert sich je nach Modul. Es ist erforderlich, jedes Mal auf die Dokumentation dieses Moduls zu verweisen.

>**Wichtig**
>
>Vergessen Sie nicht, das Modul vor jeder Aufnahme zurückzusetzen

# Equipement

Einmal enthalten, muss Jeedom Ihr Modul automatisch erkennen (falls dies nicht der Fall ist, siehe nächstes Kapitel) und daher die Befehle erstellen, die gut funktionieren. Beachten Sie, dass es aufgrund eines Fehlers in einer bestimmten Firmware (Ikea, Sonoff ...) manchmal erforderlich ist, den Modultyp direkt in der Liste "Ausrüstung" auszuwählen und dann zu speichern, um die richtigen Befehle zu erhalten.

Sie haben auf der Registerkarte Ausrüstung die folgenden Parameter :

- **Name der ZigBee-Ausrüstung** : Name Ihrer ZigBee-Ausrüstung
- **Identifikation** : eindeutige Kennungen des Geräts, auch während einer Wiedereingliederung (oder auch wenn Sie den Typ des ZigBee-Schlüssels ändern)
- **Aktivieren**
- **Sichtbar**
- **Übergeordnetes Objekt**
- **Büro**
- **Kategorie**
- **Warten Sie nicht auf die Rückgabe der Auftragsausführung (schneller, aber weniger zuverlässig))** : Warten Sie nicht, bis die Schlüsselüberprüfung anzeigt, dass der Befehl ausgeführt wurde. Es macht die Hand schneller, garantiert aber nicht, dass alles gut gelaufen ist

Auf der Befehlsregisterkarte finden Sie die Befehle Ihres Moduls (sofern es erkannt wurde)

## Bestellung für Experten

Für die Experten ist hier, wie die Kontrollen funktionieren :

- ``attributes::ENDPOINT::CLUSTER_TYPE::CLUSTER::ATTRIBUT::VALUE``, Mit dieser Option können Sie den Wert eines Attributs schreiben (achten Sie darauf, dass nicht alle Attribute geändert werden können) :
  - ``ENDPOINT`` : Endpunktnummer
  - ``CLUSTER_TYPE`` : Clustertyp (IN oder OUT)
  - ``CLUSTER`` : Clusternummer
  - ``ATTRIBUT`` : Attributnummer
  - ``VALUE`` : Wert zu schreiben
Beispiel : ``attributes::1::in::513::18::#slider#*100``, Hier schreiben wir das Attribut in Endpunkt 1, eingehender Cluster (``in``) 513, Attribut 18 mit dem Wert von ``slider*10``
- ``ENDPOINT::CLUSTER:COMMAND::PARAMS``, ermöglicht die Ausführung eines Serverbefehls mit :
  - ``ENDPOINT`` : Endpunktnummer
  - ``CLUSTER`` : Clustername
  - ``COMMAND`` : Name der Bestellung
  - ``PARAMS`` Parameter in der richtigen Reihenfolge getrennt durch ::
Beispiel : ``1::on_off::on``, hier führen wir den Befehl aus ``on`` auf Endpunkt 1 des Clusters ``on_off`` ohne Parameter
Beispiel : ``1::level::move_to_level::#slider#::0``, hier führen wir den Befehl aus ``move_to_level`` auf Endpunkt 1 des Clusters ``level`` Mit Parametern ``#slider#`` und ``0``

# Mein Modul wird nicht erkannt

Wenn Ihr Modul von jeedom nicht erkannt wird (kein Befehl), aber enthalten ist, müssen Sie das Jeedom-Team bitten, es hinzuzufügen.

>**Wichtig**
>
>Das Jeedom-Team behält sich das Recht vor, Integrationsanfragen abzulehnen. Es ist immer besser, ein bereits kompatibles Modul zu verwenden

Dazu müssen Sie die folgenden Elemente angeben (unvollständige Anfragen werden ohne Antwort des Jeedom-Teams abgelehnt) :

- Geben Sie das genaue Modell Ihres Moduls an (mit einem Link zur Verkaufsseite)
- Klicken Sie auf der Ausrüstungsseite auf Konfiguration, dann auf die Registerkarte "Rohdaten" und senden Sie den Inhalt an das Jeedom-Team
- Setzen Sie den Daemon in das Debug (und starten Sie ihn neu), führen Sie Aktionen am Gerät durch (wenn es sich um einen Temperatursensor handelt, variieren Sie die Temperatur, z. B. wenn es sich um ein Ventil handelt, ändern Sie den Sollwert ...) und senden Sie das ZigBee-Debug-Protokoll (achten Sie darauf, dass Sie den Zigbee und nicht den Zigbeed nehmen)

# Touchlink

Touchlink oder Lightlink ist ein spezieller Bestandteil des ZigBee, mit dem Sie Verwaltungsaufträge an ein Modul senden können, wenn Sie sich ganz in der Nähe befinden (50 cm)). Es wird zum Beispiel verwendet, um Lampen ohne Taste zurückzusetzen.

Dies betrifft daher alles, was ZigBee-Lampen vom Typ Philips Hue, Ikea, Osram, Icasa usw. sind. Das Prinzip ist sehr einfach, um diesen Modultyp einem ZigBee-Netzwerk zuordnen zu können. Sie müssen zuerst einen Reset durchführen. Beim Neustart des Moduls wird dann automatisch versucht, eine Verknüpfung mit dem ersten geöffneten ZigBee-Netzwerk herzustellen.

## In Touchlink zurücksetzen

Dies ist der komplizierte Teil (wie immer in Zigbee ist das Zurücksetzen / Assoziieren am schwierigsten). Mehrere Methoden :

- Führen Sie das Ein- und Ausschalten 5 oder 6 Mal schnell durch. Die Lampe blinkt normalerweise am Ende schnell, um zu signalisieren, dass sie gut ist (funktioniert selten)
- Verwenden Sie eine ZigBee-Fernbedienung und
  - Drücken Sie gleichzeitig die EIN- und AUS-Taste für 5 bis 10 Sekunden in der Nähe der Glühbirne (Vorsicht vor bestimmten Glühbirnen, manchmal müssen Sie die Glühbirne kurz zuvor aus- / einschalten) für Philips Farbton-Fernbedienungen
  - Drücken Sie die Reset-Taste (neben der Batterie) für Ikea-Fernbedienungen 5 bis 10 Sekunden lang in der Nähe der Glühbirne (Vorsicht vor bestimmten Glühbirnen, manchmal müssen Sie die Glühbirne kurz zuvor aus- und wieder einschalten)
- Für die Farbtonbirnen können Sie sie auch auf der Farbtonbrücke einfügen und dann von dieser entfernen

# FAQ

>**LQI oder RSSI ist N / A
>
>Normalerweise werden nach einem Neustart der ZigBee-Netzwerke die Werte geleert. Es muss gewartet werden, bis das Modul erneut angezeigt wird, damit die Werte zurückkehren
