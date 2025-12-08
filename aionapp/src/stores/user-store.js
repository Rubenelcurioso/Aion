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
    updateProject(project) {
      const existingProject = this.projects.find(p => p.id === project.id)

      if (!existingProject) {
        this.projects.push(project)
      } else {
        const updatedFields = ['name', 'description', 'start_date', 'end_date', 'progress']

        updatedFields.forEach(field => {
          if (existingProject[field] !== project[field]) {
            existingProject[field] = project[field]
          }
        })
      }
    },
    updateBusiness(business) {
      const existingBusiness = this.businesses.find(b => b.id === business.id)

      if (!existingBusiness) {
        this.businesses.push(business)
      } else {
        const updatedFields = ['name', 'description', 'start_date', 'end_date', 'progress']

        updatedFields.forEach(field => {
          if (existingBusiness[field] !== business[field]) {
            existingBusiness[field] = business[field]
          }
        })
      }
    },
  },
  persist: {
    storage: sessionStorage
  }
});
