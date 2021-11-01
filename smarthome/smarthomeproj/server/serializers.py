from django.contrib.auth.models import User, Group
from rest_framework import serializers
from smarthomeproj.server.models import Sensor, SensorValue, Home, Room, Photo, Profile, Vehicle, Favourite, Notification, HouseKey
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from . import mqtt as mqtt
import logging
import json
from json.decoder import JSONDecodeError

logger = logging.getLogger("django")
class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ('name',)

class UserSerializer(serializers.ModelSerializer):
    #groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups', 'first_name', 'last_name']



class User1Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    groups = serializers.CharField(required=True)
    home = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'groups','home')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        group = Group.objects.get(name = validated_data['groups'])
        user.groups.add(group)
        user.set_password(validated_data['password'])
        user = user.save()
        
        userGet = User.objects.get(username=validated_data['username'])
        logger.info(userGet)
        homeObj = Home.objects.get(pk=validated_data['home'])
        logger.info(homeObj)
        profile=Profile.objects.create(user=userGet,home = homeObj)
        
        return userGet

class SensorValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorValue
        fields = ['id','idsensor', 'value']

class HouseKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseKey
        fields = ['key']


class PhotoSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(
        max_length=None, use_url=True,
    )
    class Meta:
        model = Photo
        fields = ['photo']

class SensorSerializerMeta(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'sensortype','room', 'gpio']

class SensorSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField("get_last_value")
    roomname = serializers.SerializerMethodField("get_room_name")
    roomtype = serializers.SerializerMethodField("get_room_type")
    status = serializers.SerializerMethodField("get_status")

    def get_last_value(self,obj):
            #queryset = SensorValue.objects.all().filter(idsensor=idsensor).order_by('-created_at')[:1]
        try:
            value = SensorValue.objects.all().filter(idsensor=obj.id).order_by('-created_at')[:1]
            serializer = SensorValueSerializer(value, many=True)
            return serializer.data[0]["value"]
        except Exception:
                return 0
    
    def get_room_name(self,obj):
            #queryset = SensorValue.objects.all().filter(idsensor=idsensor).order_by('-created_at')[:1]
        try:
            room = Room.objects.get(pk=obj.room.id)
            serializer = RoomSerializer(room)
            return serializer.data["name"]
        except Exception:
                return 0

    def get_status(self,obj):
        value = SensorValue.objects.all().filter(idsensor=obj.id).order_by('-created_at')[:1]
        serializer = SensorValueSerializer(value, many=True)
        if ( len(serializer.data) > 0):
            value = serializer.data[0]["value"]

            if (obj.sensortype == "led" or obj.sensortype == "motion" or obj.sensortype == "plug" or obj.sensortype == "camera"):
                if (value == 0.0):
                    return "Off"
                else:
                    return "On"
            
            elif (obj.sensortype == "servo"):
                if (value == 0.0):
                    return "Closed"
                else:
                    return "Opened"
            
            else:
                return "Ok"
        else:
            return "no value"
    
    def get_room_type(self,obj):
            #queryset = SensorValue.objects.all().filter(idsensor=idsensor).order_by('-created_at')[:1]
        try:
            room = Room.objects.get(pk=obj.room.id)
            serializer = RoomSerializer(room)
            return serializer.data["roomtype"]
        except Exception:
                return 0
        
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'sensortype','room', 'gpio', 'value', 'roomname', 'roomtype', 'ios', 'actuator', 'status', 'temp_lim', 'lux_lim', 'auto']

    def create(self, validated_data):
        sensor = Sensor.objects.create(**validated_data)
        logger.info(sensor.id)
        sensorV = SensorValue(idsensor = sensor, value = 0.0)
        sensorV.save()
        mqtt.client.publish("/0", json.dumps(mqtt.createMessage("server","android", "updateSensors", "/"+str(sensor.id))), qos= 1)
        #mqtt.client.reinitialise()
        
        return sensor

    

class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = ['name','id', 'latitude', 'longitude','key']
    
    
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id','name','home','ip', 'roomtype', 'testing']

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id','licenseplate','brand','model', 'year','home']

class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields =  ['id','user','sensor']

class NotificationSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField("get_photo")
    def get_photo(self,obj):
        serializer = PhotoSerializer(obj.photo)
        return serializer.data["photo"]
    class Meta:
        model = Notification
        fields =  ['id', 'notification','licensePlate','description', 'profile', 'seen' ,'created', 'photo']
   

        

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False)
    home = HomeSerializer(many=False)
    favourites = serializers.SerializerMethodField("get_favourites")
    notifications = serializers.SerializerMethodField("get_notifications")
    photo = Base64ImageField(
        max_length=None, use_url=True,
    )
    def get_favourites(self,obj):
        fav = Favourite.objects.filter(user=obj.user.id)
        serializer = FavouriteSerializer(fav, many= True)
        return serializer.data
    def get_notifications(self,obj):
        notifications = Notification.objects.filter(profile=obj)
        serializer = NotificationSerializer(notifications, many=True)
        return serializer.data
        

        
    class Meta:
        model = Profile
        fields = ['id','user', 'home', 'favourites', 'notifications', 'photo']

class ProfileSerializerCompact(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False)
    
    class Meta:
        model = Profile
        fields = ['user', 'photo']

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

