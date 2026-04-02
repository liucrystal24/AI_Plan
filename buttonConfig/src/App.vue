<template>
  <div class="app-shell">
    <header class="topbar">
      <h1>可配置按钮管理</h1>
      <nav>
        <RouterLink to="/config" class="nav-link">配置页面</RouterLink>
        <RouterLink to="/display" class="nav-link">展示页面</RouterLink>
        <RouterLink to="/schema-import" class="nav-link">Schema导入页</RouterLink>
      </nav>
    </header>

    <main class="content">
      <RouterView />
    </main>
  </div>
</template>
