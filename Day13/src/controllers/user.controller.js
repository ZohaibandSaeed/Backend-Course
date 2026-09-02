import { db } from "../prisma/db.ts";

async function createUser(req, res) {
    try {
        const payload = req.body;

        if (!payload.username || !payload.password) {
            return res.status(400).json({ message: "All fields are required." });
        }

        const user = await db.orm.public.User.create({
            username: payload.username,
            password: payload.password,
        });

        res.status(201).json({ message: "User created successfully.", "user-data": user });

    } catch (error) {
        console.error(error);
        res.status(500).json({ message: "Internal server error." });
    }

}

export { createUser };