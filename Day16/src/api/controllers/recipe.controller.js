import { Recipe } from "../models/recipe.model.js";
import { answerRecipeQuestion } from "../../services/groq.service.js";

// @desc    Get all approved recipes
// @route   GET /api/recipes
// @access  Private (All authenticated users)
export const getApprovedRecipes = async (req, res) => {
    try {
        const recipes = await Recipe.find({ status: "approved" }).populate("createdBy", "name");

        res.status(200).json({
            success: true,
            count: recipes.length,
            data: recipes
        });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
};

// @desc    Get single approved recipe
// @route   GET /api/recipes/:id
// @access  Private (All authenticated users)
export const getRecipeById = async (req, res) => {
    try {
        const recipe = await Recipe.findOne({ _id: req.params.id, status: "approved" }).populate("createdBy", "name");

        if (!recipe) {
            return res.status(404).json({ success: false, message: "Recipe not found or not approved yet" });
        }

        res.status(200).json({
            success: true,
            data: recipe
        });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
};

// @desc    Ask AI a question about a recipe
// @route   POST /api/recipes/:id/ask
// @access  Private (All authenticated users)
export const askRecipeQuestion = async (req, res) => {
    try {
        const { question } = req.body;

        if (!question) {
            return res.status(400).json({ success: false, message: "Please provide a question" });
        }

        const recipe = await Recipe.findOne({ _id: req.params.id, status: "approved" });

        if (!recipe) {
            return res.status(404).json({ success: false, message: "Recipe not found or not approved yet" });
        }

        // Call Groq API for Q&A
        const answer = await answerRecipeQuestion(recipe.generatedContent, question);

        res.status(200).json({
            success: true,
            data: {
                question,
                answer,
                recipeId: recipe._id
            }
        });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
};
