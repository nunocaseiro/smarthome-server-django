import paho.mqtt.client as mqtt
import logging
import json
from json.decoder import JSONDecodeError
from .models import Room, Sensor, Photo
import re
from . import licensePlateRecognition as plate
from decimal import Decimal


logger = logging.getLogger("django")
allsensors = Sensor.objects.all().filter(ios=False)
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    
    #logger.error("Connected with result code "+str(rc))
    client.subscribe("/0")
    for sensor in allsensors:
        client.subscribe("/"+str(sensor.id))
        #logger.info("/"+sensor.name)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        pass
        #logger.info("Unexpected disconnection.")
    else:
        pass
        #logger.info("Disconnected")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    from .models import Room, Sensor, SensorValue, Vehicle, Profile, Notification, Photo
    
    #try:
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    logger.info(str(m_decode))
    m_in=json.loads(m_decode)        
    idSensor = int(msg.topic[1:])


    if(idSensor == 0):
        if(m_in["action"] == "updateSensors"):
            client.subscribe(m_in["value"], qos=1)
            logger.info("update Sensor: " + m_in["value"])
            
        #if (m_in["action"] == "removeSensor"):
        #    client.unsubscribe(m_in["value"], qos=1)
        #    logger.info("remove Sensor: " + m_in["value"])
            
        publishUpdateSensor()
    else:
        sensor = Sensor.objects.get(id=idSensor)
        if (sensor.actuator != None):
            actuator = Sensor.objects.get(id=sensor.actuator.id)
        
        if (m_in["to"] == "server" and ( m_in["from"] == "9" or m_in["from"] == "10" or m_in["from"] == "27") ):
            m_from = m_in["from"]
            #logger.info(m_from)
            if (m_in["action"] == "sval"):
                logger.info("SENSOR ATUADOR:"  + m_in["value"])
                sensorV = SensorValue(idsensor = sensor, value = m_in["value"])
                sensorV.save()
                #publishUpdateSensorValue()
                #client.publish("/android", "updateSensors", qos= 1)
                #logger.info("SENSOR ATUADOR:"  + str(sensor.actuator))
                
                if (sensor.actuator != None):
                    if (sensor.sensortype == "motion"):
                        #logger.info("ATUADOR:"  + str(actuator))
                        if (sensor.auto == True):
                            if(actuator.sensortype == "led"):
                                    #logger.info("ATUADOR:"  + str(actuator.sensortype))
                                    #logger.info("ATUADOR:"  + str(sensorV.value))

                                if sensorV.value == "0.00":
                                    client.publish("/"+str(actuator.id), json.dumps(createMessage(m_from,"server","turn","off")),qos=1)
                                if sensorV.value == "1.00":
                                    client.publish("/"+str(actuator.id), json.dumps(createMessage(m_from,"server","turn","on")),qos=1)

                    if (sensor.sensortype == "led"): 
                        #logger.info(str(sensor.name) + "||" + str(sensor.sensortype) + "||" +str(actuator.id))     
                        if (sensor.auto == True):  
                            if(actuator.sensortype == "camera"):
                                if sensorV.value == "1.00":
                                    client.publish("/"+str(actuator.id), json.dumps(createMessage(m_from,"server","photo","take")),qos=1)
                                if sensorV.value == "0.00":
                                    client.publish("/"+str(actuator.id), json.dumps(createMessage(m_from,"server","photo","off")),qos=1)

                    if (sensor.sensortype == "camera"):
                        if (sensor.auto == True):
                            if(actuator.sensortype == "plug" or actuator.sensortype == "servo"):
                                if sensorV.value == "0.00":
                                    #logger.info("TURN OFF")
                                    client.publish("/"+str(actuator.id), json.dumps(createMessage(m_from,"server","turn","off")),qos=1)
                                if sensorV.value == "1.00":
                                    #logger.info("TURN OFF")
                                    client.publish("/"+str(actuator.id), json.dumps(createMessage(m_from,"server","turn","on")),qos=1)

                    if (sensor.sensortype == "temperature"):
                        if (sensor.auto == True):
                            if(actuator.sensortype == "led" ):
                                if Decimal(sensorV.value) < Decimal(sensor.temp_lim):
                                    #logger.info("TURN OFF")
                                    client.publish("/"+str(actuator.id), json.dumps(createMessage(m_from,"server","turn","off")),qos=1)
                                if Decimal(sensorV.value) > Decimal(sensor.temp_lim):
                                    #logger.info("TURN OFF")
                                    client.publish("/"+str(actuator.id), json.dumps(createMessage(m_from,"server","turn","on")),qos=1)
                    
                    if (sensor.sensortype == "luminosity"):
                        if (sensor.auto == True):
                            if(actuator.sensortype == "led" ):
                                if Decimal(sensorV.value) > Decimal(sensor.lux_lim):
                                    #logger.info("TURN OFF")
                                    client.publish("/"+str(actuator.id), json.dumps(createMessage(m_from,"server","turn","off")),qos=1)
                                if Decimal(sensorV.value) < Decimal(sensor.lux_lim):
                                    #logger.info("TURN OFF")
                                    client.publish("/"+str(actuator.id), json.dumps(createMessage(m_from,"server","turn","on")),qos=1)

                    if (sensor.sensortype == "plug"):
                        #logger.info("ATUADOR:"  + str(actuator))
                        if (sensor.auto == True):
                            if(actuator.sensortype == "led"):
                                    #logger.info("ATUADOR:"  + str(actuator.sensortype))
                                    #logger.info("ATUADOR:"  + str(sensorV.value))

                                if sensorV.value == "0.00":
                                    client.publish("/"+str(actuator.id), json.dumps(createMessage(m_from,"server","turn","off")),qos=1)
                                if sensorV.value == "1.00":
                                    client.publish("/"+str(actuator.id), json.dumps(createMessage(m_from,"server","turn","on")),qos=1)

            if (m_in["action"] == "photo" and m_in["value"] == "sent"):

                if (sensor != None):
                    logger.info("KAESTOU")
                    photo = Photo.objects.latest('created_at')
                    logger.info(str(photo.photo))
                    plate = getLicense(photo)
                    if ( len(plate) == 6):
                        #logger.info(text)
                        #textFinal = re.sub('[\W_]+', '', text) 
                        #textFinal = textFinal.strip()
                        #logger.info(textFinal)
                        allProfiles = Profile.objects.all()
                        #lastPhoto = Photo.objects.latest('created_at') 
                        try:
                            go = Vehicle.objects.get(licenseplate=plate.upper())
                            for profile in allProfiles:
                                newNotification = Notification.objects.create(profile = profile, notification = "New vehicle detected",seen= False, licensePlate = plate.upper(), photo=photo, description = "allowed")
                                newNotification.save()
                                client.publish("/"+str(sensor.id), json.dumps(createMessage("9","server","photo","on")),qos=1)
                                logger.info(createMessageAndroid("android", profile.user.username,"newPhoto", str(newNotification.id)))
                                client.publish("/android", json.dumps(createMessageAndroid("android", profile.user.username,"newPhoto", str(newNotification.id))), qos=1)
                        except Vehicle.DoesNotExist:
                            for profile in allProfiles:
                                newNotification = Notification.objects.create(profile = profile, notification = "New vehicle detected",seen= False, licensePlate = plate.upper(), photo=photo, description = "not allowed")                        
                                newNotification.save()
                                client.publish("/android", json.dumps(createMessageAndroid("android", profile.user.username,"newPhoto", str(newNotification.id))), qos=1)
                    #client.publish("/android", "newPhoto", qos=1)
            
    #logger.info(idSensor)
    #except ValueError:
    #    logger.error(ValueError)


def getLicense(path):
        import requests
        from pprint import pprint
        regions = ['pt'] # Change to your country
        with open('/home/smarthome/smarthome/'+ str(path) , 'rb') as fp:
            response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                data=dict(regions=regions),  # Optional
                files=dict(upload=fp),
                headers={'Authorization': 'Token 52bfd1c31e9ef39556e620477a557ffd85466df9'})
        resp_in = response.json()   
        if ( len(resp_in["results"]) != 0):
            plate =  resp_in["results"][0]["candidates"][0]["plate"]
            logger.info(plate)
            return plate 
        else:
            return ""
        #pprint(response.json())          

    #         if(atuador.atuador != None):
    #             atuador2 = Sensor.objects.get(id=atuador.atuador.id)
    #             #enviar estado em vez de value
                        #if m_in["value"] == "0.00":
                        #    client.publish("/"+str(atuador.id), json.dumps(createMessage("espNuno","server","turn","off")),qos=1)
    #             if sensorValue.value == 1.00:
                    
    #                 logger.info("zero")
    #                 client.publish("/"+str(atuador.id), json.dumps(createMessage("espNuno","server","turn","off")),qos=1)
    #                 client.publish("/"+str(atuador2.id), json.dumps(createMessage("espNuno","server","turn","off")),qos=1)
    #                 client.publish("/android", "updateSensors", qos = 1)


    #         if m_in["value"] == "1.00":
    #             #if sensorValue.value == 0.00:
    #                 logger.info("um")
    #                 sensorV = SensorValue(idsensor = sensor, value = 1.0)
    #                 sensorV.save()
    #                 #publicar mensagem
                    
    #                 client.publish("/"+str(atuador.id), json.dumps(createMessage("espNuno","server","turn","on")),qos=1)
    #                 client.publish("/"+str(atuador.id), json.dumps(createMessage("espNuno","server","photo","on")),qos=1)
    #                 client.publish("/android", "updateSensors", qos= 1)
    #                 # if atuador2 tipo camera entao envia mensagem para tirar foto """

def createMessage(to,fr0m,action,value):
    send_msg = {
        "to": to,
        "from": fr0m,
        "action":action,
        "value":value
    }
    return send_msg

def createMessageAndroid(to,user,action,value):
    send_msg = {
        "to": to,
        "user": user,
        "action":action,
        "value":value
    }
    return send_msg

def subscribe(aux):
    client.subscribe("/"+str(aux), qos= 1)

def publishUpdateSensor():
    client.publish("all", json.dumps(createMessage("all","server", "updateSensors", "value")), qos= 1)

def publishUpdateSensorValue():
    client.publish("all", json.dumps(createMessage("all","server", "updateSensorValue", "value")), qos= 1)
 

client = mqtt.Client("server")
client.username_pw_set("smarthome","")
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.connect_async("161.35.8.148", 1883, 60)