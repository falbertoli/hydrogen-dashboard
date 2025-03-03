import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import HydrogenDemandView from "../views/HydrogenDemandView.vue";
import StorageView from "../views/StorageView.vue";
import CostAnalysisView from "../views/CostAnalysisView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", name: "home", component: HomeView },
    {
      path: "/hydrogen-demand",
      name: "hydrogen-demand",
      component: HydrogenDemandView,
    },
    { path: "/storage", name: "storage", component: StorageView },
    {
      path: "/cost-analysis",
      name: "cost-analysis",
      component: CostAnalysisView,
    },
  ],
});

export default router;
