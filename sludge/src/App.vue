<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <nav>
    <RouterLink to="/">Dashboard</RouterLink>
    <RouterLink to="/events">Event Log</RouterLink>
    <RouterLink to="/employees">Employees</RouterLink>
    <RouterLink to="/structure">Structure</RouterLink>
    <RouterLink to="/roles">Roles</RouterLink>
    <RouterLink to="/groups">Groups</RouterLink>
    <RouterLink to="/resources">Resources</RouterLink>
    <RouterLink to="/transfers">Transfers</RouterLink>
  </nav>

  <main>
    <RouterView />
  </main>

</template>

<style scoped>
nav {
	position: fixed;
	top: 0;
	left: 0;
	max-width: 200px;
	background-color: var(--color-background-soft);
	height: 100vh;
	margin: 0;
	border-right: 1px var(--color-border) solid;
}



nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
	display: block;
	padding: 0.5rem 1rem;
	border-bottom: 1px solid var(--color-border);
	width: 200px;
}

nav a:last-of-type {
  border: 0;
}
</style>
