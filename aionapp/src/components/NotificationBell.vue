<template>
    <q-btn flat dense round icon="notifications">
      <q-badge color="red" floating>{{ unreadCount }}</q-badge>
      <q-menu>
        <q-list style="min-width: 200px">
          <q-item v-for="notification in notifications" :key="notification.id" clickable v-close-popup @click="markAsRead(notification.id)">
            <q-item-section>{{ notification.message }}</q-item-section>
          </q-item>
        </q-list>
      </q-menu>
    </q-btn>
  </template>
  
  <script>
  import { ref, computed } from 'vue'
  
  export default {
    name: 'NotificationBell',
    setup() {
      const notifications = ref([
        { id: 1, message: 'Notification 1', read: false },
        { id: 2, message: 'Notification 2', read: false },
        { id: 3, message: 'Notification 3', read: true },
      ])
  
      const unreadCount = computed(() => {
        return notifications.value.filter(n => !n.read).length
      })

      const markAsRead = (id) => {
        const notification = notifications.value.find(n => n.id === id)
        if (notification) {
          notification.read = true
        }
      }
  
      return {
        notifications,
        unreadCount,
        markAsRead
      }
    }
  }
  </script>