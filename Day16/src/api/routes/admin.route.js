import express from "express";
import { generateRecipe, getPendingRecipes, approveRecipe } from "../controllers/admin.controller.js";
import { protect, authorize } from "../../middlewares/auth.middleware.js";

const router = express.Router();

// All routes here are protected and require admin role
router.use(protect);
router.use(authorize("admin"));

router.post("/recipes/generate", generateRecipe);
router.get("/recipes/pending", getPendingRecipes);
router.put("/recipes/:id/approve", approveRecipe);

export default router;
