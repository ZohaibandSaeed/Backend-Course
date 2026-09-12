import { Recipe } from "../models/recipe.model.js";
import { generateRecipeContent } from "../../services/groq.service.js";

// @desc    Generate a new recipe using AI (saves as pending_review)
// @route   POST /api/admin/recipes/generate
// @access  Private/Admin
export const generateRecipe = async (req, res) => {
    try {
        const { title, description } = req.body;

        if (!title || !description) {
            return res.status(400).json({ success: false, message: "Please provide title and description" });
        }

        // Call Groq API
        const generatedContent = await generateRecipeContent(title, description);

        // Save to DB as pending_review
        const recipe = await Recipe.create({
            title,
            description,
            generatedContent,
            status: "pending_review",
            createdBy: req.user.id
        });

        res.status(201).json({
            success: true,
            message: "Recipe generated successfully and is pending review.",
            data: recipe
        });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
};

// @desc    Get all pending recipes
// @route   GET /api/admin/recipes/pending
// @access  Private/Admin
export const getPendingRecipes = async (req, res) => {
    try {
        const recipes = await Recipe.find({ status: "pending_review" }).populate("createdBy", "name email");

        res.status(200).json({
            success: true,
            count: recipes.length,
            data: recipes
        });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
};

// @desc    Approve a recipe
// @route   PUT /api/admin/recipes/:id/approve
// @access  Private/Admin
export const approveRecipe = async (req, res) => {
    try {
        let recipe = await Recipe.findById(req.params.id);

        if (!recipe) {
            return res.status(404).json({ success: false, message: "Recipe not found" });
        }

        if (recipe.status === "approved") {
            return res.status(400).json({ success: false, message: "Recipe is already approved" });
        }

        recipe = await Recipe.findByIdAndUpdate(
            req.params.id,
            { status: "approved" },
            { new: true, runValidators: true }
        );

        res.status(200).json({
            success: true,
            message: "Recipe approved successfully",
            data: recipe
        });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
};
