import { createRouter, createWebHistory } from "vue-router";
import ConfigPage from "../pages/ConfigPage.vue";
import DisplayPage from "../pages/DisplayPage.vue";
import SchemaImportPage from "../pages/SchemaImportPage.vue";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      redirect: "/config",
    },
    {
      path: "/config",
      name: "config",
      component: ConfigPage,
    },
    {
      path: "/display",
      name: "display",
      component: DisplayPage,
    },
    {
      path: "/schema-import",
      name: "schema-import",
      component: SchemaImportPage,
    },
  ],
});
