import React from 'react';
import { Link, useNavigate, Outlet } from 'react-router-dom';
import { useAuth } from '../services/auth';
import '../assets/css/Tienda.css'; // Will be copied here
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

const Layout = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <>
            <nav className="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
                <div className="container">
                    <Link className="navbar-brand" to="/">Market</Link>
                    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav">
                        <span className="navbar-toggler-icon"></span>
                    </button>

                    <div id="nav" className="collapse navbar-collapse">
                        <ul className="navbar-nav me-auto">
                            {user && (
                                <>
                                    {user.role === 'GERENTE' && (
                                        <>
                                            <li className="nav-item"><Link className="nav-link" to="/ventas">Ventas</Link></li>
                                            <li className="nav-item"><Link className="nav-link" to="/reportes">Reportes</Link></li>
                                        </>
                                    )}
                                    {user.role === 'JEFE' && (
                                        <>
                                            <li className="nav-item"><Link className="nav-link" to="/productos">Productos</Link></li>
                                            <li className="nav-item"><Link className="nav-link" to="/reportes">Reportes</Link></li>
                                        </>
                                    )}
                                    {user.role === 'EMPLEADO' && (
                                        <li className="nav-item"><Link className="nav-link" to="/pos">Carrito</Link></li>
                                    )}
                                    {user.role === 'DUEÑA' && (
                                        <>
                                            <li className="nav-item"><Link className="nav-link" to="/empleados">Empleados</Link></li>
                                            <li className="nav-item"><Link className="nav-link" to="/credenciales">Credenciales</Link></li>
                                            <li className="nav-item"><Link className="nav-link" to="/movimientos">Movimientos</Link></li>
                                            <li className="nav-item"><Link className="nav-link" to="/historial">Historial</Link></li>
                                        </>
                                    )}
                                </>
                            )}
                        </ul>

                        <ul className="navbar-nav ms-auto">
                            {user ? (
                                <>
                                    <li className="nav-item">
                                        <span className="navbar-text me-2">
                                            {user.username} – <span className="text-capitalize">{user.role?.toLowerCase()}</span>
                                        </span>
                                    </li>
                                    <li className="nav-item">
                                        <button className="btn btn-link nav-link" onClick={handleLogout}>Salir</button>
                                    </li>
                                </>
                            ) : (
                                <li className="nav-item"><Link className="nav-link" to="/login">Ingresar</Link></li>
                            )}
                        </ul>
                    </div>
                </div>
            </nav>

            <div className="container">
                <Outlet />
            </div>
        </>
    );
};

export default Layout;
