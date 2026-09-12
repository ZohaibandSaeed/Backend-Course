import express from "express";
import { getApprovedRecipes, getRecipeById, askRecipeQuestion } from "../controllers/recipe.controller.js";
import { protect } from "../../middlewares/auth.middleware.js";

const router = express.Router();

// User routes - Must be logged in (but doesn't require admin role)
router.use(protect);

router.get("/", getApprovedRecipes);
router.get("/:id", getRecipeById);
router.post("/:id/ask", askRecipeQuestion);

export default router;
