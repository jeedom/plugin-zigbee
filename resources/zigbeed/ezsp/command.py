# This file is part of Jeedom.
#
# Jeedom is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# at your option any later version.
#
# Jeedom is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Jeedom. If not, see <http://www.gnu.org/licenses/>.

EZSP_COMMANDS = {
    "version": 0x00,
    "getConfigurationValue": 0x52,
    "setConfigurationValue": 0x53,
    "addEndpoint": 0x02,
    "setPolicy": 0x55,
    "getPolicy": 0x56,
    "getValue": 0xAA,
    "getExtendedValue": 0x03,
    "setValue": 0xAB,
    "setGpioCurrentConfiguration": 0xAC,
    "setGpioPowerUpDownConfiguration": 0xAD,
    "setGpioRadioPowerMask": 0xAE,
    "setCtune": 0xF5,
    "getCtune": 0xF6,
    "setChannelMap": 0xF7,
    "nop": 0x05,
    "echo": 0x81,
    "invalidCommand": 0x58,
    "callback": 0x06,
    "noCallbacks": 0x07,
    "setToken": 0x09,
    "getToken": 0x0A,
    "getMfgToken": 0x0B,
    "setMfgToken": 0x0C,
    "stackTokenChangedHandler": 0x0D,
    "getRandomNumber": 0x49,
    "setTimer":  0x0E,
    "getTimer": 0x4E,
    "timerHandler": 0x0F,
    "debugWrite": 0x12,
    "readAndClearCounters":  0x65,
    "readCounters":  0xF1,
    "counterRolloverHandler": 0xF2,
    "delayTest": 0x9D,
    "getLibraryStatus": 0x01,
    "getXncpInfo": 0x13,
    "customFrame": 0x47,
    "customFrameHandler": 0x54,
    "getEui64": 0x26,
    "getNodeId": 0x27,
    "networkInit": 0x17,
    "setManufacturerCode": 0x15,
    "setPowerDescriptor": 0x16,
    "networkInitExtended": 0x70,
    "networkState": 0x18,
    "stackStatusHandler": 0x19,
    "startScan":  0x1A,
    "energyScanResultHandler": 0x48,
    "networkFoundHandler": 0x1B,
    "scanCompleteHandler": 0x1C,
    "stopScan": 0x1D,
    "formNetwork": 0x1E,
    "joinNetwork":  0x1F,
    "leaveNetwork": 0x20,
    "findAndRejoinNetwork": 0x21,
    "permitJoining": 0x22,
    "childJoinHandler":  0x23,
    "energyScanRequest":  0x9C,
    "getNetworkParameters":  0x28,
    "getParentChildParameters": 0x29,
    "getChildData":  0x4A,
    "getNeighbor": 0x79,
    "neighborCount": 0x7A,
    "getRouteTableEntry": 0x7B,
    "setRadioPower": 0x99,
    "setRadioChannel": 0x9A,
    "setConcentrator":  0x10,
    "clearBindingTable": 0x2A,
    "setBinding": 0x2B,
    "getBinding": 0x2C,
    "deleteBinding": 0x2D,
    "bindingIsActive": 0x2E,
    "getBindingRemoteNodeId": 0x2F,
    "setBindingRemoteNodeId": 0x30,
    "remoteSetBindingHandler": 0x31,
    "remoteDeleteBindingHandler": 0x32,
    "maximumPayloadLength": 0x33,
    "sendUnicast":  0x34,
    "sendBroadcast":  0x36,
    "proxyBroadcast":  0x37,
    "sendMulticast":  0x38,
    "sendReply": 0x39,
    "messageSentHandler":  0x3F,
    "sendManyToOneRouteRequest": 0x41,
    "pollForData": 0x42,
    "pollCompleteHandler": 0x43,
    "pollHandler": 0x44,
    "incomingSenderEui64Handler": 0x62,
    "incomingMessageHandler":  0x45,
    "incomingRouteRecordHandler":  0x59,
    "changeSourceRouteHandler": 0xC4,
    "setSourceRoute":  0x5A,
    "incomingManyToOneRouteRequestHandler":  0x7D,
    "incomingRouteErrorHandler": 0x80,
    "addressTableEntryIsActive": 0x5B,
    "setAddressTableRemoteEui64": 0x5C,
    "setAddressTableRemoteNodeId": 0x5D,
    "getAddressTableRemoteEui64": 0x5E,
    "getAddressTableRemoteNodeId": 0x5F,
    "setExtendedTimeout": 0x7E,
    "getExtendedTimeout": 0x7F,
    "replaceAddressTableEntry":  0x82,
    "lookupNodeIdByEui64": 0x60,
    "lookupEui64ByNodeId": 0x61,
    "getMulticastTableEntry":  0x63,
    "setMulticastTableEntry":  0x64,
    "idConflictHandler": 0x7C,
    "sendRawMessage": 0x96,
    "macPassthroughMessageHandler":  0x97,
    "macFilterMatchMessageHandler":  0x46,
    "rawTransmitCompleteHandler": 0x98,
    "setInitialSecurityState": 0x68,
    "getCurrentSecurityState": 0x69,
    "getKey": 0x6A,
    "switchNetworkKeyHandler": 0x6E,
    "getKeyTableEntry": 0x71,
    "setKeyTableEntry":  0x72,
    "findKeyTableEntry": 0x75,
    "addOrUpdateKeyTableEntry":  0x66,
    "eraseKeyTableEntry": 0x76,
    "clearKeyTable": 0xB1,
    "requestLinkKey": 0x14,
    "zigbeeKeyEstablishmentHandler": 0x9B,
    "addTransientLinkKey": 0xAF,
    "clearTransientLinkKeys": 0x6B,
    "getTransientLinkKey":  0xCE,
    "setSecurityKey":  0xCA,
    "setSecurityParameters":  0xCB,
    "resetToFactoryDefaults": 0xCC,
    "getSecurityKeyStatus": 0xCD,
    "trustCenterJoinHandler":  0x24,
    "broadcastNextNetworkKey": 0x73,
    "broadcastNetworkKeySwitch": 0x74,
    "becomeTrustCenter": 0x77,
    "aesMmoHash":  0x6F,
    "removeDevice":  0xA8,
    "unicastNwkKeyUpdate":  0xA9,
    "generateCbkeKeys": 0xA4,
    "generateCbkeKeysHandler": 0x9E,
    "calculateSmacs":  0x9F,
    "calculateSmacsHandler":  0xA0,
    "generateCbkeKeys283k1": 0xE8,
    "generateCbkeKeysHandler283k1":  0xE9,
    "calculateSmacs283k1":  0xEA,
    "calculateSmacsHandler283k1":  0xEB,
    "clearTemporaryDataMaybeStoreLinkKey": 0xA1,
    "clearTemporaryDataMaybeStoreLinkKey283k1": 0xEE,
    "getCertificate": 0xA5,
    "getCertificate283k1": 0xEC,
    "dsaSign": 0xA6,
    "dsaSignHandler": 0xA7,
    "dsaVerify":  0xA3,
    "dsaVerifyHandler": 0x78,
    "dsaVerify283k1":  0xB0,
    "setPreinstalledCbkeData":  0xA2,
    "setPreinstalledCbkeData283k1":  0xED,
    "mfglibStart": 0x83,
    "mfglibEnd": 0x84,
    "mfglibStartTone": 0x85,
    "mfglibStopTone": 0x86,
    "mfglibStartStream": 0x87,
    "mfglibStopStream": 0x88,
    "mfglibSendPacket": 0x89,
    "mfglibSetChannel": 0x8A,
    "mfglibGetChannel": 0x8B,
    "mfglibSetPower": 0x8C,
    "mfglibGetPower": 0x8D,
    "mfglibRxHandler": 0x8E,
    "launchStandaloneBootloader": 0x8F,
    "sendBootloadMessage": 0x90,
    "getStandaloneBootloaderVersionPlatMicroPhy":  0x91,
    "incomingBootloadMessageHandler":  0x92,
    "bootloadTransmitCompleteHandler": 0x93,
    "aesEncrypt":  0x94,
    "overrideCurrentChannel": 0x95,
    "zllNetworkOps":  0xB2,
    "zllSetInitialSecurityState":  0xB3,
    "zllStartScan": 0xB4,
    "zllSetRxOnWhenIdle": 0xB5,
    "zllNetworkFoundHandler":  0xB6,
    "zllScanCompleteHandler": 0xB7,
    "zllAddressAssignmentHandler":  0xB8,
    "setLogicalAndRadioChannel": 0xB9,
    "getLogicalChannel": 0xBA,
    "zllTouchLinkTargetHandler": 0xBB,
    "zllGetTokens":  0xBC,
    "zllSetDataToken": 0xBD,
    "zllSetNonZllNetwork": 0xBF,
    "isZllNetwork": 0xBE,
    "rf4ceSetPairingTableEntry":  0xD0,
    "rf4ceGetPairingTableEntry":  0xD1,
    "rf4ceDeletePairingTableEntry": 0xD2,
    "rf4ceKeyUpdate": 0xD3,
    "rf4ceSend":  0xD4,
    "rf4ceIncomingMessageHandler":  0xD5,
    "rf4ceMessageSentHandler":  0xD6,
    "rf4ceStart":  0xD7,
    "rf4ceStop": 0xD8,
    "rf4ceDiscovery":  0xD9,
    "rf4ceDiscoveryCompleteHandler": 0xDA,
    "rf4ceDiscoveryRequestHandler":  0xDB,
    "rf4ceDiscoveryResponseHandler":  0xDC,
    "rf4ceEnableAutoDiscoveryResponse": 0xDD,
    "rf4ceAutoDiscoveryResponseCompleteHandler":  0xDE,
    "rf4cePair": 0xDF,
    "rf4cePairCompleteHandler": 0xE0,
    "rf4cePairRequestHandler": 0xE1,
    "rf4ceUnpair": 0xE2,
    "rf4ceUnpairHandler": 0xE3,
    "rf4ceUnpairCompleteHandler": 0xE4,
    "rf4ceSetPowerSavingParameters": 0xE5,
    "rf4ceSetFrequencyAgilityParameters": 0xE6,
    "rf4ceSetApplicationInfo": 0xE7,
    "rf4ceGetApplicationInfo": 0xEF,
    "rf4ceGetMaxPayload": 0xF3,
    "rf4ceGetNetworkParameters": 0xF4,
    "gpProxyTableProcessGpPairing": 0xC9,
    "dGpSend": 0xC6,
    "dGpSentHandler": 0xC7,
    "gpepIncomingMessageHandler": 0xC5,
}
