<template>
  <q-dialog v-model="dialogOpen" persistent backdrop-filter="blur(10px)">
    <q-card class="bg-dark text-accent">
      <q-stepper
        v-model="step"
        color="accent"
        animated
        dark
        class="bg-white"
      >
      <q-step
        color="dark"
        :name="1"
        title="Team Details"
        icon="people"
        :done="step > 1"
      >
        <q-input outlined bg-color="primary" color="accent" text-color="accent" v-model="teamName" label="Team Name" :rules="[
          val => val && val.length > 0 || 'Team name is required',
          val => val.length <= 255 || 'Team name too long'
        ]" />
        <q-input outlined bg-color="primary" color="accent" text-color="accent" v-model="teamDescription" type="textarea" label="Team Description" />
        
        <q-stepper-navigation>
          <q-btn unelevated @click="step = 2" color="positive" text-color="white" label="Next" />
        </q-stepper-navigation>
      </q-step>

      <q-step
        color="dark"
        :name="2"
        title="Add Members"
        icon="person_add"
        :done="step > 2"
      >
        <q-input bg-color="primary" outlined label-color="accent" color="accent" text-color="accent" v-model="searchUser" label="Search User" @update:model-value="onSearchUser">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>

        <q-list  separator class="bg-primary">
          <q-item v-for="user in filteredUsers" :key="user.id" clickable v-ripple @click="addUserToTeam(user)">
            <q-item-section>
              <q-item-label class="text-accent">{{ user }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>

        <q-list  class="q-mt-md bg-primary">
          <q-item-label header class="text-accent bg-dark">Added Members</q-item-label>
          <q-item v-for="user in addedMembers" :key="user.id">
            <q-item-section>
              <q-item-label class="text-accent">{{ user }}</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-btn  flat round color="negative" icon="remove" @click="removeUserFromTeam(user)" />
            </q-item-section>
          </q-item>
        </q-list>

        <q-stepper-navigation>
          <q-btn unelevated @click="step = 1" color="negative" text-color="white" label="Back" class="q-mr-sm" />
          <q-btn unelevated @click="step = 3" color="positive" text-color="white" label="Next" />
        </q-stepper-navigation>
      </q-step>

      <q-step
        color="dark"
        :name="3"
        title="Confirmation"
        icon="check"
        :done="step > 3"
      >
        <q-card class="bg-primary">
          <q-card-section class="text-accent">
            <div class="text-h6">Team Details</div>
            <div><strong>Name:</strong> {{ teamName }}</div>
            <div><strong>Description:</strong> {{ teamDescription }}</div>
          </q-card-section>
        </q-card>

        <q-stepper-navigation>
          <q-btn unelevated @click="step = 1" color="negative" text-color="white" label="Back" class="q-mr-sm" />
          <q-btn unelevated @click="createTeam" color="positive" text-color="white" label="Create Team" />
        </q-stepper-navigation>
      </q-step>
    </q-stepper>
    <q-card-actions align="right" class="bg-dark">
      <q-btn  unelevated label="Close" color="negative" v-close-popup />
    </q-card-actions>
  </q-card>
  </q-dialog>
</template>

<script>
import { ref } from 'vue'
import { apiPost, apiGet, apiPut } from '../utils/api-wrapper'
import { useUserStore } from 'stores/user-store';
import { useQuasar } from 'quasar';

export default {
  name: 'NewTeam',
  props: {
    bid: {
      type: String,
      required: true
    }
  },
  setup(props, { emit }) {
    const dialogOpen = ref(true)
    const step = ref(1)
    const teamName = ref('')
    const teamDescription = ref('')
    const searchUser = ref('')
    const filteredUsers = ref([])
    const addedMembers = ref([])

    const $q = useQuasar();

    const onSearchUser = async (str_val) => {
      if (str_val.length >= 3) {
        try {
          const obj_response = await apiGet('/employees/username/'+ props.bid + '/' + encodeURIComponent(str_val) + '/');
          filteredUsers.value = obj_response;
        } catch (obj_error) {
          console.error('Error searching for users:', obj_error);
        }
      } else {
        filteredUsers.value = [];
      }
    }

    const addUserToTeam = (username) => {
      if (!addedMembers.value.some(u => u === username)) {
        addedMembers.value.push(username);
      }
    }

    const removeUserFromTeam = (user) => {
      addedMembers.value = addedMembers.value.filter(u => u.id !== user.id)
    }

    const store = useUserStore()

    const createTeam = async () => {
      try {
        const obj_teamData = {
          name: teamName.value,
          description: teamDescription.value,
          business: props.bid
        };

        const obj_teamResponse = await apiPost('/new/team/', obj_teamData);

        if (obj_teamResponse && obj_teamResponse.id) {
          for (const str_username of addedMembers.value) {
            const obj_memberData = {
              business: props.bid,
              username: str_username,
              team: obj_teamResponse.id
            };
            await apiPut('/new/member/', obj_memberData);
          }
          dialogOpen.value = false;
          emit('team-created')
          $q.notify({
            type: 'positive',
            message: 'Team created successfully',
            position: 'bottom-right'
          });
        } else {
          throw new Error('Failed to create team');
        }
      } catch (obj_error) {
        console.error('Error creating team:', obj_error);
        $q.notify({
          type: 'negative',
          message: 'Error creating team',
          position: 'bottom-right'
        });
        // Handle error (e.g., show error message to user)
      }
    }

    return {
      dialogOpen,
      step,
      teamName,
      teamDescription,
      searchUser,
      filteredUsers,
      addedMembers,
      onSearchUser,
      addUserToTeam,
      removeUserFromTeam,
      createTeam
    }
  }
}
</script>
