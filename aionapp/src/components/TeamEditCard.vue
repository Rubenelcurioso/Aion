<template>
  <q-card class="team-edit-card bg-primary text-accent">
    <q-toolbar>
      <q-toolbar-title>Edit Team</q-toolbar-title>
      <q-btn flat round dense icon="close" @click="closeDialog" />
    </q-toolbar>

    <q-stepper
      v-model="step"
      color="accent"
      animated
      class="bg-white"
    >
      <q-step
        color="dark"
        :name="1"
        title="Team Details"
        icon="people"
        :done="step > 1"
      >
        <q-input standout="bg-primary text-accent" outlined bg-color="primary" color="accent" text-color="accent" v-model="teamName" label="Team Name" :rules="teamNameRules" />
        <q-input standout="bg-primary text-accent" outlined bg-color="primary" color="accent" text-color="accent" v-model="teamDescription" type="textarea" label="Team Description" />
        
        <q-stepper-navigation>
          <q-btn push text-color="white" @click="step = 2" color="positive" label="Next" />
        </q-stepper-navigation>
      </q-step>

      <q-step
        color="dark"
        :name="2"
        title="Add Members"
        icon="person_add"
        :done="step > 2"
      >
        <q-input standout="bg-primary text-accent" outlined bg-color="primary" color="accent" text-color="accent" v-model="searchUser" label="Search User" @update:model-value="onSearchUser">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>

        <q-list bordered separator class="bg-primary">
          <q-item v-for="user in filteredUsers" :key="user.id" clickable v-ripple @click="addUserToTeam(user)">
            <q-item-section>
              <q-item-label class="text-accent">{{ user }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>

        <q-list bordered class="q-mt-md">
          <q-item-label header class="text-accent bg-primary">Added Members</q-item-label>
          <q-item v-for="user in addedMembers" :key="user.id" class="bg-primary">
            <q-item-section>
              <q-item-label>{{ user }}</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-btn flat round color="negative" icon="remove" @click="removeUserFromTeam(user)" />
            </q-item-section>
          </q-item>
        </q-list>

        <q-stepper-navigation>
          <q-btn push text-color="white" @click="step = 1" color="negative" label="Back" class="q-mr-sm" />
          <q-btn push text-color="white" @click="step = 3" color="positive" label="Next" />
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
          <q-btn push text-color="white" @click="step = 1" color="negative" label="Back" class="q-mr-sm" />
          <q-btn push text-color="white" @click="onSubmit" color="positive" label="Update Team" />
        </q-stepper-navigation>
      </q-step>
    </q-stepper>
  </q-card>
</template>

<script>
import { ref, onMounted } from 'vue';
import { apiGet, apiPut } from '../utils/api-wrapper';

export default {
  name: 'TeamEditCard',
  props: {
    team: {
      type: Number,
      required: true
    },
    bid: {
      type: Number,
      required: true
    }
  },
  setup(props, { emit }) {
    const step = ref(1);
    const teamName = ref('');
    const teamDescription = ref('');
    const searchUser = ref('');
    const filteredUsers = ref([]);
    const addedMembers = ref([]);

    const loadTeamData = async () => {
      try {
        const response = await apiGet(`/team/${props.bid}/${props.team}/`);
        teamName.value = response.name;
        teamDescription.value = response.description;
        const res = await apiGet(`/employees/${props.bid}/${props.team}/`);
        addedMembers.value = res.map(member => member.username);
      } catch (error) {
        console.error('Error loading team data:', error);
      }
    };

    const onSearchUser = async (val) => {
      if (val.length >= 3) {
        try {
          const response = await apiGet('/employees/username/'+ props.bid + '/' + encodeURIComponent(val) + '/');
          filteredUsers.value = response;
        } catch (error) {
          console.error('Error searching for users:', error);
        }
      } else {
        filteredUsers.value = [];
      }
    };

    const addUserToTeam = async (username) => {
      if (!addedMembers.value.some(u => u === username)) {
        addedMembers.value.push(username);
        const memberData = {
          business: props.bid,
          username: username,
          team: props.team
        };
        await apiPut(`/new/member/`, memberData);
      }
    };

    const removeUserFromTeam = async (user) => {
      const memberData = {
        business: props.bid,
        username: user,
        team: null
      };
      await apiPut(`/new/member/`, memberData);
      addedMembers.value = addedMembers.value.filter(u => u.id !== user.id);
    };

    onMounted(() => {
      loadTeamData();
    });

    const teamNameRules = [
      val => !!val || 'Team name is required'
    ];

    const onSubmit = async () => {
      try {
        const teamData = {
          id: props.team,
          name: teamName.value,
          description: teamDescription.value,
        };
        await apiPut(`/team/update/`, teamData);
        emit('team-updated');
        closeDialog();
      } catch (error) {
        console.error('Error updating team:', error);
      }
    };

    const closeDialog = () => {
      emit('close-dialog');
    };

    return {
      step,
      teamName,
      teamDescription,
      searchUser,
      filteredUsers,
      addedMembers,
      teamNameRules,
      onSearchUser,
      addUserToTeam,
      removeUserFromTeam,
      onSubmit,
      closeDialog
    };
  },
};
</script>

<style scoped lang="scss">
.team-edit-card {
  max-width: 500px;
  margin: 0 auto;
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: $dark;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
