<template>
  <q-dialog v-model="dialogOpen" persistent backdrop-filter="blur(10px)">
    <q-card class="bg-white text-accent">
      <q-card-section>
        <q-input standout="bg-primary text-accent" outlined bg-color="primary" color="accent" text-color="accent" v-model="searchUser" label="Search User" @update:model-value="onSearchUser">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>

        <q-list bordered separator class="bg-primary">
          <q-item v-for="user in filteredUsers" :key="user.id" clickable v-ripple @click="addUserToBusiness(user)">
            <q-item-section>
              <q-item-label class="text-accent">{{ user }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>

        <q-list bordered class="q-mt-md" >
          <q-item-label header class="text-accent bg-dark">Added Members</q-item-label>
          <q-item v-for="user in addedMembers" :key="user.id" class="bg-primary">
            <q-item-section>
              <q-item-label class="text-accent">{{ user }}</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-btn flat round color="negative" icon="remove" @click="removeUserFromTeam(user)" />
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn push label="Add" color="positive" text-color="white" @click="onSubmit" v-close-popup />
        <q-btn push label="Close" color="negative" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { ref } from 'vue'
import { apiGet, apiPost } from '../utils/api-wrapper'
import { useUserStore } from 'stores/user-store';
import { useQuasar } from 'quasar';

export default {
  name: 'NewEmployee',
  props: {
    bid: {
      type: String,
      required: true
    }
  },
  setup(props, { emit }) {
    const dialogOpen = ref(true)
    const searchUser = ref('')
    const filteredUsers = ref([])
    const addedMembers = ref([])
    const userStore = useUserStore();
    const $q = useQuasar();

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

    const addUserToBusiness = (username) => {
      const currentUser = userStore.username; // Requester cannot be auto-added
      if (currentUser != username && !addedMembers.value.some(u => u === username)) {
        addedMembers.value.push(username);
      }
    }

    const removeUserFromTeam = (user) => {
      addedMembers.value = addedMembers.value.filter(u => u.id !== user.id)
    }

    const onSubmit = async () => {
      for (const employee of addedMembers.value) {
        try {
          const response = await apiPost('/new/employee/', {
            username: employee,
            business: props.bid
          });
          $q.notify({
            type: 'positive',
            message: `Employee ${employee} added successfully`,
            position: 'bottom-right'
          });
        } catch (error) {
          $q.notify({
            type: 'negative',
            message: `Error adding employee ${employee}`,
            position: 'bottom-right'
          });
        }
      }
      dialogOpen.value = false;
      emit('employee-added');
    }

    return {
      dialogOpen,
      searchUser,
      filteredUsers,
      addedMembers,
      onSearchUser,
      addUserToBusiness,
      removeUserFromTeam,
      onSubmit
    }
  }
}
</script>
