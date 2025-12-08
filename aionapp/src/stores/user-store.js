import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    uid: 0,
    username: '',
    projects: [],
    businesses: [],
  }),
  getters: {
    userId: (state) => state.uid,
    userName: (state) => state.username,
    userProjects: (state) => state.projects,
    userBusinesses: (state) => state.businesses,
  },
  actions: {
    setUser(user) {
      this.uid = user.uid;
      this.username = user.username;
    },
    setProjects(projects) {
      // Always is passed all the projects updated
      // Flushing the projects is valid because the projects are updated
      this.projects = []

      if (Array.isArray(projects)) {
        projects.forEach(project => this.updateProject(project))
      } else {
        this.updateProject(projects)
      }
    },
    setBusinesses(businesses) {
      // Always is passed all the businesses updated
      // Flushing the businesses is valid because the businesses are updated
      this.businesses = []

      if (Array.isArray(businesses)) {
        businesses.forEach(business => this.updateBusiness(business))
      } else {
        this.updateBusiness(businesses)
      }
    },
    updateProject(obj_project) {
      const obj_existingProject = this.projects.find(p => p.id === obj_project.id)

      if (!obj_existingProject) {
        this.projects.push(obj_project)
      } else {
        const arr_updatedFields = ['name', 'description', 'start_date', 'end_date', 'progress']

        arr_updatedFields.forEach(str_field => {
          if (obj_existingProject[str_field] !== obj_project[str_field]) {
            obj_existingProject[str_field] = obj_project[str_field]
          }
        })
      }
    },
    updateBusiness(obj_business) {
      const obj_existingBusiness = this.businesses.find(b => b.id === obj_business.id)

      if (!obj_existingBusiness) {
        this.businesses.push(obj_business)
      } else {
        const arr_updatedFields = ['name', 'description', 'start_date', 'end_date', 'progress']

        arr_updatedFields.forEach(str_field => {
          if (obj_existingBusiness[str_field] !== obj_business[str_field]) {
            obj_existingBusiness[str_field] = obj_business[str_field]
          }
        })
      }
    },
  },
  persist: {
    storage: sessionStorage
  }
});
