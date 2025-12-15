import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Api } from '../../services/api';

const TipoEmpleadoList = () => {
    const [items, setItems] = useState([]);
    const navigate = useNavigate();

    const loadItems = async () => {
        try {
            const data = await Api.getEmployeeTypes();
            setItems(data);
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => { loadItems(); }, []);

    const handleDelete = async (id) => {
        if (window.confirm('¿Eliminar este tipo de empleado?')) {
            try {
                await Api.deleteEmployeeType(id);
                loadItems();
            } catch (error) {
                alert('Error al eliminar');
            }
        }
    };

    return (
        <div className="container mt-4">
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h2>Tipos de Empleado</h2>
                <button className="btn btn-primary" onClick={() => navigate('/tipoempleados/nuevo')}>
                    Nuevo Tipo
                </button>
            </div>
            <table className="table table-bordered shadow-sm bg-white">
                <thead className="table-secondary">
                    <tr>
                        <th>ID</th>
                        <th>Rol</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {items.map(item => (
                        <tr key={item.idtipoEmpleado}>
                            <td>{item.idtipoEmpleado}</td>
                            <td>{item.rol}</td>
                            <td>
                                <button className="btn btn-sm btn-outline-primary me-2"
                                    onClick={() => navigate(`/tipoempleados/editar/${item.idtipoEmpleado}`)}>
                                    Editar
                                </button>
                                <button className="btn btn-sm btn-outline-danger"
                                    onClick={() => handleDelete(item.idtipoEmpleado)}>
                                    Eliminar
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default TipoEmpleadoList;
