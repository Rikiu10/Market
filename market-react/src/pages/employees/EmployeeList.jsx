import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Api } from '../../services/api';

const EmployeeList = () => {
    const [employees, setEmployees] = useState([]);
    const navigate = useNavigate();

    const loadEmployees = async () => {
        try {
            const data = await Api.getEmployees();
            setEmployees(data);
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        loadEmployees();
    }, []);

    const handleDelete = async (id) => {
        if (window.confirm('¿Eliminar empleado?')) {
            await Api.deleteEmployee(id);
            loadEmployees();
        }
    };

    return (
        <div className="container mt-4">
            <div className="d-flex justify-content-between align-items-center mb-3">
                <h2>Gestión de Empleados</h2>
                <button className="btn btn-primary" onClick={() => navigate('/empleados/nuevo')}>
                    Nuevo Empleado
                </button>
            </div>

            <div className="table-responsive">
                <table className="table table-bordered shadow-sm bg-white">
                    <thead className="table-info">
                        <tr>
                            <th>Legajo</th>
                            <th>Nombre</th>
                            <th>Apellido</th>
                            <th>Rol</th>
                            <th>Teléfono</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {employees.map(e => (
                            <tr key={e.idempleado}>
                                <td>{e.legajo}</td>
                                <td>{e.nombre}</td>
                                <td>{e.apellido}</td>
                                <td>{e.tipo_empleado_nombre || e.tipoEmpleado}</td>
                                <td>{e.telefono}</td>
                                <td>
                                    <button
                                        onClick={() => navigate(`/empleados/editar/${e.idempleado}`)}
                                        className="btn btn-sm btn-outline-primary me-2">
                                        Editar
                                    </button>
                                    <button onClick={() => handleDelete(e.idempleado)} className="btn btn-sm btn-outline-danger">
                                        Eliminar
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

        </div>
    );
};

export default EmployeeList;
