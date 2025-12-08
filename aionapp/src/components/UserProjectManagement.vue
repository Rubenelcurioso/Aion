<template>
  <div>
    <div class="text-h6 text-accent">Users</div>
    <q-separator color="#FF0000" inset size="2px"/>
    <q-table
      flat
      table-class="text-accent"
      table-header-class="bg-dark text-white"
      title=""
      :rows="users"
      :columns="columns"
      row-key="id"
    >
      <template v-slot:top-right>
        <q-btn 
          push
          icon="settings" 
          color="info" 
          @click="showDialog" 
          label="Manage" 
          class="q-mr-sm" 
          :disable="userRolePerm < 31"
        />
      </template>

      <template v-slot:body-cell-Avatar="props">
        <q-td :props="props">
          <q-avatar size="sm" color="primary" text-color="white">
            {{ props.row.username.charAt(0).toUpperCase() }}
          </q-avatar>
        </q-td>
      </template>
    </q-table>
  </div>
  <q-dialog v-model="dialogVisible" backdrop-filter="blur(10px)">
      <NewUserProject 
      :pid=props.pid 
      :users=users
      @user-mod="onUserMod" 
      @close-dialog="dialogVisible = false" />
  </q-dialog>
</template>

<script>
import { onMounted, ref } from 'vue';
import NewUserProject from 'components/NewUserProject.vue';
import { useUserStore } from 'stores/user-store';
import { apiGet } from '../utils/api-wrapper';

export default {
  name: 'UserProjectManagement',
  components: {
    NewUserProject
  },
  props: {
    pid: {
      type: Number,
      required: true
    }
  },
  setup(props){
    const dialogVisible = ref(false);
    const userStore = useUserStore();
    const users = ref([]);
    const userRolePerm = ref(userStore.projects.find(project => project.id === parseInt(props.pid)).role_perm)

    const showDialog = () => {
      dialogVisible.value = true;
    };

    const onUserMod = () => {
      dialogVisible.value = false;
      fetchUserProject();
    };

    const columns = [
      { name: 'Avatar', field: 'avatar', label: 'Avatar', align: 'left' },
      { name: 'Username', field: 'username', label: 'Username', align: 'left' },
      { name: 'Role', field: 'role_name', label: 'Role', align: 'left' }
    ];

    const fetchUserProject = async () => {
      try {
        const response = await apiGet(`/project/${props.pid}/users/`);
        users.value = response;
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    }

    onMounted(fetchUserProject);

    return {
      users,
      columns,
      dialogVisible,
      showDialog,
      onUserMod,
      props,
      userStore,
      userRolePerm
    };
  }
}
</script>
