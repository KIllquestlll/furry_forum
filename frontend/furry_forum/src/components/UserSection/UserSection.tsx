import React, { useEffect, useState } from 'react'
import axios from 'axios';

interface User {
  id: number;
  username: string;
  name: string;
  email: string;
}
function UserSection() {
    const [users, setUsers] = useState<User[]>([]);
    const [loading, setLoading] = useState(true); // Добавим состояние загрузки

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/user/user')
            .then(response => {
                setUsers(response.data);
                setLoading(false);
            })
            .catch(error => {
                console.error("Ошибка при получении данных:", error);
                setLoading(false);
            });
    }, []);

    if (loading) return <p className="text-center p-6">Загрузка пользователей...</p>;

    return (
        <div className="p-6 max-w-4xl mx-auto">
            <h1 className="text-2xl font-bold mb-4">User List (using Axios)</h1>
            <ul className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {users.map(user => (
                    <li key={user.id} className="bg-white shadow p-4 rounded-xl border border-gray-100">
                        <h2 className="text-lg font-semibold">{user.username || user.name}</h2>
                        <p className="text-sm text-gray-600">{user.email}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default UserSection;