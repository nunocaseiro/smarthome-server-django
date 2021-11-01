<template>
    <b-card no-body>
        <b-card-header class="border-0">
            <h3 class="mb-0">{{this.dataRoom.name}}</h3>
        </b-card-header>

        <el-table class="table-responsive table"
                  header-row-class-name="thead-light"
                  :data="this.sensors">
            <el-table-column label="Sensor name"
                             min-width="150px"
                             prop="name">
                <template v-slot="{row}">
                    <b-media no-body class="align-items-center">
                        <!-- <a href="#" class="avatar rounded-circle mr-3">
                            <img alt="Image placeholder" :src="row.img">
                        </a> -->
                        <b-media-body>
                            <router-link :to="{name: 'sensorDetail', params:{sensor: row.id}}"> <span class="font-weight-600 name mb-0 text-sm">{{row.name}}</span></router-link>
                          </b-media-body>
                    </b-media>
                </template>
            </el-table-column>

            <el-table-column label="Sensor status"
                             min-width="150"
                             prop="status">
                <template v-slot="{row}">
                    <b-media no-body class="align-items-center">
                        
                        <b-media-body>
                            <span class="font-weight-600 name mb-0 text-sm" v-if="row.sensortype == 'motion' || row.sensortype == 'luminosity' || row.sensortype == 'camera' || row.sensortype == 'temperature' ">{{row.status}}</span>

                             <label class="switch" v-if="row.sensortype == 'led' || row.sensortype == 'plug' || row.sensortype == 'servo'">
                                <input type="checkbox" :id="'checkbox'+row.id"  v-on:change="handleStatus(row)">
                                <span class="slider round"></span>
                            </label>
                        </b-media-body>
                    </b-media>
                </template>
            </el-table-column>

            <el-table-column label="Sensor auto"
                             min-width="150"
                             prop="auto">
                <template v-slot="{row}">
                    <b-media no-body class="align-items-center">
                        
                        <b-media-body>
                            <span class="font-weight-600 name mb-0 text-sm">{{row.auto == true ? 'Auto' : 'Manual'}}</span>

                        </b-media-body>
                    </b-media>
                </template>
            </el-table-column>

            <el-table-column label="Sensor Value"
                             min-width="150"
                             prop="value">
                <template v-slot="{row}">
                    <b-media no-body class="align-items-center">
                        
                        <b-media-body>
                            <span class="font-weight-600 name mb-0 text-sm">{{row.value}}</span>
                        </b-media-body>
                    </b-media>
                </template>
            </el-table-column>

             <el-table-column label="Type"
                             min-width="150"
                             prop="type">
                <template v-slot="{row}">
                    <b-media no-body class="align-items-center">
                        <b-media-body>
                            <span class="font-weight-600 name mb-0 text-sm">{{row.sensortype.charAt(0).toUpperCase() + row.sensortype.substring(1)}}</span>
                        </b-media-body>
                    </b-media>
                </template>
            </el-table-column>

             <el-table-column label="Actuator"
                             min-width="150"
                             prop="actuator">
                <template v-slot="{row}">
                    <b-media no-body class="align-items-center">
                        <!-- <a href="#" class="avatar rounded-circle mr-3">
                            <img alt="Image placeholder" :src="row.img">
                        </a> -->
                        <b-media-body>
                            <span class="font-weight-600 name mb-0 text-sm">{{getSensorName(row.actuator) }}</span>
                        </b-media-body>
                    </b-media>
                </template>
            </el-table-column>

             <el-table-column label="GPIO"
                             min-width="150"
                             prop="gpio">
                <template v-slot="{row}">
                    <b-media no-body class="align-items-center">
                        <!-- <a href="#" class="avatar rounded-circle mr-3">
                            <img alt="Image placeholder" :src="row.img">
                        </a> -->
                        <b-media-body>
                            <span class="font-weight-600 name mb-0 text-sm">{{row.gpio}}</span>
                        </b-media-body>
                    </b-media>
                </template>
            </el-table-column>

             

            
        </el-table>
    </b-card>
</template>
<script>
  import { Table, TableColumn} from 'element-ui'
  import axios from 'axios'
  import json from  'parse-json'
  export default {
    name: 'light-table',
    props: ['dataRoom'],
    components: {
      [Table.name]: Table,
      [TableColumn.name]: TableColumn
    },
    data() {
      return {
        room: '',
        sensors: [],
        currentPage: 1,
        
      };
    },
    mqtt:{
       '#' (data, topic) {
          console.log(topic + ': ' +  data)
          var info = JSON.parse(data);

          var id = topic.substring(1,topic.length)

          var value = info.value
          var action = info.action

          if (action == "sval"){
              for (var i = 0 ; i< this.sensors.length; i++){
                  if ( id == this.sensors[i].id ){
                      this.sensors[i].value = value
                      console.log(this.sensors[i].value)
                  }

                 this.sensors[i].status = this.getStatus(this.sensors[i])

                
              }
          }

          if (action == "updateSensors" || action == "removeSensor"){
              this.getSensors()
          }
          
      },
    },
    mounted() {
        console.log(this.dataRoom)
        this.getSensors()
    },
    methods: {
      getSensors(){
        axios.get('http://161.35.8.148/api/sensorsofroom/?room='+this.dataRoom.id).then(response=>{
          console.log(response)
          this.sensors = response.data
        })
      },
      getSensorName(id){
          for (var i = 0; i < this.sensors.length; i++){
              if( this.sensors[i].id == id){
                  return this.sensors[i].id
              }
          }
          return 'Empty'
      },
      handleStatus(sensor){
          var checkbox = document.getElementById("checkbox"+sensor.id);
          if (checkbox.checked){
              sensor.value = 1.00
              this.$mqtt.publish('/'+sensor.id, JSON.stringify({"to": String(this.dataRoom.id), "from": "server", "action": "turn", "value": "on"}))
          }else{
              sensor.value = 0.00
              this.$mqtt.publish('/'+sensor.id, JSON.stringify({"to": String(this.dataRoom.id), "from": "server", "action": "turn", "value": "off"}))
          }
          
      },
     getStatus(sensor){
         var checkbox = document.getElementById("checkbox"+sensor.id);
         if (sensor.sensortype == "led" || sensor.sensortype == "motion" || sensor.sensortype == "plug" || sensor.sensortype == "camera"){
            if (sensor.value == 0.0){
                if(checkbox){
                    checkbox.checked = false
                }
                
                return "Off"
            }else{
                if(checkbox){
                checkbox.checked = true
                }
                return "On" 
            }
         }else if(sensor.sensortype == "servo"){
              if (sensor.value == 0.0){
                  if(checkbox){
                    checkbox.checked = false
                  }
                  
                return "Closed"
            }else{
                if(checkbox)[
                    checkbox.checked = true
                ]
                return "Opened"
            }
         }else{
             return "Ok"
            }
         }
    },
  }
</script>
