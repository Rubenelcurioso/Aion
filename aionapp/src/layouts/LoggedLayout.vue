<template>
    <q-layout view="hHh LpR lFf">
      <q-header  class="bg-secondary text-black">
        <q-toolbar>
          <DrawerButton @toggle-drawer="toggleDrawer" />
  
          <q-toolbar-title class="text-center">        
          </q-toolbar-title>
          <AvatarMenu />
        </q-toolbar>
      </q-header>
  
      <MainDrawer v-model="leftDrawerOpen" />
  
      <q-page-container>
        <router-view :key="$route.params.pid || $route.params.bid || $route.fullPath" />
      </q-page-container>
    </q-layout>
  </template>
  
  <script>
  import { ref } from 'vue'
  import DrawerButton from 'components/DrawerButton.vue'
  import MainDrawer from 'components/MainDrawer.vue'
  import AvatarMenu from 'components/AvatarMenu.vue'
  
  export default {
    components: {
      DrawerButton,
      MainDrawer,
      AvatarMenu
    },
    setup() {
      const leftDrawerOpen = ref(false)
  
      const toggleDrawer = () => {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
  
      return {
        leftDrawerOpen,
        toggleDrawer
      }
    }
  }
  </script>