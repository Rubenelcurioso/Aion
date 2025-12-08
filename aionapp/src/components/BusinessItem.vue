<template>
   <q-expansion-item
        expand-separator
        icon="business"
        label="Businesses"
        caption="My businesses"
        default-opened
        class="text-accent"
    >
        <q-list>
            <q-item v-for="business in businesses" :key="business.id" clickable v-ripple :to="`/home/${store.uid}/business/${business.id}`">
              <q-item-section>
                    <q-item-label class="text-accent">{{ business.name }}</q-item-label>
                </q-item-section>
                <q-item-section side v-if="business.owner === store.uid">
                    <q-btn flat round color="negative" icon="close" @click.stop="confirmDelete(business.id)">
                        <q-tooltip>Delete business</q-tooltip>
                    </q-btn>
                </q-item-section>
            </q-item>
        </q-list>

        <q-item clickable v-ripple to="/new/business">
            <q-item-section avatar>
                <q-icon class="text-positive" name="add" color="primary" />
            </q-item-section>
            <q-item-section class="text-positive">New business</q-item-section>
        </q-item>

    </q-expansion-item>

    <q-dialog v-model="confirmDeleteDialog">
      <q-card>
        <q-card-section class="row items-center">
          <span class="q-ml-sm">Are you sure you want to delete this business?</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="warning" v-close-popup />
          <q-btn flat label="Delete" color="negative" @click="deleteBusiness" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
</template>

<script>
import { ref, onMounted } from 'vue'
import { apiGet, apiDelete } from '../utils/api-wrapper'
import { useUserStore } from 'stores/user-store'

export default {
  name: 'BusinessItem',
  setup() {
    const businesses = ref([])
    const store = useUserStore()
    const confirmDeleteDialog = ref(false)
    const businessToDelete = ref(null)

    const fetchBusinesses = async () => {
      try {
        const obj_response = await apiGet('/user/'+`${store.uid}`+'/businesses/')
        businesses.value = obj_response
        store.setBusinesses(obj_response)
      } catch (obj_error) {
        console.error('Error fetching businesses:', obj_error)
      }
    }

    const confirmDelete = (businessId) => {
      businessToDelete.value = businessId
      confirmDeleteDialog.value = true
    }

    const deleteBusiness = async () => {
      try {
        await apiDelete(`/remove/business/${businessToDelete.value}/`)
        await fetchBusinesses()
      } catch (obj_error) {
        console.error('Error deleting business:', obj_error)
      }
    }

    onMounted(fetchBusinesses)

    return {
      store,
      businesses,
      confirmDeleteDialog,
      confirmDelete,
      deleteBusiness
    }
  }
}
</script>

<style scoped>
.q-item {
  border-radius: 8px;
  margin-bottom: 4px;
}
</style>
