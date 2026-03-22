<template>
  <div class="bg-white">
    <div class="text-h6 text-accent">Project properties</div>
    <q-separator inset size="2px"/>
    <p class="text-accent q-mt-md q-mb-none sans-serif">Created at</p>
    <q-input outlined v-model="creationDate" label="" class="text-accent bg-primary" readonly/>
    <p class="text-accent q-mt-sm q-mb-none sans-serif">End date</p>
    <q-input outlined v-model="endingDate" label=" " class="text-accent bg-primary" readonly/>
    <p class="text-accent q-mt-sm q-mb-none sans-serif">Progress: {{ progression }}%</p>
    <q-linear-progress :value="progression/100" size="20px" rounded color="info" class="q-mt-sm q-mb-sm" />
    <p class="text-accent q-mt-sm q-mb-none sans-serif">Business</p>
    <q-input outlined v-model="businessName" label=" " class="text-accent bg-primary generic-border-radius" readonly/>
    <q-btn unelevated label="Edit Project" color="warning" @click="editProjectDialog" class="text-accent q-mt-md" />
  </div>

  <q-dialog v-model="editDialogVisible" backdrop-filter="blur(10px)">
      <ProjectEditCard
        :projectId=project_id
        @project-updated="onProjectUpdated"
        @close-dialog="editDialogVisible = false"
      />
    </q-dialog>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import { useUserStore } from 'stores/user-store';
import ProjectEditCard from 'components/ProjectEditCard.vue';
import { apiGet } from '../utils/api-wrapper';
import { useQuasar } from 'quasar';

export default defineComponent({
  name: 'ProjectInfo',
  props: {
    pid: Number
  },
  components:{
    ProjectEditCard
  },
  setup(props){
    const project_id = props.pid;
    const description = ref('');
    const creationDate = ref('');
    const endingDate = ref('');
    const progression = ref(0.00);
    const businessName = ref('');
    const editDialogVisible = ref(false);
    const store = useUserStore();
    const $q = useQuasar();

    const fetchProjectData = async () => {
      try {
        const obj_response = await apiGet('/project/'+project_id+'/');
        description.value = obj_response.description;
        creationDate.value = obj_response.start_date;
        endingDate.value = obj_response.end_date;
        progression.value = obj_response.progress;
        businessName.value = obj_response.business_name;
      } catch (obj_error) {
        $q.notify({
          type: 'negative',
          message: 'Error fetching project data',
          position: 'bottom-right'
        });
      }
    };

    onMounted(() => {
      fetchProjectData();
    });

    const editProjectDialog = () => {
      if(store.projects.find(obj_project => obj_project.id === project_id).role_perm >= 63){
        editDialogVisible.value = true;
      } else {
        $q.notify({
          type: 'warning',
          message: 'Insufficient permissions to edit project',
          position: 'bottom-right'
        });
      }
    };

    const onProjectUpdated = () => {
      editDialogVisible.value = false;
      fetchProjectData();
      $q.notify({
        type: 'positive',
        message: 'Project updated successfully',
        position: 'bottom-right'
      });
    }

    return{
      description,
      creationDate,
      endingDate,
      progression,
      businessName,
      editDialogVisible,
      editProjectDialog,
      onProjectUpdated,
      project_id
    }
  }
});
</script>
