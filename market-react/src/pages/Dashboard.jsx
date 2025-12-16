import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../services/auth';

const Dashboard = () => {
    const { user } = useAuth();

    if (!user) {
        return (
            <div className="text-center mt-5">
                <h1>Bienvenido a Market</h1>
                <p className="lead">Por favor inicia sesión para continuar.</p>
                <Link to="/login" className="btn btn-lg btn-primary">Ingresar</Link>
            </div>
        );
    }

    return (
        <div>
            <h1 className="h4 mb-4">Dashboard - {user.role}</h1>
            <div className="row g-3">
                {user.role === 'GERENTE' && (
                    <>
                        <div className="col-md-4">
                            <Link to="/ventas" className="text-decoration-none">
                                <div className="card shadow-sm h-100">
                                    <div className="card-body">
                                        <h5 className="card-title text-dark">Ventas</h5>
                                        <p className="text-muted mb-0">Diarias · Semanales · Mensuales</p>
                                    </div>
                                </div>
                            </Link>
                        </div>
                        <div className="col-md-4">
                            <Link to="/reportes" className="text-decoration-none">
                                <div className="card shadow-sm h-100">
                                    <div className="card-body">
                                        <h5 className="card-title text-dark">Reportes</h5>
                                        <p className="text-muted mb-0">KPIs y comparativas</p>
                                    </div>
                                </div>
                            </Link>
                        </div>
                    </>
                )}

                {user.role === 'JEFE' && (
                    <>
                        <div className="col-md-4">
                            <Link to="/productos" className="text-decoration-none">
                                <div className="card shadow-sm h-100">
                                    <div className="card-body">
                                        <h5 className="card-title text-dark">Inventario</h5>
                                        <p className="text-muted mb-0">Stock, entradas y bajas</p>
                                    </div>
                                </div>
                            </Link>
                        </div>
                        <div className="col-md-4">
                            <Link to="/reportes" className="text-decoration-none">
                                <div className="card shadow-sm h-100">
                                    <div className="card-body">
                                        <h5 className="card-title text-dark">Reportes</h5>
                                        <p className="text-muted mb-0">Movimientos y alertas</p>
                                    </div>
                                </div>
                            </Link>
                        </div>
                    </>
                )}

                {user.role === 'EMPLEADO' && (
                    <div className="col-md-4">
                        <Link to="/pos" className="text-decoration-none">
                            <div className="card shadow-sm h-100">
                                <div className="card-body">
                                    <h5 className="card-title text-dark">Punto de Venta</h5>
                                    <p className="text-muted mb-0">Registrar venta</p>
                                </div>
                            </div>
                        </Link>
                    </div>
                )}

                {(user.role === 'DUEÑA' || user.role?.includes('DUE')) && (
                    <>
                        <div className="col-md-4">
                            <Link to="/empleados" className="text-decoration-none">
                                <div className="card shadow-sm h-100">
                                    <div className="card-body">
                                        <h5 className="card-title text-dark">Empleados</h5>
                                        <p className="text-muted mb-0">Crear · Editar · Eliminar</p>
                                    </div>
                                </div>
                            </Link>
                        </div>
                        <div className="col-md-4">
                            <Link to="/movimientos" className="text-decoration-none">
                                <div className="card shadow-sm h-100">
                                    <div className="card-body">
                                        <h5 className="card-title text-dark">Movimientos</h5>
                                        <p className="text-muted mb-0">Gestionar movimientos</p>
                                    </div>
                                </div>
                            </Link>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
