<template>
  <q-page class="q-pa-md bg-primary">
    <q-card class="bg-white text-accent generic-border-radius">
      <q-card-section>
        <div class="text-center">
          <h3 class="text-accent q-mb-sm">{{ projectName }}</h3>     
          <h5 class="courier-font q-mb-sm">{{ description }}</h5>
        </div>
      </q-card-section>

      <q-separator inset size="2px"/>

      <q-card-section>
      <q-tabs
        v-model="tab"
        class="text-white bg-dark justify-center q-mb"
        align="center"
        indicator-color="dark"
        active-color="accent"
        active-bg-color="white"
      >
        <q-tab name="properties" label="Properties" />
        <q-tab name="tasks" label="Tasks" />
        <q-tab name="userManagement" label="User Management" />
        <q-tab name="charts" label="Charts" />
      </q-tabs>

      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="properties" class="bg-white">
          <ProjectInfo
            :pid=Number(route.params.pid)
          />
        </q-tab-panel>

        <q-tab-panel name="tasks" class="bg-white">
          <TaskTable />      
        </q-tab-panel>
        <q-tab-panel name="userManagement" class="bg-white">
          <UserProjectManagement
            :pid=Number(route.params.pid)
          />
        </q-tab-panel>


        <q-tab-panel name="charts" class="bg-white">
          <ApexCharts
            :pid=Number(route.params.pid)
          />
        </q-tab-panel>
      </q-tab-panels>
    </q-card-section>
  </q-card>
  </q-page>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import TaskTable from 'components/TaskTable.vue';
import ProjectInfo from 'components/ProjectInfo.vue';
import UserProjectManagement from 'components/UserProjectManagement.vue';
import ApexCharts from 'components/ApexCharts.vue';
import { apiGet } from '../utils/api-wrapper';

export default defineComponent({
  name: 'ProjectPage',
  components: {
    TaskTable,
    ProjectInfo,
    UserProjectManagement,
    ApexCharts
  },
  setup() {
    const route = useRoute();
    const tab = ref('properties');
    const project_id = Number(route.params.pid);
    const projectName = ref('');
    const description = ref('');

    const fetchProjectData = async () => {
      const response = await apiGet('/project/' + project_id + '/');
      projectName.value = response.name;
      description.value = response.description;
    };

    onMounted(() => {
      fetchProjectData();
    });

    return {
      tab,
      route,
      projectName,
      description
    };
  }
});
</script>
