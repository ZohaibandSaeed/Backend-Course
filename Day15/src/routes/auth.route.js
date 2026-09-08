import { Router } from "express";
import { Register, GetUser, Login } from "../controllers/auth.controller.js";

const router = Router();

router.post("/register", Register);
router.post("/login", Login);
router.get("/get", GetUser);

export default router;