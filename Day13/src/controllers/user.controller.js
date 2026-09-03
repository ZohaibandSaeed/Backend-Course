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

async function getAllUser(req, res) {
    try {

        const users = await db.orm.public.User.all();
        if (!users) {
            return res.status(404).json({
                "message": "No user found",
            })
        }

        res.status(200).json({
            "message": "Users fetched successfully",
            "user-data": users
        })

    } catch (error) {
        console.error(error);
        res.status(500).json({ message: "Internal server error." });
    }
}

async function getOneUser(req, res) {
    try {

        const payload = req.params;

        if (!payload.username) {
            return res.status(400).json({
                "message": "Username is required",
            });
        }

        const data = await db.orm.public.User.where({
            username: payload.username,
        }).first();

        if (!data) {
            return res.status(404).json({
                "message": "User not found",
            });
        }

        res.status(200).json({
            "message": "User found",
            "user-data": data,
        });

    } catch (error) {
        console.error(error);
        res.status(500).json({ message: "Internal server error." });
    }
}

async function deleteUser(req, res) {
    try {

        const payload = req.params;

        if (!payload.username) {
            return res.status(400).json({
                "message": "username is required",
            });
        }

        const data = await db.orm.public.User.where({
            username: payload.username
        }).delete();

        if (!data) {
            return res.status(404).json({
                "message": "User not found in database"
            });
        }

        res.status(200).json({
            "message": "User delete successfully",
            "user deleted": data.username
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({
            "message": "Internal server error."
        });
    }

}

async function updateUser(req, res) {
    try {

        const payload = req.body;
        const u_data = req.params;

        if (!payload.username || !payload.password || !u_data.username) {
            return res.status(400).json({
                "message": "All fields are required"
            });
        }

        const update_data = await db.orm.public.User.where({
            username: u_data.username
        }).update({
            username: payload.username,
            password: payload.password
        });

        if (!update_data) {
            return res.status(404).json({
                "message": "User not found in database",
            });
        }

        res.status(200).json({
            "message": "User updated successfully",
            "user-data": update_data,
        });

    } catch (error) {
        console.error(error);
        res.status(500).json({
            "message": "Internal server error."
        });
    }
}

export { createUser, getAllUser, getOneUser, deleteUser, updateUser };