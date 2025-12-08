<template>
    <q-btn flat round>
      <q-avatar size="26px" color="blue">
        {{ store.username.charAt(0).toUpperCase() }}
      </q-avatar>
      <q-menu>
        <q-list style="min-width: 150px">
          <q-item clickable v-close-popup @click="openSettings">
            <q-item-section>Settings</q-item-section>
          </q-item>
          <q-item clickable v-close-popup @click="logout">
            <q-item-section>Log out</q-item-section>
          </q-item>
        </q-list>
      </q-menu>
    </q-btn>
  </template>

  <script>
 import { useRouter } from 'vue-router'
 import { apiPost } from '../utils/api-wrapper'
 import { removeTokens } from '../utils/token-management'
 import { useUserStore } from 'stores/user-store'

  export default {
    name: 'AvatarMenu',
    setup() {
      const openSettings = () => {
        // Implement settings logic here
        console.log('Opening settings')
      }

      const store = useUserStore()
      const router = useRouter()

      const logout = async () => {
        try {
          const response = await apiPost('/logout/', {})
          removeTokens()
          router.push('/login')
        } catch (error) {
          console.error('Logout failed', error)
        }
      }

      return {
        store,
        openSettings,
        logout
      }
    }
  }
  </script>