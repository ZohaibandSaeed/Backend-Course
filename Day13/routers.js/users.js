import { Router } from "express";
const router = Router();

import { CreateUser, getUsers } from "../controlers/users.js";

router.post("/create", CreateUser);
router.get("/getUsers", getUsers);

export default router;