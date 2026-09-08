import { Router } from "express";
import { AuthMiddleWare } from "../middleware/auth.middleware.js";
import { Dashboard } from "../controllers/dashboard.controller.js";

const router = Router();

router.get("/dashboard", AuthMiddleWare, Dashboard);

export default router;