<template>
    <q-card class="bg-white text-accent">
      <q-card-section>
        <div class="row items-center justify-between">
          <div class="text-h6">My teams</div>
        </div>
      </q-card-section>
  
      <q-separator color="#FF0000" inset size="2px"/>
  
      <q-card-section>
        
        <q-list class="bg-primary" bordered separator>
          <q-item v-for="team in teams" :key="team.id" clickable v-ripple>
            <q-item-section avatar>
              <q-avatar :color="team.color" text-color="dark">
                {{ team.initials }}
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-black">{{ team.team.name }}</q-item-label>
              <q-item-label caption>Business: {{ team.business_name }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
        
        <div class="text-center q-mt-sm">
        </div>
      </q-card-section>
    </q-card>
  </template>
  
  <script>
  import { defineComponent, ref, onMounted } from 'vue';
  import { apiGet } from '../utils/api-wrapper';
  import { useUserStore } from 'stores/user-store';
  
  export default defineComponent({
    name: 'TaskTeamList',
    setup() {
      const teams = ref([]);
      const store = useUserStore();

      const fetchTeams = async () => {
        try {
          const response = await apiGet(`user/${store.uid}/team/`)
          teams.value = response;
          console.log(response)
        } catch (error) {
          console.error('Error fetching teams:', error);
        }
      }

      onMounted(fetchTeams);
  
      return {
        teams,
        fetchTeams
      };
    },
  });
  </script>