import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    try {
      const storedUser = localStorage.getItem('market_user');
      return storedUser ? JSON.parse(storedUser) : null;
    } catch (error) {
      console.error("Error parsing stored user:", error);
      return null;
    }
  });

  const login = async (username, password) => {
    // REAL API LOGIN
    try {
      const response = await fetch('http://localhost:8000/api/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        alert(errorData.error || 'Credenciales inválidas');
        return false;
      }

      const data = await response.json();
      const userData = { username: data.username, role: data.role };
      setUser(userData);
      localStorage.setItem('market_user', JSON.stringify(userData));
      return true;
    } catch (error) {
      console.error('Login error:', error);
      alert('Error de conexión con el servidor');
      return false;
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('market_user');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
