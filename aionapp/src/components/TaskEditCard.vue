<template>
  <q-card class="task-edit-card bg-white">
    <q-toolbar class="bg-dark text-white">
      <q-toolbar-title>Edit task</q-toolbar-title>
      <q-btn flat round dense icon="close" @click="closeDialog" color="white" />
    </q-toolbar>

    <q-form @submit="onSubmit" class="q-gutter-md">
      <q-card-section class="q-ml-xs q-mt-md q-ma-none">
        <q-input standout="bg-primary text-accent" outlined bg-color="primary" color="accent" v-model="taskName" label="Task name" :rules="taskNameRules" />
      </q-card-section>

      <q-card-section class="q-ml-xs q-ma-none">
        <div class="row q-col-gutter-md">
          <div class="col-6">
            <q-input standout="bg-primary text-accent" outlined bg-color="primary" color="accent" v-model="startDate" label="Start date" type="date" :rules="startDateRules" />
          </div>
          <div class="col-6">
            <q-input standout="bg-primary text-accent" outlined bg-color="primary" color="accent" v-model="endDate" label="End date" type="date" :rules="endDateRules" />
          </div>
        </div>
      </q-card-section>

      <q-card-section class="q-ml-xs q-ma-none" >
        <div class="text-subtitle2 text-accent">Priority</div>
        <div class="q-gutter-sm row">
          <div class="row justify-center items-center">
            <q-radio keep-color v-model="priority" val="L" label="" color="light-blue" class="text-accent" />
            <BadgeTypes label="LOW" />
          </div>
          <div class="row justify-center items-center">
            <q-radio keep-color v-model="priority" val="M" label="" color="orange" class="text-accent" />
            <BadgeTypes label="MEDIUM" />
          </div>
          <div class="row justify-center items-center">
            <q-radio keep-color v-model="priority" val="H" label="" color="red" class="text-accent" />  
            <BadgeTypes label="HIGH" />
          </div>
        </div>
      </q-card-section> 

      <q-card-section class="q-ml-xs q-ma-none">
        <div class="text-subtitle2 text-accent">Status</div>
        <div class="q-gutter-sm row">
          <div class="row justify-center items-center">
            <q-radio keep-color v-model="status" val="TODO" label="" color="light-green " class="text-accent" />
            <BadgeTypes label="To do" />
          </div>
          <div class="row justify-center items-center">
            <q-radio keep-color v-model="status" val="IN_PROGRESS" label="" color="blue" class="text-accent" />
            <BadgeTypes label="In progress" />
          </div>
          <div class="row justify-center items-center">
            <q-radio keep-color v-model="status" val="DONE" label="" color="green" class="text-accent" />
            <BadgeTypes label="Done" /> 
          </div> 
        </div>
      </q-card-section>

      <q-card-section class="q-ml-xs q-ma-none">
        <q-select
          outlined
          bg-color="primary"
          color="accent"
          text-color="accent"
          popup-content-class="text-accent bg-primary"
          v-model="assignedUser"
          :options="userOptions"
          label="Assign to user"
          :rules="[val => !!val || 'Please assign the task to a user']"
        />
      </q-card-section>

      <q-card-section class="q-ml-xs q-ma-none">
        <q-select
          outlined
          bg-color="primary"
          color="accent"
          text-color="accent"
          popup-content-class="text-accent bg-primary"
          v-model="assignedTeam"
          :options="teamOptions"
          label="Assign to Team"
        />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn push text-color="white" type="submit" color="warning" label="Update" />
      </q-card-actions>
    </q-form>
  </q-card>
</template>

<script>
import { ref, onMounted, inject } from 'vue';
import { useRoute } from 'vue-router';
import { apiGet, apiPut } from '../utils/api-wrapper';
import { useUserStore } from 'stores/user-store';
import BadgeTypes from './BadgeTypes.vue';
import { useQuasar } from 'quasar'

export default {
  name: 'TaskEditCard',
  props: {
    taskId: {
      type: String,
      required: true
    }
  },
  components: {
    BadgeTypes
  },
  setup(props, { emit }) {
    const taskName = ref('');
    const startDate = ref('');
    const endDate = ref('');
    const priority = ref('L');
    const status = ref('TODO');
    const assignedUser = ref(null);
    const assignedTeam = ref(null);
    const route = useRoute();
    const userOptions = ref([]);
    const teamOptions = ref([]);
    const refresh = inject('refresh');
    const store = useUserStore();
    const $q = useQuasar()

    const loadTaskData = async () => {
      try {
        const response = await apiGet(`/task/${props.taskId}/`);
        taskName.value = response.name;
        startDate.value = response.start_date;
        endDate.value = response.end_date;
        priority.value = response.priority;
        status.value = response.status;
        assignedUser.value = response.user_assigned;
        assignedTeam.value = response.team_assigned;
      } catch (error) {
        console.error('Error loading task data:', error);
      }
    };

    const loadUserOptions = async () => {
      const response = await apiGet('/project/'+route.params.pid+'/users/');
      userOptions.value = response.map(user => ({ label: user.username, value: user.id }));
    };

    const loadTeamOptions = async () => {
      const business_id = store.projects.find(project => project.id === parseInt(route.params.pid)).business;
      const response = await apiGet(`/business/${business_id}/teams/`);
      teamOptions.value = response.map(team => ({ label: team.name, value: team.id }));
    };

    onMounted(() => {
      loadTaskData();
      loadUserOptions();
      loadTeamOptions();
    });

    const taskNameRules = [
      val => !!val || 'Task name is required'
    ];

    const startDateRules = [
      val => !!val || 'Start date is required',
      val => !endDate.value || val <= endDate.value || 'Start date must be before or equal to end date'
    ];

    const endDateRules = [
      val => !!val || 'End date is required',
      val => !startDate.value || val >= startDate.value || 'End date must be after or equal to start date'
    ];

    const onSubmit = async () => {
      try {
        const taskData = {
          name: taskName.value,
          start_date: startDate.value,
          end_date: endDate.value,
          priority: priority.value,
          project: route.params.pid,
          user_assigned: assignedUser.value.label,
          team_assigned: assignedTeam.value ? assignedTeam.value.value : null,
          status: status.value
        };
        await apiPut(`/task/${props.taskId}/`, taskData);
        emit('task-updated');
        closeDialog();
      } catch (error) {
        console.error('Error updating task:', error);
        $q.notify({ type: 'negative', message: 'Error updating task', position: 'bottom-right' })
      }
    };

    const closeDialog = () => {
      emit('close-dialog');
    };

    return {
      taskName,
      startDate,
      endDate,
      priority,
      status,
      assignedUser,
      assignedTeam,
      userOptions,
      teamOptions,
      taskNameRules,
      startDateRules,
      endDateRules,
      onSubmit,
      closeDialog
    };
  },
};
</script>

<style scoped lang="scss">
.project-edit-card {
  max-width: 500px;
  margin: 0 auto;
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: $third;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #FFFFFF;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>