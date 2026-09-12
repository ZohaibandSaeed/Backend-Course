import mongoose from "mongoose";

const recipeSchema = new mongoose.Schema(
    {
        title: {
            type: String,
            required: [true, "Please add a recipe title"],
        },
        description: {
            type: String,
            required: [true, "Please add a description"],
        },
        generatedContent: {
            type: String,
            // Will contain the markdown/structured text from Groq AI
        },
        status: {
            type: String,
            enum: ["pending_review", "approved"],
            default: "pending_review",
        },
        createdBy: {
            type: mongoose.Schema.ObjectId,
            ref: "User",
            required: true,
        },
    },
    { timestamps: true }
);

export const Recipe = mongoose.model("Recipe", recipeSchema);
