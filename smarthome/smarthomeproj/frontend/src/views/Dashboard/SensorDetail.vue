<template>
  <div>
  <base-header class="pb-6 pb-8 pt-5 pt-md-8 bg-gradient-success">
      <!-- Card stats -->
      <b-row>
       
      
      </b-row>
    </base-header>
    
    <div>
 <b-container class="mt--8 pb-5">
      <b-row class="justify-content-center">
        <b-col lg="7" md="5">
          <b-card no-body class="bg-secondary border-0 mb-0">
            <b-card-body class="px-lg-7 py-lg-5">
              <validation-observer  ref="formValidator">
                <b-form role="form" @submit.prevent="">
                    <div class="col-lg-2" >
                <img :src="image"  height=100 alt="Image" align =center class="rounded-0" style=" padding-left: 125px;"></img>
                </div>
                <br>
                <br>
                     <label for="SensorName">Name: </label>
                  <base-input value class="mb-3" name="SensorName" placeholder="Sensor name" v-model="sensor.name"> </base-input>


                    <label for="types">Type: </label>
                    <select class="form-control mb-3 w-100" id="types" name="types" v-model="sensor.sensortype" @change="onchangeType($event)">
                    <option v-for="type in this.allTypes" v-bind:value="type">{{type.charAt(0).toUpperCase() + type.substring(1)}}</option>   
                    </select>

                    <label for="rooms">Room: </label>
                    <select class="form-control mb-3 w-100" id="rooms" name="rooms" v-model="sensor.room"  @change="getSensorsOfRoomHandle($event)">
                    <option v-for="room in this.allRooms" v-bind:value="room.id" >{{room.name}}</option>   
                    </select>

                    <label for="actuators">Actuator: </label>
                    <select class="form-control mb-3 w-100" id="actuators" name="actuators" v-model="sensor.actuator" placeholder="Actuator" >
                    <option v-bind:value="'None'">None</option>
                    <option v-for="sensor in this.allSensorsOfRoom" v-bind:value="sensor.id">{{sensor.name}}</option>   
                    </select>
                    
                    <label for="actuators" v-if="sensor.sensortype=='luminosity'">Luminosity limit: </label>
                    <base-input value class="mb-3" type="number" name="luminosity" placeholder="Luminosity limit" v-model="sensor.lux_lim" v-if="sensor.sensortype=='luminosity'"> </base-input>


                    <label for="actuators" v-if="sensor.sensortype=='temperature'" >Temperature limit: </label>
                    <base-input value class="mb-3" type="number" name="temperature" placeholder="Temperature limit" v-model="sensor.temp_lim" v-if="sensor.sensortype=='temperature'"> </base-input>

                    <label for="gpio">Gpio: </label>
                    <base-input value class="mb-3" name="gpio" type="number" placeholder="GPIO" v-model="sensor.gpio"> </base-input>

                    <label for="auto">Auto: </label>
                    <base-checkbox class="mb-3" name="auto" v-model="sensor.auto" ></base-checkbox>
                  
                    <div class="text-center">
                      <base-button type="primary" native-type="submit" class="my-4" v-on:click="saveSensor()">Save</base-button>
                       <base-button type="danger" native-type="submit" class="my-4" v-on:click="deleteSensor()">Delete</base-button>
                    </div>
                </b-form>
              </validation-observer>
            </b-card-body>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
</div>

   

  </div>
</template>
<script>
import axios from 'axios'
import BaseCheckbox from '../../components/Inputs/BaseCheckbox.vue';


export default {
    components: {
        BaseCheckbox
    
    }, 
    data() {
        return {
            sensorId: '',
            sensor: {},
            allRooms: [],
            allSensors: [],
            allSensorsOfRoom:[],
            allTypes: [],
            image: require('@/assets/configurations_icon.png')
        };
},
    mounted(){
        this.sensorId = this.$route.params.sensor;
        this.getRooms();
        this.getTypes();
       


    },
     methods: {
      getSensor(){
        axios.get('http://161.35.8.148/api/sensors/'+this.sensorId+'/').then(response=>{
            
          this.sensor = response.data
          console.log(response.data)
          this.onchangeType(event)
          this.getSensorsOfRoom(this.sensor.room);
        })
      },
      getRooms(){
        axios.get('http://161.35.8.148/api/actualrooms?home=1').then(response=>{
          
          this.allRooms = response.data
          this.getSensor();
        })
      },
      getSensorsOfRoom(id){
        
        axios.get('http://161.35.8.148/api/sensorsofroom/?room='+id).then(response=>{
          console.log(response)
          for (var i = 0; i< response.data.length; i++){
              this.allSensorsOfRoom.push(response.data[i])
          }
        })
      },
      getSensorsOfRoomHandle(event){
        this.allSensorsOfRoom = []
        var value = event.target.value
        axios.get('http://161.35.8.148/api/sensorsofroom/?room='+value).then(response=>{
          console.log(response)
           for (var i = 0; i< response.data.length; i++){
              this.allSensorsOfRoom.push(response.data[i])
          }
         
        })
      },
      getImage(image){
        return require('@/assets/configurations_icon.png')
      },
    getTypes(){
        axios.get('http://161.35.8.148/api/sensortypes/').then(response=>{
            for(var i = 0 ; i < response.data.data.length; i++){
                this.allTypes.push(response.data.data[i])
            }
          })
        },
      
        onchange(event){
            console.log(event.target.value)
        },
        onchangeType(event){
            if (event.target.value != null){
            console.log(event.target.value)
            var value = event.target.value
            }else{
                value = this.sensor.sensortype
            }
           
            switch(value){
                case 'led':
                this.image = require('@/assets/light_icon.png')
                   break;
                case 'camera':
                    this.image = require('@/assets/camera_icon.png')
                    break;
                case 'plug':
                    this.image = require('@/assets/plug_icon.png')
                   break;
                case 'motion':
                    this.image = require('@/assets/configurations_icon.png')
                    break;
                case 'temperature':
                     this.image = require('@/assets/termometre_icon.png')
                    break;
                case 'luminosity':
                     this.image = require('@/assets/configurations_icon.png')
                    break;
                case 'servo':
                     this.image = require('@/assets/door_icon.png')
                    break;
                default:
                    this.image = require('@/assets/configurations_icon.png')
            }
               
        },
        saveSensor(){
          axios.put('http://161.35.8.148/api/sensors/'+this.sensor.id+'/', this.sensor).then(response=>{
            console.log(response)
          })
        },
        deleteSensor(){
          axios.delete('http://161.35.8.148/api/sensors/'+this.sensor.id+'/').then(response=>{
            console.log(response)
            setTimeout(()=>{
            
            this.$router.push("/")
          },1000)
          })
        }
            
     },
};
</script>
<style></style>
