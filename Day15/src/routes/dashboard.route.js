import { Router } from "express";
import { AuthMiddleWare, IsAdmin } from "../middleware/auth.middleware.js";
import { Dashboard } from "../controllers/dashboard.controller.js";

const router = Router();

router.get("/dashboard", AuthMiddleWare, IsAdmin, Dashboard);

export default router;