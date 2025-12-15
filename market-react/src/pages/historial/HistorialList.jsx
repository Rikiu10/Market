import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Api } from '../../services/api';

const HistorialList = () => {
    const [history, setHistory] = useState([]);
    const navigate = useNavigate();

    const loadHistory = async () => {
        try {
            const data = await Api.getAlertHistory(); // Reusing the method name I chose earlier
            setHistory(data);
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => { loadHistory(); }, []);

    const handleDelete = async (id) => {
        if (window.confirm('¿Eliminar registro de historial?')) {
            try {
                await Api.deleteHistory(id);
                loadHistory();
            } catch (error) {
                alert('Error al eliminar');
            }
        }
    };

    return (
        <div className="container mt-4">
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h2>Historial de Alertas</h2>
                <button className="btn btn-primary" onClick={() => navigate('/historial/nuevo')}>
                    Nuevo Registro
                </button>
            </div>
            <table className="table table-bordered shadow-sm bg-white">
                <thead className="table-light">
                    <tr>
                        <th>ID</th>
                        <th>Fecha</th>
                        <th>Producto</th>
                        <th>Alerta</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {history.map(h => (
                        <tr key={h.idhistorial}>
                            <td>{h.idhistorial}</td>
                            <td>{h.fecha}</td>
                            <td>{h.producto || h.producto_nombre}</td>
                            <td>{h.alerta || h.alerta_descripcion}</td>
                            <td>
                                <button className="btn btn-sm btn-outline-primary me-2"
                                    onClick={() => navigate(`/historial/editar/${h.idhistorial}`)}>
                                    Editar
                                </button>
                                <button className="btn btn-sm btn-outline-danger"
                                    onClick={() => handleDelete(h.idhistorial)}>
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

export default HistorialList;
