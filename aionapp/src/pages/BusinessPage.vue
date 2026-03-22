<template>
  <q-page class="q-pa-md bg-primary">
    <q-card class="bg-dark text-accent generic-border-radius">
      <q-card-section class="q-ma-none bg-dark">
        <div class="text-h6 text-white">Business information</div>
      </q-card-section>

      <q-separator inset size="2px"/>

      <q-card-section class="q-ma-none bg-white">
        <div class="text-h6 text-accent">{{ business.name }}</div>
        <div class="text-subtitle2 text-accent"><q-icon name="location_on"/>Location: {{ business.location }}</div>
      </q-card-section>

      <q-card-section class="q-ma-none bg-white">
        <q-input outlined bg-color="primary" color="accent" text-color="accent" v-model="business.description" label="Description" :readonly="!isOwner" />
      </q-card-section>

      <q-card-section class="q-ma-none bg-white">
        <q-input outlined bg-color="primary" color="accent" text-color="accent" v-model="business.email" label="Email" :readonly="!isOwner" />
      </q-card-section>

      <q-card-section class="q-ma-none bg-white">
        <q-input outlined bg-color="primary" color="accent" text-color="accent" v-model="business.phone" label="Phone" :readonly="!isOwner" />
      </q-card-section>

      <q-card-actions align="right" v-if="isOwner" class="bg-white">
        <q-btn unelevated text-color="white" color="warning" label="Save" @click="saveBusiness" />
      </q-card-actions>
    </q-card>

    <q-card class="q-mt-md bg-dark">
      <q-card-section class="bg-dark">
        <div class="text-h6 text-white">Employee Management</div>
      </q-card-section>

      <q-separator inset size="2px"/>

      <q-card-section class="bg-white">
        <q-list  separator class="bg-primary text-accent">
          <q-item v-for="employee in employees" :key="employee.id" dark>
            <q-item-section>
              <q-item-label class="text-accent">{{ employee.username }}</q-item-label>
              <q-item-label caption class="text-accent">{{ employee.fullname }}</q-item-label>
            </q-item-section>
            <q-item-section side v-if="isOwner">
              <q-btn flat round color="negative" icon="delete" @click="deleteEmployee(employee.username)" />
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>

      <q-card-actions align="right" v-if="isOwner" class="bg-white">
        <q-btn unelevated text-color="white" color="positive" label="Add employee" @click="showNewEmployeeDialog = true" />
        <NewEmployee v-model="showNewEmployeeDialog" :bid="route.params.bid" @employee-added="onEmployeeAdded" />
      </q-card-actions>
    </q-card>

    <q-card class="q-mt-md bg-dark">
      <q-card-section class="bg-dark">
        <div class="text-h6 text-white">Team Management</div>
      </q-card-section>

      <q-separator inset size="2px"/>

      <q-card-section class="bg-white">
        <q-list  separator class="bg-primary text-accent">
          <q-item v-for="team in teams" :key="team.id" clickable v-ripple dark @click="openTeamEditDialog(team)">
            <q-item-section>
              <q-item-label class="text-accent">{{ team.name }}</q-item-label>
            </q-item-section>
            <q-item-section side v-if="isOwner">
              <q-btn flat round color="negative" icon="delete" @click.stop="deleteTeam(team.id)" />
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>

      <q-card-actions align="right" v-if="isOwner" class="bg-white">
        <q-btn unelevated text-color="white" color="positive" label="Add Team" @click="showNewTeamDialog = true" />
        <NewTeam v-model="showNewTeamDialog" :bid="route.params.bid" @team-created="onTeamCreated" />
      </q-card-actions>
    </q-card>

    <q-dialog v-model="editDialogVisible" backdrop-filter="blur(10px)">
      <TeamEditCard :team="selectedTeam" :bid="route.params.bid" @team-updated="onTeamUpdated" @close-dialog="editDialogVisible = false" />
    </q-dialog>
    
  </q-page>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { apiGet, apiPut, apiDelete } from '../utils/api-wrapper'
import { useUserStore } from 'stores/user-store'
import { useRoute } from 'vue-router'
import NewTeam from 'components/NewTeam.vue'
import NewEmployee from 'components/NewEmployee.vue'
import TeamEditCard from 'components/TeamEditCard.vue'
import { useQuasar } from 'quasar'

export default {
  name: 'BusinessPage',
  components:{
    NewTeam,
    NewEmployee,
    TeamEditCard
  },
  setup() {
    const business = ref({})
    const employees = ref([])
    const teams = ref([])
    const store = useUserStore()
    const route = useRoute()
    const editDialogVisible = ref(false)
    const showNewTeamDialog = ref(false)
    const showNewEmployeeDialog = ref(false)
    const selectedTeam = ref(null)
    const $q = useQuasar()

    const isOwner = computed(() => {
      return store.businesses.some(business => business.id == route.params.bid && business.owner === store.uid)
    })

    const fetchBusiness = async () => {
      try {
        const response = await apiGet(`/business/${route.params.bid}/`)
        business.value = response
      } catch (error) {
        console.error('Error fetching business:', error)
      }
    }

    const fetchEmployees = async () => {
      try {
        const response = await apiGet(`/business/${route.params.bid}/employees/`)
        employees.value = response
      } catch (error) {
        console.error('Error fetching employees:', error)
      }
    }

    const fetchTeams = async () => {
      try {
        const response = await apiGet(`/business/${route.params.bid}/teams/`)
        teams.value = response
      } catch (error) {
        console.error('Error fetching teams:', error)
      }
    }

    const deleteEmployee = async (employee) => {
      if (!isOwner.value) return
      try {
        await apiDelete(`/remove/employee/${route.params.bid}/${employee}/`)
        fetchEmployees()
        $q.notify({ type: 'positive', message: 'Employee deleted successfully', position: 'bottom-right' })
      } catch (error) {
        console.error('Error deleting employee:', error)
        $q.notify({ type: 'negative', message: 'Error deleting employee', position: 'bottom-right' })
      }
    }

    const deleteTeam = async (teamId) => {
      if (!isOwner.value) return
      try {
        await apiDelete(`/remove/team/${route.params.bid}/${teamId}/`)
        fetchTeams()
        $q.notify({ type: 'positive', message: 'Team deleted successfully', position: 'bottom-right' })
      } catch (error) {
        console.error('Error deleting team:', error)
        $q.notify({ type: 'negative', message: 'Error deleting team', position: 'bottom-right' })
      }
    }

    const saveBusiness = async () => {
      if (!isOwner.value) return
      try {
        const businessData = {
          business: route.params.bid,
          name: business.value.name,
          description: business.value.description,
          phone: business.value.phone,
          email: business.value.email,
        }
        await apiPut(`/business/update/`, businessData)
        $q.notify({ type: 'positive', message: 'Business information saved successfully', position: 'bottom-right' })
      } catch (error) {
        console.error('Error saving business:', error)
        $q.notify({ type: 'negative', message: 'Error saving business information', position: 'bottom-right' })
      }
    }

    const openTeamEditDialog = (team) => {
      if (!isOwner.value) return
      selectedTeam.value = team.id
      editDialogVisible.value = true
    }

    const onEmployeeAdded = () => {
      showNewEmployeeDialog.value = false
      fetchEmployees()
    }

    const onTeamCreated = () => {
      showNewTeamDialog.value = false
      fetchTeams()
    }

    const onTeamUpdated = () => {
      editDialogVisible.value = false
      fetchTeams()
    }

    onMounted(() => {
      fetchBusiness()
      fetchEmployees()
      fetchTeams()
    })

    return {
      business,
      employees,
      teams,
      store,
      saveBusiness,
      NewTeam,
      NewEmployee,
      TeamEditCard,
      showNewTeamDialog,
      showNewEmployeeDialog,
      route,
      deleteEmployee,
      deleteTeam,
      editDialogVisible,
      selectedTeam,
      openTeamEditDialog,
      isOwner,
      onEmployeeAdded,
      onTeamCreated,
      onTeamUpdated
    }
  }
}
</script>
