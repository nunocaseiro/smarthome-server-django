<template>
  <div>

    <base-header class="pb-4 pb-8 pt-5 pt-md-5 bg-gradient-success">
      <!-- Card stats -->
    <a class="btn btn-dark btn-lg" role="button" href="http://arci-smarthome.space/static/app-debug.apk" style="margin-top: 50px">Download Android App</a>
    </base-header>
    <b-container fluid class="mt--6">
    
    <!--Tables-->
      <div v-for="room in rooms" :key="room.id">
        <light-table v-bind:dataRoom="room" ></light-table>
        <br>
      </div>
       

      
      <!--End tables-->
    </b-container>

  </div>
</template>
<script>
// Components
  import BaseProgress from '@/components/BaseProgress';
  import StatsCard from '@/components/Cards/StatsCard';
  import LightTable from './Tables/RegularTables/LightTable'
  import axios from 'axios'
  
  export default {
    components: {
      BaseProgress,
      StatsCard,
      LightTable
        
    },
    data() {
      return {
        rooms: []
      };
    },mqtt:{
        'all' (data, topic) {
          console.log(topic + ': ' + String.fromCharCode.apply(null, data))
      }
    },
    methods: {
      getRooms(){
        axios.get('http://161.35.8.148/api/actualrooms/?home=1').then(response=>{
          console.log(response)
          this.rooms = response.data
        })
      },
      
    },
    
    mounted() {
      this.getRooms()
    }
  };
</script>
<style>
.el-table .cell{
  padding-left: 0px;
  padding-right: 0px;
}
</style>
