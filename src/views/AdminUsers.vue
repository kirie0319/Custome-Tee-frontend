<!-- src/views/AdminUsers.vue -->
<template>
  <div class="min-h-screen p-6">
    <div class="max-w-7xl mx-auto">
      <div class="mb-6">
        <h1 class="text-3xl font-bold">User Management</h1>
      </div>

      <!-- 検索フィルター -->
      <div class="bg-white p-4 rounded-lg shadow mb-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <input 
              type="text"
              v-model="searchQuery"
              placeholder="Search by username or email"
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500"
              @input="debounceSearch"
            >
          </div>
          <div class="flex justify-end">
            <button
              @click="fetchUsers"
              class="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
            >
              Search
            </button>
          </div>
        </div>
      </div>

      <!-- ユーザー一覧テーブル -->
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                User
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Email
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Role
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Orders
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="user in users" :key="user.id">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div>
                    <div class="text-sm font-medium text-gray-900">
                      {{ user.username }}
                    </div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ user.email }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                  :class="user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                >
                  {{ user.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ user.is_admin ? 'Admin' : 'User' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ user.orders_count }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button
                  @click="openUserModal(user)"
                  class="text-indigo-600 hover:text-indigo-900 mr-4"
                >
                  Edit
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- ページネーション -->
      <div class="mt-4 flex justify-between items-center">
        <div class="text-sm text-gray-700">
          Showing {{ (currentPage - 1) * perPage + 1 }} to {{ Math.min(currentPage * perPage, totalItems) }} of {{ totalItems }} users
        </div>
        <div class="flex space-x-2">
          <button 
            @click="prevPage" 
            :disabled="currentPage === 1"
           class="px-3 py-1 border rounded-md hover:bg-gray-100 disabled:opacity-50"
         >
           Previous
         </button>
         <button
           @click="nextPage"
           :disabled="currentPage >= totalPages"
           class="px-3 py-1 border rounded-md hover:bg-gray-100 disabled:opacity-50"
         >
           Next
         </button>
       </div>
     </div>
   </div>

   <!-- ユーザー編集モーダル -->
   <div v-if="selectedUser" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center">
     <div class="bg-white rounded-lg p-6 max-w-xl w-full mx-4">
       <div class="flex justify-between items-start">
         <h2 class="text-xl font-bold">Edit User</h2>
         <button @click="selectedUser = null" class="text-gray-400 hover:text-gray-500">
           <span class="sr-only">Close</span>
           ×
         </button>
       </div>
       <div class="mt-4 space-y-4">
         <div>
           <label class="block text-sm font-medium text-gray-700">Username</label>
           <input 
             type="text"
             v-model="selectedUser.username"
             class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500"
             disabled
           >
         </div>
         <div>
           <label class="block text-sm font-medium text-gray-700">Email</label>
           <input 
             type="email"
             v-model="selectedUser.email"
             class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500"
             disabled
           >
         </div>
         <div>
           <label class="block text-sm font-medium text-gray-700">Status</label>
           <select 
             v-model="selectedUser.is_active"
             class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500"
           >
             <option :value="true">Active</option>
             <option :value="false">Inactive</option>
           </select>
         </div>
         <div>
           <label class="block text-sm font-medium text-gray-700">Role</label>
           <select 
             v-model="selectedUser.is_admin"
             class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500"
           >
             <option :value="false">User</option>
             <option :value="true">Admin</option>
           </select>
         </div>
         <div class="flex justify-end space-x-3">
           <button
             @click="selectedUser = null"
             class="px-4 py-2 border rounded-md hover:bg-gray-100"
           >
             Cancel
           </button>
           <button
             @click="updateUser"
             class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
           >
             Save Changes
           </button>
         </div>
       </div>
     </div>
   </div>
 </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import { debounce } from 'lodash'
import type { User, PaginatedResponseUser } from '@/types/admin'

const authStore = useAuthStore()
const users = ref<User[]>([])
const selectedUser = ref<User | null>(null)
const searchQuery = ref('')
const currentPage = ref(1)
const perPage = ref(10)
const totalItems = ref(0)
const totalPages = ref(1)

// const fetchUsers = async () => {
//  try {
//    const response = await axios.get('http://localhost:5000/api/admin/users', {
//      headers: { Authorization: `Bearer ${authStore.token}` },
//      params: {
//        page: currentPage.value,
//        per_page: perPage.value,
//        search: searchQuery.value
//      }
//    })
   
//    users.value = response.data.users
//    totalItems.value = response.data.total
//    totalPages.value = response.data.pages
//  } catch (error) {
//    console.error('Failed to fetch users:', error)
//  }
// }

// 型付きのfetchUsers
const fetchUsers = async () => {
    try {
        const response = await axios.get<PaginatedResponseUser<User>>('http://localhost:5000/api/admin/users', {
            headers: { Authorization: `Bearer ${authStore.token}` },
            params: {
                page: currentPage.value,
                per_page: perPage.value,
                search: searchQuery.value
            }
        })
        
        users.value = response.data.users
        totalItems.value = response.data.total
        totalPages.value = response.data.pages
    } catch (error) {
        console.error('Failed to fetch users:', error)
    }
}

const openUserModal = (user: User) => {
 selectedUser.value = { ...user }
}

const updateUser = async () => {
    // selectedUserがnullの場合の早期リターン
  if (!selectedUser.value) {
    console.error('No user selected')
    return
  }
 try {
   await axios.post(
     'http://localhost:5000/api/admin/users/manage',
     {
       user_id: selectedUser.value.id,
       action: selectedUser.value.is_active ? 'activate' : 'deactivate'
     },
     { headers: { Authorization: `Bearer ${authStore.token}` } }
   )

   if (selectedUser.value.is_admin !== users.value.find(u => u.id === selectedUser.value.id).is_admin) {
     await axios.post(
       'http://localhost:5000/api/admin/users/manage',
       {
         user_id: selectedUser.value.id,
         action: selectedUser.value.is_admin ? 'make_admin' : 'remove_admin'
       },
       { headers: { Authorization: `Bearer ${authStore.token}` } }
     )
     // 現在のユーザーを検索
    const currentUser = users.value.find(u => u.id === selectedUser.value?.id)
    if (currentUser && selectedUser.value.is_admin !== currentUser.is_admin) {
      await axios.post(
        'http://localhost:5000/api/admin/users/manage',
        {
          user_id: selectedUser.value.id,
          action: selectedUser.value.is_admin ? 'make_admin' : 'remove_admin'
        },
        { headers: { Authorization: `Bearer ${authStore.token}` } }
      )
    }
    
   }

   await fetchUsers()
   selectedUser.value = null
 } catch (error) {
   console.error('Failed to update user:', error)
 }
}

const debounceSearch = debounce(() => {
 currentPage.value = 1
 fetchUsers()
}, 300)

const prevPage = () => {
 if (currentPage.value > 1) {
   currentPage.value--
   fetchUsers()
 }
}

const nextPage = () => {
 if (currentPage.value < totalPages.value) {
   currentPage.value++
   fetchUsers()
 }
}

onMounted(() => {
 fetchUsers()
})
</script>