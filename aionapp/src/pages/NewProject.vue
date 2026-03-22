<template>
  <q-page class="flex flex-center bg-primary text-accent">
    <q-stepper
      class="bg-white"
      v-model="step"
      color="accent"
      animated
      
    >
      <q-step
        color="dark"
        :name="1"
        title="Project Details"
        icon="assignment"
        :done="step > 1"
      >
        <q-input outlined class="q-ma-md" bg-color="primary" color="accent" text-color="accent" v-model="projectName" label="Project Name" />
        <q-input outlined class="q-ma-md" bg-color="primary" color="accent" text-color="accent" v-model="projectDescription" type="textarea" label="Project Description" />
        <q-input outlined class="q-ma-md" bg-color="primary"  color="accent" text-color="accent" v-model="startDate" type="date" label="Start Date" />
        <q-input outlined class="q-ma-md" bg-color="primary" color="accent" text-color="accent" v-model="endDate" type="date" label="End Date" />
        
        <q-stepper-navigation>
          <q-btn unelevated text-color="white" @click="step = 2" color="positive" label="Next" />
        </q-stepper-navigation>
      </q-step>

      <q-step
        color="dark"
        :name="2"
        title="Add Users"
        icon="people"
        :done="step > 2"
      >
        <q-input outlined bg-color="primary" color="accent" text-color="accent" v-model="searchUser" label="Search User" @update:model-value="onSearchUser" >
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>

        <q-list  separator class="bg-primary">
          <q-item v-for="user in filteredUsers" :key="user.id" clickable v-ripple @click="addUserToProject(user)">
            <q-item-section>
              <q-item-label class="text-accent">{{ user }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>

        <q-list  class="q-mt-md" >
          <q-item-label header class="text-accent bg-dark">Added Users</q-item-label>
          <q-item v-for="user in addedUsers" :key="user.id" class="bg-primary">
            <q-item-section>
              <q-item-label class="text-accent">{{ user.username }}</q-item-label>
              <q-select
                v-model="model"
                :options="roleOptions"
                label="Role"
                dense
                options-dense
                color="accent"
                popup-content-class="text-accent bg-primary"
                style="min-width: 50px;"
              />
            </q-item-section>
            <q-item-section side>
              <q-btn flat round color="negative" icon="remove" @click="removeUserFromProject(user)" />
            </q-item-section>
          </q-item>
        </q-list>

        <q-stepper-navigation>
          <q-btn  unelevated text-color="white" @click="step = 1" color="negative" label="Back" class="q-mr-sm" />
          <q-btn unelevated text-color="white" @click="createProject" color="positive" label="Create Project" />
        </q-stepper-navigation>
      </q-step>
    </q-stepper>
  </q-page>
</template>

<script>
import { ref } from 'vue'
import { apiPost, apiGet } from '../utils/api-wrapper'
import { useUserStore } from 'stores/user-store';
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'

export default {
  name: 'NewProject',
  setup() {
    const $q = useQuasar()
    const step = ref(1)
    const projectName = ref('')
    const projectDescription = ref('')
    const startDate = ref('')
    const endDate = ref('')
    const searchUser = ref('')
    const filteredUsers = ref([])
    const addedUsers = ref([])
    const roleOptions = ref([])
    const model = ref(null)

    const fetchRoles = async () => {
      try {
        const response = await apiGet('/roles/');
        roleOptions.value = response
          .filter(role => role.name.toLowerCase() !== 'owner')
          .map(role => ({ value: role.id, label: role.name }));      
      } 
        catch (error) {
        console.error('Error fetching roles:', error);
      }
    }

    fetchRoles();
    const store = useUserStore()
    const router = useRouter()

    const onSearchUser = async (val) => {
      if (val.length >= 3) {
        try {
          const response = await apiGet('/username/' + encodeURIComponent(val) + '/');
          filteredUsers.value = response;
        } catch (error) {
          console.error('Error searching for users:', error);
        }
      } else {
        filteredUsers.value = [];
      }
    }

    const addUserToProject = (username) => {
      const currentUser = store.username; 
      if (username !== currentUser && !addedUsers.value.some(u => u.username === username)) {
        addedUsers.value.push({ username, role: roleOptions.value[0].value })
      }
    }

    const removeUserFromProject = (user) => {
      addedUsers.value = addedUsers.value.filter(u => u.id !== user.id)
    }

    const createProject = async () => {
      try {
        const projectData = {
          name: projectName.value,
          description: projectDescription.value,
          start_date: startDate.value,
          end_date: endDate.value,
          owner_id: store.uid,
        };

        const projectResponse = await apiPost('/new/project/', projectData);

        if (projectResponse && projectResponse.id) {
          for (const user of addedUsers.value) {
            const userProjectRoleData = {
              user: user.username,
              project: projectResponse.id,
              role: user.role
            };
            await apiPost('/userprojectrole/', userProjectRoleData);
          }
          $q.notify({
            type: 'positive',
            message: 'Project created successfully!',
            position: 'bottom-right'
          });
          await router.push(`/home/${store.uid}/project/${projectResponse.id}/`);
        } else {
          throw new Error('Failed to create project');
        }
      } catch (error) {
        console.error('Error creating project:', error);
        $q.notify({
          type: 'negative',
          message: 'Error creating project: ' + error.message,
          position: 'bottom-right'
        });
      }
    }

    return {
      step,
      projectName,
      projectDescription,
      startDate,
      endDate,
      searchUser,
      filteredUsers,
      addedUsers,
      onSearchUser,
      addUserToProject,
      removeUserFromProject,
      createProject,
      model,
      roleOptions
    }
  }
}
</script>
