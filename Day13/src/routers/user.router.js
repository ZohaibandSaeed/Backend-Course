import { Router } from "express";
import { createUser, getAllUser, getOneUser, deleteUser, updateUser } from "../controllers/user.controller.js";

const router = Router();

router.post("/create", createUser);
router.get("/all", getAllUser);
router.get("/one/:username", getOneUser);
router.delete("/delete/:username", deleteUser);
router.put("/update/:username", updateUser);

export default router;