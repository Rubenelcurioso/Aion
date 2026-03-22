<template>
  <q-card class="project-edit-card bg-white">
    <q-toolbar class="bg-dark text-white">
      <q-toolbar-title>Project edit</q-toolbar-title>
      <q-btn flat round dense icon="close" @click="closeDialog" color="white" />
    </q-toolbar>

    <q-form @submit="onSubmit" class="q-gutter-md">
      <q-card-section class="q-ml-xs q-mt-md q-ma-none">
        <q-input outlined bg-color="primary" color="accent" v-model="projectName" label="Project name" :rules="projectNameRules" class="text-accent" />
      </q-card-section>

      <q-card-section class="q-ml-xs q-ma-none">
        <div class="row q-col-gutter-md">
          <div class="col-6">
            <q-input outlined bg-color="primary" color="accent" v-model="startDate" label="Start date" type="date" :rules="startDateRules" class="text-accent" />
          </div>
          <div class="col-6">
            <q-input outlined bg-color="primary" color="accent" v-model="endDate" label="End date" type="date" :rules="endDateRules" class="text-accent" />
          </div>
        </div>
      </q-card-section>

      <q-card-section class="q-ml-xs q-ma-none">
        <q-select
          outlined
          bg-color="primary"
          class="text-accent"
          v-model="selectedBusiness"
          :options="businesses"
          label="Select an organization"
          option-value="value"
          option-label="label"
          emit-value
          map-options
          color="accent"
          popup-content-class="text-accent bg-primary"
        />
      </q-card-section>

      <q-card-section class="q-ml-xs q-ma-none">
        <q-input outlined bg-color="primary" class="text-accent" color="accent" v-model="description" label="Description" type="textarea"/>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn unelevated text-color="white" type="submit" color="warning" label="Update" />
      </q-card-actions>
    </q-form>
  </q-card>
</template>

<script>
import { ref, onMounted, inject } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useUserStore } from 'stores/user-store';
import { apiGet, apiPut } from '../utils/api-wrapper';

export default {
  name: 'ProjectEditCard',
  props: {
    projectId: {
      type: String,
      required: true
    }
  },
  setup(props, { emit }) {
    const projectName = ref('');
    const startDate = ref('');
    const endDate = ref('');
    const description = ref('');
    const projectManager = ref(null);
    const route = useRoute();
    const store = useUserStore();
    const userOptions = ref([]);
    const refresh = inject('refresh');

    const userStore = useUserStore();
    const businesses = ref([]);
    const selectedBusiness = ref(null);

    const loadProjectData = async () => {
      try {
        const obj_response = await apiGet(`/project/${props.projectId}/`);
        projectName.value = obj_response.name;
        startDate.value = obj_response.start_date;
        endDate.value = obj_response.end_date;
        description.value = obj_response.description;
        selectedBusiness.value = obj_response.business.id;
      } catch (obj_error) {
        console.error('Error loading project data:', obj_error);
      }
    };

    onMounted(() => {
      loadProjectData();
      businesses.value = userStore.businesses.map(business => ({
        value: business.id,
        label: business.name
      }));
    });

    const projectNameRules = [
      val => !!val || 'Project name is required'
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
      if(store.projects.find(obj_project => obj_project.id === props.projectId).role_perm < 63){
        emit('project-updated');
        closeDialog();
      }else{
          try {
          const obj_projectData = {
            project_id: props.projectId,
            name: projectName.value,
            start_date: startDate.value,
            end_date: endDate.value,
            description: description.value,
            project_manager: projectManager.value,
            business: selectedBusiness.value
          };
          await apiPut(`/project/update/`, obj_projectData);
          emit('project-updated');
          closeDialog();
        } catch (obj_error) {
          console.error('Error updating project:', obj_error);
        }
      }

    };

    const closeDialog = () => {
      emit('close-dialog');
    };

    return {
      projectName,
      startDate,
      endDate,
      description,
      projectManager,
      userOptions,
      businesses,
      selectedBusiness,
      projectNameRules,
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
  background: $purple-3;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: $purple-4;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>