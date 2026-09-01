import { db } from "../src/prisma/db.ts"

const CreateUser = async (req, res) => {
    try {

        const data = req.body;

        if (!data.name || !data.email) {
            res.status(400).json({
                "message": "Invalid request"
            });
            return;
        }

        const user = await db.orm.public.User.create({
            name: data.name,
            email: data.email
        });
        res.status(201).json({
            "message": "User created successfully"
        });

    } catch (error) {
        console.log(error);
        res.status(500).json({ message: "Internal server error" });
    }
}

const getUsers = async (req, res) => {
    try {
        const users = await db.orm.public.User.all();
        res.json(users);
    } catch (error) {
        console.log(error);
        res.status(500).json({ message: "Internal server error" });
    }
}

export {
    CreateUser,
    getUsers
}