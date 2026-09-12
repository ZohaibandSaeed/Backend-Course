import Groq from "groq-sdk";
import dotenv from "dotenv";

dotenv.config();

const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });

export const generateRecipeContent = async (title, description) => {
    try {
        const prompt = `You are an expert chef. Create a complete, professional, and detailed recipe for "${title}". 
Description provided by the user: "${description}"
Please provide the recipe in a well-structured markdown format including:
- Catchy Title
- Brief Introduction
- Ingredients list (with measurements)
- Step-by-step cooking instructions
- Prep time, cooking time, and servings
- Tips for best results.`;

        const chatCompletion = await groq.chat.completions.create({
            messages: [
                {
                    role: "system",
                    content: "You are a professional chef. Always respond with clear, well-formatted markdown recipes."
                },
                {
                    role: "user",
                    content: prompt,
                },
            ],
            model: "llama3-8b-8192", // Using an efficient and capable model
        });

        return chatCompletion.choices[0]?.message?.content || "";
    } catch (error) {
        throw new Error("Failed to generate recipe from AI: " + error.message);
    }
};

export const answerRecipeQuestion = async (recipeContent, question) => {
    try {
        const prompt = `You are a helpful culinary assistant. A user has a question about a specific recipe.
Here is the complete recipe content:
---
${recipeContent}
---
The user's question is: "${question}"
Please answer the user's question accurately, based ONLY on the provided recipe content. If the answer is not in the recipe, kindly state that you don't know based on the provided recipe.`;

        const chatCompletion = await groq.chat.completions.create({
            messages: [
                {
                    role: "system",
                    content: "You are a helpful assistant that answers questions based ONLY on provided context."
                },
                {
                    role: "user",
                    content: prompt,
                },
            ],
            model: "llama3-8b-8192", 
        });

        return chatCompletion.choices[0]?.message?.content || "";
    } catch (error) {
        throw new Error("Failed to answer question from AI: " + error.message);
    }
};
