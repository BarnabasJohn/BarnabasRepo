"use client";
import React from 'react';
import axios from 'axios';
import { useRouter } from 'next/router';
import Link from 'next/link';

export default function Login () {

    const [newUser, setNewUser] = React.useState({ email: '', password: ''});

    const router = useRouter()

    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';


    // Login user
    const loginUser = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        try {
            const response = await axios.post(`${apiUrl}/auth/login`, newUser);

            console.log(response.status)

            localStorage.setItem('token', response.data.access_token);

            console.log(response.data.access_token)

            router.push('/index/page')

        } catch (error) {
            console.error('Error logging in user:', error);
        }
    };

    return (
        <div>
            <form onSubmit={loginUser} className="mb-6 p-4 bg-blue-100 rounded shadow">
                <input
                    placeholder="Please enter email"
                    value={newUser.email}
                    onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                    className="mb-2 w-full p-2 border border-gray-300 rounded"
                />
                <input
                    placeholder="Please enter password"
                    type='password'
                    value={newUser.password}
                    onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                    className="mb-2 w-full p-2 border border-gray-300 rounded"
                />
                <button type="submit" className="w-full p-2 text-white bg-blue-500 rounded hover:bg-blue-600">
                    Login
                </button>
            </form>

            <div className="m-6 p-4 bg-blue-100 rounded shadow">
                <p>Dont have an acount?</p>

                <button className="w-full p-2 text-white bg-blue-500 rounded hover:bg-blue-600">
                    <Link href="/register/page">Register here</Link>
                </button>
            </div>
        </div>
    )
}


