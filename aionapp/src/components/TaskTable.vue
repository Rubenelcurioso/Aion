<template>
  <div class="q-ma-none bg-white">
    <div class="text-h6 text-accent">Tasks</div>
    <q-separator color="#FF0000" inset size="2px"/>
    <q-table    
      flat
      table-class="text-accent"
      table-header-class="bg-dark text-white"
      title=""
      :rows="rows"
      :columns="columns"
      row-key="id"
      :selected-rows-label="getSelectedString"
      selection="single"
      v-model:selected="selected"
    >
    
    <template v-slot:top>
      <div>
        <q-btn-group rounded unelevated>
          <q-btn push icon="add" color="positive" @click="showDialog" label="New task" class="q-mr-none" :disable="userRolePerm < 7" />
          <q-btn push icon="edit" color="warning" @click="editSelectedRow" label="Edit selected" :disable="!selected.length || userRolePerm < 7" class="q-mr-none" />
          <q-btn push icon="delete" color="negative" @click="removeSelectedRows" label="Remove selected" :disable="!selected.length || userRolePerm < 7" />
        </q-btn-group>
      </div>
    </template>
    
    <template v-slot:body="props">
      <q-tr :props="props">
        <q-td auto-width>
          <q-checkbox v-model="props.selected" />
        </q-td>
        <q-td v-for="col in props.cols" :key="col.name" :props="props">
          <template v-if="col.name === 'priority' || col.name === 'status'">
            <BadgeTypes :label="props.row[col.field]" />
          </template>
          {{ col.name === 'name' ? props.row['name'] : '' }}
          {{ col.name === 'team' ? props.row['team'] : '' }}
          {{ col.name === 'user' ? props.row['user'] : '' }}
          {{ col.name === 'start_date' ? props.row['start_date'] : '' }}
          {{ col.name === 'end_date' ? props.row['end_date'] : '' }}
        </q-td>
      </q-tr>
    </template>

    </q-table>

    <q-dialog v-model="dialogVisible" backdrop-filter="blur(10px)">
      <TaskCreationCard @task-created="onTaskCreate" @close-d="dialogVisible = false" />
    </q-dialog>

    <q-dialog v-model="editDialogVisible" backdrop-filter="blur(10px)">
      <TaskEditCard :taskId="selected[0].id" @task-updated="onTaskEdit" @close-dialog="editDialogVisible = false" />    
    </q-dialog>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted, watch } from 'vue'
import TaskCreationCard from 'components/TaskCreationCard.vue'
import TaskEditCard from 'components/TaskEditCard.vue'
import BadgeTypes from 'components/BadgeTypes.vue'
import { apiGet, apiDelete, apiPut } from '../utils/api-wrapper'
import { useRoute } from 'vue-router'
import { useUserStore } from 'stores/user-store'
import { useQuasar } from 'quasar'

const columns = [
        {
          name: 'name',
          required: true,
          label: 'Task name',
          align: 'left',
          field: 'name',
          format: val => `${val}`,
        },
        { name: 'user', align: 'center', label: 'Assigned to', field: 'user', sortable: true },
        { name: 'start_date', label: 'Starts', field: 'start_date', sortable: true },
        { name: 'end_date', label: 'Ends', field: 'end_date', sortable: true },
        { name: 'priority', label: 'Priority', field: 'priority', sortable: true },
        { name: 'status', label: 'Status', field: 'status', sortable: true},
        { name: 'team', label: 'Team assigned', field: 'team', sortable: true},
]

export default defineComponent({
  name: 'TaskTable',
  components : {
    TaskCreationCard,
    TaskEditCard,
    BadgeTypes
    },
  setup () {
    const route = useRoute()
    const selected = ref([])
    const dialogVisible = ref(false)
    const editDialogVisible = ref(false)
    const rows = ref([])
    const store = useUserStore()
    const userRolePerm = ref(store.projects.find(project => project.id === parseInt(route.params.pid)).role_perm)
    const $q = useQuasar()

    const getSelectedString = () => {
      return selected.value.length === 0 ? '' : `${selected.value.length} record${selected.value.length > 1 ? 's' : ''} selected of ${rows.value.length}`
    }

    const showDialog = () => {
      dialogVisible.value = true
    }

    const fetchTasks = async () => {
      try {
        const response = await apiGet('project/'+route.params.pid+'/tasks/');
        rows.value = response;
      } catch (error) {
        console.error('Error fetching tasks:', error);
      }
    }

    const removeSelectedRows = async () => {
      try {
        for (const row of selected.value) {
          await apiDelete(`/remove/task/${row.id}/`);
        }
        await fetchTasks();
        selected.value = [];
        $q.notify({ type: 'positive', message: 'Tasks removed successfully', position: 'bottom-right' })
      } catch (error) {
        console.error('Error removing tasks:', error);
        $q.notify({ type: 'negative', message: 'Error removing tasks', position: 'bottom-right' })
      }
    }

    const editSelectedRow = () => {
      if (selected.value.length === 1) {
        editDialogVisible.value = true;
      }
    }

    const onTaskEdit = async () => {
      await fetchTasks();
      editDialogVisible.value = false;
      selected.value = [];
      $q.notify({ type: 'positive', message: 'Task updated successfully', position: 'bottom-right' })
    }

    const onTaskCreate = async () => {
      await fetchTasks();
      dialogVisible.value = false;
      $q.notify({ type: 'positive', message: 'Task created successfully', position: 'bottom-right' })
    }

    onMounted(() => {
      fetchTasks()
    })

    return {
      selected,
      getSelectedString,
      columns,
      rows,
      dialogVisible,
      editDialogVisible,
      showDialog,
      removeSelectedRows,
      editSelectedRow,
      onTaskEdit,
      onTaskCreate,
      userRolePerm,
    }
  }
});
</script>