<template>
  <q-dialog v-model="dialogOpen" persistent>
    <q-card class="bg-white text-white">
      <q-card-section>
        <q-input bg-color="primary" outlined label-color="accent" v-model="searchUser" label="Search User" @update:model-value="onSearchUser">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>

        <q-list bordered separator class="bg-white text-accent">
          <q-item v-for="user in filteredUsers" :key="user.id" clickable v-ripple @click="addUserToProject(user)">
            <q-item-section>
              <q-item-label>{{ user }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>

        <q-list bordered class="q-mt-md bg-primary">
          <q-item-label header class="text-accent">Added members</q-item-label>
          <q-separator color="#FF0000" inset size="2px" class="q-ma-sm"/>
          <q-item v-for="user in addedMembers" :key="user.id" class="bg-primary">
            <q-item-section>
              <q-item-label class="text-accent">{{ user.username }}</q-item-label>
              <q-select
                v-model="user.role"
                :options="roleOptions"
                option-value="value"
                option-label="label"
                label="Role"
                dense
                options-dense
                outlined
                bg-color="primary"
                color="accent"
                popup-content-class="text-accent bg-primary"
                style="min-width: 100px;"
                @update:model-value="updateUserRole(user)"
              />
            </q-item-section>
            <q-item-section side>
              <q-btn flat round color="negative" icon="remove" @click="removeUserFromProject(user)" />
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn push label="Save" color="positive" @click="onSubmit" />
        <q-btn push label="Close" color="negative" v-close-popup @click="closeDialog" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { ref, onMounted } from 'vue'
import { apiGet, apiPut, apiDelete } from '../utils/api-wrapper'
import { useUserStore } from 'stores/user-store';
import { useQuasar } from 'quasar';

export default {
  name: 'NewUserProject',
  props: {
    pid: {
      type: Number,
      required: true
    },
    users: {
      type: Array,
      required: true
    }
  },
  setup(props, { emit }) {
    const dialogOpen = ref(true)
    const searchUser = ref('')
    const filteredUsers = ref([])
    const addedMembers = ref([])
    const userStore = useUserStore();
    const roleOptions = ref([])
    const model = ref(null)
    const $q = useQuasar();

    const fetchRoles = async () => {
      try {
        const obj_response = await apiGet('/roles/');
        roleOptions.value = obj_response
          .filter(obj_role => obj_role.name.toLowerCase() !== 'owner')
          .map(obj_role => ({ value: obj_role.id, label: obj_role.name }));
      } catch (obj_error) {
        $q.notify({
          type: 'negative',
          message: 'Error fetching roles',
          position: 'bottom-right'
        });
      }
    }

    fetchRoles();

    const onSearchUser = async (str_val) => {
      if (str_val.length >= 3) {
        try {
          const obj_response = await apiGet('/username/' + encodeURIComponent(str_val) + '/');
          filteredUsers.value = obj_response;
        } catch (obj_error) {
          console.error('Error searching for users:', obj_error);
        }
      } else {
        filteredUsers.value = [];
      }
    }

    const addUserToProject = (user) => {
      const currentUser = userStore.username;
      if (currentUser !== user && !addedMembers.value.some(u => u.username === user)) {
        const defaultRole = roleOptions.value[2];
        addedMembers.value.push({username: user, role: defaultRole});
      }
    }

    const removeUserFromProject = async (obj_user) => {
      const userStore = useUserStore();
      const int_projectRolePerm = userStore.projects.find(obj_project => obj_project.id === props.pid)?.role_perm;

      if (int_projectRolePerm >= 31) {
        const obj_userToRemove = addedMembers.value.find(obj_u => obj_u.username === obj_user.username);
        if (obj_userToRemove && int_projectRolePerm > obj_userToRemove.role_perm) {
          try {
            const obj_response = await apiDelete(`/remove/user/${obj_user.username}/${props.pid}/`);
            addedMembers.value = addedMembers.value.filter(obj_u => obj_u.username !== obj_user.username);
            emit('user-mod');
            $q.notify({
              type: 'positive',
              message: `User ${obj_user.username} removed successfully`,
              position: 'bottom-right'
            });
          } catch (obj_error) {
            $q.notify({
              type: 'negative',
              message: `Error removing user ${obj_user.username}`,
              position: 'bottom-right'
            });
          }
        } else {
          console.warn('Cannot remove user with equal or higher role permission');
        }
      } else {
        console.warn('Insufficient permissions to remove user from project');
      }
    }

    const updateUserRole = (user) => {
      const updatedUser = addedMembers.value.find(u => u.username === user.username);
      if (updatedUser) {
        updatedUser.role = user.role.label;
      }
    }

    const onSubmit = async () => {
      for (const obj_user of addedMembers.value) {
        if(obj_user.role !== undefined){
          const obj_role_id = roleOptions.value.find(obj_option => obj_option.label === obj_user.role);
          if(obj_role_id !== undefined){
            try {
              const obj_userData = {
              user: obj_user.username,
              project: props.pid,
              role: obj_role_id.value
              };
              const obj_response = await apiPut('/userprojectrole/update/', obj_userData);
              $q.notify({
                type: 'positive',
                message: `User ${obj_user.username} added successfully`,
                position: 'bottom-right'
              });
            } catch (obj_error) {
              $q.notify({
                type: 'negative',
                message: `Error adding user ${obj_user.username} to project`,
                position: 'bottom-right'
              });
            }
          }
        }
      }
      dialogOpen.value = false;
      emit('user-mod');
    }

    const closeDialog = () => {
      dialogOpen.value = false;
      emit('close-dialog');
    }

    const updateAddedMembers = () => {
      addedMembers.value = props.users.map(user => ({
        ...user,
        role: roleOptions.value.find(role => role.value === user.role) || roleOptions.value[2]
      }));
    }

    onMounted(() => {
      updateAddedMembers();
    });

    return {
      dialogOpen,
      searchUser,
      filteredUsers,
      addedMembers,
      onSearchUser,
      addUserToProject,
      removeUserFromProject,
      updateUserRole,
      onSubmit,
      closeDialog,
      model,
      roleOptions
    }
  }
}
</script>
