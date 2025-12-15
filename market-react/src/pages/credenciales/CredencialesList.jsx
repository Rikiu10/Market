import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Api } from '../../services/api';

const CredencialesList = () => {
    const [items, setItems] = useState([]);
    const navigate = useNavigate();

    const loadItems = async () => {
        try {
            const data = await Api.getCredentials();
            setItems(data);
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => { loadItems(); }, []);

    const handleDelete = async (id) => {
        if (window.confirm('¿Eliminar esta credencial? Cuidado, podría dejar a un usuario sin acceso.')) {
            try {
                await Api.deleteCredential(id);
                loadItems();
            } catch (error) {
                alert('Error al eliminar');
            }
        }
    };

    return (
        <div className="container mt-4">
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h2>Gestión de Credenciales</h2>
                <button className="btn btn-primary" onClick={() => navigate('/credenciales/nueva')}>
                    Nueva Credencial
                </button>
            </div>
            <table className="table table-bordered shadow-sm bg-white">
                <thead className="table-secondary">
                    <tr>
                        <th>ID</th>
                        <th>Usuario</th>
                        <th>Password (Hash/Plain)</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {items.map(item => (
                        <tr key={item.idcredenciales}>
                            <td>{item.idcredenciales}</td>
                            <td>{item.user}</td>
                            <td className="text-muted">******</td>
                            <td>
                                <button className="btn btn-sm btn-outline-primary me-2"
                                    onClick={() => navigate(`/credenciales/editar/${item.idcredenciales}`)}>
                                    Editar
                                </button>
                                <button className="btn btn-sm btn-outline-danger"
                                    onClick={() => handleDelete(item.idcredenciales)}>
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

export default CredencialesList;
