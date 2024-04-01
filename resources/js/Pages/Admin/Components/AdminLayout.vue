<template>
    <Head title="Admin" />

    <div class="antialiased bg-gray-50 dark:bg-gray-900">
        <!-- Navbar -->
        <Navbar/>
        <!-- end -->

        <!-- Sidebar -->
        <Sidebar/>
        <!-- end -->

        <!-- Main -->
        <main class="p-4 md:ml-64 h-auto pt-20">
            <slot/>
        </main>
        <!-- end -->
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { initFlowbite } from 'flowbite'
import Navbar from './Navbar.vue'
import Sidebar from './Sidebar.vue'
import {Head} from "@inertiajs/vue3";
import ProductList from "@/Pages/Admin/Product/ProductList.vue";

// initialize components based on data attribute selectors
onMounted(() => {
    initFlowbite();
})
</script>
