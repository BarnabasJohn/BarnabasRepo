"use client";
import React from 'react';
import axios from 'axios';
import { useRouter } from 'next/router';
import Link from 'next/link';

export default function Register () {

    const router = useRouter()

    const [newUser, setNewUser] = React.useState({ name: '', email: '', password1: '', password2: ''});

    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';

    // Create user
    const createUser = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        try {
        const response = await axios.post(`${apiUrl}/auth/create`, newUser);

        console.log('Successful registration')

        router.push('/')

        } catch (error) {
        console.error('Error creating user:', error);
        }
    };

    return (
        <div>
            <form onSubmit={createUser} className="mb-6 p-4 bg-blue-100 rounded shadow">
                <input
                    placeholder="Name"
                    value={newUser.name}
                    onChange={(e) => setNewUser({ ...newUser, name: e.target.value })}
                    className="mb-2 w-full p-2 border border-gray-300 rounded"
                />
                <input
                    placeholder="Email"
                    value={newUser.email}
                    onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                    className="mb-2 w-full p-2 border border-gray-300 rounded"
                />
                <input
                    placeholder="Password1"
                    type='password'
                    value={newUser.password1}
                    onChange={(e) => setNewUser({ ...newUser, password1: e.target.value })}
                    className="mb-2 w-full p-2 border border-gray-300 rounded"
                />
                <input
                    placeholder="Password2"
                    type='password'
                    value={newUser.password2}
                    onChange={(e) => setNewUser({ ...newUser, password2: e.target.value })}
                    className="mb-2 w-full p-2 border border-gray-300 rounded"
                />
                <button type="submit" className="w-full p-2 text-white bg-blue-500 rounded hover:bg-blue-600">
                    Register User
                </button>
            </form>

            <div className="m-6 p-4 bg-blue-100 rounded shadow">
                <p>Already have an acount?</p>
                <button className="w-full p-2 text-white bg-blue-500 rounded hover:bg-blue-600">
                    <Link href="/">Login here</Link>
                </button>
            </div>
        </div>
    )
}