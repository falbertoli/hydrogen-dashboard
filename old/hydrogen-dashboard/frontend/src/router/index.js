import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import HydrogenDemandView from "../views/HydrogenDemandView.vue";
import StorageSpaceView from "../views/StorageSpaceView.vue";
import StorageView from "../views/StorageView.vue";
import CostAnalysisView from "../views/CostAnalysisView.vue";
import RegulationsView from "@/views/RegulationsView.vue";
import SustainabilityView from "@/views/SustainabilityView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", name: "home", component: HomeView },
    {
      path: "/hydrogen-demand",
      name: "hydrogen-demand",
      component: HydrogenDemandView,
    },
    {
      path: "/storage-space",
      name: "storage-space",
      component: StorageSpaceView,
    },
    // {
    //   path: "/cost-analysis",
    //   name: "cost-analysis",
    //   component: CostAnalysisView,
    // },
    // { path: "/storage-cost", name: "storage-cost", component: StorageCostView },
    // ,
    // { path: "/regulations", name: "regulations", component: RegulationsView },
    // ,
    // {
    //   path: "/sustainability",
    //   name: "sustainability",
    //   component: SustainabilityView,
    // },
  ],
});

export default router;
